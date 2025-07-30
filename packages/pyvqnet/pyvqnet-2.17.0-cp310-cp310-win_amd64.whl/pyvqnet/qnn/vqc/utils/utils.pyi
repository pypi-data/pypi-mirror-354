from ....backends import check_not_default_backend as check_not_default_backend, get_backend as get_backend, global_backend as global_backend
from ....device import DEV_CPU as DEV_CPU, DEV_GPU_0 as DEV_GPU_0
from ....tensor.utils import FLOAT_2_COMPLEX as FLOAT_2_COMPLEX
from _typeshed import Incomplete
from pyvqnet import tensor as tensor
from pyvqnet.dtype import C_DTYPE as C_DTYPE, complex_dtype_to_float_dtype as complex_dtype_to_float_dtype, float_dtype_to_complex_dtype as float_dtype_to_complex_dtype, get_readable_dtype_str as get_readable_dtype_str, kcomplex128 as kcomplex128, kcomplex32 as kcomplex32, kcomplex64 as kcomplex64, kfloat16 as kfloat16, kfloat32 as kfloat32, kfloat64 as kfloat64, vqnet_complex_dtypes as vqnet_complex_dtypes, vqnet_float_dtypes as vqnet_float_dtypes
from pyvqnet.nn import Parameter as Parameter
from string import ascii_lowercase
from typing import Callable

ABC = ascii_lowercase
ABC_ARRAY: Incomplete
INV_SQRT2: Incomplete
SQRT2: Incomplete
CNOT_BLOCK_SIZE: int

def all_wires(list_of_wires):
    """
    remove same wires index,keep wires order, return a new wires list.
    """
def qgate_op_creator(oper, has_params, trainable, init_params, wires, dtype, use_dagger, **hyper_parameters):
    """
    use data from op history to create quantum gate operator or measure obs.
    """
def COMPLEX_2_FLOAT(param): ...
def expand_matrix(mat, wires, wire_order, format: str = 'dense'): ...
def check_wires_valid(valid_num, wires, name) -> None: ...
def check_wires(wires, num_wires) -> None: ...
def maybe_reshape_param_to_valid(valid_num, param, name):
    """
    reshape param into (b,valid_num) if possible
    """
def find_nodes_without_post(node): ...
def cov_matrix(prob, obs, wires: Incomplete | None = None, diag_approx: bool = False): ...
def marginal_prob(prob, num_wires, wires): ...
def probs(q_state, num_wires, wires): ...
def rearrange_coeff(wires, coeff): ...
def qpanda_paulisum_str_parse(qpanda_paulisum_str, num_wires):
    """
    {'X0': 0.23,'Y1':-3.5}->
    {'wires': [0,  1], 'observables': ['x', 'y']
,'coefficient':[0.23,-3.5]} 
    
    """
def get_obname(input_string): ...
def helper_parse_paulisum(obs, number_of_wires: int) -> dict:
    """
    input like:{'X0 Z1':4 ,'X1 Z0':3}
    {'wires': [],
        'observables': [],
        'coefficient': []}
    or PauliX() ==> {
        'wires': [0, 2, 3],
        'coeff_ordered': ['X', 'Y', 'Z'],
        'coefficient': [1, 0.5, 0.4]
    }
    """
def apply_unitary_einsum(state, mat, wires):
    """Apply the unitary to the statevector using einsum method.

    """
def apply_operation_tensordot(mat, state, wires):
    """Apply `tensordot`. This is more efficent at higher qubit
    numbers.

     
    """
def apply_diagonal_unitary(state, phases, wires):
    """Apply multiplication of a phase vector to subsystems of the quantum state.

    This represents the multiplication with diagonal gates in a more efficient manner.

    """
def apply_gate_operation_impl(state, mat, wires, name: str = ''):
    """
    return new state after this gate operation.
    """
apply_unitary_operation = apply_gate_operation_impl

def apply_unitary_bmm(state, mat, wires, name: str = ''):
    """Apply the unitary to the statevector using bmm method.

        """
def stack_broadcasted_single_qubit_rot_angles(op_dict): ...
def single_qubit_rot_angles_from_op_name(op_name: str, params: Incomplete | None = None):
    """
    unbroadcast single_qubit_rot_angles list.
    """
def create_op_originir(name, originir_str_list, wires, params, use_dagger) -> None:
    """
    create_op_originir
    """
def save_op_history(op_history, name, wires, params, use_dagger, q_machine, hyper_parameters={}) -> None:
    """normal quantum gate operator save into dict list."""

op_name_dict: Incomplete

def construct_modules_from_ops(operations: list, op_class_dict, measure_name_dict):
    """
    create a Module list from op_history(dict)
    
    """
def construct_op_with_autograd_param(current_gate, op_class_dict, measure_name_dict): ...
def check_same_dtype(t1, t2): ...
def check_same_device(t1, t2): ...
def get_sum_mat(op_list): ...
def expand_vector(vector, original_wires, expanded_wires): ...
def get_obs_eigvals(observables, all_wires): ...
def get_prod_mat(op_list):
    """
    return mat of op ,not permuted to sorted(wires)
    """
def reduce_matrices(mats_and_wires_gen, reduce_func: Callable): ...
