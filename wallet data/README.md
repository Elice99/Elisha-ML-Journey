🪙 Crypto Wallet Trader Classifier API

Overview

This project implements a machine learning pipeline to classify crypto wallets as either "Good Traders" (🟢) or "Bad Traders" (🔴) based on their transaction history and activity metrics. The trained Logistic Regression model is containerized using Docker and deployed as a high-performance FastAPI service for real-time predictions.

🚀 Key Features

Machine Learning Pipeline: A Python script (train.py) handles data loading, feature engineering (calculating metrics like vol_per_tx and activity_per_week), cross-validation, and final model training.

Model Persistence: The DictVectorizer and the final LogisticRegression model are saved using pickle to the wallet_classifer=1.0.bin file.

FastAPI Service: The main.py application loads the pre-trained model and exposes a robust /predict endpoint.

Containerization: A Dockerfile and Pipfile ensure a consistent, isolated, and easily deployable environment using Docker.

📂 Project Structure

File

Description

train.py

Main script for model training, validation (K-Fold), and saving the final model artifact.

dune_data.csv

Mock dataset containing wallet activity metrics and the target trader classification.

wallet_classifer=1.0.bin

The pickled output file containing the trained DictVectorizer and LogisticRegression model.

main.py

The FastAPI application that loads the saved model and serves the prediction endpoint.

Pipfile

Defines all project dependencies (FastAPI, scikit-learn, pandas, uvicorn, numpy).

Dockerfile

Instructions for building the Docker image for deployment.

🛠️ Prerequisites

To run this project, you need the following installed:

Python 3.10+ (or the version specified in Pipfile).

pipenv (for dependency management: pip install pipenv).

Docker (for containerizing and running the API service).

🏃 Getting Started

Step 1: Train the Model

First, you need to run the training script to generate the model artifact (wallet_classifer=1.0.bin).

pipenv install --dev
pipenv run python train.py


This script will output the saved model file, which is required for the FastAPI service.

Step 2: Build the Docker Image

Use the provided Dockerfile to build the prediction service image.

# wallet-predictor is the name of your image
docker build -t wallet-predictor .


Step 3: Run the API Service

Run the container, mapping the internal port 9696 to a port on your host machine (e.g., 8080).

docker run -it --rm -p 8080:9696 wallet-predictor


The prediction service will now be running at http://localhost:8080.

🎯 API Usage

The prediction endpoint is a POST request that expects a JSON body containing the four engineered features used by the model.

Endpoint

POST /predict

Request Body (WalletInfo Schema)

The model requires the following features, which represent calculated metrics from raw wallet data:

Field

Type

Description

tx_count_365d

float

Total number of transactions in the last 365 days.

vol_per_tx

float

Average volume per transaction (Total Volume / Tx Count).

activity_per_week

float

Average transactions per active week.

avg_weekly_vol

float

Average volume transacted per active week.

Example Request

If your service is running on port 8080:

{
  "tx_count_365d": 300.0,
  "vol_per_tx": 3333.33,
  "activity_per_week": 20.0,
  "avg_weekly_vol": 66666.67
}


Example Response

{
  "good_trader_probability": 0.8973,
  "good_trader": true,
  "classification_threshold": 0.7
}


The service returns the raw probability of the wallet being a "Good Trader" and a boolean classification based on the internal threshold of 0.7.