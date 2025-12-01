import joblib
import numpy as np

# ============================
# Load model + encoder
# ============================
model = joblib.load("backend/app/model/second_innings_model.pkl")
le = joblib.load("backend/app/model/second_innings_label_encoder.pkl")

# ============================
# Manual input
# ============================
score_1 = int(input("Enter first innings score: "))
score_2 = int(input("Enter second innings score: "))

diff = score_1 - score_2

print(f"\nUsing:")
print(f"  First innings score:  {score_1}")
print(f"  Second innings score: {score_2}")
print(f"  Difference:           {diff}")

# ============================
# Prepare input
# ============================
X = np.array([[score_1, score_2, diff]])

# Predict probabilities
probs = model.predict_proba(X)[0] * 100

# Map to labels
labels = le.inverse_transform([0, 1, 2])
result = dict(zip(labels, probs))

# ============================
# Display results
# ============================
print("\nProbabilities for the team batting first:")
print(f"  Win:  {result['won']:.4f}")
print(f"  Draw: {result['draw']:.4f}")
print(f"  Loss: {result['lost']:.4f}")

print("\nProbabilities for the opponent:")
print(f"  Win:  {result['lost']:.4f}")
print(f"  Draw: {result['draw']:.4f}")
print(f"  Loss: {result['won']:.4f}")
