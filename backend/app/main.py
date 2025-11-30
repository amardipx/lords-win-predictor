from fastapi import FastAPI
from pydantic import BaseModel, Field
from .predict import predict_probabilities

app = FastAPI(
    title="Lords Win Probability API",
    description="Predict win/draw/loss probabilities based on 1st innings score at Lord's.",
    version="1.0.0"
)

# ----------------------------
# Request body schema
# ----------------------------

class ScoreRequest(BaseModel):
    score: int = Field(..., example=320, ge=0, description="First innings score")

# ----------------------------
# Response schema
# ----------------------------

class ProbabilityResponse(BaseModel):
    win_probability: float
    draw_probability: float
    loss_probability: float


# ----------------------------
# Root endpoint
# ----------------------------
@app.get("/")
def root():
    return {"message": "Lords Win Probability API is running."}


# ----------------------------
# Prediction endpoint
# ----------------------------
@app.post("/predict", response_model=ProbabilityResponse)
def predict(req: ScoreRequest):

    probabilities = predict_probabilities(req.score)

    return {
        "win_probability":  probabilities["win probability"],
        "draw_probability": probabilities["draw probability"],
        "loss_probability": probabilities["loss probability"]
    }
