import ast
from textwrap import dedent

from flake8_qiskit_migration.plugin import Plugin


def _results(code: str):
    code = dedent(code)
    tree = ast.parse(code)
    plugin = Plugin(tree)
    return {f"{line}:{col} {msg}" for line, col, msg, _ in plugin.run()}


def test_trivial_case():
    assert _results("") == set()


def test_simple_import_path():
    code = """
    from qiskit import QuantumCircuit
    import qiskit.extensions
    import qiskit.extensions.item  # should raise error even though `.item` doesn't exist as whole path is deprecated
    import qiskit.quantum_info.synthesis.OneQubitEulerDecomposer
    import numpy
    """
    assert _results(code) == {
        "3:0 QKT100: qiskit.extensions has been removed; most objects have been moved to `qiskit.circuit.library` (see https://docs.quantum.ibm.com/api/migration-guides/qiskit-1.0-features)",
        "4:0 QKT100: qiskit.extensions.item has been removed; most objects have been moved to `qiskit.circuit.library` (see https://docs.quantum.ibm.com/api/migration-guides/qiskit-1.0-features)",
        "5:0 QKT100: qiskit.quantum_info.synthesis.OneQubitEulerDecomposer has moved to `qiskit.synthesis.one_qubit.OneQubitEulerDecomposer`",
    }


def test_simple_from_import_path():
    code = """
    from qiskit.quantum_info.synthesis import OneQubitEulerDecomposer
    from qiskit.quantum_info.synthesis import XXDecomposer as xxd
    from qiskit.quantum_info.synthesis import NonDeprecatedClass
    from qiskit.quantum_info.synthesis import OtherNonDeprecatedClass as XXDecomposer
    """
    assert _results(code) == {
        "2:0 QKT100: qiskit.quantum_info.synthesis.OneQubitEulerDecomposer has moved to `qiskit.synthesis.one_qubit.OneQubitEulerDecomposer`",
        "3:0 QKT100: qiskit.quantum_info.synthesis.XXDecomposer has moved to `qiskit.synthesis.two_qubits.XXDecomposer`",
    }


def test_module_attribute_later_in_script():
    code = """
    import qiskit.quantum_info.synthesis
    xxd = qiskit.quantum_info.synthesis.XXDecomposer()
    qiskit.quantum_info.synthesis.OneQubitEulerDecomposer().run()
    allowed = qiskit.quantum_info.synthesis.AllowedPath
    """
    assert _results(code) == {
        "3:6 QKT100: qiskit.quantum_info.synthesis.XXDecomposer has moved to `qiskit.synthesis.two_qubits.XXDecomposer`",
        "4:0 QKT100: qiskit.quantum_info.synthesis.OneQubitEulerDecomposer has moved to `qiskit.synthesis.one_qubit.OneQubitEulerDecomposer`",
    }


def test_module_attribute_later_in_script_with_alias():
    code = """
    import qiskit as qk
    qk.extensions.thing()
    """
    assert _results(code) == {
        "3:0 QKT100: qiskit.extensions.thing has been removed; most objects have been moved to `qiskit.circuit.library` (see https://docs.quantum.ibm.com/api/migration-guides/qiskit-1.0-features)",
    }


def test_alias_scope():
    code = """
    import safe_module as qk

    def my_function():
        import qiskit as qk
        return qk.extensions.thing()  # deprecated

    print(qk.extensions.thing())  # safe import
    """
    assert _results(code) == {
        "6:11 QKT100: qiskit.extensions.thing has been removed; most objects have been moved to `qiskit.circuit.library` (see https://docs.quantum.ibm.com/api/migration-guides/qiskit-1.0-features)",
    }

    code = """
    import qiskit as qk

    def my_function():
        import safe_module as qk
        return qk.extensions.thing()  # safe

    print(qk.extensions.thing())  # deprecated
    """
    assert _results(code) == {
        "8:6 QKT100: qiskit.extensions.thing has been removed; most objects have been moved to `qiskit.circuit.library` (see https://docs.quantum.ibm.com/api/migration-guides/qiskit-1.0-features)",
    }

def test_exceptions():
    code = """
    from qiskit.fake_provider.utils import json_decoder
    """
    assert _results(code) == set()

