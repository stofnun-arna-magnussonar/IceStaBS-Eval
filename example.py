from evaluation.statistics import (
    data_from_file,
    build_overview_data,
    generate_summary_table,
    generate_per_rule_table,
    leaderboard_from_per_rule_table,
    f_score_per_tool,
)


data = data_from_file("data/corrections.tsv")
overview = build_overview_data(data)
f1_scores = f_score_per_tool(overview)
# print the first row
per_rule = generate_per_rule_table(overview)
leaderboard = leaderboard_from_per_rule_table(per_rule)
