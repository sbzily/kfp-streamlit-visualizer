from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass(frozen=True)
class Step:
    id: str
    description: str = ""
    annotation: Optional[str] = None  # e.g. "CustomJob", "BigQuery"
    

@dataclass(frozen=True)
class PipelineDef:
    name: str
    steps: List[Step]
    edges: List[Tuple[str, str]]  # (from, to)


def steps_index(steps: List[Step]) -> Dict[str, Step]:
    return {s.id: s for s in steps}