def test_basicaer():
    code = """
    from qiskit import BasicAer
    """
    assert _results(code) == {
        "2:0 QKT100: qiskit.BasicAer has been removed; either install separate `qiskit-aer` package and replace import with `qiskit_aer.Aer`, or follow https://docs.quantum.ibm.com/api/migration-guides/qiskit-1.0-features#providers.basicaer"
    }

def test_providers():
    code = """
    from qiskit.providers.fake_provider import FakeCairo
    from qiskit.providers.fake_provider import GenericBackendV2
    from qiskit.providers.fake_provider import FakeBackend
    """
    assert _results(code) == {
        "2:0 QKT100: qiskit.providers.fake_provider.FakeCairo has moved; install separate `qiskit-ibm-runtime` package and replace `qiskit.providers.fake_provider` with `qiskit_ibm_runtime.fake_provider`",
        "2:0 QKT200: qiskit.providers.fake_provider.FakeCairo has been removed in Qiskit 2.0; use `GenericBackendV2` or `qiskit_ibm_runtime.fake_provider`",
        "4:0 QKT200: qiskit.providers.fake_provider.FakeBackend has been removed in Qiskit 2.0; use `GenericBackendV2` or `qiskit_ibm_runtime.fake_provider`",
    }

def test_utils():
    code = """
    from qiskit.utils import valid_import
    from qiskit.utils import QuantumInstance, entangler_map
    """
    assert _results(code) == {
        "3:0 QKT100: qiskit.utils.entangler_map has been removed with no replacement",
        "3:0 QKT100: qiskit.utils.QuantumInstance has been removed; see https://docs.quantum.ibm.com/api/migration-guides/qiskit-quantum-instance"
    }


# ---- QKT200 tests (Qiskit 2.0 removals) ----

def test_pulse_removal():
    code = """
    import qiskit.pulse
    from qiskit.pulse import ScheduleBlock
    from qiskit.pulse.library import Gaussian
    """
    results = _results(code)
    assert all("QKT200" in r for r in results)
    assert len(results) == 3


def test_qobj_removal():
    code = """
    from qiskit.qobj import QasmQobj
    import qiskit.qobj
    """
    results = _results(code)
    assert all("QKT200" in r for r in results)
    assert len(results) == 2


def test_classicalfunction_removal():
    code = """
    from qiskit.circuit.classicalfunction import ClassicalFunction
    from qiskit.circuit.classicalfunction import BooleanExpression
    """
    results = _results(code)
    assert all("QKT200" in r for r in results)
    assert len(results) == 2


def test_backendv1_removal():
    code = """
    from qiskit.providers import BackendV1
    from qiskit.providers import BackendV2Converter
    """
    results = _results(code)
    assert all("QKT200" in r for r in results)
    assert len(results) == 2


def test_provider_models_removal():
    code = """
    from qiskit.providers.models import BackendConfiguration
    from qiskit.providers.models import BackendProperties
    """
    results = _results(code)
    assert all("QKT200" in r for r in results)
    assert len(results) == 2


def test_primitive_v1_removal():
    code = """
    from qiskit.primitives import Estimator
    from qiskit.primitives import Sampler
    from qiskit.primitives import BackendEstimator
    from qiskit.primitives import BackendSampler
    from qiskit.primitives import StatevectorEstimator
    from qiskit.primitives import StatevectorSampler
    """
    results = _results(code)
    # StatevectorEstimator and StatevectorSampler are exceptions (valid V2 classes)
    qkt200_results = {r for r in results if "QKT200" in r}
    assert len(qkt200_results) == 4


def test_transpiler_passes_v2():
    code = """
    from qiskit.transpiler.passes import ASAPSchedule
    from qiskit.transpiler.passes import CXCancellation
    from qiskit.transpiler.passes import StochasticSwap
    from qiskit.transpiler.passes import PulseGates
    """
    results = _results(code)
    qkt200_results = {r for r in results if "QKT200" in r}
    assert len(qkt200_results) == 4


def test_assembler_removal():
    code = """
    from qiskit.assembler import assemble_circuits
    from qiskit.compiler import assemble
    """
    results = _results(code)
    qkt200_results = {r for r in results if "QKT200" in r}
    assert len(qkt200_results) == 2


def test_scheduler_removal():
    code = """
    from qiskit.scheduler import schedule_circuit
    """
    results = _results(code)
    assert any("QKT200" in r for r in results)


