import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
import joblib
import numpy as np
import os

# Path to backend model directory
MODEL_DIR = os.path.join("backend", "app", "model")


def load_data():
    df = pd.read_csv("data/first_innings_scores.csv")

    df["Score"] = pd.to_numeric(df["Score"], errors="coerce")
    df = df.dropna()

    return df


def encode_labels(df):
    """
    Convert textual results into numerical classes:
    lost -> 0
    draw -> 1
    won  -> 2
    """
    le = LabelEncoder()
    df["ResultEncoded"] = le.fit_transform(df["Result"])
    return df, le


def train_model(X, y):
    model = LogisticRegression(
        multi_class="multinomial",
        solver="lbfgs",
        max_iter=500
    )
    model.fit(X, y)
    return model


def save_artifacts(model, label_encoder):
    # Ensure backend/app/model directory exists
    os.makedirs(MODEL_DIR, exist_ok=True)

    model_path = os.path.join(MODEL_DIR, "lords_model.pkl")
    encoder_path = os.path.join(MODEL_DIR, "label_encoder.pkl")

    joblib.dump(model, model_path)
    joblib.dump(label_encoder, encoder_path)

    print(f"\nModel saved to {model_path}")
    print(f"Label encoder saved to {encoder_path}")


def main():
    print("Loading data...")
    df = load_data()

    print("Encoding labels...")
    df, label_encoder = encode_labels(df)

    X = df[["Score"]].values
    y = df["ResultEncoded"].values

    print("Training model...")
    model = train_model(X, y)

    print("Evaluating model...")
    preds = model.predict(X)
    acc = accuracy_score(y, preds)
    print(f"\nTraining Accuracy: {acc:.3f}\n")

    print("Classification Report:")
    print(classification_report(y, preds, target_names=label_encoder.classes_))

    example_score = 300
    example_prob = model.predict_proba([[example_score]])[0]
    print(f"\nExample: Score = {example_score}")
    for label, p in zip(label_encoder.classes_, example_prob):
        print(f"  {label}: {p:.3f}")

    save_artifacts(model, label_encoder)


if __name__ == "__main__":
    main()
