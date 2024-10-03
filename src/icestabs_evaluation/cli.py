import argparse
import logging
from typing import Dict
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
        "--benchmark",
        "-b",
        required=True,
        help="Path to the IceStaBS benchmark set JSON file",
    )
    single_file_parser.add_argument(
        "--tool_name",
        "-t",
        help="The name of the tool to evaluate, for visualization purposes",
        required=True,
    )
    single_file_parser.add_argument(
        "--file", "-f", help="Path to the single file to evaluate", required=True
    )
    single_file_parser.add_argument(
        "--output_format",
        "-o",
        help="Output format for the evaluation results",
        choices=["json", "table"],
        default="table",
    )

    # Subparser for config file evaluation
    config_file_parser = subparsers.add_parser(
        "config", help="Evaluate using a config file"
    )
    config_file_parser.add_argument(
        "--config", "-c", required=True, help="Path to the configuration YAML file"
    )
    config_file_parser.add_argument(
        "--rules", "-r", required=True, help="Path to the benchmark JSON file"
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
        logger.info(f"Using benchmark file: {args.benchmark}")
        global RULES
        RULES = load_rules_json(args.benchmark)
        logger.info("Rules loaded successfully")

        evaluate_single_output(args, RULES)
        # Add your logic for single file evaluation here

    elif args.mode == "csv":
        logger.info(f"Evaluating with csv file: {args.csv}")
        logger.info(f"Using benchmark file: {args.benchmark}")

        # Add your logic for csv file-based evaluation

    elif args.mode == "config":
        logger.info(f"Evaluating with config file: {args.config}")
        logger.info(f"Using benchmark file: {args.benchmark}")

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


def tables_to_json(tables: Dict[str, DataFrame]) -> Dict[str, dict]:
    return {
        table_name: table.to_dict(orient="records")
        for table_name, table in tables.items()
    }


def format_visual_summary(
    tool_name: str, tables: Dict[str, DataFrame], output_format: str
):
    """Basic visual summary of the evaluation results.

    Args:
        tool_name (str): Name of the tool that is being described.
        tables (List[DataFrame]): List of DataFrames to display.
    """
    from rich.console import Console

    console = Console()

    if output_format == "json":
        console.print(tables_to_json(tables))
        return
    if output_format == "table":
        console.print(f"\n[bold]Summary for single tool: '{tool_name}'[/bold]\n")

        for table_name, table in tables.items():
            console.print(f"[bold]{table_name}:[/bold]")
            console.print(f"{table.to_markdown(tablefmt='github', index=False)}\n")


def evaluate_single_output(args: argparse.Namespace, RULES):
    """
    Evaluates the output of a single tool based on the provided arguments and benchmark.

    Args:
        args (argparse.Namespace): The command-line arguments containing the input file and tool name.
        RULES: An object containing the benchmark and methods to retrieve original and standardized examples.

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

    # generate the main overview data used for the calculation
    overview_data = build_overview_data(data)

    # format the summary table
    summary_table = generate_summary_table(overview_data)
    summary_table = summary_table.reset_index(inplace=False)
    summary_renaming_map = {
        "Total_Count": "total_correct",
        "ex_1": "ex_1_correct",
        "ex_2": "ex_2_correct",
        "ex_3": "ex_3_correct",
    }
    summary_table = summary_table.rename(columns=summary_renaming_map)

    # format the per rule table
    per_rule_table = generate_per_rule_table(overview_data)
    per_rule_table = per_rule_table.reset_index(inplace=False)
    per_rule_table = per_rule_table.rename(columns={"Total": "total_possible"})

    # calculate the F1 scores per tool
    f1_scores_table = f_score_per_tool(overview_data)

    tables = {
        "Score per example": summary_table,
        "Score per rule chapter": per_rule_table,
        "F1 scores per tool": f1_scores_table,
    }

    format_visual_summary(tool_name, tables, args.output_format)


if __name__ == "__main__":
    main()
