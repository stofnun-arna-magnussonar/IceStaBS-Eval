import argparse
import logging
from typing import List
from pandas import DataFrame
from . import load_rules_json, IceStaBSEvalException


logger = logging.getLogger(__name__)
# logging format
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


def main():
    parser = argparse.ArgumentParser(description="IceStaBS-SP Evaluation tool CLI")

    subparsers = parser.add_subparsers(dest="mode", help="Mode of operation")

    # Subparser for single file evaluation
    single_file_parser = subparsers.add_parser("single", help="Evaluate a single file")
    single_file_parser.add_argument(
        "--rules", "-r", required=True, help="Path to the rules JSON file"
    )
    single_file_parser.add_argument(
        "--tool_name", "-t", help="The name of the tool to evaluate", required=True
    )
    single_file_parser.add_argument(
        "--file", "-f", help="Path to the single file to evaluate", required=True
    )

    # Subparser for config file evaluation
    config_file_parser = subparsers.add_parser(
        "config", help="Evaluate using a config file"
    )
    config_file_parser.add_argument(
        "--config", "-c", required=True, help="Path to the configuration YAML file"
    )
    config_file_parser.add_argument(
        "--rules", "-r", required=True, help="Path to the rules JSON file"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARNING)

    # Handling different modes
    if args.mode == "single":
        logger.info(f"Evaluating single file: {args.file} with tool {args.tool_name}")
        logger.info(f"Using rules file: {args.rules}")
        global RULES
        RULES = load_rules_json(args.rules)
        logger.info("Rules loaded successfully")

        evaluate_single_output(args, RULES)
        # Add your logic for single file evaluation here

    elif args.mode == "csv":
        logger.info(f"Evaluating with csv file: {args.csv}")
        logger.info(f"Using rules file: {args.rules}")

        # Add your logic for csv file-based evaluation

    elif args.mode == "config":
        logger.info(f"Evaluating with config file: {args.config}")
        logger.info(f"Using rules file: {args.rules}")

        # Add your logic for config file-based evaluation here

    else:
        parser.print_help()


def list_to_dict(tool_name, rule_classes, lines) -> dict:
    interim = zip(list(rule_classes) * 3, lines)
    result = {}
    for rule_class, line in interim:
        if rule_class not in result:
            result[rule_class] = []
        result[rule_class].append(line)

    return {tool_name: result}


def validate_input_file(lines, rule_classes):
    # validate the number of lines, as it should be RULES * 3
    if len(lines) != len(rule_classes) * 3:
        raise IceStaBSEvalException(
            f"Invalid number of lines in file. Should be equal to , found {len(lines)}"
        )
    logger.info("Input file length valid.")


def visual_summary(tool_name: str, tables: List[DataFrame]):
    """Basic visual summary of the evaluation results.

    Args:
        tool_name (str): Name of the tool that is being described.
        tables (List[DataFrame]): List of DataFrames to display.
    """
    from rich.console import Console
    from rich.table import Table

    console = Console()

    console.print(f"\n[bold]Summary for {tool_name}[/bold]\n")

    for table in tables:
        console.print(f"[bold]{tool_name}[/bold]")
        console.print(f"{table}\n")


def evaluate_single_output(args: argparse.Namespace, RULES):
    """
    Evaluates the output of a single tool based on the provided arguments and rules.

    Args:
        args (argparse.Namespace): The command-line arguments containing the input file and tool name.
        RULES: An object containing the rules and methods to retrieve original and standardized examples.

    Returns:
        None

    This function performs the following steps:
    1. Loads the input file specified in the arguments.
    2. Converts the file content into a dictionary format suitable for evaluation.
    3. Retrieves original and standardized examples from the RULES object.
    4. Builds an overview of the data.
    5. Generates summary tables and F1 scores for the tool.
    6. Visualizes the summary data.

    The function logs the progress at various stages for debugging and informational purposes.
    """
    from . import (
        data_from_dict,
        build_overview_data,
    )
    from .statistics import (
        generate_summary_table,
        generate_per_rule_table,
        f_score_per_tool,
    )

    input_file = args.file
    tool_name = args.tool_name
    rule_classes = RULES.keys()
    lines = []

    logger.info(f"Loading file: {input_file}")
    with open(args.file, "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
    logger.info(f"File loaded successfully!")

    data_dict = list_to_dict(tool_name, rule_classes, lines)
    data_dict["original"] = RULES.get_original_examples()
    data_dict["standardized"] = RULES.get_standardized_examples()
    data = data_from_dict(data_dict)
    logger.info("Data loaded successfully!")

    overview_data = build_overview_data(data)

    summary_table = generate_summary_table(overview_data)
    per_rule_table = generate_per_rule_table(overview_data)
    f1_scores_table = f_score_per_tool(overview_data)

    visual_summary(tool_name, [summary_table, per_rule_table, f1_scores_table])


if __name__ == "__main__":
    main()
