import datetime

import joblib
import numpy as np
import pandas as pd
from flask import Flask, jsonify, render_template, request, url_for
from flask_cors import cross_origin

app = Flask(__name__, template_folder="template")

def load_model():
    """Loads the model from the specified model path."""

    MODEL_PATH = "./models/model.pkl"
    model = joblib.load(open(MODEL_PATH, "rb"))
    print("Model Loaded")
    return model


def preprocessor(input_lst: list) -> np.ndarray:
    """Prepares the input user data for the model"""

    SCALAR_PATH = "prep.pkl"

    # convert into 2D numpy array for scaling
    input_lst = np.array(input_lst).reshape(1, -1)

    scalar = joblib.load(open(SCALAR_PATH, "rb"))
    print("Scaler Loaded")

    return scalar.transform(input_lst)


@app.route("/", methods=["GET"])
@cross_origin()
def home():
    return render_template("index2.html")


@app.route("/predict", methods=["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":
        # DATE
        date = request.form["date"]
        day = float(pd.to_datetime(date, format="%Y-%m-%d").day)
        month = float(pd.to_datetime(date, format="%Y-%m-%d").month)
        # MinTemp
        minTemp = float(request.form["mintemp"])
        # MaxTemp
        maxTemp = float(request.form["maxtemp"])
        # Rainfall
        rainfall = float(request.form["rainfall"])
        # Evaporation
        evaporation = float(request.form["evaporation"])
        # Sunshine
        sunshine = float(request.form["sunshine"])
        # Wind Gust Speed
        windGustSpeed = float(request.form["windgustspeed"])
        # Wind Speed 9am
        windSpeed9am = float(request.form["windspeed9am"])
        # Wind Speed 3pm
        windSpeed3pm = float(request.form["windspeed3pm"])
        # Humidity 9am
        humidity9am = float(request.form["humidity9am"])
        # Humidity 3pm
        humidity3pm = float(request.form["humidity3pm"])
        # Pressure 9am
        pressure9am = float(request.form["pressure9am"])
        # Pressure 3pm
        pressure3pm = float(request.form["pressure3pm"])
        # Temperature 9am
        temp9am = float(request.form["temp9am"])
        # Temperature 3pm
        temp3pm = float(request.form["temp3pm"])
        # Cloud 9am
        cloud9am = float(request.form["cloud9am"])
        # Cloud 3pm
        cloud3pm = float(request.form["cloud3pm"])
        # Cloud 3pm
        location = int(request.form["location"])
        # Wind Dir 9am
        winddDir9am = int(request.form["winddir9am"])
        # Wind Dir 3pm
        winddDir3pm = int(request.form["winddir3pm"])
        # Wind Gust Dir
        windGustDir = int(request.form["windgustdir"])
        # Rain Today
        rainToday = int(request.form["raintoday"])

        input_lst = [
            location,
            minTemp,
            maxTemp,
            rainfall,
            evaporation,
            sunshine,
            windGustDir,
            windGustSpeed,
            winddDir9am,
            winddDir3pm,
            windSpeed9am,
            windSpeed3pm,
            humidity9am,
            humidity3pm,
            pressure9am,
            pressure3pm,
            cloud9am,
            cloud3pm,
            temp9am,
            temp3pm,
            rainToday,
            month,
            day,
        ]
        print(input_lst)

        input_lst = preprocessor(input_lst)

        model = load_model()
        pred = model.predict(input_lst)
        if pred[0][0] > 0.5:
            return render_template("rain.html")
        else:
            return render_template("sunny.html")

    return render_template("predictor.html")