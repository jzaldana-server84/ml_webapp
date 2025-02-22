import dash_core_components as dcc
import dash_html_components as html

def ui_layout():
    return html.Div([
        dcc.Dropdown(
            id="model-selector",
            options=[
                {"label": "Prophet", "value": "prophet"},
                {"label": "ARIMA", "value": "arima"},
                {"label": "LSTM", "value": "lstm"}
            ],
            placeholder="Select a forecasting model"
        ),
        dcc.Graph(id="forecast-plot")
    ])
