from __future__ import annotations

import ast
from dataclasses import dataclass
import importlib.metadata

from .deprecated_paths import DEPRECATED_PATHS, EXCEPTIONS
from .deprecated_paths_v2 import DEPRECATED_PATHS_V2, EXCEPTIONS_V2
from .deprecated_methods import DEPRECATED_METHODS_V1, DEPRECATED_METHODS_V2
from .deprecated_kwargs import DEPRECATED_KWARGS_V2, DEPRECATED_METHOD_KWARGS_V1

RULE_SETS = [
    ("QKT100", DEPRECATED_PATHS, EXCEPTIONS),
    ("QKT200", DEPRECATED_PATHS_V2, EXCEPTIONS_V2),
]

METHOD_RULE_SETS = [
    ("QKT101", DEPRECATED_METHODS_V1),
    ("QKT201", DEPRECATED_METHODS_V2),
]

KWARG_RULE_SETS = [
    ("QKT202", DEPRECATED_KWARGS_V2),
]

METHOD_KWARG_RULE_SETS = [
    ("QKT102", DEPRECATED_METHOD_KWARGS_V1),
]


def _check_path(path: str, original_import_path: str, prefix: str, paths_dict: dict, exceptions: list) -> str | None:
    """
    Recursively check if a path matches a deprecated path in the given dict.

    Returns a formatted message string if deprecated, None otherwise.
    """
    if path in exceptions:
        return None
    if path not in paths_dict:
        parent = ".".join(path.split(".")[:-1])
        if "." not in parent:
            return None
        return _check_path(parent, original_import_path, prefix, paths_dict, exceptions)
    return f"{prefix}: " + paths_dict[path].format(original_import_path)


def deprecation_messages(path: str, original_import_path: str | None = None) -> list[str]:
    """
    Build deprecation messages from all rule sets.

    Args:
        path: Python import path of the form `qiskit.extensions.thing`

    Returns:
        List of deprecation message strings (may be empty)
    """
    original_import_path = original_import_path or path
    if "." not in path:
        return []
    messages = []
    for prefix, paths_dict, exceptions in RULE_SETS:
        msg = _check_path(path, original_import_path, prefix, paths_dict, exceptions)
        if msg is not None:
            messages.append(msg)
    return messages


def _get_dotted_name(node: ast.expr) -> str | None:
    """Reconstruct a dotted name from an AST node (Name or Attribute chain)."""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = _get_dotted_name(node.value)
        if parent is not None:
            return f"{parent}.{node.attr}"
    return None


