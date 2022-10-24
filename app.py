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
#df = df.style.format({'cases': "{:,.0f}", 'deaths': "{:,.0f}",'recovered': "{:,.0f}"})

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
        html.P('''In December 2019, a number of cases that pointed to a potential respiratory disease were reported in Wuhan, China. The World Health Organisation (WHO) 
        made the first announcement of a novel coronavirus SARS-CoV-2 in January 2020 and 2 months later, a pandemic was declared [1]. The COVID-19 pandemic has had a significant global impact, 
        with more than 535M (+198k) cases and 6.31M (+463) deaths worldwide.''', style={'textAlign':'justify', 'marginLeft' : '15px', 'marginRight': '15px'}),
        html.P('Data was retrieved through the Disease.sh open API and preprocessed to allow for visualisation of COVID statistics over time.',
        style={'textAlign':'justify', 'marginLeft' : '15px', 'marginRight': '15px'}),
        
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
        html.P('''In June 2020, the Global Vaccine Summit took place and the WHO received funding for vaccination research. Less than a year after the pandemic declaration, 
        January 5th, the first vaccine from Pfizer/BioNTech received an emergency use validation [1]. Papers reporting on the impact of vaccination programmes and the deaths 
        averted, estimated a  63 percent reduction in mortality with the possibility of an increased percentage, had the vaccine distribution covered low-income countries as well [2].
        ''',style={'textAlign':'justify', 'marginLeft' : '15px', 'marginRight': '15px'}),
        html.P('''Interact with the map below to find out the statistics of each country, in regards to the total confirmed cases, total recovered, total vaccines distributed and the 
        total deaths. The colorscale has been set to display the percentage of vaccines distributred (calculated by the total vaccines distributed / population). It is important to note 
        that the maximum percentage, may reflect the 1st dose, 2nd dose and/or 3rd dose of vaccine coverage, however, it is impossible with this data to be assured of that. There possibly 
        still is a percentage of the population that remains unvaccinated.
        ''',style={'textAlign':'justify', 'marginLeft' : '15px', 'marginRight': '15px'}),

        html.Br(),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id='world', figure=fig1, responsive=True))
            ]
        ),

        html.Br(),
        html.Hr(),
        html.Br(),

        html.H3('Highest Ranked in',style={'marginLeft' : '15px'}),
        html.P('''The following graphs have been made to provide some perspective on the ways data can be presented. On the left side, one can select between [cases, recovered, deaths,  
        vaccination_percentage] and the respective highest ranked countries will appear. Please note that the population has not been taken into consideration in the first 3 options, 
        therefore the results are misguided in the sense that population massively affects them.''',style={'textAlign':'justify', 'marginLeft' : '15px', 'marginRight': '15px'}),
        html.P('''On the right side, one can select through the same options however, the number of those ia calculated per 1 Million people, thereby examining the same amount of people 
        and allowing for true comparison.''',style={'textAlign':'justify', 'marginLeft' : '15px', 'marginRight': '15px'}),

        html.Br(),
        dbc.Row([
            dbc.Col([html.Div([fig_dropdown, fig_plot],style={'textAlign':'center', 'marginLeft' : '5px', 'marginRight': '5px'})
            ]),
            dbc.Col([html.Div([fig3_dropdown, fig3_plot],style={'textAlign':'center', 'marginLeft' : '5px', 'marginRight': '5px'})
            ])
        ],className="g-0"),

        html.Br(),
        html.Hr(),
        html.Br(),

        html.H3('Resources',style={'marginLeft' : '15px'}),
        html.P('''[1] World, H. O. (2020). Timeline: WHO’s COVID-19 response. World Health Organization. 
        https://www.who.int/emergencies/diseases/novel-coronavirus-2019/interactive-timeline#event-51''',
        style={'textAlign':'justify', 'marginLeft' : '15px', 'marginRight': '15px'}),
        html.P('''[2] Watson, O. J., Barnsley, G., Toor, J., Hogan, A. B., Winskill, P., & Ghani, A. C. (2022). Global impact of the first year of COVID-19 vaccination: 
        a mathematical modelling study. The Lancet Infectious Diseases, 22(9), 1293–1302. https://doi.org/10.1016/S1473-3099(22)00320-6''',
        style={'textAlign':'justify', 'marginLeft' : '15px', 'marginRight': '15px'})



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
        fig.layout.coloraxis.colorbar.title = 'vaccination'

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
        fig.layout.coloraxis.colorbar.title = 'cases'

    elif fig3_name == 'deathsPerOneMillion':
        dftemp = df.nlargest(10, ['deathsPerOneMillion'])
        fig = px.bar(dftemp, x="country", y="deathsPerOneMillion", color="deathsPerOneMillion",
                     hover_data=['country'],color_continuous_scale='Reds')
        fig.layout.coloraxis.colorbar.title = 'deaths'

    elif fig3_name == 'recoveredPerOneMillion':
        dftemp = df.nlargest(10, ['recoveredPerOneMillion'])
        fig = px.bar(dftemp, x="country", y="recoveredPerOneMillion", color="recoveredPerOneMillion",
                     hover_data=['country'],color_continuous_scale='Greens')
        fig.layout.coloraxis.colorbar.title = 'recovered'
    elif fig3_name == 'vaccination_percentage':
        dftemp = df.nlargest(10, ['vaccination_percentage'])
        fig = px.bar(dftemp, x="country", y="vaccination_percentage", color="vaccination_percentage",
                     hover_data=['country'],color_continuous_scale='Blues')
        fig.layout.coloraxis.colorbar.title = 'vaccination'

    fig.update_layout(yaxis={'visible': False, 'showticklabels': False}, xaxis={'visible': False, 'showticklabels': False})

    return dcc.Graph(figure=fig)


app.run_server(debug=True, use_reloader=True)  # Turn off reloader if inside Jupyter


# if __name__ == '__main__':
#     app.run_server(debug=True)