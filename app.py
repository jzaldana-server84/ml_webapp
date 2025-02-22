import os
import dash
import dash_uploader as du
import dash_html_components as html
import dash_core_components as dcc
import dash_ag_grid as dag
import pandas as pd
from dash.dependencies import Input, Output

UPLOAD_FOLDER = "uploads"

app = dash.Dash(__name__)
du.configure_upload(app, UPLOAD_FOLDER)

@du.callback(
    output=Output("upload-data", "isCompleted"),
    id="upload-data"
)
def callback_on_completion(status):
    if status:
        file_path = max([UPLOAD_FOLDER + "/" + f for f in os.listdir(UPLOAD_FOLDER)], key=os.path.getctime)
        os.chmod(file_path, 0o666)

app.layout = html.Div([
    html.H2("Forecasting App"),
    
    # File Upload
    du.Upload(id="upload-data", text="Drag & Drop or Click to Upload CSV", filetypes=["csv"], max_files=1),
    
    # Table Display
    dag.AgGrid(id="data-table"),
])

@app.callback(
    Output("data-table", "rowData"),
    Input("upload-data", "isCompleted"),
    prevent_initial_call=True
)
def update_table(is_completed):
    if is_completed:
        file_path = max([UPLOAD_FOLDER + "/" + f for f in os.listdir(UPLOAD_FOLDER)], key=os.path.getctime)
        os.chmod(file_path, 0o666)
        df = pd.read_csv(file_path)
        return df.to_dict("records")
    
    return []

if __name__ == '__main__':
    app.run_server(debug=True)

@app.callback(
    Output("forecast-plot", "figure"),
    Input("model-selector", "value"),
    Input("upload-data", "isCompleted"),
    prevent_initial_call=True
)
def run_forecast(model_name, is_completed):
    file_path = max([UPLOAD_FOLDER + "/" + f for f in os.listdir(UPLOAD_FOLDER)], key=os.path.getctime)
    df = pd.read_csv(file_path)

    if model_name == "prophet":
        from models.prophet_model import forecast_prophet
        forecast = forecast_prophet(df)
    elif model_name == "arima":
        from models.arima_model import forecast_arima
        forecast = forecast_arima(df)
    else:
        return {}

    # Plot
    import plotly.express as px
    fig = px.line(forecast, x="ds", y="yhat", title=f"{model_name} Forecast")
    return fig
