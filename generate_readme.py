from pandas import DataFrame
from typing import Dict
from evaluation.statistics import (
    data_from_file,
    build_overview_data,
    generate_summary_table,
    generate_per_rule_table,
    leaderboard_from_per_rule_table,
    f_score_per_tool,
)
from evaluation import CONFIG as eval_config

MD_TEMPLATE = """
# Icelandic Standardization Benchmark Set: Spelling and punctuation (*IceStaBS-SP*)

This repository contains the Icelandic Standardization Benchmark Set (*IceStaBS*) for spelling and punctuation (*SP*).

## Quick Overview

<!-- token_level_f1_scores -->

## Evaluation

### Tools

<!-- tool_description -->

## Leaderboards

### Sentence-level Correctness

A straight-forward way to evaluate the tools is to calculate the percentage of sentences that are correctly standardized.
This is done by comparing the output of the tool to the expected output. If the input is identical to the expected output, the sentence is considered correct.

#### Statistics per tool

<!-- statistics_per_tool -->

#### Statistics per rule

<!-- statistics_per_rule -->

#### Per-rule leaderboard

<!-- per_rule_leaderboard -->

### Token-level correctness

In addition to the sentence-level correctness, we also calculate the token-level F1 score for each tool.

#### Token-level F1 Score per Tool

<!-- token_level_f1_scores -->
"""


# - [**Byte-Level Neural Error Correction Model for Icelandic - Yfirlestur (22.09)**](http://hdl.handle.net/20.500.12537/255)
#   - Evaluation ID: `byt5-22-09`
# - [**Byte-Level Neural Error Correction Model for Icelandic - Yfirlestur (23.12)**](http://hdl.handle.net/20.500.12537/321)
#   - Evaluation ID: `byt5-23-12`
# - [**Byte-Level Neural Error Correction Model for Icelandic - Yfirlestur (24.03)**](http://hdl.handle.net/20.500.12537/324)
#   - Evaluation ID: `byt5-24-03`
# - Google Docs Spelling and Grammar check
#   - Evaluation ID: `google`
# - [**GreynirCorrect**]()
#   - Evaluation ID: `greynir`
# - [**Icelandic GPT-SW3 for Spell and Grammar Checking**](https://huggingface.co/mideind/icelandic-gpt-sw3-6.7b-gec)
#   - Evaluation ID: `ice-gpt-sw3`
# - [**Skrambi**]()
#   - Evaluation ID: `skrambi`
# - MS Word Spelling and Grammar check
#   - Evaluation ID: `ms_word`


def generate_tool_description(config: Dict[str, str]) -> str:
    tool_description = ""
    for tool, tool_info in config["GLOBALS"]["tools"].items():
        if tool_info["url"] == "":
            tool_description += f"- **{tool_info['name']}**\n"
        else:
            tool_description += f"- [**{tool_info['name']}**]({tool_info['url']})\n"
        tool_description += f"  - Evaluation ID: `{tool_info['id']}`\n"
    return tool_description


def generate_readme(
    config: Dict[str, str],
    md: str,
    summary: DataFrame,
    f1_scores: DataFrame,
    per_rule: DataFrame,
    leaderboard: DataFrame,
    tool_names: Dict[str, str],
):

    per_tool_board = summary.to_markdown()
    per_rule_board = per_rule.to_markdown()
    leaderboard = leaderboard.to_markdown(index=False)
    token_level_f1 = f1_scores.to_markdown(index=False)

    md = md.replace("<!-- tool_description -->", generate_tool_description(config))

    md = md.replace("<!-- statistics_per_tool -->", per_tool_board)
    md = md.replace("<!-- statistics_per_rule -->", per_rule_board)
    md = md.replace("<!-- per_rule_leaderboard -->", leaderboard)
    md = md.replace("<!-- token_level_f1_scores -->", token_level_f1)

    # replace all the tool instances of the tool name keys with the tool name values
    for tool in tool_names.keys():
        md = md.replace(tool, tool_names[tool])

    # wrap the tool names in backticks if they are not already
    for tool in tool_names.values():
        md = md.replace(tool, f"`{tool}`")
        md = md.replace(f"``{tool}``", f"`{tool}`")

    with open("README.md", "w") as f:
        f.write(md)


if __name__ == "__main__":
    tool_name_map = {
        "byt5-22-09": "byt5-22-09",
        "byt5-23-12": "byt5-23-12",
        "byt5-24-03": "byt5-24-03",
        "google": "google",
        "greynir_correct": "greynir",
        "ice-gpt-sw3": "ice-gpt-sw3",
        "skrambi": "skrambi",
        "word": "ms_word",
    }
    data = data_from_file("data/corrections.tsv")
    overview = build_overview_data(data)
    # print the first row
    summary_table = generate_summary_table(overview)
    per_rule = generate_per_rule_table(overview)
    leaderboard = leaderboard_from_per_rule_table(per_rule)
    f1_scores = f_score_per_tool(overview)

    f1_scores = f1_scores.rename(
        columns={
            "tool": "Tool",
            "precision": "Precision",
            "recall": "Recall",
            "f1_score": "F1 Score",
        }
    )

    per_rule.index.name = "Rule class"

    leaderboard = leaderboard.rename(
        columns={
            "rule_class": "Rule class",
            "best_tool": "Best Tool",
            "score": "Score",
            "possible": "Possible",
            "percentage": "%",
        }
    )
    summary_table = summary_table.rename(
        columns={
            "ex_1": "Example 1",
            "ex_2": "Example 2",
            "ex_3": "Example 3",
            "Total_Count": "Total",
            "Percentage": "%",
        }
    )
    summary_table.index.name = "Tool"

    f1_scores = f1_scores.sort_values(by="F1 Score", ascending=False)
    summary_table = summary_table.sort_values(by="%", ascending=False)

    generate_readme(
        eval_config,
        MD_TEMPLATE,
        summary_table,
        f1_scores,
        per_rule,
        leaderboard,
        tool_name_map,
    )
