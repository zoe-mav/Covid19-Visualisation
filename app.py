import dash
import requests

import plotly.graph_objects as go # or plotly.express as px
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

from dash import html, dcc


df = pd.read_csv('countries.csv')

url = "https://disease.sh/v3/covid-19/all"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)
world_stats = response.json()

#------------------------------------------------------------------------
#Figures

df['text'] = df['country'].astype(str) + '<br>' + \
    'Confirmed Cases ' + df['cases'].astype(str) + '<br>' + \
    'Total Recovered ' + df['recovered'].astype(str) + '<br>' + \
    'Vaccines Distributed ' + df['vaccinations'].astype(str) + '<br>' + \
    'Deaths ' + df['deaths'].astype(str) 

fig1 = go.Figure(data=go.Choropleth(
    locations = df['countryInfo.iso3'],
    z = df['vaccination_percentage'],
    text = df['text'],
    colorscale = 'Blues',
    autocolorscale=False,
    colorbar_tickprefix = '%',
    colorbar_title = '% Vaccines<br>Distributed',
))
       
fig1.update_layout(
    width=1200,
    height=800,
    autosize=True,
    margin=dict(t=0, b=0, l=0, r=0),
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    )
)

fig_names = ['cases', 'deaths', 'recovered', 'vaccination_percentage']
fig_dropdown = html.Div([
    dcc.Dropdown(
        id='fig_dropdown',
        options=[{'label': x, 'value': x} for x in fig_names],
        value='recovered'
    )])
fig_plot = html.Div(id='fig_plot')

fig3_names = ['casesPerOneMillion', 'deathsPerOneMillion','recoveredPerOneMillion','vaccination_percentage']
fig3_dropdown = html.Div([
    dcc.Dropdown(
        id='fig3_dropdown',
        options=[{'label': x, 'value': x} for x in fig3_names],
        value='recoveredPerOneMillion'
    )])
fig3_plot = html.Div(id='fig3_plot')



#------------------------------------------------------------------------
# Dash

app = dash.Dash(meta_tags=[{'name': 'viewport',
                'content': 'width=device-width, initial-scale=2.0, maximum-scale=2.2, minimum-scale=0.5,'}],  external_stylesheets=[dbc.themes.ZEPHYR]
                )
server = app.server

theme = {
    'darkblue' : "#261c66", 
    'green' : "#89ca1e", 
    'lightblue' : "#535daa"
    }

stats = {'red': '#DA4167',
         'blue': '#3772FF',
         'green': '#56CA3F',
         'gray': '#525453'}

app.layout = dbc.Container(
    [
        html.Br(),
        html.H1("COVID-19 Visualisation 2020-22", style={'textAlign':'center', 'color': theme['lightblue']}),
        html.H2("SDC Task", style={'textAlign':'center', 'color': theme['green']}),
        html.P('''Data processing and visualization pipeline for COVID data. You will retrieve the data from a public API (e.g., covidtracking.com), 
        write code to process the data as needed, and provide visualizations of COVID infections over time.''', style={'textAlign':'center'}),

        html.Br(),
        html.Hr(),
        html.Br(),
        
        html.H3('Global Statistics',style={'marginLeft' : '15px'}),
        html.Br(),
        dbc.Row([
            dbc.Col([html.Div( 
                children=[
                    html.H5(children='Confirmed Cases',
                            style={'textAlign': 'center'}),

                    html.H4(children=format(world_stats["cases"], ',d'),
                            style={'textAlign': 'center',
                                   'color': stats['gray']}),

                    html.Br(),

                    html.H5(children='Vaccines Distributed',
                            style={'textAlign': 'center'}),

                    html.H4(children=format(df.vaccinations.sum(), ',d'),
                            style={'textAlign': 'center',
                                   'color': stats['blue']})
                ])
            ]),

            dbc.Col([html.Div(children=[
                    html.H5(children='Total Recovered',
                            style={'textAlign': 'center'}),

                    html.H4(children=format(world_stats["recovered"], ',d'),
                            style={'textAlign': 'center',
                                   'color': stats['green']}),

                    html.Br(),

                    html.H5(children='Deaths',
                            style={'textAlign': 'center'}),

                    html.H4(children=format(world_stats["deaths"], ',d'),
                            style={'textAlign': 'center',
                                   'color': stats['red']})
                ])
            ])
        ],className="g-0"),


        
        html.Br(),
        html.Hr(),
        html.Br(),
        
        html.H3('2022 Global Vaccine Coverage',style={'marginLeft' : '15px'}),
        html.P("Explain blah blah",style={'marginLeft' : '15px'}),

        html.Br(),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id='world', figure=fig1, responsive=True))
            ]
        ),
        html.Br(),
        html.P("Explain blah blah", style={'textAlign':'center'}),

        html.Br(),
        html.Hr(),
        html.Br(),

        html.H3('Highest Ranking in',style={'marginLeft' : '15px'}),
        html.P("Explain blah blah",style={'marginLeft' : '15px'}),
        html.Br(),
        dbc.Row([
            dbc.Col([html.Div([fig_dropdown, fig_plot])
            ]),
            dbc.Col([html.Div([fig3_dropdown, fig3_plot])
            ])
        ],className="g-0"),

        html.Br(),
        html.Hr(),
        html.Br(),



],
fluid=True,
className="dbc", 
)



