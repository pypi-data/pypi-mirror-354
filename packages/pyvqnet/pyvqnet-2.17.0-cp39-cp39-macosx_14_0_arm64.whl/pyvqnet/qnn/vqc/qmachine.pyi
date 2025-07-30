from pyvqnet.device import *
from _typeshed import Incomplete
from pyvqnet.backends import global_backend as global_backend
from pyvqnet.dtype import get_readable_dtype_str as get_readable_dtype_str, kcomplex128 as kcomplex128, kcomplex64 as kcomplex64, kfloat32 as kfloat32, kfloat64 as kfloat64
from pyvqnet.nn import Module as Module, Parameter as Parameter
from pyvqnet.tensor import QTensor as QTensor, tensor as tensor

change_save_op_history_enable: bool
change_just_define_op_not_run_enable: bool
valid_set_grad_mode: Incomplete

def get_just_define_op_not_run_enable():
    """
    get flag if change_just_define_op_not_run_enable
    """
def set_just_define_op_not_run_enable(flag) -> None:
    """
    set flag of if_show_bp_info
    """
def get_if_save_op_history_enable():
    """
    get flag change_save_op_history_enable
    """
def set_if_save_op_history_enable(flag) -> None:
    """
    set flag of if_show_bp_info
    """

class not_just_define_op:
    prev: bool
    def __init__(self) -> None: ...
    def __enter__(self) -> None: ...
    def __exit__(self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: types.TracebackType | None) -> None: ...

class not_save_op_history:
    """
    enter scope of not save operations history when doing gate operations
    """
    prev: bool
    def __init__(self) -> None: ...
    def __enter__(self) -> None: ...
    def __exit__(self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: types.TracebackType | None) -> None: ...

class AbstractQMachine(Module):
    batch_size: int
    num_wires: Incomplete
    originir_str_list: Incomplete
    dtype: Incomplete
    op_history: Incomplete
    total_params: int
    total_train_params: int
    train_params_indices: Incomplete
    states_before_measure: Incomplete
    save_ir: Incomplete
    params_dict: Incomplete
    just_defined: bool
    in_qadjoint: bool
    def __init__(self, num_wires, dtype=..., save_ir: bool = False, use_tn: bool = False) -> None: ...
    def set_in_qadjoint(self, flag) -> None: ...
    def get_in_qadjoint(self): ...
    @property
    def grad_mode(self): ...
    @grad_mode.setter
    def grad_mode(self, new_value) -> None: ...
    def set_grad_mode(self, value) -> None: ...
    def get_grad_mode(self): ...
    def set_just_defined(self, value) -> None: ...
    def get_just_defined(self):
        """
        just create operations list before measure, not do real exec.
        """
    def set_save_op_history_flag(self, flag) -> None: ...
    def get_save_op_history_flag(self): ...
    def set_if_in_measure(self, if_in_measure) -> None: ...
    def set_if_op_within_measure_proc(self, if_op_within_measure) -> None: ...
    def get_if_op_within_measure_proc(self): ...
    def reset_op_history(self) -> None: ...
    def forward(self, x, *args, **kwargs) -> None: ...
    def add_train_params_indice(self, p) -> None: ...
    def add_params_infos(self, params) -> None: ...

class QMachine(AbstractQMachine):
    grad_mode: Incomplete
    states: Incomplete
    def __init__(self, num_wires, dtype=..., grad_mode: str = '', save_ir: bool = False) -> None:
        '''
        
        A simulator class for variational quantum computing, including statevectors whose states attribute is a quantum circuit.

        :param num_wires: the number of qubits.
        :param dtype: The data type of the calculation data. The default is pyvqnet.kcomplex64, and the corresponding parameter precision is pyvqnet.kfloat32.
        :param grad_mode: gradient calculation mode,can be "adjoint",default: "", use autograd。
        :param save_ir: save operation to originIR if set to True, default:False.

        :return:
            A QMachine instance.
        '''
    def set_enable_decompose(self, flag) -> None: ...
    def get_enable_decompose(self): ...
    batch_size: Incomplete
    def set_states(self, states) -> None: ...
    def reset_states(self, batchsize: int):
        """
        reset states

        :param batchsize: batchsize
        """
    def init_states(self, init_state) -> None: ...