def test_result_mitigation_removal():
    code = """
    from qiskit.result.mitigation import LocalReadoutMitigator
    """
    results = _results(code)
    assert any("QKT200" in r for r in results)


def test_visualization_v2():
    code = """
    from qiskit.visualization import pulse_drawer
    from qiskit.visualization import visualize_transition
    """
    results = _results(code)
    qkt200_results = {r for r in results if "QKT200" in r}
    # Only pulse_drawer is removed in 2.0; visualize_transition is NOT removed
    assert len(qkt200_results) == 1
    assert any("pulse_drawer" in r for r in qkt200_results)


def test_fake_backend_v1_removal():
    code = """
    from qiskit.providers.fake_provider import FakeBackend
    from qiskit.providers.fake_provider import Fake1Q
    from qiskit.providers.fake_provider import GenericBackendV2
    """
    results = _results(code)
    # FakeBackend and Fake1Q should trigger QKT200
    # GenericBackendV2 is an exception (still valid)
    qkt200_results = {r for r in results if "QKT200" in r}
    assert len(qkt200_results) == 2


def test_both_codes_pulse():
    """qiskit.pulse paths that were deprecated in 1.0 AND removed in 2.0
    should produce both QKT100 and QKT200 messages."""
    code = """
    from qiskit.pulse.library.parametric_pulses import Gaussian
    """
    results = _results(code)
    assert any("QKT100" in r for r in results)
    assert any("QKT200" in r for r in results)


def test_v2_only_no_v1():
    """Paths removed in 2.0 but NOT deprecated in 1.0 should only produce QKT200."""
    code = """
    from qiskit.providers import BackendV1
    """
    results = _results(code)
    assert any("QKT200" in r for r in results)
    assert not any("QKT100" in r for r in results)


def test_v2_exceptions():
    """V2 exceptions should not trigger QKT200."""
    code = """
    from qiskit.primitives import StatevectorEstimator
    from qiskit.primitives import BaseEstimatorV2
    from qiskit.providers.fake_provider import GenericBackendV2
    """
    results = _results(code)
    qkt200_results = {r for r in results if "QKT200" in r}
    assert len(qkt200_results) == 0


def test_compiler_sequence_schedule_removal():
    code = """
    from qiskit.compiler import sequence
    from qiskit.compiler import schedule
    """
    results = _results(code)
    qkt200_results = {r for r in results if "QKT200" in r}
    assert len(qkt200_results) == 2
    assert all("Pulse removal" in r for r in qkt200_results)


def test_rzx_templates_removal():
    code = """
    from qiskit.transpiler.passes import rzx_templates
    """
    results = _results(code)
    assert any("QKT200" in r and "Pulse removal" in r for r in results)


def test_no_false_positives():
    """Valid Qiskit 2.0 imports should not trigger any warnings."""
    code = """
    from qiskit.circuit import QuantumCircuit
    from qiskit.transpiler import generate_preset_pass_manager
    from qiskit.transpiler.passes import SabreSwap
    from qiskit.primitives import StatevectorEstimator
    from qiskit.providers.fake_provider import GenericBackendV2
    import qiskit.qasm2
    import numpy
    """
    assert _results(code) == set()


def test_dual_message_pulse_specific():
    """A QKT100-specific pulse path also triggers QKT200 via the catch-all."""
    code = """
    from qiskit.pulse.builder import cx
    """
    results = _results(code)
    qkt100 = {r for r in results if "QKT100" in r}
    qkt200 = {r for r in results if "QKT200" in r}
    assert len(qkt100) == 1
    assert len(qkt200) == 1


# ---- QKT101 tests (Qiskit 1.0 removed methods) ----

def test_removed_qasm_method():
    """QuantumCircuit.qasm() was removed in Qiskit 1.0."""
    code = """
    from qiskit.circuit import QuantumCircuit
    qc = QuantumCircuit(2)
    qc.qasm()
    """
    results = _results(code)
    qkt101 = {r for r in results if "QKT101" in r}
    assert len(qkt101) == 1
    assert any(".qasm()" in r for r in qkt101)


