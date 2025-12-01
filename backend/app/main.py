from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from .predict import predict_probabilities, predict_second_innings


app = FastAPI(
    title="Lords Win Probability API",
    description="Predict win/draw/loss probabilities for Test matches at Lord's.",
    version="1.1.0"
)

# ----------------------------
# CORS
# ----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# Schemas
# ----------------------------
class ScoreRequest(BaseModel):
    score: int = Field(..., ge=0, description="First innings score")


class SecondInningsRequest(BaseModel):
    score_1: int = Field(..., ge=0, description="First innings score")
    score_2: int = Field(..., ge=0, description="Second innings score")


# ----------------------------
# Root endpoint
# ----------------------------
@app.get("/")
def root():
    return {"message": "Lords Win Probability API is running."}


# ----------------------------
# FIRST INNINGS ENDPOINT
# ----------------------------
@app.post("/predict")
def predict(req: ScoreRequest):
    return predict_probabilities(req.score)


# ----------------------------
# SECOND INNINGS ENDPOINT
# ----------------------------
@app.post("/predict/second")
def predict_second(req: SecondInningsRequest):
    return predict_second_innings(req.score_1, req.score_2)
