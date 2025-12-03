import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import joblib

# ===========================
# Load CSV
# ===========================
third = pd.read_csv("data/third_innings_scores.csv")

# Ensure correct dtypes
third["Score"] = third["Score"].astype(int)
third["Target"] = third["Target"].astype(int)
third["Result"] = third["Result"].astype(str)

# ===========================
# Build dataset
# ===========================
df = pd.DataFrame({
    "score_3": third["Score"],
    "target": third["Target"],
    "diff": third["Score"] - third["Target"],
    "result": third["Result"]
})

# ===========================
# Encode result labels
# ===========================
le = LabelEncoder()
df["y"] = le.fit_transform(df["result"])

X = df[["score_3", "target", "diff"]]
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
joblib.dump(model, "backend/app/model/third_innings_model.pkl")
joblib.dump(le, "backend/app/model/third_innings_label_encoder.pkl")

print("Saved third innings model and label encoder.")
