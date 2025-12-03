import pandas as pd

# Load cleaned data
df = pd.read_csv("data/lords-clean.csv")

output_rows = []

for i in range(len(df) - 1):
    current_row = df.iloc[i]
    next_row = df.iloc[i + 1]

    # Only third innings rows
    if current_row["Inns"] != 3:
        continue

    # Valid pair must be followed by Inns == 4
    if next_row["Inns"] == 4:
        score = int(current_row["Score"])              # convert to integer
        target = int(float(next_row["Target"]))         # safely convert float → int
        result = current_row["Result"]

        output_rows.append([score, target, result])

    # If next row starts a new match, skip both
    elif next_row["Inns"] == 1:
        continue

# Save output
out_df = pd.DataFrame(output_rows, columns=["Score", "Target", "Result"])
out_df.to_csv("data/third_innings_scores.csv", index=False)

print("✅ third_innings_scores.csv generated successfully!")
print("Total valid rows:", len(out_df))
print(out_df.head())
