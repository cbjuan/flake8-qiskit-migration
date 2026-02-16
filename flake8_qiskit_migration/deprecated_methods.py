### This file contains deprecated/removed method names for Qiskit 1.0 and 2.0.
### Dictionaries are in the form:
###     "method_name": "{} advice to user"
### where `{}` will be replaced with `.method_name()`.
###
### These are only flagged when the file imports from `qiskit`.
### Without type inference we can't know the receiver type, so we
### restrict to method names specific enough to avoid false positives.

DEPRECATED_METHODS_V1 = {
    # QuantumCircuit / Instruction / Register .qasm() removed
    "qasm": "{} has been removed in Qiskit 1.0; use `qiskit.qasm2.dumps(circuit)` instead",
    # QuantumCircuit.bind_parameters → .assign_parameters()
    "bind_parameters": "{} has been removed in Qiskit 1.0; use `.assign_parameters()` instead",
    # Removed QC gate aliases
    "cnot": "{} has been removed in Qiskit 1.0; use `.cx()` instead",
    "toffoli": "{} has been removed in Qiskit 1.0; use `.ccx()` instead",
    "fredkin": "{} has been removed in Qiskit 1.0; use `.cswap()` instead",
    "mct": "{} has been removed in Qiskit 1.0; use `.mcx()` instead",
    # Removed QC methods (from qiskit.extensions removal)
    "snapshot": "{} has been removed in Qiskit 1.0; use Aer save instructions instead",
    "squ": "{} has been removed in Qiskit 1.0; use `.append(UnitaryGate(...))` instead",
    "diagonal": "{} has been removed in Qiskit 1.0; use `.append(DiagonalGate(...))` instead",
    "hamiltonian": "{} has been removed in Qiskit 1.0; use `.append(HamiltonianGate(...))` instead",
    "isometry": "{} has been removed in Qiskit 1.0; use `.append(Isometry(...))` instead",
    "iso": "{} has been removed in Qiskit 1.0; use `.append(Isometry(...))` instead",
    "uc": "{} has been removed in Qiskit 1.0; use `.append(UCGate(...))` instead",
    "ucrx": "{} has been removed in Qiskit 1.0; use `.append(UCRXGate(...))` instead",
    "ucry": "{} has been removed in Qiskit 1.0; use `.append(UCRYGate(...))` instead",
    "ucrz": "{} has been removed in Qiskit 1.0; use `.append(UCRZGate(...))` instead",
}

DEPRECATED_METHODS_V2 = {
    # Instruction / InstructionSet .c_if() → if_test context manager
    "c_if": "{} has been removed in Qiskit 2.0; use the `if_test` context manager instead",
    # Instruction.condition_bits() removed with c_if
    "condition_bits": "{} has been removed in Qiskit 2.0; use `IfElseOp` instead",
    # QuantumCircuit / DAGCircuit calibration methods (Pulse removal)
    "add_calibration": "{} has been removed in Qiskit 2.0 as part of Pulse removal",
    "has_calibration_for": "{} has been removed in Qiskit 2.0 as part of Pulse removal",
    # BackendV2 channel methods (Pulse removal)
    "instruction_schedule_map": "{} has been removed in Qiskit 2.0 as part of Pulse removal",
    "drive_channel": "{} has been removed in Qiskit 2.0 as part of Pulse removal",
    "measure_channel": "{} has been removed in Qiskit 2.0 as part of Pulse removal",
    "acquire_channel": "{} has been removed in Qiskit 2.0 as part of Pulse removal",
    "control_channel": "{} has been removed in Qiskit 2.0 as part of Pulse removal",
    # Target methods (Pulse removal)
    "has_calibration": "{} has been removed in Qiskit 2.0 as part of Pulse removal",
    "get_calibration": "{} has been removed in Qiskit 2.0 as part of Pulse removal",
    "update_from_instruction_schedule_map": "{} has been removed in Qiskit 2.0 as part of Pulse removal",
    # Target.target_to_backend_properties()
    "target_to_backend_properties": "{} has been removed in Qiskit 2.0",
}
