# Basic Litserve Example

from litserve import LitServer

# Create a LitServer instance
app = LitServer()

# Define a machine learning model endpoint
from sklearn.linear_model import LinearRegression
import numpy as np

# Initialize a simple machine learning model
model = LinearRegression()
# Train the model with dummy data
X_train = np.array([[1], [2], [3], [4], [5]])
y_train = np.array([2, 4, 6, 8, 10])
model.fit(X_train, y_train)

@app.route("/predict", methods=["POST"])
def predict(data):
    # Predict using the trained model
    input_value = data.get("input")
    if input_value is None:
        return {"error": "Input value is required"}
    prediction = model.predict(np.array([[input_value]]))
    return {"input": input_value, "prediction": prediction[0]}

# Run the server
if __name__ == "__main__":
    app.run(port=5000)
