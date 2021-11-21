import datetime
import json
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
from dash.dependencies import Input, Output

# pip install pyorbital
from pyorbital.orbital import Orbital
satellite = Orbital('TERRA')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

with open("out/matched_live_tennis_games.json", "r") as infile:
    matched_games = json.load(infile)

app.layout = html.Div([
    html.H1("LIVE Tennis Arbitrage"),
    html.Div(id="box", children=[
        html.Table([
            html.Thead(
                html.Tr([html.Th(th) for th in ["Site", "Player 1", "Odds (P1)", "Odds (P2)", "Player 2", "Arbitrage", "Link"]])
            ),
            html.Tbody([
                html.Tr([
                    html.Td(site),
                    html.Td(match[site]["player_A"]["lastname"]),
                    html.Td(match[site]["player_A"]["odds"]),
                    html.Td(match[site]["player_B"]["odds"]),
                    html.Td(match[site]["player_B"]["lastname"]),
                    html.Td(match[site]["arbitrage"]),
                    html.Td(html.A(href=match[site]["link"], children=match[site]["link"], target="_blank"))
                ]) for site in match
            ])
        ]) for match in matched_games
    ]),
    dcc.Interval(
        id='interval-component',
        interval=1*1000, # in milliseconds
        n_intervals=0
    )
])


@app.callback(Output(component_id='box', component_property='children'),
              Input('interval-component', 'n_intervals'))
def update_table(n):
    with open("out/matched_live_tennis_games.json", "r") as infile:
        matched_games = json.load(infile)
    return [
        html.Table([
            html.Thead(
                html.Tr([html.Th(th) for th in ["Site", "Player 1", "Odds (P1)", "Odds (P2)", "Player 2", "Arbitrage", "Link"]])
            ),
            html.Tbody([
                html.Tr([
                    html.Td(site),
                    html.Td(match[site]["player_A"]["lastname"]),
                    html.Td(match[site]["player_A"]["odds"]),
                    html.Td(match[site]["player_B"]["odds"]),
                    html.Td(match[site]["player_B"]["lastname"]),
                    html.Td(match[site]["arbitrage"]),
                    html.Td(html.A(href=match[site]["link"], children=match[site]["link"], target="_blank"))
                ]) for site in match
            ])
        ]) for match in matched_games
    ]



if __name__ == '__main__':
    app.run_server(debug=True)