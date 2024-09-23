
# Icelandic Standardization Benchmark Set: Spelling and punctuation

This repository contains the Icelandic Standardization Benchmark Set (*IceStaBS*) for spelling and punctuation (*SP*).

# Overview

## Benchark Set

The benchmark set is based on the Rules of the icelandic written standard. The rules are available at [ritreglur.arnastofnun.is](https://ritreglur.arnastofnun.is/).

The rules of the icelandic written standard are divided into 33 chapters, with each class containing a various amount of sections and sub-rules.

We designate 246 specific rules which are applicable in the context of automatic correction of spelling and grammar.
This, combined to the fact that the rules are divided into 3 examples each, results in a total of 738 examples,
which can be used to evaluate the performance of automatic spelling and grammar correction tools, based on the standardization rules of the Icelandic language.

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

Stór stafur er alltaf ritaður í upphafi máls og í nýrri málsgrein á eftir punkti. Á eftir upphrópunarmerki, spurningarmerki og tvípunkti er stundum stór stafur, en aldrei á eftir kommu eða semíkommu, eins og ráða má af eftirfarandi dæmum og skýringum (sjá nánar um greinarmerki í reglum um greinarmerki).

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
        "ritreglur_url": "https://ritreglur.arnastofnun.is/#1.2.1"
    },
