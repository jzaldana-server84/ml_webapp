from prophet import Prophet
import pandas as pd

def forecast_prophet(df, periods=30):
    df = df.rename(columns={"date": "ds", "value": "y"})
    model = Prophet()
    model.fit(df)
    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)
    return forecast[["ds", "yhat"]]
