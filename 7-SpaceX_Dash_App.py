# Import required libraries
import pandas as pd
import numpy
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                            options= numpy.append('All Sites', spacex_df['Launch Site'].unique()),
                                            value='All Sites',
                                            placeholder='Select a launch site',
                                            style={'width':'80%', 'padding':'3px', 'font-size':'20px', 'textAlign': 'center'}
                                            ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=min_payload,
                                                max=max_payload,
                                                step=1000,
                                                value=[min_payload, max_payload],
                                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'))

def update_pie_chart(site_dropdown):
    if site_dropdown == 'All Sites':
        # Create a pie chart of the success for all sites
        pie_chart_df = spacex_df[spacex_df['class'] == 1].groupby(['Launch Site']).size().reset_index(name='count')
        fig = px.pie(pie_chart_df, values='count', names='Launch Site', title='Total Success Launches By Site')
        return fig
    else:
        # return the outcomes piechart for a selected site
        pie_chart_df = spacex_df[spacex_df['Launch Site'] == site_dropdown].groupby('class')['class'].size().reset_index(name='count')
        pie_chart_df['class'] = pie_chart_df['class'].map({0: 'Failure', 1: 'Success'})

        fig = px.pie(pie_chart_df, values='count', names='class', title='Total Success vs Failes Launches for site ' + site_dropdown)

        return fig
                

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload-slider', component_property='value'))

def update_scatter_chart(site_dropdown, payload_slider):
    if site_dropdown == 'All Sites':
        scatter_df = spacex_df
    else:
        scatter_df = spacex_df[spacex_df['Launch Site'] == site_dropdown]
    
    scatter_df = scatter_df[scatter_df['Payload Mass (kg)'].between(payload_slider[0], payload_slider[1])]
    scatter_df['class'] = scatter_df['class'].map({0: 'Failure', 1: 'Success'})
    fig = px.scatter(scatter_df, x='Payload Mass (kg)', y='class', title='Correlation between Payload and Success for site: ' + site_dropdown)

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
