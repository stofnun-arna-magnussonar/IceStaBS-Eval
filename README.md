# IceStaBS-Eval

IceStaBS-Eval is a Python (3.10+) package for evaluating the performance of automatic spelling and grammar correction tools on the Icelandic language, by using the Icelandic Standardization Benchmark Set: Spelling and Punctuation (IceStaBS:SP) benchmark set.

# Overview

## Installation

```bash
pip install git+https://github.com/stofnun-arna-magnussonar/IceStaBS-Eval.git
```

Running `icestabs-eval --help` should then produce the following output:

```bash
usage: icestabs-eval [-h] [--verbose] {single,config} ...

IceStaBS-SP Evaluation tool CLI

positional arguments:
  {single,config}  Mode of operation
    single         Evaluate a single file
    config         Evaluate using a config file

options:
  -h, --help       show this help message and exit
  --verbose, -v    Enable verbose logging
```

## Usage (CLI)

After installation, running the following command:

```bash
# Note: the path to the IceStaBS-SP benchmark set must be provided
icestabs-eval --verbose\
     single \
    --rules '/path/to/IceStaBS.json' \
    --file 'demo_corrections.txt'
    --tool 'demo_tool' \
```

will:

- Read the rules in the file `IceStaBS.json` at the given location.
- Evaluate the performance of a **single** tool, with the designated name `demo_tool`
- The file `demo_corrections.txt` will be read as this tool's output file, on the IceStabs-SP benchark set sentences

This will in turn produce the following output to the command line>

```bash
Summary for demo_tool

demo_tool
example_id  ex_1  ex_2  ex_3  Total_Count  Percentage
tool
demo_tool    107   109    99          315   42.510121

demo_tool
tool        Total  demo_tool
rule_class
1             153         64
2              60         34
3              12          6
4              21         14
5              75         18
6              12          9
7              21          6
8              39         23
9               3          3
10             21          9
11              3          2
12             30         25
13             12          1
14             30         22
15             36         20
16             12          7
17              9          0
18              3          3
19             21          9
20              6          4
21             42         11
22             24          5
23              3          0
24              6          0
25              3          2
26             33          7
27              6          0
28              6          3
29             18          5
31              9          0
32             12          3

demo_tool
        tool  precision    recall  f1_score
0  demo_tool   0.712406  0.454982  0.555311
```

## Contents

### IceStaBS-Evaluation

The IceStaBS-Evaluation package contains the tools to evaluate the performance of automatic spelling and grammar correction tools on the Icelandic language, by using the Icelandic Standardization Benchmark Set: Spelling and Punctuation (IceStaBS-SP) benchmark set.

### M14-Eval

Aside from the IceStaBS-Evaluation package, the repository contains the source code used in used in the evaluation of various Icelandic spell and grammar checking tool.

This is provided as use-case examples of how to use the IceStaBS-Evaluation package and for reproducibility purposes.

directory structure is as follows:

- `M14-Eval/`: Contains the source code used in the evaluation of the M14 spell and grammar checking tool.
  - `data/`: Contains the data used in the evaluation, both manually generated and automatically generated.
  - `M14-eval-config.yml`: Configuaration file for the evaluation.
  - `correcting-env.yml`: Metadata on the Conda environment used in generating the corrections and during evaluation.
  - `generate_corrections.py`: Python script that generates corrected output for each tool
  - `generate_readme.py`: Python script that uses the IceStaBS-Evaluation package to generate a README file for the evaluation, with statistics on each tool.
  - `README.md`: The README file for the evaluation.

## Benchmark Set

The main prerequesite for the code in this repository is the Icelandic Standardization Benchmark Set: Spelling and Punctuation (IceStaBS-SP) benchmark set.

The benchmark set is based on the Rules of the Icelandic written standard. The rules are available at [ritreglur.arnastofnun.is](https://ritreglur.arnastofnun.is/).

The rules of the Icelandic written standard are divided into 33 chapters, with each class containing a various amount of sections and sub-rules.

We designate 246 specific rules which are applicable in the context of automatic correction of spelling and grammar.
This, combined to the fact that the rules are divided into 3 examples each, results in a total of 738 examples,
which can be used to evaluate the performance of automatic spelling and grammar correction tools, based on the Language Usage Database (\*Málfarsbankinn.)

These attributes allow for a detailed evaluation of the performance of the tools on the _IceStaBS_ dataset.

We make the benchmark set available in JSON format, which can be found in the `data` directory of this repository.

<!-- ## Contents

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

````

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
``` -->
