from .swap_q1 import swap_global_global_q1 as swap_global_global_q1, swap_local_global_q1 as swap_local_global_q1
from _typeshed import Incomplete
from pyvqnet.distributed import CommController as CommController, get_rank as get_rank
from pyvqnet.tensor import arange as arange, cat as cat, no_grad as no_grad, permute as permute, swapaxis as swapaxis

class QubitsPermutation:
    num_elements: Incomplete
    map: Incomplete
    imap: Incomplete
    def __init__(self, num_elements) -> None: ...
    def obtain_intermediate_inverse_maps(self, target_map, M): ...
    def set_new_permutation_from_map(self, m, style_of_map: str = 'direct') -> None: ...
    def exchange_two_elements(self, element_1, element_2) -> None: ...

class QubitReorder:
    """
    multi qubits reorder,[q3,q2,q1,q0]
    """
    num_qubits: Incomplete
    num_proc: Incomplete
    n_global: Incomplete
    n_local: Incomplete
    comm: Incomplete
    local_states: Incomplete
    cur_map: Incomplete
    batch_size: Incomplete
    target_map: Incomplete
    def __init__(self, num_qubits, num_proc, local_states) -> None:
        """

        :param num_qubits: number of total qubits.
        :param num_proc: number of process in distributed env, should be equal to global qubits number.
        :param local_states = state vectors qtensor data in distributed env.
        """
    def apply_1q_local_global_swap(self, local_qubit, num_g) -> None: ...
    def run(self, target_map): ...
    def run_ll(self, target_map) -> None: ...
    def run_gg(self, target_map) -> None: ...
    def run_gl(self, target_map) -> None:
        """
        Do local qubit permute or local-global qubit permute or global-global qubit permute
        :param target_map: target qubits order list
        """