def test_removed_bind_parameters():
    """QuantumCircuit.bind_parameters() → .assign_parameters()."""
    code = """
    from qiskit.circuit import QuantumCircuit
    qc = QuantumCircuit(2)
    qc.bind_parameters({})
    """
    results = _results(code)
    qkt101 = {r for r in results if "QKT101" in r}
    assert len(qkt101) == 1
    assert any(".bind_parameters()" in r for r in qkt101)


def test_removed_qc_aliases():
    """Removed QC convenience method aliases."""
    code = """
    from qiskit.circuit import QuantumCircuit
    qc = QuantumCircuit(3)
    qc.cnot(0, 1)
    qc.toffoli(0, 1, 2)
    qc.fredkin(0, 1, 2)
    qc.mct([0, 1], 2)
    """
    results = _results(code)
    qkt101 = {r for r in results if "QKT101" in r}
    assert any(".cnot()" in r for r in qkt101)
    assert any(".toffoli()" in r for r in qkt101)
    assert any(".fredkin()" in r for r in qkt101)
    assert any(".mct()" in r for r in qkt101)


def test_removed_extension_methods():
    """Removed QC methods from extensions module."""
    code = """
    from qiskit.circuit import QuantumCircuit
    qc = QuantumCircuit(2)
    qc.snapshot("snap")
    qc.squ([[1, 0], [0, 1]], 0)
    qc.diagonal([1, 1, 1, -1])
    qc.isometry([[1, 0], [0, 1]], [0], [])
    qc.ucrx([0.1], 0, 1)
    """
    results = _results(code)
    qkt101 = {r for r in results if "QKT101" in r}
    assert any(".snapshot()" in r for r in qkt101)
    assert any(".squ()" in r for r in qkt101)
    assert any(".diagonal()" in r for r in qkt101)
    assert any(".isometry()" in r for r in qkt101)
    assert any(".ucrx()" in r for r in qkt101)


def test_no_method_false_positive_without_qiskit():
    """Methods should NOT be flagged if the file doesn't import qiskit."""
    code = """
    import some_other_library
    obj = some_other_library.Thing()
    obj.qasm()
    obj.c_if(x, 1)
    obj.bind_parameters({})
    """
    assert _results(code) == set()


# ---- QKT102 tests (Qiskit 1.0 removed keyword arguments, heuristic) ----

def test_pass_manager_append_max_iteration():
    """PassManager.append(max_iteration=...) removed in 1.0."""
    code = """
    from qiskit.transpiler import PassManager
    pm = PassManager()
    pm.append(my_pass, max_iteration=5)
    """
    results = _results(code)
    qkt102 = {r for r in results if "QKT102" in r}
    assert len(qkt102) == 1
    assert any("max_iteration" in r for r in qkt102)


def test_pass_manager_replace_max_iteration():
    """PassManager.replace(max_iteration=...) removed in 1.0."""
    code = """
    from qiskit.transpiler import PassManager
    pm = PassManager()
    pm.replace(0, my_pass, max_iteration=3)
    """
    results = _results(code)
    qkt102 = {r for r in results if "QKT102" in r}
    assert len(qkt102) == 1
    assert any("max_iteration" in r for r in qkt102)


def test_method_kwarg_no_false_positive_without_qiskit():
    """append(max_iteration=...) without qiskit import should NOT trigger."""
    code = """
    import some_library
    pm = some_library.Manager()
    pm.append(task, max_iteration=5)
    """
    assert _results(code) == set()


# ---- QKT201 tests (Qiskit 2.0 removed methods) ----

def test_c_if_removal():
    """Instruction.c_if() / InstructionSet.c_if() removed in 2.0."""
    code = """
    from qiskit.circuit import QuantumCircuit
    qc = QuantumCircuit(2, 2)
    qc.measure(0, 0)
    qc.x(1).c_if(0, 1)
    """
    results = _results(code)
    qkt201 = {r for r in results if "QKT201" in r}
    assert len(qkt201) == 1
    assert any(".c_if()" in r and "if_test" in r for r in qkt201)


def test_calibration_methods_removal():
    """QC calibration methods removed in 2.0 (Pulse removal)."""
    code = """
    from qiskit.circuit import QuantumCircuit
    qc = QuantumCircuit(2)
    qc.add_calibration("x", [0], None)
    qc.has_calibration_for(None)
    """
    results = _results(code)
    qkt201 = {r for r in results if "QKT201" in r}
    assert any("add_calibration" in r for r in qkt201)
    assert any("has_calibration_for" in r for r in qkt201)


