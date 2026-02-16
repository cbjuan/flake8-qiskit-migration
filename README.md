# flake8-qiskit-migration

Flake8 plugin to detect deprecated/removed imports, methods, and arguments in Qiskit 1.0 and 2.0.

### Error codes

| Code | What it detects |
|------|-----------------|
| **QKT100** | Import paths deprecated in Qiskit 1.0 ([migration guide](https://docs.quantum.ibm.com/api/migration-guides/qiskit-1.0-features)) |
| **QKT101** | Method calls removed in Qiskit 1.0 (e.g. `.qasm()`, `.cnot()`, `.bind_parameters()`) |
| **QKT102** | Keyword arguments removed in Qiskit 1.0 (e.g. `PassManager.append(max_iteration=...)`) |
| **QKT200** | Import paths removed in Qiskit 2.0 ([migration guide](https://docs.quantum.ibm.com/migration-guides/qiskit-2.0)) |
| **QKT201** | Method calls removed in Qiskit 2.0 (e.g. `.c_if()`, `.add_calibration()`, `.drive_channel()`) |
| **QKT202** | Keyword arguments removed in Qiskit 2.0 (e.g. `transpile(backend_properties=...)`) |

> [!NOTE]
> QKT101/QKT102/QKT201 use heuristic detection (method name matching in files
> that import `qiskit`). Without type inference, false positives are possible
> but unlikely for the Qiskit-specific names we check. QKT202 tracks which
> functions were imported from `qiskit` and has near-zero false positives.

> [!WARNING]
> This tool does not detect assignments such as `qk = qiskit` (although it can
> handle _aliases_ such as `import qiskit as qk`).

This tool is to help you quickly identify deprecated API usage and work out how
to fix it. This tool is not perfect and will make some mistakes, so make sure
to test your project thoroughly after migrating.

## Through pipx

We recommend using this plugin through [`pipx`](https://github.com/pypa/pipx).
If you have `pipx` installed, simply run:

```sh
pipx run flake8-qiskit-migration <path-to-source>
```

This will install this plugin in a temporary environment and run it. If you're
at the root of your Python project, then `<path-to-source>` is `./`.

## With Python venv

If you don't want to use `pipx`, you can manually create a new environment for
the linter. This approach also lets you use
[`nbqa`](https://github.com/nbQA-dev/nbQA) to check Jupyter notebooks. Delete
the environment when you're finished.

```sh
# Make new environment and install
python -m venv .flake8-qiskit-migration-venv
source .flake8-qiskit-migration-venv/bin/activate
pip install flake8-qiskit-migration

# Run all migration checks
flake8 --select QKT <path-to-source>  # e.g. `src/`

# Run only Qiskit 1.0 checks (imports + methods)
flake8 --select QKT1 <path-to-source>

# Run only Qiskit 2.0 checks (imports + methods + kwargs)
flake8 --select QKT2 <path-to-source>

# Run only import checks
flake8 --select QKT100,QKT200 <path-to-source>

# Run plugin on notebooks
pip install nbqa
nbqa flake8 ./**/*.ipynb --select QKT

# Deactivate and delete environment
deactivate
rm -r .flake8-qiskit-migration-venv
```

## With existing flake8

If you already have `flake8` installed and want run this plugin that way,
To run only the deprecation detection plugin, use the `--select`
argument. You'll probably want to uninstall it when you're done.

```sh
# Install plugin
pip install flake8-qiskit-migration

# Run all flake8 checks (including this plugin)
flake8 <path-to-source>

# Run only this plugin (all checks)
flake8 --select QKT <path-to-source>

# Run only Qiskit 1.0 checks
flake8 --select QKT1 <path-to-source>

# Run only Qiskit 2.0 checks
flake8 --select QKT2 <path-to-source>

# Uninstall plugin
pip uninstall flake8-qiskit-migration
```
