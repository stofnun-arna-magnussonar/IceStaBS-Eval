
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

We evaluate 9 tools on the *IceStaBS* dataset:

| Tool       |   Precision |   Recall |   F1 Score |
|------------|-------------|----------|------------|
| `byt5-23-12` |    0.764168 | 0.501801 |   0.605797 |
| `byt5-24-03` |    0.76386  | 0.449275 |   0.565779 |
| `byt5-22-09` |    0.712406 | 0.454982 |   0.555311 |
| `greynir`    |    0.652632 | 0.475703 |   0.550296 |
| `skrambi`    |    0.62585  | 0.342432 |   0.442662 |
| `google`     |    0.674877 | 0.326579 |   0.440161 |
| `ms_word`       |    0.416822 | 0.311453 |   0.356515 |
| `puki`       |    0.346705 | 0.174603 |   0.232246 |

The tool with the highest F1 score is `byt5-23-12` with a token-level F-1 score of *0.61*.

## Tools

- [**Byte-Level Neural Error Correction Model for Icelandic - Yfirlestur (22.09)**](http://hdl.handle.net/20.500.12537/255)
  - Evaluation ID: `byt5-22-09`
- [**Byte-Level Neural Error Correction Model for Icelandic - Yfirlestur (23.12)**](http://hdl.handle.net/20.500.12537/321)
  - Evaluation ID: `byt5-23-12`
- [**Byte-Level Neural Error Correction Model for Icelandic - Yfirlestur (24.03)**](http://hdl.handle.net/20.500.12537/324)
  - Evaluation ID: `byt5-24-03`
- [**GreynirCorrect**](https://github.com/mideind/GreynirCorrect)
  - Evaluation ID: `greynir`
- [**Icelandic GPT-SW3 for Spell and Grammar Checking**](https://huggingface.co/mideind/icelandic-gpt-sw3-6.7b-gec)
  - Evaluation ID: `ice-gpt-sw3`
- [**Skrambi**](https://`skrambi`.arnastofnun.is/)
  - Evaluation ID: `skrambi`
- **Google Docs Spelling and Grammar check**
  - Evaluation ID: `google`
- **MS Word Spelling and Grammar check**
  - Evaluation ID: `ms_word`
- [**Ritvilluvörnin Púki**](https://`puki`.is/)
  - Evaluation ID: `puki`


## Leaderboards

### Sentence-level Correctness

A straight-forward way to evaluate the tools is to calculate the percentage of sentences that are correctly standardized.
This is done by comparing the output of the tool to the expected output. If the input is identical to the expected output, the sentence is considered correct.

### Statistics per tool

| Tool       |   Ex. 1 |   Ex. 2 |   Ex. 3 |   Total |       % |
|------------|---------|---------|---------|---------|---------|
| `byt5-23-12` |     114 |     119 |     109 |     342 | 46.1538 |
| `greynir`    |     114 |     108 |     103 |     325 | 43.8596 |
| `byt5-22-09` |     107 |     109 |      99 |     315 | 42.5101 |
| `byt5-24-03` |     104 |     106 |      97 |     307 | 41.4305 |
| `skrambi`    |      82 |      80 |      87 |     249 | 33.6032 |
| `google`     |      77 |      72 |      66 |     215 | 29.0148 |
| `ms_word`       |      54 |      71 |      67 |     192 | 25.9109 |
| `puki`       |      35 |      48 |      39 |     122 | 16.4642 |

### Statistics per rule

|   Class |   Total |   `byt5-22-09` |   `byt5-23-12` |   `byt5-24-03` |   `google` |   `greynir` |   `puki` |   `skrambi` |   `ms_word` |
|---------|---------|--------------|--------------|--------------|----------|-----------|--------|-----------|--------|
|       1 |     153 |           64 |           67 |           52 |        0 |        68 |     14 |        14 |     26 |
|       2 |      60 |           34 |           35 |           32 |       23 |        27 |      0 |        16 |     15 |
|       3 |      12 |            6 |            5 |            5 |        8 |         9 |      5 |        10 |      3 |
|       4 |      21 |           14 |           12 |           13 |       10 |        17 |     14 |        21 |     13 |
|       5 |      75 |           18 |           26 |           25 |       39 |        31 |     16 |        36 |     28 |
|       6 |      12 |            9 |           10 |           10 |       12 |        10 |      4 |         8 |      9 |
|       7 |      21 |            6 |            5 |            8 |       13 |        14 |      7 |        12 |     10 |
|       8 |      39 |           23 |           26 |           27 |       24 |        28 |     10 |        25 |     13 |
|       9 |       3 |            3 |            3 |            2 |        2 |         3 |      2 |         2 |      0 |
|      10 |      21 |            9 |           11 |           11 |       12 |        12 |      7 |        13 |      8 |
|      11 |       3 |            2 |            2 |            2 |        2 |         2 |      1 |         2 |      2 |
|      12 |      30 |           25 |           25 |           22 |        8 |        17 |      2 |        18 |     18 |
|      13 |      12 |            1 |            3 |            4 |        5 |         6 |      5 |         7 |      1 |
|      14 |      30 |           22 |           23 |           23 |       17 |        17 |      8 |        19 |     17 |
|      15 |      36 |           20 |           17 |           15 |       12 |        18 |      3 |        15 |      8 |
|      16 |      12 |            7 |            9 |            8 |        6 |        11 |      7 |         7 |      3 |
|      17 |       9 |            0 |            1 |            1 |        0 |         3 |      3 |         3 |      0 |
|      18 |       3 |            3 |            3 |            3 |        2 |         3 |      2 |         3 |      3 |
|      19 |      21 |            9 |           12 |           10 |       15 |        14 |      7 |        12 |      8 |
|      20 |       6 |            4 |            3 |            3 |        4 |         5 |      4 |         5 |      4 |
|      21 |      42 |           11 |           11 |           10 |        1 |         1 |      1 |         1 |      1 |
|      22 |      24 |            5 |           12 |            6 |        0 |         2 |      0 |         0 |      1 |
|      23 |       3 |            0 |            0 |            0 |        0 |         0 |      0 |         0 |      0 |
|      24 |       6 |            0 |            0 |            1 |        0 |         0 |      0 |         0 |      0 |
|      25 |       3 |            2 |            0 |            0 |        0 |         0 |      0 |         0 |      0 |
|      26 |      33 |            7 |           11 |            9 |        0 |         2 |      0 |         0 |      1 |
|      27 |       6 |            0 |            0 |            0 |        0 |         0 |      0 |         0 |      0 |
|      28 |       6 |            3 |            2 |            0 |        0 |         0 |      0 |         0 |      0 |
|      29 |      18 |            5 |            4 |            3 |        0 |         3 |      0 |         0 |      0 |
|      31 |       9 |            0 |            0 |            0 |        0 |         2 |      0 |         0 |      0 |
|      32 |      12 |            3 |            4 |            2 |        0 |         0 |      0 |         0 |      0 |

### Per-rule leaderboard

|   Class | Best Tool   |   Score |   Possible |        % |
|---------|-------------|---------|------------|----------|
|       1 | `greynir`     |      68 |        153 |  44.4444 |
|       2 | `byt5-23-12`  |      35 |         60 |  58.3333 |
|       3 | `skrambi`     |      10 |         12 |  83.3333 |
|       4 | `skrambi`     |      21 |         21 | 100      |
|       5 | `google`      |      39 |         75 |  52      |
|       6 | `google`      |      12 |         12 | 100      |
|       7 | `greynir`     |      14 |         21 |  66.6667 |
|       8 | `greynir`     |      28 |         39 |  71.7949 |
|       9 | `byt5-22-09`  |       3 |          3 | 100      |
|      10 | `skrambi`     |      13 |         21 |  61.9048 |
|      11 | `byt5-22-09`  |       2 |          3 |  66.6667 |
|      12 | `byt5-22-09`  |      25 |         30 |  83.3333 |
|      13 | `skrambi`     |       7 |         12 |  58.3333 |
|      14 | `byt5-23-12`  |      23 |         30 |  76.6667 |
|      15 | `byt5-22-09`  |      20 |         36 |  55.5556 |
|      16 | `greynir`     |      11 |         12 |  91.6667 |
|      17 | `greynir`     |       3 |          9 |  33.3333 |
|      18 | `byt5-22-09`  |       3 |          3 | 100      |
|      19 | `google`      |      15 |         21 |  71.4286 |
|      20 | `greynir`     |       5 |          6 |  83.3333 |
|      21 | `byt5-22-09`  |      11 |         42 |  26.1905 |
|      22 | `byt5-23-12`  |      12 |         24 |  50      |
|      23 | `byt5-22-09`  |       0 |          3 |   0      |
|      24 | `byt5-24-03`  |       1 |          6 |  16.6667 |
|      25 | `byt5-22-09`  |       2 |          3 |  66.6667 |
|      26 | `byt5-23-12`  |      11 |         33 |  33.3333 |
|      27 | `byt5-22-09`  |       0 |          6 |   0      |
|      28 | `byt5-22-09`  |       3 |          6 |  50      |
|      29 | `byt5-22-09`  |       5 |         18 |  27.7778 |
|      31 | `greynir`     |       2 |          9 |  22.2222 |
|      32 | `byt5-23-12`  |       4 |         12 |  33.3333 |

### Token-level correctness

In addition to the sentence-level correctness, we also calculate the token-level F1 score for each tool.

### Token-level F1 Score per Tool

| Tool       |   Precision |   Recall |   F1 Score |
|------------|-------------|----------|------------|
| `byt5-23-12` |    0.764168 | 0.501801 |   0.605797 |
| `byt5-24-03` |    0.76386  | 0.449275 |   0.565779 |
| `byt5-22-09` |    0.712406 | 0.454982 |   0.555311 |
| `greynir`    |    0.652632 | 0.475703 |   0.550296 |
| `skrambi`    |    0.62585  | 0.342432 |   0.442662 |
| `google`     |    0.674877 | 0.326579 |   0.440161 |
| `ms_word`       |    0.416822 | 0.311453 |   0.356515 |
| `puki`       |    0.346705 | 0.174603 |   0.232246 |


# Acknowledgements



---

This README was automatically generated on 2024-09-24 at 17:13:15.

