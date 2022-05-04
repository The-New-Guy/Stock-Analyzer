import pandas as pd
import pmdarima as pm
from pandas.tseries.offsets import DateOffset


class arima:
    """Class for creating an ARIMA model of a time series."""

    def generate(data, days_to_forecast=30, training_size=0.75):
        """Generates a new ARIMA model.

        Args:
            data: Time series data to generate an ARIMA model for.
            days_to_forecast: Number of days into the future to forecast. Default is 30.
            training_size: Percentage of data points to place in training set. Default is 0.75 (75%).

        Returns:
            Returns a tuple containing: trained model, fitted model, model training results,
            model test results, and model forecast results.
        """

        # Split up the dataset into training and test data.
        size = int(data.size * training_size)
        train, test = data[0:size], data[size:data.size]

        # Select a forecast period and create those dates for later.
        add_dates = [data.index[-1] + DateOffset(days=x) for x in range(days_to_forecast)]
        future_dates = pd.DataFrame(index=add_dates[1:], columns=["Close"])

        model = pm.auto_arima(train)

        test_pred, confint = model.predict(n_periods=test.size, return_conf_int=True)
        test_cf = pd.DataFrame(confint)

        forecast, confint = model.predict(n_periods=len(future_dates), return_conf_int=True)
        forecast_cf = pd.DataFrame(confint)

        # Produce model driven datasets.
        return (
            model,
            {
                "name": "Predicted vs Test Confidence Interval (ARIMA)",
                "type": "scatter",
                "showlegend": False,
                "fill": "toself",
                "fillcolor": "rgba(0,176,246,0.2)",
                "line": { "color": "transparent" },
                "x": (
                    test.index.values.astype('datetime64[ms]').astype('int64').tolist()
                    + test.index.values[::-1].astype('datetime64[ms]').astype('int64').tolist()
                ),
                "y": test_cf[0].tolist() + test_cf[1][::-1].tolist(),
            },
            {
                "name": "Forecast Confidence Interval (ARIMA)",
                "type": "scatter",
                "showlegend": False,
                "fill": "toself",
                "fillcolor": "rgba(0,100,80,0.2)",
                "line": { "color": "transparent" },
                "x": (
                    future_dates.index.values.astype('datetime64[ms]').astype('int64').tolist()
                    + future_dates.index.values[::-1].astype('datetime64[ms]').astype('int64').tolist()
                ),
                "y": forecast_cf[0].tolist() + forecast_cf[1][::-1].tolist(),
            },
            {
                "name": "Forecast (ARIMA)",
                "type": "scatter",
                "x": future_dates.index.values.astype('datetime64[ms]').astype('int64').tolist(),
                "y": forecast.tolist(),
            },
            {
                "name": "Predicted vs Test (ARIMA)",
                "type": "scatter",
                "x": test.index.values.astype('datetime64[ms]').astype('int64').tolist(),
                "y": test_pred.tolist(),
            },
        )
