import json
import os
from typing import Any, Dict, List
from dataclasses import dataclass
from collections import namedtuple


@dataclass
class _StatOverview:
    rule: str # corresponds to the 'Ritregla' column
    tool: str # follows ex_1, ex_2, ex_3 in the tool column name
    example_id: str # ex_1, ex_2, ex_3 at the start of the tool column name
    input_text: str # oldeidrett_1, oldeidrett_2, oldeidrett_3
    output_text: str # e.g. ex_3_greynir_correct
    correct: str # Leiðrétt dæmi 1, 2, 3
    tp_score: int # true positive tokens
    fp_score: int # false positive tokens
    tn_score: int # true negative tokens
    fn_score: int # false negative tokens
    sent_level_correct: int # 1 if the output is identical to expected, 0 otherwise
    
@dataclass
class RuleExample:
    original_sentence: str
    standardized_sentence: str
    suggestion: str
    original_part: str
    standardized_part: str
    
    
@dataclass
class SingleRule:
    short_suggestion: str
    long_suggestion: str
    examples: List[RuleExample]
    error_code: str
    ritreglur_url: str
    
Rules = Dict[str, SingleRule]

def load_rules_json(rules_filepath: str) -> Dict[str, Any]:
    with open(rules_filepath, 'r') as f:
        rules = json.load(f)
    new_rules = {}
    # Convert the rules to a Rule object
    for rule_name, rule_data in rules.items():
        if rule_data == None:
            continue
        examples = rule_data.pop('examples')
        ex_1 = RuleExample(**examples['1'])
        ex_2 = RuleExample(**examples['2'])
        ex_3 = RuleExample(**examples['3'])
        rule_data['examples'] = [ex_1, ex_2, ex_3]
        new_rules[rule_name] = SingleRule(**rule_data)
    # print(rules.keys())
    return new_rules

# find the current files path 
current_file_path = os.path.abspath(__file__)
RULES = load_rules_json(os.path.join(os.path.dirname(os.path.dirname(current_file_path)), 'data/IceStaBS-SP.json'))