import joblib
import numpy as np

# ============================
# Load model + encoder
# ============================
model = joblib.load("backend/app/model/third_innings_model.pkl")
le = joblib.load("backend/app/model/third_innings_label_encoder.pkl")

# ============================
# Manual input
# ============================
score_1 = int(input("Enter FIRST innings score (Team A): "))
score_2 = int(input("Enter SECOND innings score (Team B): "))
score_3 = int(input("Enter THIRD innings score  (Team A): "))

print("\n==========================================")
print("            🏏 MATCH SITUATION")
print("==========================================")

# ============================
# Compute leads + target
# ============================

lead_after_two = score_1 - score_2

# Who leads?
if lead_after_two > 0:
    print(f"After two innings: **Team A leads by {lead_after_two} runs.**")
elif lead_after_two < 0:
    print(f"After two innings: **Team B leads by {abs(lead_after_two)} runs.**")
else:
    print("After two innings: **Scores are level!**")

# Check for innings defeat
if score_3 < lead_after_two:
    print("\n==========================================")
    print("             ❌ INNINGS DEFEAT")
    print("==========================================")
    print(f"Team A scored {score_3}, which is fewer than the {lead_after_two} required to make Team B bat again.")
    print("➡️ Team A loses **by an innings**.")
    exit()

# Compute target normally
target = (score_1 - score_2) + score_3 + 1

print("\n==========================================")
print("           🏁 FOURTH INNINGS TARGET")
print("==========================================")
print(f"Target for Team B to win: **{target} runs**")

# Difference metric for ML model
diff = score_3 - target

# ============================
# Prepare input
# ============================
X = np.array([[score_3, target, diff]])

# Predict probabilities
probs = model.predict_proba(X)[0] * 100

labels = le.inverse_transform([0, 1, 2])
result = dict(zip(labels, probs))

# ============================
# Display results
# ============================

print("\n==========================================")
print(" 🔮 WIN PROBABILITY PREDICTIONS")
print("==========================================")

print("\nFor Team A (the team that batted in the 3rd innings):")
print(f"  🏆 Win Probability : {result['won']:.2f}%")
print(f"  ⚖️ Draw Probability: {result['draw']:.2f}%")
print(f"  ❌ Loss Probability: {result['lost']:.2f}%")

print("\nFor Team B (the chasing team):")
print(f"  🏆 Win Probability : {result['lost']:.2f}%")
print(f"  ⚖️ Draw Probability: {result['draw']:.2f}%")
print(f"  ❌ Loss Probability: {result['won']:.2f}%")

print("\n==========================================")
print("                END OF ANALYSIS")
print("==========================================")
