from flask import Flask, jsonify, request
from flask_cors import CORS
from pyparsing import line
from yfinance import Ticker
import pandas as pd
import numpy as np
from models.linear import linear_regression
from models.arima import arima
from models.prophet import prophet

# Configuration.
DEBUG = True

# Instantiate the app.
app = Flask(__name__)
app.config.from_object(__name__)

# Enable CORS.
CORS(app, resources={r"/*": {"origins": "*"}})

# Microsoft Ticker object.
msft_ticker = Ticker("MSFT")

# Get all available historical market data.
msft_history = msft_ticker.history(period="max")

# == Routes == #


# Sanity check route.
@app.route("/ping", methods=["GET"])
def ping_pong():
    return jsonify("pong!")


# Quick Summary.
@app.route("/summary", methods=["GET"])
def get_summary():
    return jsonify(
        {
            "status": "success",
            "summary": msft_history.head(request.args.get("count", default=25, type=int))
            .reset_index()
            .to_json(orient="records"),
        }
    )


# Quick Summary.
@app.route("/v1/client/data", methods=["GET"])
def get_data():
    # The list of datasets sent back to be plotted.
    datasets = []

    # Get data from specified data range.
    start_date = request.args.get("start_date", default="2021-01-01", type=str)
    end_date = request.args.get("end_date", default="2022-04-01", type=str)
    date_mask = (msft_history.index >= start_date) & (msft_history.index < end_date)

    # Primary raw dataset with no modifications.
    disableRawData = request.args.get("disable_raw", default=False, type=lambda v: v.lower() == 'true')
    if not disableRawData:
        datasets.append({
            "name": "Raw Data",
            "type": "line",
            "x": msft_history.loc[date_mask].index.values.astype('datetime64[ms]').astype('int64').tolist(),
            "y": msft_history.loc[date_mask].to_dict(orient="records"),
        })

    # Everything else will focus on a specific field of the data.

    # Select out the desired data field.
    field = request.args.get("field", default="Close", type=str)
    selectedField = getattr(msft_history.loc[date_mask], field)

    # Transformations of the data.
    transformsList = request.args.getlist("transform")
    for transform in transformsList:
        if transform == 'diff':
            diff = selectedField.diff().dropna()
            datasets.append(
                {
                    "name": "Difference",
                    "type": "line",
                    "x": diff.index.values.astype('datetime64[ms]').astype('int64').tolist(),
                    "y": diff.tolist(),
                }
            )
        if transform == 'log':
            log = np.log(selectedField)
            datasets.append(
                {
                    "name": "Log",
                    "type": "line",
                    "x": log.index.values.astype('datetime64[ms]').astype('int64').tolist(),
                    "y": log.tolist(),
                }
            )
        if transform == 'diff log':
            diff_log = np.log(selectedField/selectedField.shift(1)).dropna()
            datasets.append(
                {
                    "name": "Difference + Log",
                    "type": "line",
                    "x": diff_log.index.values.astype('datetime64[ms]').astype('int64').tolist(),
                    "y": diff_log.tolist(),
                }
            )

    # Models of the data.
    modelsList = request.args.getlist("model")
    for model in modelsList:
        if model == 'linear':
            # model, model_fit, train, test, fc = linear_regression.generate(selectedField)
            datasets += linear_regression.generate(selectedField)[2:]
        if model == 'arima':
            # model, test, test_cf, fc, fc_cf = arima.generate(selectedField)
            datasets += arima.generate(selectedField)[1:]
        if model == 'prophet':
            # model, fc, fc_cf = prophet.generate(selectedField)
            datasets += prophet.generate(selectedField)[1:]

    return jsonify(
        {
            "status": "success",
            "data": datasets,
        }
    )


if __name__ == "__main__":
    app.run()
