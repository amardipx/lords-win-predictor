import pandas as pd

# Load data
df = pd.read_csv("data/lords-clean.csv")

# Ensure StartDate is string
df["StartDate"] = df["StartDate"].astype(str)

# Sort by match date + innings
df = df.sort_values(["StartDate", "Inns"])

# Extract ONLY second innings (Inns == 2)
second_innings = df[df["Inns"] == 2].copy()

# Function to extract run value from Score format (e.g., '391/8d', '42/0', '391')
def extract_runs(score):
    score_str = str(score)
    return score_str.split("/")[0]  # take part before '/'

# Apply
second_innings["Score"] = second_innings["Score"].apply(extract_runs).astype(int)

# Build final dataframe
final_df = second_innings[["Score", "Result"]].reset_index(drop=True)

output_path = "data/second_innings_scores.csv"
final_df.to_csv(output_path, index=False)

print(final_df.head(15))
print("\nTotal matches:", len(final_df))
print("Saved to", output_path)
