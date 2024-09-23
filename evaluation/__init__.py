
import pandas as pd

from dataclasses import dataclass
from typing import List

from .statistics import data_from_file, build_overview_data
from .globals import RULES

overview_data = []

    
def evaluate_tool(tool_name: str, tool_output: List[str]) -> pd.DataFrame:
    rule_classes = RULES.keys()

def get_example_set(set_nr: int) -> List[str]:
    if set_nr not in [1, 2, 3]:
        raise ValueError(f"Invalid example set number: {set_nr}")
    set_nr = set_nr-1
    return [RULES[key].examples[set_nr].original_sentence for key in RULES.keys()]
    
    

__all__ = [ evaluate_tool,
           data_from_file,
              build_overview_data,
           ]
