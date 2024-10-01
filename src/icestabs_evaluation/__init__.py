import json
import yaml
from typing import List
from typing import Any, Dict, List
from dataclasses import dataclass


class IceStaBSEvalException(Exception):
    pass


@dataclass
class _StatOverview:
    rule: str  # corresponds to the 'Ritregla' column
    tool: str  # follows ex_1, ex_2, ex_3 in the tool column name
    example_id: str  # ex_1, ex_2, ex_3 at the start of the tool column name
    input_text: str  # oldeidrett_1, oldeidrett_2, oldeidrett_3
    output_text: str  # e.g. ex_3_greynir_correct
    correct: str  # Leiðrétt dæmi 1, 2, 3
    tp_score: int  # true positive tokens
    fp_score: int  # false positive tokens
    tn_score: int  # true negative tokens
    fn_score: int  # false negative tokens
    sent_level_correct: int  # 1 if the output is identical to expected, 0 otherwise


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


class RulesContainer:
    """
    RulesContainer is a class that manages a collection of rules and provides methods to retrieve original and standardized sentences from these rules.

    Attributes:
        rules (Dict[str, SingleRule]): A dictionary where keys are rule identifiers and values are SingleRule objects.

    Methods:
        __init__(rules: Dict[str, SingleRule]):
            Initializes the RulesContainer with a dictionary of rules.

        get_original_set(set_nr: int) -> List[str]:
            Retrieves a specific set of original sentences across all rules.
            Args:
                set_nr (int): The set number (1, 2, or 3) to retrieve.
            Returns:
                List[str]: A list of original sentences from the specified set.
            Raises:
                ValueError: If the set number is not 1, 2, or 3.

        get_standardized_set(set_nr: int) -> List[str]:
            Retrieves a specific set of standardized sentences across all rules.
            Args:
                set_nr (int): The set number (1, 2, or 3) to retrieve.
            Returns:
                List[str]: A list of standardized sentences from the specified set.
            Raises:
                ValueError: If the set number is not 1, 2, or 3.

        get_original_examples() -> Dict[str, List[str]]:
            Retrieves all the original examples from the rules.
            Returns:
                Dict[str, List[str]]: A dictionary where keys are rule identifiers and values are lists of original sentences.

        get_standardized_examples() -> Dict[str, List[str]]:
            Retrieves all the standardized examples from the rules.
            Returns:
                Dict[str, List[str]]: A dictionary where keys are rule identifiers and values are lists of standardized sentences.

        keys():
            Retrieves the keys of the rules dictionary.
            Returns:
                dict_keys: The keys of the rules dictionary.
    """

    def __init__(self, rules: Dict[str, SingleRule]):
        self.rules = rules

    def get_original_set(self, set_nr: int) -> List[str]:
        """Get a specific set of original sentences across all rules."""
        if set_nr not in [1, 2, 3]:
            raise ValueError(f"Invalid example set number: {set_nr}")
        set_nr = set_nr - 1
        return [
            self.rules[key].examples[set_nr].original_sentence
            for key in self.rules.keys()
            if self.rules[key].examples[set_nr] is not None
        ]

    def get_standardized_set(self, set_nr: int) -> List[str]:
        """Get a specific set of standardized sentences across all rules."""
        if set_nr not in [1, 2, 3]:
            raise ValueError(f"Invalid example set number: {set_nr}")
        set_nr = set_nr - 1
        return [
            self.rules[key].examples[set_nr].standardized_sentence
            for key in self.rules.keys()
            if self.rules[key].examples[set_nr] is not None
        ]

    def get_original_examples(self) -> Dict[str, List[str]]:
        """Get all the original examples from the rules."""
        return {
            key: [
                ex.original_sentence
                for ex in self.rules[key].examples
                if ex is not None
            ]
            for key in self.rules.keys()
        }

    def get_standardized_examples(self) -> Dict[str, List[str]]:
        """Get all the standardized examples from the rules."""
        return {
            key: [
                ex.standardized_sentence
                for ex in self.rules[key].examples
                if ex is not None
            ]
            for key in self.rules.keys()
        }

    def keys(self):
        return self.rules.keys()


def load_config_yaml(config_filepath: str) -> RulesContainer:
    """
    Load a YAML configuration file.

    This function reads a YAML file from the specified file path and returns its contents as a dictionary.

    Args:
        config_filepath (str): The path to the YAML configuration file.

    Returns:
        Dict[str, Any]: The contents of the YAML file as a dictionary.

    Raises:
        FileNotFoundError: If the file at the specified path does not exist.
    """
    try:
        with open(config_filepath, "r") as f:
            config = yaml.safe_load(f)
        return config
    except FileNotFoundError:
        raise FileNotFoundError(
            "The config file was not found at the given path. Please make sure the file exists."
        )


def load_rules_json(rules_filepath: str) -> RulesContainer:
    """
    Load rules from a JSON file and convert them into a RulesContainer object.
    """
    try:
        with open(rules_filepath, "r") as f:
            rules = json.load(f)
        new_rules = {}
        # Convert the rules to a SingleRule object
        for rule_name, rule_data in rules.items():
            if rule_data is None:
                continue
            examples = rule_data.pop("examples")
            ex_1 = RuleExample(**examples["1"])
            ex_2 = RuleExample(**examples["2"])
            try:
                ex_3 = RuleExample(**examples["3"])
            except KeyError:
                ex_3 = None
            rule_data["examples"] = [ex_1, ex_2, ex_3]
            new_rules[rule_name] = SingleRule(**rule_data)

        return RulesContainer(new_rules)

    except FileNotFoundError:
        raise FileNotFoundError(
            f"The IceStaBS-SP.json file was not found at the given path {rules_filepath}. Please make sure the file exists."
        )


from .statistics import (
    data_from_tsv,
    data_from_dict,
    build_overview_data,
)


__all__ = [
    data_from_tsv,
    data_from_dict,
    build_overview_data,
    load_rules_json,
    load_config_yaml,
]
