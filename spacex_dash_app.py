# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
# import dash_html_components as html
# import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

launch_site = spacex_df['Launch Site'].unique().tolist()
launch_site_options = [{'label': 'All Sites', 'value': 'ALL'}]
for ls in launch_site:
    launch_site_options.append({'label': ls, 'value': ls})

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                    options=launch_site_options,
                                    value='ALL',
                                    placeholder='Select a Launch Site here',
                                    searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    marks={i: str(i) for i in range(0, 10000+1, 500)},
                                    value=[min_payload, max_payload]              
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        data = spacex_df[['class', 'Launch Site']].groupby('Launch Site').sum()
        fig = px.pie(data, values='class', names=data.index, 
                     title='The total success launches in each launch site')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        data = filtered_df['class'].value_counts()
        fig = px.pie(data, values=data.values, names=data.index, 
                     title=f'The success and failed count for {entered_site}')
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), 
               Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart(site, payload):
    range_df = spacex_df[((spacex_df['Payload Mass (kg)'] >= payload[0]) & (spacex_df['Payload Mass (kg)'] <= payload[1]))]
    if site == 'ALL':
        data = range_df[['class', 'Payload Mass (kg)', 'Booster Version Category']]
        fig = px.scatter(data, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                     title='The scatter plot between Payload mass and Class')
        return fig
    else:
        filtered_df = range_df[range_df['Launch Site'] == site]
        data = filtered_df[['class', 'Payload Mass (kg)', 'Booster Version Category']]
        fig = px.scatter(data, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                     title=f'The scatter plot between Payload mass and Class for launch site {site}')
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
