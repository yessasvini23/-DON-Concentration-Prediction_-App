# -*- coding: utf-8 -*-
"""Mycotoxin_prediction.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1NRRiJQ8wPvhIKDwZ1iuVTPaileFQVrDW

Steps in Our Approach
Load and Inspect Data

Check for missing values, outliers, and inconsistencies.
Generate summary statistics and visualizations.
Data Preprocessing

Handle missing data (imputation or removal).
Normalize spectral features.
Detect anomalies if needed.
Data Visualization

Plot spectral reflectance trends.
Create heatmaps or pairplots.
Model Training

Split data into train/test sets.
Train a neural network as a baseline model.
Optimize hyperparameters using a search technique.
Model Evaluation

Compute performance metrics (MAE, RMSE, R²).
Plot actual vs predicted values.
Analyze residuals.
Interpretability & Deployment

Use SHAP/LIME for feature importance.
Package into a deployable API using Flask/FastAPI.
"""

import pandas as pd

# Load the dataset
file_path = "MLE-Assignment.csv"  # Ensure the file is in your working directory
df = pd.read_csv(file_path)

# Display basic info and first few rows
print(df.info())
print(df.head())

"""Step 1: Load and Inspect the Data
Create a Python script (ml_pipeline.py) and copy the following code into it:
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Load dataset
file_path = "MLE-Assignment.csv"  # Ensure the file is in the working directory
df = pd.read_csv(file_path)

# Display dataset information
print("Dataset Information:")
print(df.info())

# Show first few rows
print("\nFirst Few Rows:")
print(df.head())

# Check for missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Summary statistics
print("\nSummary Statistics:")
print(df.describe())

# Plot histogram for the target variable (DON concentration)
plt.figure(figsize=(8, 5))
sns.histplot(df.iloc[:, -1], bins=30, kde=True)  # Assuming last column is the target
plt.xlabel("DON Concentration")
plt.ylabel("Frequency")
plt.title("Distribution of DON Concentration")
plt.show()

"""Step 2: Preprocessing
After confirming the dataset structure, add this preprocessing step:



"""

# Handle missing values by filling with the median of numeric columns only
for column in df.select_dtypes(include=np.number).columns:
    df[column].fillna(df[column].median(), inplace=True)

# Extract features (spectral data) and target variable (DON concentration)
# Exclude the 'hsi_id' column from features
X = df.iloc[:, 1:-1].values  # Assuming first column is 'hsi_id' and last is target
y = df.iloc[:, -1].values

# Normalize the spectral data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

print(f"Training samples: {X_train.shape[0]}, Testing samples: {X_test.shape[0]}")

"""Step 3: Train a Neural Network Model

"""

# Train a simple neural network
model = MLPRegressor(hidden_layer_sizes=(64, 32), activation='relu', solver='adam', max_iter=500, random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate performance
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("\nModel Performance:")
print(f"Mean Absolute Error (MAE): {mae:.4f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")
print(f"R² Score: {r2:.4f}")

# Scatter plot of actual vs predicted
plt.figure(figsize=(8, 6))
sns.scatterplot(x=y_test, y=y_pred, alpha=0.7)
plt.xlabel("Actual DON Concentration")
plt.ylabel("Predicted DON Concentration")
plt.title("Actual vs Predicted DON Concentration")
plt.show()

"""Step 4: Save the Model for Deployment
To save the model for later use:
"""

import joblib

# Save the trained model and scaler
joblib.dump(model, "don_prediction_model.pkl")
joblib.dump(scaler, "scaler.pkl")

print("Model and scaler saved successfully!")

"""Step 5: Deploy Using FastAPI
Create a new file app.py for serving predictions:

"""

#!pip install python-multipart
from fastapi import FastAPI
import joblib
import numpy as np

app = FastAPI()

# Load the saved model and scaler
model = joblib.load("don_prediction_model.pkl")
scaler = joblib.load("scaler.pkl")

@app.get("/")
def home():
    return {"message": "DON Prediction API is running"}

@app.post("/predict/")
def predict(features: list):
    features = np.array(features).reshape(1, -1)
    features_scaled = scaler.transform(features)
    prediction = model.predict(features_scaled)
    return {"predicted_don_concentration": float(prediction[0])}

import pandas as pd

df = pd.read_csv("MLE-Assignment.csv")
print(df.shape)  # This tells you the number of columns (features)

import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler
import pandas as pd
import os

# Get the current working directory
current_directory = os.getcwd()

# Specify the file path relative to the current working directory
# If your file is in a different location, update 'MLE-Assignment.csv' with the correct path
file_path = os.path.join(current_directory, "MLE-Assignment.csv")

# Check if the file exists
if not os.path.exists(file_path):
    raise FileNotFoundError(f"The file '{file_path}' does not exist. Please check the file path and ensure the file is present.")

# Load dataset (replace 'MLE-Assignment.csv' with your actual dataset)
df = pd.read_csv(file_path)

# Assuming the features are in columns 1 to N and the target is in the last column
# Exclude the 'hsi_id' column which is likely the first column
X = df.iloc[:, 1:-1].values  # Feature columns, excluding the first and last columns
y = df.iloc[:, -1].values   # Target column

# Fit StandardScaler on training data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Save the fitted scaler
with open("scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

print("Scaler fitted and saved successfully!")

# Load the trained model and fitted scaler
scaler = pickle.load(open("scaler.pkl", "rb"))

# Before using the scaler, check if it has been fitted
if not hasattr(scaler, "mean_"):
    raise ValueError("The StandardScaler is not fitted. Train and save it properly.")

# Example of scaling input data
def preprocess_input(features):
    features_array = np.array(features).reshape(1, -1)
    scaled_features = scaler.transform(features_array)  # This will now work correctly
    return scaled_features

from sklearn.preprocessing import StandardScaler
import numpy as np

# Sample training and test data (replace with your actual data)
X_train = np.array([[1, 2], [3, 4], [5, 6]])
X_test = np.array([[7, 8], [9, 10]])

# Create a StandardScaler instance
scaler = StandardScaler()

# Fit the scaler to the training data
scaler.fit(X_train)

# Transform the training and test data
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Print the scaled data
print("Scaled Training Data:\n", X_train_scaled)
print("Scaled Test Data:\n", X_test_scaled)

# or use fit_transform on the training data.
scaler2 = StandardScaler()
X_train_scaled2 = scaler2.fit_transform(X_train)
print("Scaled Training Data using fit_transform:\n", X_train_scaled2)