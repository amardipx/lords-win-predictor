import joblib
import numpy as np

# Load model + label encoder
model = joblib.load("model/lords_model.pkl")
label_encoder = joblib.load("model/label_encoder.pkl")

def predict_probabilities(score: int):
    """
    Return probabilities in fixed order:
    win → draw → loss
    (values as percentages 1–100)
    """
    score_array = np.array([[score]])
    probs = model.predict_proba(score_array)[0]
    classes = label_encoder.classes_

    percentages = probs * 100

    # Raw mapping from class → probability
    cls_to_pct = {cls: pct for cls, pct in zip(classes, percentages)}

    # Fixed display order
    return {
        "win probability":  float(cls_to_pct["won"]),
        "draw probability": float(cls_to_pct["draw"]),
        "loss probability": float(cls_to_pct["lost"]),
    }

if __name__ == "__main__":
    example_score = 320
    result = predict_probabilities(example_score)

    print(f"Score: {example_score}")
    for outcome, p in result.items():
        print(f"{outcome}: {p:.2f}%")
