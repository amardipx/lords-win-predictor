import pandas as pd

df = pd.read_csv("data/lords-clean.csv")

df["StartDate"] = df["StartDate"].astype(str)

df = df.sort_values("StartDate")
first_innings = df.groupby("StartDate").first().reset_index()

def extract_runs(score):
    """Return the part before the slash."""
    score_str = str(score)
    return score_str.split("/")[0]  # everything before `/`

first_innings["Score"] = first_innings["Score"].apply(extract_runs)

final_df = first_innings[["Score", "Result"]]

final_df.to_csv("data/first_innings_scores.csv", index=False)

print(final_df.head(15))
print("\nTotal matches:", len(final_df))
print("Saved to data/first_innings_scores.csv")
