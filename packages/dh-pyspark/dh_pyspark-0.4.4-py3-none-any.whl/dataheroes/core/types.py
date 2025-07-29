from dataclasses import asdict, dataclass
from typing import Any, Dict, Iterable, Tuple, Optional, Union


@dataclass
class CoresetSampleParams:
    coreset_size: Optional[Union[int, float, Tuple[int, Union[int, float]]]] = None
    det_weights_behaviour: Optional[str] = None
    deterministic_size: Optional[Union[int, float]] = None
    order: Optional[str] = "sort"
    # Not in rebuild
    # keep_duplicates: bool = False
    # sum_to_previous: bool = False

    def __post_init__(self):
        self.det_weights_behaviour = self.det_weights_behaviour if self.det_weights_behaviour is not None else "keep"

    def to_dict(self):
        return asdict(self)


@dataclass
class CoresetSampleParamsClassification(CoresetSampleParams):
    deterministic_size: Optional[float] = None
    sample_all: Optional[Iterable] = None
    class_size: Optional[Dict[Any, Union[int, float]]] = None
    minimum_size: Optional[Union[int, str, Dict[Any, int]]] = None
    fair: Optional[Union[str, bool]] = "training"

    def __post_init__(self):
        super().__post_init__()
        self.fair = self.fair if self.fair is not None else "training"
