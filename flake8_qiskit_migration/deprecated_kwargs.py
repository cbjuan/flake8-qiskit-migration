### This file contains removed keyword arguments for Qiskit 2.0 functions.
### Dictionaries are in the form:
###     ("full.import.path", "kwarg_name"): "advice to user"
###
### These are only flagged when the call target is confirmed to be
### a function imported from qiskit (tracked by the Visitor).
###
### Functions that are re-exported at multiple paths need entries for
### each path (e.g. `qiskit.transpile` and `qiskit.compiler.transpile`).

DEPRECATED_KWARGS_V2 = {
    # ----------------------------------------------------------------
    # transpile() removed kwargs
    # Common imports: `from qiskit import transpile`
    #                 `from qiskit.compiler import transpile`
    # ----------------------------------------------------------------
    ("qiskit.transpile", "backend_properties"):
        "The `backend_properties` argument of `transpile()` has been removed in Qiskit 2.0; use `target` or `backend` instead",
    ("qiskit.transpile", "instruction_durations"):
        "The `instruction_durations` argument of `transpile()` has been removed in Qiskit 2.0; use `target` or `backend` instead",
    ("qiskit.transpile", "timing_constraints"):
        "The `timing_constraints` argument of `transpile()` has been removed in Qiskit 2.0; use `target` or `backend` instead",
    ("qiskit.transpile", "inst_map"):
        "The `inst_map` argument of `transpile()` has been removed in Qiskit 2.0 as part of Pulse removal",

    ("qiskit.compiler.transpile", "backend_properties"):
        "The `backend_properties` argument of `transpile()` has been removed in Qiskit 2.0; use `target` or `backend` instead",
    ("qiskit.compiler.transpile", "instruction_durations"):
        "The `instruction_durations` argument of `transpile()` has been removed in Qiskit 2.0; use `target` or `backend` instead",
    ("qiskit.compiler.transpile", "timing_constraints"):
        "The `timing_constraints` argument of `transpile()` has been removed in Qiskit 2.0; use `target` or `backend` instead",
    ("qiskit.compiler.transpile", "inst_map"):
        "The `inst_map` argument of `transpile()` has been removed in Qiskit 2.0 as part of Pulse removal",

    # ----------------------------------------------------------------
    # generate_preset_pass_manager() removed kwargs
    # Common imports: `from qiskit.transpiler import generate_preset_pass_manager`
    #                 `from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager`
    # ----------------------------------------------------------------
    ("qiskit.transpiler.generate_preset_pass_manager", "backend_properties"):
        "The `backend_properties` argument of `generate_preset_pass_manager()` has been removed in Qiskit 2.0; use `target` or `backend` instead",
    ("qiskit.transpiler.generate_preset_pass_manager", "instruction_durations"):
        "The `instruction_durations` argument of `generate_preset_pass_manager()` has been removed in Qiskit 2.0; use `target` or `backend` instead",
    ("qiskit.transpiler.generate_preset_pass_manager", "timing_constraints"):
        "The `timing_constraints` argument of `generate_preset_pass_manager()` has been removed in Qiskit 2.0; use `target` or `backend` instead",
    ("qiskit.transpiler.generate_preset_pass_manager", "inst_map"):
        "The `inst_map` argument of `generate_preset_pass_manager()` has been removed in Qiskit 2.0 as part of Pulse removal",

    ("qiskit.transpiler.preset_passmanagers.generate_preset_pass_manager", "backend_properties"):
        "The `backend_properties` argument of `generate_preset_pass_manager()` has been removed in Qiskit 2.0; use `target` or `backend` instead",
    ("qiskit.transpiler.preset_passmanagers.generate_preset_pass_manager", "instruction_durations"):
        "The `instruction_durations` argument of `generate_preset_pass_manager()` has been removed in Qiskit 2.0; use `target` or `backend` instead",
    ("qiskit.transpiler.preset_passmanagers.generate_preset_pass_manager", "timing_constraints"):
        "The `timing_constraints` argument of `generate_preset_pass_manager()` has been removed in Qiskit 2.0; use `target` or `backend` instead",
    ("qiskit.transpiler.preset_passmanagers.generate_preset_pass_manager", "inst_map"):
        "The `inst_map` argument of `generate_preset_pass_manager()` has been removed in Qiskit 2.0 as part of Pulse removal",

    # ----------------------------------------------------------------
    # generate_routing_passmanager() — backend_properties removed
    # ----------------------------------------------------------------
    ("qiskit.transpiler.preset_passmanagers.common.generate_routing_passmanager", "backend_properties"):
        "The `backend_properties` argument of `generate_routing_passmanager()` has been removed in Qiskit 2.0; use `target` instead",
    ("qiskit.transpiler.preset_passmanagers.generate_routing_passmanager", "backend_properties"):
        "The `backend_properties` argument of `generate_routing_passmanager()` has been removed in Qiskit 2.0; use `target` instead",

    # ----------------------------------------------------------------
    # generate_translation_passmanager() — backend_properties removed
    # ----------------------------------------------------------------
    ("qiskit.transpiler.preset_passmanagers.common.generate_translation_passmanager", "backend_properties"):
        "The `backend_properties` argument of `generate_translation_passmanager()` has been removed in Qiskit 2.0; use `target` instead",
    ("qiskit.transpiler.preset_passmanagers.generate_translation_passmanager", "backend_properties"):
        "The `backend_properties` argument of `generate_translation_passmanager()` has been removed in Qiskit 2.0; use `target` instead",

    # ----------------------------------------------------------------
    # PassManagerConfig — backend_properties and inst_map removed
    # ----------------------------------------------------------------
    ("qiskit.transpiler.PassManagerConfig", "backend_properties"):
        "The `backend_properties` argument of `PassManagerConfig()` has been removed in Qiskit 2.0; use `target` instead",
    ("qiskit.transpiler.PassManagerConfig", "inst_map"):
        "The `inst_map` argument of `PassManagerConfig()` has been removed in Qiskit 2.0 as part of Pulse removal",
    ("qiskit.transpiler.passmanager_config.PassManagerConfig", "backend_properties"):
        "The `backend_properties` argument of `PassManagerConfig()` has been removed in Qiskit 2.0; use `target` instead",
    ("qiskit.transpiler.passmanager_config.PassManagerConfig", "inst_map"):
        "The `inst_map` argument of `PassManagerConfig()` has been removed in Qiskit 2.0 as part of Pulse removal",

    # ----------------------------------------------------------------
    # Target.from_configuration() — backend_properties and inst_map removed
    # ----------------------------------------------------------------
    ("qiskit.transpiler.Target.from_configuration", "backend_properties"):
        "The `backend_properties` argument of `Target.from_configuration()` has been removed in Qiskit 2.0",
    ("qiskit.transpiler.Target.from_configuration", "inst_map"):
        "The `inst_map` argument of `Target.from_configuration()` has been removed in Qiskit 2.0 as part of Pulse removal",
    ("qiskit.transpiler.target.Target.from_configuration", "backend_properties"):
        "The `backend_properties` argument of `Target.from_configuration()` has been removed in Qiskit 2.0",
    ("qiskit.transpiler.target.Target.from_configuration", "inst_map"):
        "The `inst_map` argument of `Target.from_configuration()` has been removed in Qiskit 2.0 as part of Pulse removal",

    # ----------------------------------------------------------------
    # Transpiler pass constructors — removed backend_properties-related args
    # ----------------------------------------------------------------
    ("qiskit.transpiler.passes.DenseLayout", "backend_prop"):
        "The `backend_prop` argument of `DenseLayout()` has been removed in Qiskit 2.0; use `target` instead",
    ("qiskit.transpiler.passes.layout.dense_layout.DenseLayout", "backend_prop"):
        "The `backend_prop` argument of `DenseLayout()` has been removed in Qiskit 2.0; use `target` instead",

    ("qiskit.transpiler.passes.VF2Layout", "properties"):
        "The `properties` argument of `VF2Layout()` has been removed in Qiskit 2.0; use `target` instead",
    ("qiskit.transpiler.passes.layout.vf2_layout.VF2Layout", "properties"):
        "The `properties` argument of `VF2Layout()` has been removed in Qiskit 2.0; use `target` instead",

    ("qiskit.transpiler.passes.VF2PostLayout", "properties"):
        "The `properties` argument of `VF2PostLayout()` has been removed in Qiskit 2.0; use `target` instead",
    ("qiskit.transpiler.passes.layout.vf2_post_layout.VF2PostLayout", "properties"):
        "The `properties` argument of `VF2PostLayout()` has been removed in Qiskit 2.0; use `target` instead",

    ("qiskit.transpiler.passes.UnitarySynthesis", "backend_props"):
        "The `backend_props` argument of `UnitarySynthesis()` has been removed in Qiskit 2.0; use `target` instead",
    ("qiskit.transpiler.passes.synthesis.unitary_synthesis.UnitarySynthesis", "backend_props"):
        "The `backend_props` argument of `UnitarySynthesis()` has been removed in Qiskit 2.0; use `target` instead",
}

### ----------------------------------------------------------------
### Qiskit 1.0 removed keyword arguments (method-name heuristic)
### ----------------------------------------------------------------
### These are keyed by (method_name, kwarg_name) and use the same
### heuristic as QKT101: only flagged when the file imports qiskit.
### The method + kwarg combination must be Qiskit-specific enough
### to avoid false positives.

DEPRECATED_METHOD_KWARGS_V1 = {
    ("append", "max_iteration"):
        "The `max_iteration` argument of `PassManager.append()` has been removed in Qiskit 1.0; use explicit flow controllers instead",
    ("replace", "max_iteration"):
        "The `max_iteration` argument of `PassManager.replace()` has been removed in Qiskit 1.0; use explicit flow controllers instead",
}
