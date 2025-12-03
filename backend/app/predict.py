import joblib
import numpy as np
import os

# ------------------------------
# Model directory
# ------------------------------
MODEL_DIR = os.path.join(os.path.dirname(__file__), "model")

# ------------------------------
# FIRST INNINGS MODEL
# ------------------------------
first_model = joblib.load(os.path.join(MODEL_DIR, "lords_model.pkl"))
first_encoder = joblib.load(os.path.join(MODEL_DIR, "label_encoder.pkl"))

# ------------------------------
# SECOND INNINGS MODEL
# ------------------------------
second_model = joblib.load(os.path.join(MODEL_DIR, "second_innings_model.pkl"))
second_encoder = joblib.load(os.path.join(MODEL_DIR, "second_innings_label_encoder.pkl"))

# ------------------------------
# THIRD INNINGS MODEL
# ------------------------------
third_model = joblib.load(os.path.join(MODEL_DIR, "third_innings_model.pkl"))
third_encoder = joblib.load(os.path.join(MODEL_DIR, "third_innings_label_encoder.pkl"))


# ============================================================
# FIRST INNINGS PREDICTION
# ============================================================
def predict_probabilities(score: int):
    X = np.array([[score]])
    probs = first_model.predict_proba(X)[0] * 100
    labels = first_encoder.classes_

    cls_to_pct = {cls: pct for cls, pct in zip(labels, probs)}

    team_a = {
        "win":  float(cls_to_pct["won"]),
        "draw": float(cls_to_pct["draw"]),
        "loss": float(cls_to_pct["lost"])
    }

    team_b = {
        "win":  float(cls_to_pct["lost"]),
        "draw": float(cls_to_pct["draw"]),
        "loss": float(cls_to_pct["won"])
    }

    return {
        "team_a": team_a,
        "team_b": team_b
    }


# ============================================================
# SECOND INNINGS PREDICTION
# ============================================================
def predict_second_innings(score_1: int, score_2: int):
    diff = score_1 - score_2
    X = np.array([[score_1, score_2, diff]])

    probs = second_model.predict_proba(X)[0] * 100
    labels = second_encoder.inverse_transform([0, 1, 2])
    result = dict(zip(labels, probs))

    team_a = {
        "win":  float(result["won"]),
        "draw": float(result["draw"]),
        "loss": float(result["lost"])
    }

    team_b = {
        "win":  float(result["lost"]),
        "draw": float(result["draw"]),
        "loss": float(result["won"])
    }

    return {
        "team_a": team_a,
        "team_b": team_b
    }


# ============================================================
# THIRD INNINGS PREDICTION
# ============================================================
def predict_third_innings(score_1: int, score_2: int, score_3: int):

    # Lead after two innings
    lead_after_two = score_1 - score_2

    # Check innings defeat
    if score_3 < lead_after_two:
        return {
            "innings_defeat": True,
            "message": "Team A loses by an innings.",
            "team_a": {"win": 0.0, "draw": 0.0, "loss": 100.0},
            "team_b": {"win": 100.0, "draw": 0.0, "loss": 0.0},
            "target": None
        }

    # Compute target
    target = (score_1 - score_2) + score_3 + 1
    diff = score_3 - target

    X = np.array([[score_3, target, diff]])

    probs = third_model.predict_proba(X)[0] * 100
    labels = third_encoder.inverse_transform([0, 1, 2])
    result = dict(zip(labels, probs))

    team_a = {
        "win":  float(result["won"]),
        "draw": float(result["draw"]),
        "loss": float(result["lost"])
    }

    team_b = {
        "win":  float(result["lost"]),
        "draw": float(result["draw"]),
        "loss": float(result["won"])
    }

    return {
        "innings_defeat": False,
        "target": int(target),
        "team_a": team_a,
        "team_b": team_b
    }
