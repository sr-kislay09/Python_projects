import pandas as pd
import matplotlib.pyplot as plt
import io
import numpy as np
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
import joblib
from pydantic import BaseModel
import logging
from sklearn.preprocessing import LabelEncoder

app = FastAPI()
logging.basicConfig(level=logging.INFO)

# Load the trained model
model = joblib.load('trained_model.pkl')

# Define a Pydantic model for the prediction response
class PredictionResponse(BaseModel):
    predictions: list

@app.get("/", response_class=HTMLResponse)
async def read_root():
    html_code = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Traffic Accident Prediction</title>
    </head>
    <body>
        <h1>Traffic Accident Prediction</h1>
        <form action="/predict/" method="post" enctype="multipart/form-data">
            <input type="file" name="file" accept=".csv">
            <button type="submit">Upload and Predict</button>
        </form>
        <form action="/feature-importance/" method="get">
            <button type="submit">Get Feature Importance</button>
        </form>
    </body>
    </html>
    """
    return HTMLResponse(content=html_code)

@app.post("/predict/")
async def predict(file: UploadFile):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file type. Only CSV files are accepted.")
    
    try:
        # Read the CSV file
        df = pd.read_csv(file.file)

        # Define your features used for prediction
        features = ['Sex_of_Casualty', 'Age_of_Casualty', 'Casualty_Severity']

        # Check if the required features are in the uploaded file
        missing_features = [f for f in features if f not in df.columns]
        if missing_features:
            return {"error": f"Missing columns in uploaded file: {', '.join(missing_features)}"}

        # Drop non-numeric columns and handle categorical data
        df = df[features]
        df = df.dropna()  # Optionally drop rows with missing values
        
        # Encode categorical variables
        label_encoders = {}
        for column in df.select_dtypes(include=['object']).columns:
            le = LabelEncoder()
            df[column] = le.fit_transform(df[column])
            label_encoders[column] = le

        # Ensure that all features are numeric
        X = df[features]

        # Predict using the loaded model
        predictions = model.predict(X)

        # Create histogram of predictions
        buf = io.BytesIO()
        plt.figure(figsize=(10, 6))
        plt.hist(predictions, bins=np.arange(min(predictions)-0.5, max(predictions)+1.5, 1), edgecolor='black')
        plt.xlabel('Predicted Values')
        plt.ylabel('Frequency')
        plt.title('Histogram of Predictions')
        plt.grid(True)
        plt.savefig(buf, format='png')
        buf.seek(0)

        # Log prediction success
        logging.info("Prediction and histogram generation successful.")
        
        # Return the histogram as an image
        return StreamingResponse(buf, media_type="image/png")

    except Exception as e:
        logging.error(f"Prediction failed: {str(e)}")
        return {"error": str(e)}

@app.get("/feature-importance/")
async def feature_importance():
    try:
        # Get feature importances from the model
        importances = model.feature_importances_  # For tree-based models
        feature_names = ['Sex_of_Casualty', 'Age_of_Casualty', 'Casualty_Severity']
        
        # Plot feature importances
        buf = io.BytesIO()
        plt.figure(figsize=(15, 10))
        indices = np.argsort(importances)[::-1]
        plt.bar(range(len(importances)), importances[indices], align='center')
        plt.xticks(range(len(importances)), np.array(feature_names)[indices], rotation=45)
        plt.xlim([-1, len(importances)])
        plt.xlabel('Feature')
        plt.ylabel('Importance')
        plt.title('Feature Importances')
        plt.grid(True)
        plt.savefig(buf, format='png')
        buf.seek(0)

        # Log feature importance retrieval success
        logging.info("Feature importance retrieval successful.")
        
        # Return the bar graph as an image
        return StreamingResponse(buf, media_type="image/png")

    except Exception as e:
        logging.error(f"Feature importance retrieval failed: {str(e)}")
        return {"error": str(e)}

# To run the FastAPI server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
