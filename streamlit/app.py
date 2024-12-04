import streamlit as st
import pandas as pd
from tensorflow.keras.models import load_model
import joblib
import numpy as np
import plotly.graph_objects as go

monthly_model = load_model("./models/time_series/lstm_model_monthly.h5")
weekly_model = load_model("./models/time_series/lstm_model_weekly.h5")
daily_model = load_model("./models/time_series/lstm_model_daily.h5")

monthly_scaler = joblib.load("./models/time_series/scaler_monthly.pkl")
weekly_scaler = joblib.load("./models/time_series/scaler_weekly.pkl")
daily_scaler = joblib.load("./models/time_series/scaler_daily.pkl")

monthly_dates = pd.read_csv("./data/synthetic_monthly_dates.csv")
weekly_dates = pd.read_csv("./data/synthetic_weekly_dates.csv")
daily_dates = pd.read_csv("./data/synthetic_daily_dates.csv")

st.title("Time Series Forecasting with LSTM")
st.sidebar.header("Choose Forecasting Type")

st.markdown(
    """
    Welcome to the **Time Series Forecasting App**!  
    Use the sidebar to select forecasting options and view results.
    """
)

st.sidebar.markdown("### About the Model")
st.sidebar.write("This app demonstrates LSTM-based time series forecasting with predictions visualized interactively.")

forecast_type = st.sidebar.radio(
    "Select Forecast Interval",
    ("Monthly", "Weekly")
)

if forecast_type == "Monthly":
    st.subheader("Monthly Forecast")
    model = monthly_model
    scaler = monthly_scaler
    dates = monthly_dates
    future_steps = 12
    ts = 12
    last_sequence = np.zeros((ts, 1))
    st.components.v1.html(open("./images/lstm_monthly_forecast.html", "r").read(), height=400, width=850)
    st.write("Forecasting for the **next 12 months** starting from the last date in the training data.")
elif forecast_type == "Weekly":
    st.subheader("Weekly Forecast")
    model = weekly_model
    scaler = weekly_scaler
    dates = weekly_dates
    future_steps = 52
    ts = 7
    last_sequence = np.zeros((ts, 1))
    st.components.v1.html(open("./images/lstm_weekly_forecast.html", "r").read(), height=400, width=850)

    st.write("Forecasting for the **next 52 weeks** starting from the last date in the training data.")
# elif forecast_type == "Daily":
#     st.subheader("Daily Forecast")
#     st.write("Forecasting for the **next 365 days** starting from the last date in the training data.")
#     model = daily_model
#     scaler = daily_scaler
#     dates = daily_dates
#     future_steps = 365
#     ts = 30
#     last_sequence = np.zeros((ts, 1))
#     st.components.v1.html(open("./images/lstm_daily_forecast.html", "r").read(), height=400, width=850)

st.markdown(
    """
    ---
    Visit the [GitHub Repo](https://github.com/bharath03-a/Gun-Violence-Incidents) for more details.
    """,
    unsafe_allow_html=True,
)

def predict_future(model, scaler, last_sequence, future_steps, ts):
    future_predictions = []
    for _ in range(future_steps):
        next_pred = model.predict(last_sequence.reshape(1, ts, 1))[0]
        future_predictions.append(next_pred)
        last_sequence = np.append(last_sequence[1:], next_pred).reshape(ts, 1)

    future_predictions = scaler.inverse_transform(np.array(future_predictions).reshape(-1, 1))
    return future_predictions

if st.sidebar.button("Predict"):
    predictions = predict_future(model, scaler, last_sequence, future_steps, ts)
    dates["Predictions"] = predictions

    dates["Predictions"] = dates["Predictions"].apply(lambda x: int(round(x)))

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=dates["Date"],
            y=dates["Predictions"].values,
            mode="lines+markers",
            name="Predictions",
        )
    )
    fig.update_layout(
        title=f"{forecast_type} Predictions",
        xaxis_title="Date",
        yaxis_title="Predicted Value",
        template="plotly_white",
    )
    st.plotly_chart(fig)

    st.subheader(f"{forecast_type} Predictions")
    st.dataframe(dates)

    st.sidebar.subheader("Download Predictions")
    csv = dates.to_csv(index=False).encode("utf-8")
    st.sidebar.download_button(
        label="Download CSV",
        data=csv,
        file_name=f"{forecast_type}_predictions.csv",
        mime="text/csv",
    )