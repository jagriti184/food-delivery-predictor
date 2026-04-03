import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

# ✅ Dataset (distance, prep_time, traffic → time)
data = {
    "distance": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "prep_time": [5, 10, 15, 20, 10, 15, 25, 30, 20, 15],
    "traffic": [1, 2, 3, 1, 2, 3, 1, 2, 3, 2],
    "time": [10, 18, 30, 22, 28, 40, 26, 48, 55, 35]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# ✅ Features (INPUT)
X = df[["distance", "prep_time", "traffic"]]

# ✅ Target (OUTPUT)
y = df["time"]

# Train model
model = LinearRegression()
model.fit(X, y)

# Save model
pickle.dump(model, open("model.pkl", "wb"))

print("✅ Model trained and saved successfully!")