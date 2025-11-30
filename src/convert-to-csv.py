import re
import pandas as pd

# Load raw text
with open("data/lords-raw.txt", "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]

# Skip the header (first line contains column names, not data)
lines = lines[1:]

# Regex pattern that handles multi-word teams & opposition
pattern = re.compile(
    r"^(?P<Team>[A-Za-z ]+)\s+"
    r"(?P<Score>[0-9/]+d?)\s+"
    r"(?P<Overs>[0-9.]+)\s+"
    r"(?P<Target>[0-9]*)\s*"
    r"(?P<RPO>[0-9.]+)\s+"
    r"(?P<Inns>[1-4])\s+"
    r"(?P<Result>won|lost|draw)\s+v\s+"
    r"(?P<Opposition>[A-Za-z ]+)\s+"
    r"(?P<StartDate>\d{1,2}\s+[A-Za-z]{3}\s+\d{4})$"
)

rows = []

for line in lines:
    match = pattern.match(line)
    if match:
        rows.append(match.groupdict())
    else:
        print("❌ Could not parse line:", line)

df = pd.DataFrame(rows)

df.to_csv("data/lords-clean.csv", index=False)

print("✅ CSV created successfully!")
print("Total rows:", len(df))
print(df.head())
