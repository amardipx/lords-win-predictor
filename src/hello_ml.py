import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

print("NumPy version:", np.__version__)
print("Pandas version:", pd.__version__)

X = np.array([[1], [2], [3], [4]])
y = np.array([0, 0, 1, 1])

model = LogisticRegression()
model.fit(X, y)

pred = model.predict([[2.5]])
print("Prediction for 2.5 is:", pred[0])
