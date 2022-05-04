from prophet import Prophet
# from prophet.plot import plot_plotly, plot_components_plotly


class prophet:
    """Class for creating a Prophet model of a time series."""

    def generate(data, days_to_forecast=30, training_size=0.75):
        """Generates a new Prophet model.

        Args:
            data: Time series data to generate a Prophet model for.
            days_to_forecast: Number of days into the future to forecast. Default is 30.
            training_size: Percentage of data points to place in training set. Default is 0.75 (75%).

        Returns:
            Returns a tuple containing: trained model, fitted model, model training results,
            model test results, and model forecast results.
        """

        # Split up the dataset into training and test data.
        # size = int(data.size * training_size)
        # train, test = data[0:size], data[size:data.size]

        # Prophet model.
        model = Prophet(daily_seasonality=True, yearly_seasonality=True)

        # Fit the model.
        model.fit(data.reset_index().rename(columns={"Date": "ds", "Close": "y"}))

        # Select a forecast period and create those dates for later.
        future_dates = model.make_future_dataframe(periods=days_to_forecast)

        # Generate forecast.
        forecast = model.predict(future_dates)

        # plot_plotly(model, forecast)

        # Produce model driven datasets.
        return (
            model,
            # {
            #     "name": "Predicted vs Test (Prophet)",
            #     "type": "scatter",
            #     # "showlegend": False,
            #     "fill": "tozerox",
            #     "fillcolor": "rgba(0,176,246,0.2)",
            #     "line": { "color": "transparent" },
            #     "x": (
            #         test.index.values.astype('datetime64[ms]').astype('int64').tolist()
            #         + test.index.values[::-1].astype('datetime64[ms]').astype('int64').tolist()
            #     ),
            #     "y": test_cf[0].tolist() + test_cf[1][::-1].tolist(),
            # },
            {
                "name": "Forecast Confidence Interval (Prophet)",
                "type": "scatter",
                "showlegend": False,
                "fill": "toself",
                "fillcolor": "rgba(0,100,80,0.2)",
                "line": { "color": "transparent" },
                "x": (
                    future_dates.values.astype('datetime64[ms]').astype('int64').flatten().tolist()
                    + future_dates.values[::-1].astype('datetime64[ms]').astype('int64').flatten().tolist()
                ),
                "y": forecast.yhat_lower.tolist() + forecast.yhat_upper[::-1].tolist(),
            },
            {
                "name": "Forecast (Prophet)",
                "type": "scatter",
                "x": future_dates.values.astype('datetime64[ms]').astype('int64').flatten().tolist(),
                "y": forecast.yhat.tolist(),
            },
            # {
            #     "name": "Predicted vs Test (Prophet)",
            #     "type": "scatter",
            #     "x": test.index.values.astype('datetime64[ms]').astype('int64').tolist(),
            #     "y": test_pred.tolist(),
            # },
        )
