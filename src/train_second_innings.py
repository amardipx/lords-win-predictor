import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import joblib

# ===========================
# Load both CSVs
# ===========================
first = pd.read_csv("data/first_innings_scores.csv")
second = pd.read_csv("data/second_innings_scores.csv")

assert len(first) == len(second), "Row mismatch between first and second innings!"

# ===========================
# Build dataset
# ===========================
df = pd.DataFrame({
    "score_1": first["Score"].astype(int),
    "score_2": second["Score"].astype(int),
    "result": first["Result"].astype(str)   # result from perspective of first-batting team
})

df["diff"] = df["score_1"] - df["score_2"]

# ===========================
# Encode result labels
# ===========================
le = LabelEncoder()
df["y"] = le.fit_transform(df["result"])

X = df[["score_1", "score_2", "diff"]]
y = df["y"]

# ===========================
# Train/test split
# ===========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# ===========================
# Model pipeline
# ===========================
model = Pipeline([
    ("scaler", StandardScaler()),
    ("clf", LogisticRegression(
        multi_class="multinomial",
        max_iter=5000
    ))
])

model.fit(X_train, y_train)

# ===========================
# Sanity check accuracy
# ===========================
acc = model.score(X_test, y_test)
print("Validation accuracy:", acc)

# ===========================
# Save artifacts
# ===========================
joblib.dump(model, "backend/app/model/second_innings_model.pkl")
joblib.dump(le, "backend/app/model/second_innings_label_encoder.pkl")

print("Saved second innings model and label encoder.")
