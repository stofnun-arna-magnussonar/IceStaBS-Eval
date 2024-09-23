from evaluation.statistics import (
    data_from_file,
    build_overview_data,
    generate_summary_table,
    generate_per_rule_table,
    leaderboard_from_per_rule_table,
    f_score_per_tool,
)

MD_TEMPLATE = """
# Icelandic Standardization Benchmark Set: Spelling and punctuation (*IceStaBS-SP*)

This repository contains the Icelandic Standardization Benchmark Set (*IceStaBS*) for spelling and punctuation (*SP*).

## Evaluation

The following tools were evaluated on the _IceStaBS-SP_ dataset:
- Byte-Level Neural Error Correction Model for Icelandic - Yfirlestur (22.09)
  - Id: `byt5-22-09`
- Byte-Level Neural Error Correction Model for Icelandic - Yfirlestur (23.12)
  - Id: `byt5-23-12`
- Byte-Level Neural Error Correction Model for Icelandic - Yfirlestur (24.03)
  - Id: `byt5-24-03`
- Google Docs Spelling and Grammar check
  - Id: `google_docs`
- GreynirCorrect
  - Id: `greynir-correct`
- Icelandic GPT-SW3 for Spell and Grammar Checking
  - Id: `ice-gpt-sw3`
- Skrambi
  - Id: `skrambi`
- MS Word Spelling and Grammar check
  - Id: `word`

 

## Leaderboards

### Statistics per tool

<!-- statistics_per_tool -->

### Statistics per rule

<!-- statistics_per_rule -->

### Per-rule leaderboard

<!-- per_rule_leaderboard -->

### Token-level F1 Score per Tool

<!-- token_level_f1_scores -->
"""


def generate_readme(md, summary, f1_scores, per_rule, leaderboard):
    # rename the columns to be more human-readable

    per_tool_board = summary.to_markdown()
    per_rule_board = per_rule.to_markdown()
    leaderboard = leaderboard.to_markdown(index=False)
    token_level_f1 = f1_scores.to_markdown(index=False)

    md = md.replace("<!-- statistics_per_tool -->", per_tool_board)
    md = md.replace("<!-- statistics_per_rule -->", per_rule_board)
    md = md.replace("<!-- per_rule_leaderboard -->", leaderboard)
    md = md.replace("<!-- token_level_f1_scores -->", token_level_f1)

    with open("README.md", "w") as f:
        f.write(md)


if __name__ == "__main__":

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
    per_rule = per_rule.rename(
        columns={
            "rule_class": "Rule class",
        }
    )

    leaderboard = leaderboard.rename(
        columns={
            "rule_class": "Rule class",
        }
    )
    summary_table = summary_table.rename(
        columns={
            "tool": "Tool",
            "ex_1": "Example 1",
            "ex_2": "Example 2",
            "ex_3": "Example 3",
            "Total_Count": "Total",
            "Percentage": "%",
        }
    )

    f1_scores = f1_scores.sort_values(by="F1 Score", ascending=False)
    summary_table = summary_table.sort_values(by="%", ascending=False)

    generate_readme(MD_TEMPLATE, summary_table, f1_scores, per_rule, leaderboard)