def test_backend_channel_methods():
    """BackendV2 channel methods removed in 2.0 (Pulse removal)."""
    code = """
    from qiskit.providers import BackendV2
    backend = BackendV2()
    backend.drive_channel(0)
    backend.measure_channel(0)
    backend.acquire_channel(0)
    backend.control_channel((0, 1))
    """
    results = _results(code)
    qkt201 = {r for r in results if "QKT201" in r}
    assert any("drive_channel" in r for r in qkt201)
    assert any("measure_channel" in r for r in qkt201)
    assert any("acquire_channel" in r for r in qkt201)
    assert any("control_channel" in r for r in qkt201)


def test_target_pulse_methods():
    """Target pulse-related methods removed in 2.0."""
    code = """
    from qiskit.transpiler import Target
    t = Target()
    t.has_calibration("cx", (0, 1))
    t.get_calibration("cx", (0, 1))
    t.instruction_schedule_map()
    t.update_from_instruction_schedule_map(None)
    """
    results = _results(code)
    qkt201 = {r for r in results if "QKT201" in r}
    assert any("has_calibration" in r for r in qkt201)
    assert any("get_calibration" in r for r in qkt201)
    assert any("instruction_schedule_map" in r for r in qkt201)
    assert any("update_from_instruction_schedule_map" in r for r in qkt201)


def test_condition_bits_removal():
    """Instruction.condition_bits() removed in 2.0."""
    code = """
    from qiskit.circuit import QuantumCircuit
    qc = QuantumCircuit(2, 2)
    inst = qc.data[0]
    inst.operation.condition_bits()
    """
    results = _results(code)
    qkt201 = {r for r in results if "QKT201" in r}
    assert any("condition_bits" in r for r in qkt201)


# ---- QKT202 tests (Qiskit 2.0 removed keyword arguments) ----

def test_transpile_removed_kwargs():
    """transpile() removed kwargs in 2.0."""
    code = """
    from qiskit.compiler import transpile
    transpile(qc, backend_properties=props)
    """
    results = _results(code)
    qkt202 = {r for r in results if "QKT202" in r}
    assert len(qkt202) == 1
    assert any("backend_properties" in r for r in qkt202)


def test_transpile_multiple_removed_kwargs():
    """Multiple removed kwargs on a single transpile() call."""
    code = """
    from qiskit.compiler import transpile
    transpile(qc, backend_properties=props, inst_map=imap, timing_constraints=tc)
    """
    results = _results(code)
    qkt202 = {r for r in results if "QKT202" in r}
    assert len(qkt202) == 3
    assert any("backend_properties" in r for r in qkt202)
    assert any("inst_map" in r for r in qkt202)
    assert any("timing_constraints" in r for r in qkt202)


def test_generate_pm_removed_kwargs():
    """generate_preset_pass_manager() removed kwargs in 2.0."""
    code = """
    from qiskit.transpiler import generate_preset_pass_manager
    generate_preset_pass_manager(backend_properties=props, inst_map=imap)
    """
    results = _results(code)
    qkt202 = {r for r in results if "QKT202" in r}
    assert len(qkt202) == 2
    assert any("backend_properties" in r for r in qkt202)
    assert any("inst_map" in r for r in qkt202)


def test_transpile_aliased():
    """transpile() with alias should still detect removed kwargs."""
    code = """
    from qiskit.compiler import transpile as tp
    tp(qc, backend_properties=props)
    """
    results = _results(code)
    qkt202 = {r for r in results if "QKT202" in r}
    assert len(qkt202) == 1


def test_transpile_dotted_call():
    """qiskit.compiler.transpile() via dotted access should detect removed kwargs."""
    code = """
    import qiskit.compiler
    qiskit.compiler.transpile(qc, backend_properties=props)
    """
    results = _results(code)
    qkt202 = {r for r in results if "QKT202" in r}
    assert len(qkt202) == 1


def test_transpile_bare_import_dotted_call():
    """import qiskit; qiskit.transpile(...) should detect removed kwargs."""
    code = """
    import qiskit
    qiskit.transpile(qc, backend_properties=props)
    """
    results = _results(code)
    qkt202 = {r for r in results if "QKT202" in r}
    assert len(qkt202) == 1
    assert any("backend_properties" in r for r in qkt202)


