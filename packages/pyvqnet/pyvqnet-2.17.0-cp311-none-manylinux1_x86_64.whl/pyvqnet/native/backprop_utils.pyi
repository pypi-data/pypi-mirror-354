from .._core import Tensor as CoreTensor
from ..device import DEV_CPU as DEV_CPU, DEV_GPU_0 as DEV_GPU_0
from ..dtype import vqnet_complex_float_dtypes as vqnet_complex_float_dtypes
from _typeshed import Incomplete

global_cache_map: Incomplete
use_qtensor_graphnode: bool

def set_use_qtensor_graphnode(flag) -> None: ...
def get_use_qtensor_graphnode(): ...
def erase_global_cache_map() -> None: ...
def get_global_cache_map(id): ...
def del_kv_in_global_cache_map(key) -> None: ...
def set_global_cache_map(id, fake) -> None: ...

class DummyTensor:
    id: Incomplete
    nodes: Incomplete
    device: Incomplete
    requires_grad: Incomplete
    shape: Incomplete
    dtype: Incomplete
    grad: Incomplete
    data: Incomplete
    def __init__(self, input_id, t) -> None: ...
    def hook_function(self): ...

def create_fake_tensor(input_id, if_weights, t): ...

class keep_activation_in_graph:
    prev: bool
    def __init__(self) -> None: ...
    def __enter__(self) -> None: ...
    def __exit__(self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: types.TracebackType | None) -> None: ...

class AutoGradNode:
    """
    A dummy autograd node for internal gradients calculation.
    It simply mocks QTensor without real data reference to save some storage.
    For internal activation may not need real data for backward.
    """
    id: Incomplete
    if_not_dummy: Incomplete
    tensor: Incomplete
    name: Incomplete
    df: Incomplete
    device: Incomplete
    def __init__(self, tensor, df, name: str = '') -> None: ...

def backprop(g, end_node, save_grad: bool = False, save_intern_act: bool = True): ...
def backprop_impl(g, end_node, save_grad: bool, save_intern_act: bool):
    """
    real backpropgation impl
    """
def get_core_tensor_ingrad(node, i, outgrad, parent) -> CoreTensor:
    """
    calculate grad based on df.
    """
def free_backprop_grad(g, end_node) -> None: ...
def post_accum_grad_for_dp(end_node) -> None:
    """
    #all grad are done calculation, do all_reduce for data paralled(dp)
    """
