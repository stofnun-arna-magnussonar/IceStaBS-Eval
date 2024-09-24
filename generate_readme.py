from pandas import DataFrame
from typing import Dict
from datetime import datetime
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
# Icelandic Standardization Benchmark Set: Spelling and punctuation

This repository contains the Icelandic Standardization Benchmark Set (*IceStaBS*) for spelling and punctuation (*SP*).

# Overview

## Benchark Set

The benchmark set is based on the Rules of the icelandic written standard. The rules are available at [ritreglur.arnastofnun.is](https://ritreglur.arnastofnun.is/).

The rules of the icelandic written standard are divided into 33 chapters, with each class containing a various amount of sections and sub-rules.

We designate 246 specific rules which are applicable in the context of automatic correction of spelling and grammar.
This, combined to the fact that the rules are divided into 3 examples each, results in a total of 738 examples,
which can be used to evaluate the performance of automatic spelling and grammar correction tools, based on the Language Usage Database (*Málfarsbankinn.)

These attributes allow for a detailed evaluation of the performance of the tools on the _IceStaBS_ dataset.

We make the benchmark set available in JSON format, which can be found in the `data` directory of this repository.

## Contents

The entry for each official spelling rule we cover contains:

- A reference to the rule number.
- A short explanation of the rule
- A longer explanation
- Three short examples (1-2 sentences) of a text containing the relevant error
- The relevant error code in the [Icelandic Error Corpus](http://hdl.handle.net/20.500.12537/105)
- The URL to the online entry of the spelling rule in question.

An example is given below, for rule a one of two examples of [rule 1.2.1](https://ritreglur.arnastofnun.is/#1.2.1).

The relevant excerpt of the original rule is as follows:

```
1.2.1 Stór stafur er ritaður í upphafi máls

Stór stafur er alltaf ritaður í upphafi máls og í nýrri málsgrein á eftir punkti. Á eftir upphrópunarmerki, spurningarmerki 
og tvípunkti er stundum stór stafur, en aldrei á eftir kommu eða semíkommu, eins og ráða má af eftirfarandi dæmum og
skýringum (sjá nánar um greinarmerki í reglum um greinarmerki).

    Hann er kominn. Það var nú gott. [Upphaf máls og ný málsgrein á eftir punkti.]

```

The JSON entry (non-exhaustive) for this rule is as follows:

```json
    "1.2.1 (a)": {
        "short_suggestion": "<villa> á líklega að vera með stórum staf, <leiðrétt>, þar sem það kemur á eftir punkti.",
        "long_suggestion": "Stór stafur er alltaf ritaður í upphafi máls og í nýrri málsgrein á eftir punkti. Sjá ritreglu 1.2.1 (https://ritreglur.arnastofnun.is/#1.2.1).",
        "examples": {
            "1": {
                "original_sentence": "Afi og amma ætla að koma í heimsókn. þau koma bráðum.",
                "standardized_sentence": "Afi og amma ætla að koma í heimsókn. Þau koma bráðum.",
                "suggestion": "<þau> á líklega að vera með stórum staf, <Þau>, þar sem það kemur á eftir punkti.",
                "original_part": "þau",
                "standardized_part": "Þau"
            },
            "2": {
                "original_sentence": "Ráðgert er að nýtt hús rísi í vor. vinnan við það er þó ekki hafin.",
                "standardized_sentence": "Ráðgert er að nýtt hús rísi í vor. Vinnan við það er þó ekki hafin.",
                "suggestion": "<vinnan> á líklega að vera með stórum staf, <Vinnan>, þar sem það kemur á eftir punkti.",
                "original_part": "vinnan",
                "standardized_part": "Vinnan"
            },
            "3": {
                "original_sentence": "Margt skiptir máli þegar skáldsögur eru skrifaðar. málfar er t.d. mikilvægar þáttur.",
                "standardized_sentence": "Margt skiptir máli þegar skáldsögur eru skrifaðar. Málfar er t.d. mikilvægar þáttur.",
                "suggestion": "<málfar> á líklega að vera með stórum staf, <Málfar>, þar sem það kemur á eftir punkti.",
                "original_part": "málfar",
                "standardized_part": "Málfar"
            }
        },
        "error_code": "lower4upper-initial",
        "ritreglur_url": "https://ritreglur.arnastofnun.is/#/1.2.1 (a)"
    },
```

# Evaluation

## Quick Overview

We evaluate <tool_count> tools on the *IceStaBS* dataset:

<!-- token_level_f1_scores -->

The tool with the highest F1 score is <tool_1> with a token-level F-1 score of *<score_1>*.

## Tools

<!-- tool_description -->

## Leaderboards

### Sentence-level Correctness

A straight-forward way to evaluate the tools is to calculate the percentage of sentences that are correctly standardized.
This is done by comparing the output of the tool to the expected output. If the input is identical to the expected output, the sentence is considered correct.

### Statistics per tool

<!-- statistics_per_tool -->

### Statistics per rule

<!-- statistics_per_rule -->

### Per-rule leaderboard

<!-- per_rule_leaderboard -->

### Token-level correctness

In addition to the sentence-level correctness, we also calculate the token-level F1 score for each tool.

### Token-level F1 Score per Tool

<!-- token_level_f1_scores -->

<!-- footer -->
"""


def generate_tool_description(config: Dict[str, str]) -> str:
    tool_description = ""
    for tool, tool_info in config["GLOBALS"]["tools"].items():
        if tool_info["url"] == "":
            tool_description += f"- **{tool_info['name']}**\n"
        else:
            tool_description += f"- [**{tool_info['name']}**]({tool_info['url']})\n"
        tool_description += f"  - Evaluation ID: `{tool_info['id']}`\n"
    return tool_description


def footer():
    gen_date = datetime.now().strftime("%Y-%m-%d at %H:%M:%S")
    footer = f"""
# Acknowledgements



---

This README was automatically generated on {gen_date}.
"""

    return footer


def generate_readme(
    config: Dict[str, str],
    md: str,
    summary: DataFrame,
    f1_scores: DataFrame,
    per_rule: DataFrame,
    leaderboard: DataFrame,
    tool_names: Dict[str, str],
):

    highest_f1 = f1_scores.iloc[0]
    md = md.replace("<tool_count>", str(len(tool_names)))
    md = md.replace("<tool_1>", tool_names[highest_f1["Tool"]])
    md = md.replace("<score_1>", str(round(highest_f1["F1 Score"], 2)))

    per_tool_board = summary.to_markdown(tablefmt="github")
    per_rule_board = per_rule.to_markdown(tablefmt="github")
    leaderboard = leaderboard.to_markdown(index=False, tablefmt="github")
    token_level_f1 = f1_scores.to_markdown(index=False, tablefmt="github")

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

    md = md.replace("<!-- footer -->", footer())

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
        "puki": "puki",
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

    per_rule.index.name = "Class"

    leaderboard = leaderboard.rename(
        columns={
            "rule_class": "Class",
            "best_tool": "Best Tool",
            "score": "Score",
            "possible": "Possible",
            "percentage": "%",
        }
    )
    summary_table = summary_table.rename(
        columns={
            "ex_1": "Ex. 1",
            "ex_2": "Ex. 2",
            "ex_3": "Ex. 3",
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