def test_kwarg_no_false_positive_other_library():
    """transpile from another library should NOT trigger QKT202."""
    code = """
    from my_library import transpile
    transpile(backend_properties=props)
    """
    assert _results(code) == set()


def test_kwarg_no_false_positive_valid_kwargs():
    """Valid transpile kwargs should NOT trigger QKT202."""
    code = """
    from qiskit.compiler import transpile
    transpile(qc, target=target, optimization_level=2)
    """
    results = _results(code)
    qkt202 = {r for r in results if "QKT202" in r}
    assert len(qkt202) == 0


def test_target_from_configuration_kwargs():
    """Target.from_configuration() removed kwargs."""
    code = """
    from qiskit.transpiler import Target
    Target.from_configuration(num_qubits=2, inst_map=imap)
    """
    results = _results(code)
    qkt202 = {r for r in results if "QKT202" in r}
    assert len(qkt202) == 1
    assert any("inst_map" in r for r in qkt202)


def test_transpile_reexported_path():
    """from qiskit import transpile (re-exported) should detect removed kwargs."""
    code = """
    from qiskit import transpile
    transpile(qc, backend_properties=props)
    """
    results = _results(code)
    qkt202 = {r for r in results if "QKT202" in r}
    assert len(qkt202) == 1
    assert any("backend_properties" in r for r in qkt202)


def test_transpile_reexported_all_kwargs():
    """All four removed transpile() kwargs via re-exported path."""
    code = """
    from qiskit import transpile
    transpile(qc, backend_properties=p, instruction_durations=d, timing_constraints=t, inst_map=i)
    """
    results = _results(code)
    qkt202 = {r for r in results if "QKT202" in r}
    assert len(qkt202) == 4


def test_generate_pm_reexported_path():
    """generate_preset_pass_manager via preset_passmanagers submodule."""
    code = """
    from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
    generate_preset_pass_manager(backend_properties=props, timing_constraints=tc)
    """
    results = _results(code)
    qkt202 = {r for r in results if "QKT202" in r}
    assert len(qkt202) == 2


def test_pass_manager_config_kwargs():
    """PassManagerConfig removed kwargs (backend_properties and inst_map)."""
    code = """
    from qiskit.transpiler import PassManagerConfig
    PassManagerConfig(backend_properties=props, inst_map=imap)
    """
    results = _results(code)
    qkt202 = {r for r in results if "QKT202" in r}
    assert len(qkt202) == 2
    assert any("backend_properties" in r for r in qkt202)
    assert any("inst_map" in r for r in qkt202)


def test_dense_layout_backend_prop():
    """DenseLayout(backend_prop=...) removed in 2.0."""
    code = """
    from qiskit.transpiler.passes import DenseLayout
    DenseLayout(backend_prop=props)
    """
    results = _results(code)
    qkt202 = {r for r in results if "QKT202" in r}
    assert len(qkt202) == 1
    assert any("backend_prop" in r for r in qkt202)


def test_vf2_layout_properties():
    """VF2Layout(properties=...) removed in 2.0."""
    code = """
    from qiskit.transpiler.passes import VF2Layout
    VF2Layout(properties=props)
    """
    results = _results(code)
    qkt202 = {r for r in results if "QKT202" in r}
    assert len(qkt202) == 1
    assert any("properties" in r for r in qkt202)


def test_vf2_post_layout_properties():
    """VF2PostLayout(properties=...) removed in 2.0."""
    code = """
    from qiskit.transpiler.passes import VF2PostLayout
    VF2PostLayout(properties=props)
    """
    results = _results(code)
    qkt202 = {r for r in results if "QKT202" in r}
    assert len(qkt202) == 1
    assert any("properties" in r for r in qkt202)


def test_unitary_synthesis_backend_props():
    """UnitarySynthesis(backend_props=...) removed in 2.0."""
    code = """
    from qiskit.transpiler.passes import UnitarySynthesis
    UnitarySynthesis(backend_props=props)
    """
    results = _results(code)
    qkt202 = {r for r in results if "QKT202" in r}
    assert len(qkt202) == 1
    assert any("backend_props" in r for r in qkt202)
