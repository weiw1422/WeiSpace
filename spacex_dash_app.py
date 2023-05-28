# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

set_launch_site = set(spacex_df['Launch Site'])

launch_site_list = list(set_launch_site)


# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                html.Div(['Launch Site', dcc.Dropdown(id ='site-dropdown',                                 
                                                        options = [
                                                            {'label': 'All Sites', 'value': 'ALL'},
                                                            {'label': f'{launch_site_list[0]}', 'value':f'{launch_site_list[0]}'},
                                                            {'label': launch_site_list[1], 'value':launch_site_list[1]},
                                                            {'label': launch_site_list[2], 'value':launch_site_list[2]},
                                                            {'label': launch_site_list[3], 'value':launch_site_list[3]},
                                                        ],
                                                        value = 'ALL',

                                                        placeholder = 'Select a Launch Site here',
                                                        searchable = True
                                                        )  
                                            ]),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)


                                html.Div(dcc.RangeSlider(id = 'payload-slider',
                                                        min = 0, max = 10000, step = 1000,
                                                        marks = {0:'0', 100:'100'},
                                                        value = [min_payload, max_payload]



                                )),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# Function decorator to specify function input and output


@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    



              
                  Input(component_id='site-dropdown', component_property='value'),
                  

                  
              )
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='The success rate')
        return fig
    else:
        df_entered = filtered_df[filtered_df['Launch Site']==entered_site]
        df_entered['number'] = df_entered['class']
        df1 = df_entered.groupby(['class'])['number'].count().reset_index()
        print(df1)
        fig = px.pie(df1,values = 'number', names= 'class', title = 'success vs failure')
        return fig
        
        
        # return the outcomes piechart for a selected site



# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), 
              Input(component_id='payload-slider', component_property='value')
              ])
def get_scatter_chart(entered_site, range):
    #print(spacex_df.head())
    filtered_df = spacex_df
    print(range)
    #print(filtered_df.head())
    if entered_site == 'ALL':
        #print(filtered_df.head())
        #df3 = filtered_df[filtered_df['Payload Mass (kg)'< range[1]]]
        fig1 = px.scatter(filtered_df, x= "Payload Mass (kg)", y="class", color = 'Booster Version Category',
         title='Payload vs Mission outcome',range_x = range) 
        return fig1
    else:
        df2 = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig1 = px.scatter(df2, x= "Payload Mass (kg)", y="class", color = 'Booster Version Category',
         title='Payload vs Mission outcome',range_x = range) 
        return fig1

        
        
        
        # return the outcomes scatterchart for a selected site




# Run the app
if __name__ == '__main__':
    app.run_server()
