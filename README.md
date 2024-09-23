
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

| tool            |   Example 1 |   Example 2 |   Example 3 |   Total |         % |
|:----------------|------------:|------------:|------------:|--------:|----------:|
| byt5-23-12      |         114 |         119 |         113 |     346 | 47.0748   |
| greynir_correct |         114 |         111 |         105 |     330 | 44.898    |
| byt5-22-09      |         107 |         109 |         100 |     316 | 42.9932   |
| byt5-24-03      |         105 |         107 |         100 |     312 | 42.449    |
| ice-gpt-sw3     |          89 |          86 |          70 |     245 | 33.3333   |
| google          |          77 |          75 |          68 |     220 | 29.932    |
| word            |          54 |          72 |          68 |     194 | 26.3946   |
| skrambi         |           0 |           1 |           3 |       4 |  0.544218 |

### Statistics per rule

|   rule_class |   Total |   byt5-22-09 |   byt5-23-12 |   byt5-24-03 |   google |   greynir_correct |   ice-gpt-sw3 |   skrambi |   word |
|-------------:|--------:|-------------:|-------------:|-------------:|---------:|------------------:|--------------:|----------:|-------:|
|            1 |     150 |           64 |           67 |           52 |        0 |                68 |            60 |         0 |     26 |
|            2 |      60 |           34 |           35 |           32 |       23 |                27 |            18 |         0 |     15 |
|            3 |      12 |            6 |            5 |            5 |        8 |                 9 |             3 |         0 |      3 |
|            4 |      21 |           14 |           12 |           13 |       10 |                17 |             6 |         0 |     13 |
|            5 |      75 |           18 |           26 |           25 |       39 |                32 |            16 |         0 |     28 |
|            6 |      12 |           10 |           11 |           11 |       12 |                10 |             4 |         0 |      9 |
|            7 |      21 |            6 |            5 |            8 |       13 |                14 |             7 |         0 |     10 |
|            8 |      39 |           23 |           26 |           27 |       24 |                28 |            17 |         1 |     13 |
|            9 |       3 |            3 |            3 |            2 |        2 |                 3 |             2 |         0 |      0 |
|           10 |      21 |            9 |           11 |           11 |       12 |                12 |             8 |         0 |      8 |
|           11 |       3 |            2 |            2 |            2 |        2 |                 2 |             2 |         0 |      2 |
|           12 |      30 |           25 |           25 |           23 |       10 |                18 |            19 |         0 |     18 |
|           13 |      12 |            1 |            3 |            4 |        5 |                 6 |             2 |         0 |      1 |
|           14 |      30 |           22 |           23 |           24 |       17 |                17 |            10 |         0 |     17 |
|           15 |      33 |           20 |           17 |           15 |       12 |                19 |             7 |         0 |      8 |
|           16 |      12 |            7 |            9 |            8 |        6 |                11 |             4 |         0 |      3 |
|           17 |       9 |            0 |            1 |            1 |        0 |                 3 |             1 |         0 |      0 |
|           18 |       3 |            3 |            3 |            3 |        2 |                 3 |             3 |         0 |      3 |
|           19 |      21 |            9 |           12 |           10 |       15 |                14 |            10 |         0 |      8 |
|           20 |       6 |            4 |            3 |            3 |        4 |                 5 |             4 |         0 |      4 |
|           21 |      42 |           10 |           10 |            9 |        1 |                 1 |            12 |         1 |      1 |
|           22 |      24 |            5 |           12 |            6 |        0 |                 2 |             7 |         0 |      1 |
|           23 |       3 |            0 |            1 |            0 |        0 |                 0 |             1 |         0 |      0 |
|           24 |       6 |            0 |            0 |            1 |        0 |                 0 |             0 |         0 |      0 |
|           25 |       3 |            3 |            2 |            2 |        2 |                 2 |             1 |         2 |      2 |
|           26 |      33 |            7 |           11 |            9 |        0 |                 2 |            12 |         0 |      1 |
|           27 |       6 |            0 |            1 |            1 |        1 |                 0 |             0 |         0 |      0 |
|           28 |       6 |            3 |            2 |            0 |        0 |                 0 |             3 |         0 |      0 |
|           29 |      18 |            5 |            4 |            3 |        0 |                 3 |             3 |         0 |      0 |
|           31 |       9 |            0 |            0 |            0 |        0 |                 2 |             1 |         0 |      0 |
|           32 |      12 |            3 |            4 |            2 |        0 |                 0 |             2 |         0 |      0 |

### Per-rule leaderboard

|   Rule class | best_tool       |   score |   possible |   percentage |
|-------------:|:----------------|--------:|-----------:|-------------:|
|            1 | greynir_correct |      68 |        150 |      45.3333 |
|            2 | byt5-23-12      |      35 |         60 |      58.3333 |
|            3 | greynir_correct |       9 |         12 |      75      |
|            4 | greynir_correct |      17 |         21 |      80.9524 |
|            5 | google          |      39 |         75 |      52      |
|            6 | google          |      12 |         12 |     100      |
|            7 | greynir_correct |      14 |         21 |      66.6667 |
|            8 | greynir_correct |      28 |         39 |      71.7949 |
|            9 | byt5-22-09      |       3 |          3 |     100      |
|           10 | google          |      12 |         21 |      57.1429 |
|           11 | byt5-22-09      |       2 |          3 |      66.6667 |
|           12 | byt5-22-09      |      25 |         30 |      83.3333 |
|           13 | greynir_correct |       6 |         12 |      50      |
|           14 | byt5-24-03      |      24 |         30 |      80      |
|           15 | byt5-22-09      |      20 |         33 |      60.6061 |
|           16 | greynir_correct |      11 |         12 |      91.6667 |
|           17 | greynir_correct |       3 |          9 |      33.3333 |
|           18 | byt5-22-09      |       3 |          3 |     100      |
|           19 | google          |      15 |         21 |      71.4286 |
|           20 | greynir_correct |       5 |          6 |      83.3333 |
|           21 | ice-gpt-sw3     |      12 |         42 |      28.5714 |
|           22 | byt5-23-12      |      12 |         24 |      50      |
|           23 | byt5-23-12      |       1 |          3 |      33.3333 |
|           24 | byt5-24-03      |       1 |          6 |      16.6667 |
|           25 | byt5-22-09      |       3 |          3 |     100      |
|           26 | ice-gpt-sw3     |      12 |         33 |      36.3636 |
|           27 | byt5-23-12      |       1 |          6 |      16.6667 |
|           28 | byt5-22-09      |       3 |          6 |      50      |
|           29 | byt5-22-09      |       5 |         18 |      27.7778 |
|           31 | greynir_correct |       2 |          9 |      22.2222 |
|           32 | byt5-23-12      |       4 |         12 |      33.3333 |

### Token-level F1 Score per Tool

| Tool            |   Precision |     Recall |   F1 Score |
|:----------------|------------:|-----------:|-----------:|
| byt5-23-12      |  0.768382   | 0.503614   |  0.608443  |
| byt5-24-03      |  0.770186   | 0.450363   |  0.568373  |
| byt5-22-09      |  0.71537    | 0.454217   |  0.555637  |
| greynir_correct |  0.654991   | 0.478873   |  0.553254  |
| ice-gpt-sw3     |  0.565863   | 0.380774   |  0.455224  |
| google          |  0.683168   | 0.329356   |  0.444444  |
| word            |  0.450704   | 0.314165   |  0.370248  |
| skrambi         |  0.00205339 | 0.00236407 |  0.0021978 |
