from dash.dependencies import Output
import pandas as pd
from dash import dcc, html
import dash
from load_data import StockDataLocal
from dash.dependencies import Output, Input
import plotly_express as px
from time_filtering import filter_time

stock_data_object = StockDataLocal()

symbol_dict = dict(AAPL = "Apple", NVDA = "Nvidia", TSLA = "Tesla", IBM = "IBM")

stock_options_dropdown = [{"label" : name, "value": symbol}
                        for symbol, name in symbol_dict.items()]

df_dict = {symbol: stock_data_object.stock_dataframe(symbol)
            for symbol in symbol_dict}

slider_marks = {i : mark for i, mark in enumerate(["1 Day", "1 Week", "1 Month", "3 Months", "1 Year", "5 Year", "Max"])}

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Stocks viewer"),
    html.H2("This is a cool app"),
    dcc.Dropdown(id = "stocks-picker-dropdown", className = '',
                options = stock_options_dropdown,
                value = 'AAPL'
                 ),
    dcc.Graph(id ="stock-graph", className = ''),

    dcc.Slider(id = "time-slider", className='',
    min = 0, max = 6,
    step = None,
    value = 2,
    marks = slider_marks)
])

@app.callback(
    Output("stock-graph", "figure"),
    Input("stock-picker-dropdown", "value"),
    Input("time-slider", "value")
)
def update_graph(stock, time_index):

    dff_daily, dff_intraday = df_dict[stock]

    dff = dff_intraday if time_index <= 2 else dff_daily

    days = {i: day for i, day in enumerate([1,7,30,90,365, 365*5])}

    dff = dff if time_index == 6 else filter_time(dff, days[time_index])

    fig = px.line(dff, x = dff.index, y = "close")

    return fig # fig object goes into Output() property ie figure property

if __name__ == "__main__":
    app.run_server(debug = True)