```

# Evaluation

## Quick Overview

We evaluate 8 tools on the *IceStaBS* dataset:

| Tool            |   Precision |     Recall |   F1 Score |
|:----------------|------------:|-----------:|-----------:|
| `byt5-23-12`      |  0.768382   | 0.503614   |  0.608443  |
| `byt5-24-03`      |  0.770186   | 0.450363   |  0.568373  |
| `byt5-22-09`      |  0.71537    | 0.454217   |  0.555637  |
| `greynir` |  0.654991   | 0.478873   |  0.553254  |
| `ice-gpt-sw3`     |  0.565863   | 0.380774   |  0.455224  |
| `google`          |  0.683168   | 0.329356   |  0.444444  |
| `ms_word`            |  0.450704   | 0.314165   |  0.370248  |
| `skrambi`         |  0.00205339 | 0.00236407 |  0.0021978 |

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
- [**Ritvilluvörnin Púki**](https://puki.is/)
  - Evaluation ID: `puki`


## Leaderboards

### Sentence-level Correctness

A straight-forward way to evaluate the tools is to calculate the percentage of sentences that are correctly standardized.
This is done by comparing the output of the tool to the expected output. If the input is identical to the expected output, the sentence is considered correct.

### Statistics per tool

| Tool            |   Ex. 1 |   Ex. 2 |   Ex. 3 |   Total |         % |
|:----------------|--------:|--------:|--------:|--------:|----------:|
| `byt5-23-12`      |     114 |     119 |     113 |     346 | 47.0748   |
| `greynir` |     114 |     111 |     105 |     330 | 44.898    |
| `byt5-22-09`      |     107 |     109 |     100 |     316 | 42.9932   |
| `byt5-24-03`      |     105 |     107 |     100 |     312 | 42.449    |
| `ice-gpt-sw3`     |      89 |      86 |      70 |     245 | 33.3333   |
| `google`          |      77 |      75 |      68 |     220 | 29.932    |
| `ms_word`            |      54 |      72 |      68 |     194 | 26.3946   |
| `skrambi`         |       0 |       1 |       3 |       4 |  0.544218 |

### Statistics per rule

|   Class |   Total |   `byt5-22-09` |   `byt5-23-12` |   `byt5-24-03` |   `google` |   `greynir` |   `ice-gpt-sw3` |   `skrambi` |   `ms_word` |
|--------:|--------:|-------------:|-------------:|-------------:|---------:|------------------:|--------------:|----------:|-------:|
|       1 |     150 |           64 |           67 |           52 |        0 |                68 |            60 |         0 |     26 |
|       2 |      60 |           34 |           35 |           32 |       23 |                27 |            18 |         0 |     15 |
|       3 |      12 |            6 |            5 |            5 |        8 |                 9 |             3 |         0 |      3 |
|       4 |      21 |           14 |           12 |           13 |       10 |                17 |             6 |         0 |     13 |
|       5 |      75 |           18 |           26 |           25 |       39 |                32 |            16 |         0 |     28 |
|       6 |      12 |           10 |           11 |           11 |       12 |                10 |             4 |         0 |      9 |
|       7 |      21 |            6 |            5 |            8 |       13 |                14 |             7 |         0 |     10 |
|       8 |      39 |           23 |           26 |           27 |       24 |                28 |            17 |         1 |     13 |
|       9 |       3 |            3 |            3 |            2 |        2 |                 3 |             2 |         0 |      0 |
|      10 |      21 |            9 |           11 |           11 |       12 |                12 |             8 |         0 |      8 |
|      11 |       3 |            2 |            2 |            2 |        2 |                 2 |             2 |         0 |      2 |
|      12 |      30 |           25 |           25 |           23 |       10 |                18 |            19 |         0 |     18 |
|      13 |      12 |            1 |            3 |            4 |        5 |                 6 |             2 |         0 |      1 |
|      14 |      30 |           22 |           23 |           24 |       17 |                17 |            10 |         0 |     17 |
|      15 |      33 |           20 |           17 |           15 |       12 |                19 |             7 |         0 |      8 |
|      16 |      12 |            7 |            9 |            8 |        6 |                11 |             4 |         0 |      3 |
|      17 |       9 |            0 |            1 |            1 |        0 |                 3 |             1 |         0 |      0 |
|      18 |       3 |            3 |            3 |            3 |        2 |                 3 |             3 |         0 |      3 |
|      19 |      21 |            9 |           12 |           10 |       15 |                14 |            10 |         0 |      8 |
|      20 |       6 |            4 |            3 |            3 |        4 |                 5 |             4 |         0 |      4 |
|      21 |      42 |           10 |           10 |            9 |        1 |                 1 |            12 |         1 |      1 |
|      22 |      24 |            5 |           12 |            6 |        0 |                 2 |             7 |         0 |      1 |
|      23 |       3 |            0 |            1 |            0 |        0 |                 0 |             1 |         0 |      0 |
|      24 |       6 |            0 |            0 |            1 |        0 |                 0 |             0 |         0 |      0 |
|      25 |       3 |            3 |            2 |            2 |        2 |                 2 |             1 |         2 |      2 |
|      26 |      33 |            7 |           11 |            9 |        0 |                 2 |            12 |         0 |      1 |
|      27 |       6 |            0 |            1 |            1 |        1 |                 0 |             0 |         0 |      0 |
|      28 |       6 |            3 |            2 |            0 |        0 |                 0 |             3 |         0 |      0 |
|      29 |      18 |            5 |            4 |            3 |        0 |                 3 |             3 |         0 |      0 |
|      31 |       9 |            0 |            0 |            0 |        0 |                 2 |             1 |         0 |      0 |
|      32 |      12 |            3 |            4 |            2 |        0 |                 0 |             2 |         0 |      0 |

### Per-rule leaderboard

|   Class | Best Tool       |   Score |   Possible |        % |
|--------:|:----------------|--------:|-----------:|---------:|
|       1 | `greynir` |      68 |        150 |  45.3333 |
|       2 | `byt5-23-12`      |      35 |         60 |  58.3333 |
|       3 | `greynir` |       9 |         12 |  75      |
|       4 | `greynir` |      17 |         21 |  80.9524 |
|       5 | `google`          |      39 |         75 |  52      |
|       6 | `google`          |      12 |         12 | 100      |
|       7 | `greynir` |      14 |         21 |  66.6667 |
|       8 | `greynir` |      28 |         39 |  71.7949 |
|       9 | `byt5-22-09`      |       3 |          3 | 100      |
|      10 | `google`          |      12 |         21 |  57.1429 |
|      11 | `byt5-22-09`      |       2 |          3 |  66.6667 |
|      12 | `byt5-22-09`      |      25 |         30 |  83.3333 |
|      13 | `greynir` |       6 |         12 |  50      |
|      14 | `byt5-24-03`      |      24 |         30 |  80      |
|      15 | `byt5-22-09`      |      20 |         33 |  60.6061 |
|      16 | `greynir` |      11 |         12 |  91.6667 |
|      17 | `greynir` |       3 |          9 |  33.3333 |
|      18 | `byt5-22-09`      |       3 |          3 | 100      |
|      19 | `google`          |      15 |         21 |  71.4286 |
|      20 | `greynir` |       5 |          6 |  83.3333 |
|      21 | `ice-gpt-sw3`     |      12 |         42 |  28.5714 |
|      22 | `byt5-23-12`      |      12 |         24 |  50      |
|      23 | `byt5-23-12`      |       1 |          3 |  33.3333 |
|      24 | `byt5-24-03`      |       1 |          6 |  16.6667 |
|      25 | `byt5-22-09`      |       3 |          3 | 100      |
|      26 | `ice-gpt-sw3`     |      12 |         33 |  36.3636 |
|      27 | `byt5-23-12`      |       1 |          6 |  16.6667 |
|      28 | `byt5-22-09`      |       3 |          6 |  50      |
|      29 | `byt5-22-09`      |       5 |         18 |  27.7778 |
|      31 | `greynir` |       2 |          9 |  22.2222 |
|      32 | `byt5-23-12`      |       4 |         12 |  33.3333 |

### Token-level correctness

In addition to the sentence-level correctness, we also calculate the token-level F1 score for each tool.

### Token-level F1 Score per Tool

| Tool            |   Precision |     Recall |   F1 Score |
|:----------------|------------:|-----------:|-----------:|
| `byt5-23-12`      |  0.768382   | 0.503614   |  0.608443  |
| `byt5-24-03`      |  0.770186   | 0.450363   |  0.568373  |
| `byt5-22-09`      |  0.71537    | 0.454217   |  0.555637  |
| `greynir` |  0.654991   | 0.478873   |  0.553254  |
| `ice-gpt-sw3`     |  0.565863   | 0.380774   |  0.455224  |
| `google`          |  0.683168   | 0.329356   |  0.444444  |
| `ms_word`            |  0.450704   | 0.314165   |  0.370248  |
| `skrambi`         |  0.00205339 | 0.00236407 |  0.0021978 |


# Acknowledgements

---

This README was automatically generated on 2024-09-23 at 22:50:08.

