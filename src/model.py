import os
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from src.config import (
    DATA_PROCESSED_DIR,
    MODELS_DIR,
    ROUTE_DATA_FILE,
    MODEL_FILE
)


# load the processed route data
def load_dataset():
    path = os.path.join(DATA_PROCESSED_DIR, ROUTE_DATA_FILE)
    if not os.path.exists(path):
        print("Dataset not found.")
        return None
    return pd.read_csv(path)


# train random forest to predict gnss accuracy from coordinates and speed
def train_model():
    df = load_dataset()
    if df is None:
        return None

    # input features and target
    X = df[["Latitude", "Longitude", "Altitude", "Speed(m/s)"]]
    y = df["Accuracy(m)"]

    # 80/20 train test split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    # initialize and fit random forest
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # evaluate model performance
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)
    rmse = mse ** 0.5
    r2 = r2_score(y_test, predictions)

    print("\n==============================")
    print("MODEL PERFORMANCE")
    print("==============================")
    print(f"MAE  : {mae:.4f}")
    print(f"RMSE : {rmse:.4f}")
    print(f"R²   : {r2:.4f}")

    # save trained model to output/models
    model_path = os.path.join(MODELS_DIR, MODEL_FILE)
    joblib.dump(model, model_path)
    print("\nModel Saved Successfully")
    print(model_path)

    return model


# helper to predict accuracy for individual points
def predict_accuracy(model, latitude, longitude, altitude, speed):
    prediction = model.predict([[latitude, longitude, altitude, speed]])
    return prediction[0]


# load saved model from disk
def load_model():
    model_path = os.path.join(MODELS_DIR, MODEL_FILE)
    if not os.path.exists(model_path):
        return None
    return joblib.load(model_path)


if __name__ == "__main__":
    train_model()