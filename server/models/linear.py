import pandas as pd
import numpy as np
from pandas.tseries.offsets import DateOffset

class linear_regression:
    """Class for calculating linear regression of a time series."""

    def generate(data, days_to_forecast=30, training_size=0.75):
        """Linear regression model using NumPy Poly 1D fit.

        Args:
            data: Time series data to perform linear regression on.
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

        x = np.arange(train.size)
        y = np.arange(test.size)
        fc = np.arange(future_dates.size)

        # Create and fit model.
        model = np.polyfit(x, train, 1)
        model_fit = np.poly1d(model)

        # Produce model driven datasets.
        return (
            model,
            model_fit,
            {
                "name": "Predicted vs Training (LR)",
                "type": "line",
                "x": train.index.values.astype('datetime64[ms]').astype('int64').tolist(),
                "y": model_fit(x).tolist(),
            },
            {
                "name": "Predicted vs Test (LR)",
                "type": "line",
                "x": test.index.values.astype('datetime64[ms]').astype('int64').tolist(),
                "y": model_fit(y + x[-1]).tolist(),
            },
            {
                "name": "Forecast (LR)",
                "type": "line",
                "x": future_dates.index.values.astype('datetime64[ms]').astype('int64').tolist(),
                "y": model_fit(fc + data.size).tolist(),
            },
        )
