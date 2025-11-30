import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
import joblib
import numpy as np
import os

def load_data():
    df = pd.read_csv("data/first_innings_scores.csv")

    # Convert Score to numeric (just in case)
    df["Score"] = pd.to_numeric(df["Score"], errors="coerce")

    # Drop any rows with missing values
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
    os.makedirs("model", exist_ok=True)
    joblib.dump(model, "model/lords_model.pkl")
    joblib.dump(label_encoder, "model/label_encoder.pkl")
    print("\nModel saved to model/lords_model.pkl")
    print("Label encoder saved to model/label_encoder.pkl")

def main():
    print("Loading data...")
    df = load_data()

    print("Encoding labels...")
    df, label_encoder = encode_labels(df)

    # Features and labels
    X = df[["Score"]].values          # Score → model input
    y = df["ResultEncoded"].values    # Encoded labels

    print("Training model...")
    model = train_model(X, y)

    print("Evaluating model...")
    preds = model.predict(X)
    acc = accuracy_score(y, preds)
    print(f"\nTraining Accuracy: {acc:.3f}\n")

    print("Classification Report:")
    print(classification_report(y, preds, target_names=label_encoder.classes_))

    # Example prediction
    example_score = 300
    example_prob = model.predict_proba([[example_score]])[0]
    print(f"\nExample: Score = {example_score}")
    for label, p in zip(label_encoder.classes_, example_prob):
        print(f"  {label}: {p:.3f}")

    # Save model + label encoder
    save_artifacts(model, label_encoder)

if __name__ == "__main__":
    main()
