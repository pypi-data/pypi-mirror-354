from dataclasses import dataclass, asdict
from typing import Union, Callable
from typing import Tuple, List


BUFFER_NODE_ID = 'buffer'


class ScoringFailCodes:
    @dataclass
    class FailCode:
        code: int
        message: str
        _code_to_message = None

        def __post_init__(self):
            self._code_to_message[self.code] = self.message

    code_to_message = FailCode._code_to_message = {}

    # All score codes *MUST BE NEGATIVE*, but distinctly indicative of failure.
    train_model_absent = FailCode(
        code=-9990001,
        message="train model absent")
    function_call_failed = FailCode(
        code=-9990002,
        message="scoring function failed")
    function_score_too_low = FailCode(
        code=-9990003,
        message="scoring function returned score < 0, score ignored")
    function_score_too_high = FailCode(
        code=-9990004,
        message="scoring function returned score > 1, score ignored")


@dataclass
class TreeParams:
    chunk_size: int = None
    num_cores: int = 1
    leaf_factor: int = 2
    model_train_function: Callable = None
    model_train_function_params: dict = None
    optimized_for: str = None
    max_memory_gb: int = None
    is_mutable_coreset_size: bool = None
    save_all: bool = False

    def to_dict(self):
        return asdict(self)



def nodes_below(node: Tuple[int, int], level: int, n_children: int = 2) -> List[Tuple[int, int]]:
    """Returns all **possible** nodes below a given node in a tree, at a specified `level`."""
    node_lvl, node_idx = node
    levels_below = level - node_lvl
    start_idx = node_idx * (n_children**levels_below)
    nodes = [(level, idx) for idx in range(start_idx, start_idx + (n_children**levels_below))]
    return nodes