class Visitor(ast.NodeVisitor):
    """
    Visitor to detect deprecated imports, method calls, and keyword arguments.
    Includes support for aliases and scopes, but not assignments.
    """

    def __init__(self):
        self.problems: list[Problem] = []
        self.mappings: list[dict[str, str]] = [{}]  # track aliases for each scope
        self.imports_qiskit: bool = False  # set True if any qiskit import is found
        # Maps local name → full qiskit import path for from-imports
        # e.g. {"transpile": "qiskit.compiler.transpile"}
        self.qiskit_functions: list[dict[str, str]] = [{}]  # scoped like mappings

    def enter_scope(self) -> None:
        """Add new mapping for scoped aliases"""
        self.mappings.append({})
        self.qiskit_functions.append({})

    def exit_scope(self) -> None:
        """Delete scoped aliases"""
        self.mappings.pop()
        self.qiskit_functions.pop()

    def add_alias(self, alias: ast.alias) -> None:
        if alias.asname is None or alias.asname == alias.name:
            return
        self.mappings[-1][alias.asname] = alias.name

    def resolve_aliases(self, name: str) -> str:
        for mapping in reversed(self.mappings):
            name = mapping.get(name, name)
        return name

    def _resolve_func_path(self, node: ast.expr) -> str | None:
        """Resolve a function call target to a full qiskit import path, or None."""
        if isinstance(node, ast.Name):
            # Look up in qiskit_functions (scoped)
            for scope in reversed(self.qiskit_functions):
                if node.id in scope:
                    return scope[node.id]
            return None
        if isinstance(node, ast.Attribute):
            # Build dotted path and resolve aliases
            dotted = _get_dotted_name(node)
            if dotted is None:
                return None
            parts = dotted.split(".", 1)
            root = parts[0]
            rest = parts[1] if len(parts) > 1 else ""
            # First try qiskit_functions for the root (e.g. Target → qiskit.transpiler.Target)
            for scope in reversed(self.qiskit_functions):
                if root in scope:
                    full_root = scope[root]
                    return f"{full_root}.{rest}" if rest else full_root
            # Then try alias resolution (e.g. qk → qiskit)
            resolved_root = self.resolve_aliases(root)
            resolved = f"{resolved_root}.{rest}" if rest else resolved_root
            if resolved.startswith("qiskit."):
                return resolved
        return None

    def report_if_deprecated(self, path: str, node) -> bool:
        """
        Adds path to problems if deprecated, ignores otherwise
        Returns True if any problem was reported
        """
        msgs = deprecation_messages(path)
        for msg in msgs:
            self.problems.append(Problem(node, msg))
        return len(msgs) > 0

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            self.add_alias(alias)
            if alias.name.startswith("qiskit"):
                self.imports_qiskit = True
            self.report_if_deprecated(alias.name, node)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.module and node.module.startswith("qiskit"):
            self.imports_qiskit = True
        for alias in node.names:
            self.add_alias(alias)
            path = f"{node.module}.{alias.name}"
            # Track the local name → full qiskit path for kwarg checking
            if node.module and node.module.startswith("qiskit"):
                local_name = alias.asname if alias.asname else alias.name
                self.qiskit_functions[-1][local_name] = path
            self.report_if_deprecated(path, node)
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> None:
        def _get_parents(node):
            if isinstance(node, ast.Name):
                return node.id
            if isinstance(node, ast.Attribute):
                parents = _get_parents(node.value)
                parents = self.resolve_aliases(parents)
                return f"{parents}.{node.attr}"

        path = _get_parents(node)
        if not self.report_if_deprecated(path, node):
            self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        # A) Check for deprecated method calls (e.g. obj.c_if(), qc.qasm())
        if isinstance(node.func, ast.Attribute) and self.imports_qiskit:
            method_name = node.func.attr
            for prefix, methods_dict in METHOD_RULE_SETS:
                if method_name in methods_dict:
                    msg = f"{prefix}: " + methods_dict[method_name].format(
                        f".{method_name}()"
                    )
                    self.problems.append(Problem(node, msg))

        # B) Check for deprecated kwargs on known qiskit functions
        func_path = self._resolve_func_path(node.func)
        if func_path and node.keywords:
            for prefix, kwargs_dict in KWARG_RULE_SETS:
                for kw in node.keywords:
                    if kw.arg and (func_path, kw.arg) in kwargs_dict:
                        msg = f"{prefix}: " + kwargs_dict[(func_path, kw.arg)]
                        self.problems.append(Problem(node, msg))

        # C) Check for deprecated kwargs on method calls (heuristic)
        if isinstance(node.func, ast.Attribute) and self.imports_qiskit and node.keywords:
            method_name = node.func.attr
            for prefix, method_kwargs_dict in METHOD_KWARG_RULE_SETS:
                for kw in node.keywords:
                    if kw.arg and (method_name, kw.arg) in method_kwargs_dict:
                        msg = f"{prefix}: " + method_kwargs_dict[(method_name, kw.arg)]
                        self.problems.append(Problem(node, msg))

        self.generic_visit(node)

    # Push / pop scopes for aliases
    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.enter_scope()
        self.generic_visit(node)
        self.exit_scope()

    def visit_AsyncFunctionDef(self, node: ast.FunctionDef):
        self.enter_scope()
        self.generic_visit(node)
        self.exit_scope()

    def visit_ClassDef(self, node: ast.FunctionDef):
        self.enter_scope()
        self.generic_visit(node)
        self.exit_scope()


class Plugin:
    name = "flake8_qiskit_migration"
    version = importlib.metadata.version("flake8_qiskit_migration")

    def __init__(self, tree: ast.AST):
        self._tree = tree

    def run(self):
        """
        Yields:
            int: Line number of problem
            int: Character number of problem
            str: Message for user
           Type: (unused)
        """
        v = Visitor()
        v.visit(self._tree)
        for problem in v.problems:
            yield problem.format()


@dataclass
class Problem:
    node: ast.AST
    msg: str

    def format(self):
        return (self.node.lineno, self.node.col_offset, self.msg, None)
