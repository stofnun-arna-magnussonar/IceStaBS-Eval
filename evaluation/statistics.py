import pandas as pd

from .token_level_eval import token_level_eval
from .globals import _StatOverview


def data_from_file(filepath: str) -> pd.DataFrame:
    """
    Read a TSV file into a DataFrame.
    """
    try:
        df = pd.read_csv(filepath, sep="\t", encoding="utf-8")
        return df
    except FileNotFoundError as e:
        print(f"File not found: {filepath} - {e}")
        return pd.DataFrame()


# build the overview data from the corrections dataframe


def build_overview_data(corrections: pd.DataFrame) -> pd.DataFrame:
    overview_data = []
    for col_name in corrections.columns:
        if col_name.startswith("ex_"):
            if col_name.endswith("standardized") or col_name.endswith("original"):
                continue
            example_nr = col_name.split("_")[1]
            example_id = "_".join(col_name.split("_")[:2])
            tool = "_".join(col_name.split("_")[2:])
            for i, row in corrections.iterrows():
                standardized_label = f"ex_{example_nr}_standardized"
                original_label = f"ex_{example_nr}_original"
                token_level_stats = token_level_eval(
                    row[original_label],
                    row[col_name],
                    row[standardized_label],
                )
                single_output_data = _StatOverview(
                    rule=row["Ritregla"],
                    tool=tool,
                    example_id=example_id,
                    input_text=row[original_label],
                    output_text=row[col_name],
                    correct=row[standardized_label],
                    tp_score=token_level_stats.true_positive,
                    fp_score=token_level_stats.false_positive,
                    tn_score=token_level_stats.true_negative,
                    fn_score=token_level_stats.false_negative,
                    sent_level_correct=(
                        1 if row[col_name] == row[standardized_label] else 0
                    ),
                )
                overview_data.append(single_output_data)
    overview_df = pd.DataFrame([vars(x) for x in overview_data])
    return overview_df


def f_score_per_tool(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate the F1 score for each tool in the DataFrame.
    """
    # create a new DataFrame to store the results
    f1_scores = pd.DataFrame(columns=["tool", "precision", "recall", "f1_score"])
    # sum the true positive, false positive and false negative scores for each tool
    for tool in df["tool"].unique():
        if tool in ["standardized, original"]:
            continue
        tool_df = df[df["tool"] == tool]
        tp = tool_df["tp_score"].sum()
        fp = tool_df["fp_score"].sum()
        fn = tool_df["fn_score"].sum()
        # calculate the precision, recall and F1 score
        precision = tp / (tp + fp) if tp + fp > 0 else 0
        recall = tp / (tp + fn) if tp + fn > 0 else 0
        f1_score = (
            2 * (precision * recall) / (precision + recall)
            if precision + recall > 0
            else 0
        )
        # append the results to the new DataFrame
        new_row = pd.DataFrame(
            {
                "tool": [tool],
                "precision": [precision],
                "recall": [recall],
                "f1_score": [f1_score],
            }
        )
        f1_scores = pd.concat([f1_scores, new_row], ignore_index=True)

    return f1_scores


def generate_summary_table(df: pd.DataFrame) -> pd.DataFrame:
    # Pivot table to sum up the 'sent_level_correct' values based on 'tool' and 'example_id'
    summary_table = pd.pivot_table(
        df,
        values="sent_level_correct",
        index="tool",
        columns="example_id",
        aggfunc="sum",
        fill_value=0,
    )

    num_rule_checks = len(df["rule"].unique())
    summary_table["Total_Count"] = summary_table.sum(axis=1)
    summary_table["Percentage"] = (
        summary_table["Total_Count"] / (num_rule_checks * 3) * 100
    )

    return summary_table


def generate_per_rule_table(df: pd.DataFrame) -> pd.DataFrame:
    # Helper function to extract the starting number of the rule
    def rule_class(rule):
        # Assuming the rule starts with a number followed by a period
        return int(rule.split(".")[0])

    # Apply the helper function to extract the starting rule number for each row
    df["rule_class"] = df["rule"].apply(rule_class)

    # Pivot table to sum the 'sent_level_correct' values based on 'rule_class' and 'tool'
    summary_table = pd.pivot_table(
        df,
        values="sent_level_correct",
        index="rule_class",  # Use the extracted rule_class for the row index
        columns="tool",  # Use tool as the column index
        aggfunc="sum",  # Sum up the 'sent_level_correct' values
        fill_value=0,  # Replace NaN values with 0
    )

    # add a column that counts the occurances of each rule id, by dividing the total count by the number of tools
    # but it should remaine an integer!
    num_tools = len(df["tool"].unique())
    summary_table["Total"] = df.groupby("rule_class")["rule"].count() / num_tools
    summary_table["Total"] = summary_table["Total"].astype(int)

    # the Total column should be after rule_class
    cols = summary_table.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    summary_table = summary_table[cols]

    return summary_table


def leaderboard_from_per_rule_table(df: pd.DataFrame) -> pd.DataFrame:
    """Get the highest scoring rules from the per rule table, by comparing to the total column"""

    output_cols = ["rule_class", "best_tool", "score", "possible", "percentage"]

    # Create a new DataFrame to store the results
    result = pd.DataFrame(columns=output_cols)

    # Iterate through each row in the input DataFrame
    for index, row in df.iterrows():
        rule_class = index
        possible = row["Total"]

        # Find the best tool (excluding 'Total' column)
        tool_columns = [col for col in df.columns if col != "Total"]
        best_tool = row[tool_columns].idxmax()
        score = row[best_tool]

        # Calculate percentage
        percentage = (score / possible) * 100 if possible > 0 else 0

        # Append the results to the new DataFrame
        new_row = pd.DataFrame(
            {
                "rule_class": [rule_class],
                "best_tool": [best_tool],
                "score": [score],
                "possible": [possible],
                "percentage": [percentage],
            }
        )
        result = pd.concat([result, new_row], ignore_index=True)

    # Sort the result by the rule_class in ascending order
    result = result.sort_values(by="rule_class")

    return result