@app.callback(
dash.dependencies.Output('fig_plot', 'children'),
[dash.dependencies.Input('fig_dropdown', 'value')])
def update_output(fig_name):
    return treemap(fig_name)

def treemap(fig_name):
    if fig_name == 'cases':
        dftemp = df.nlargest(10, ['cases'])
        fig = px.treemap(dftemp, path=['country'], values='cases',
                  color='cases', hover_data=['country'],color_continuous_scale='Greys')
    elif fig_name == 'deaths': 
        dftemp = df.nlargest(10, ['deaths'])
        fig = px.treemap(dftemp, path=['country'], values='deaths',
                  color='deaths', hover_data=['country'],color_continuous_scale='Reds')
    elif fig_name == 'recovered': 
        dftemp = df.nlargest(10, ['recovered'])
        fig = px.treemap(dftemp, path=['country'], values='recovered',
                  color='recovered', hover_data=['country'],color_continuous_scale='Greens')
    elif fig_name == 'vaccination_percentage': 
        dftemp = df.nlargest(10, ['vaccination_percentage'])
        fig = px.treemap(dftemp, path=['country'], values='vaccination_percentage',
                  color='vaccination_percentage', hover_data=['country'],color_continuous_scale='Blues')
    return dcc.Graph(figure=fig)

@app.callback(
dash.dependencies.Output('fig3_plot', 'children'),
[dash.dependencies.Input('fig3_dropdown', 'value')])
def update_output(fig3_name):
    return barplot(fig3_name)

def barplot(fig3_name):
    if fig3_name == 'casesPerOneMillion':
        dftemp = df.nlargest(10, ['casesPerOneMillion'])
        fig = px.bar(dftemp, x="country", y="casesPerOneMillion", color="casesPerOneMillion",
                     hover_data=['country'],color_continuous_scale='Greys')
    elif fig3_name == 'deathsPerOneMillion':
        dftemp = df.nlargest(10, ['deathsPerOneMillion'])
        fig = px.bar(dftemp, x="country", y="deathsPerOneMillion", color="deathsPerOneMillion",
                     hover_data=['country'],color_continuous_scale='Reds')
    elif fig3_name == 'recoveredPerOneMillion':
        dftemp = df.nlargest(10, ['recoveredPerOneMillion'])
        fig = px.bar(dftemp, x="country", y="recoveredPerOneMillion", color="recoveredPerOneMillion",
                     hover_data=['country'],color_continuous_scale='Greens')
    elif fig3_name == 'vaccination_percentage':
        dftemp = df.nlargest(10, ['vaccination_percentage'])
        fig = px.bar(dftemp, x="country", y="vaccination_percentage", color="vaccination_percentage",
                     hover_data=['country'],color_continuous_scale='Blues')
    return dcc.Graph(figure=fig)


#app.run_server(debug=True, use_reloader=True)  # Turn off reloader if inside Jupyter


if __name__ == '__main__':
    app.run_server(debug=True)