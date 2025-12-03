import re
import pandas as pd

INPUT = "data/lords-raw.txt"
OUTPUT = "data/lords-clean.csv"

def clean_score(raw_score: str) -> str:
    """
    Extract the numeric runs from a score string.
    Examples:
        191/8  -> 191
        529/5d -> 529
        14/2   -> 14
    """
    match = re.match(r"(\d+)", raw_score)
    return match.group(1) if match else raw_score.strip()

pattern = re.compile(
    r"""^
    (?P<Team>[A-Za-z ]+?)\s+
    (?P<Score>[0-9/]+d?)\s+
    (?P<Overs>[0-9.]+)\s+
    (?P<Target>[0-9]*)\s*
    (?P<RPO>[0-9.]+)\s+
    (?P<Inns>[1-4])\s+
    (?P<Result>won|lost|draw)\s+
    (?:v\s+)?(?P<Opposition>[A-Za-z ]+?)\s+
    (?P<StartDate>\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4})
    $""",
    re.VERBOSE,
)

rows = []
failed = []

with open(INPUT, "r", encoding="utf-8") as fh:
    lines = [ln.strip() for ln in fh if ln.strip()]

# skip header
if lines and ("Team" in lines[0] and "Score" in lines[0]):
    lines = lines[1:]

for line in lines:
    m = pattern.match(line)
    if not m:
        failed.append(line)
        continue

    d = m.groupdict()

    raw_score = d["Score"].strip()
    score = clean_score(raw_score)

    target = d["Target"].strip()
    if d["Inns"] != "4" or target == "":
        target = ""

    rows.append({
        "Team": d["Team"].strip(),
        "Score": score,
        "Target": target,
        "Inns": d["Inns"].strip(),
        "Result": d["Result"].strip(),
        "Opposition": d["Opposition"].strip(),
        "Start Date": d["StartDate"].strip(),
    })

df = pd.DataFrame(rows, columns=["Team", "Score", "Target", "Inns", "Result", "Opposition", "Start Date"])
df.to_csv(OUTPUT, index=False)

print(f"✅ Written {len(df)} rows to {OUTPUT}")
if failed:
    print(f"⚠️ {len(failed)} lines could not be parsed:")
    for ln in failed:
        print("  -", ln)
