# Import required packages
import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash import Input, Output, callback

# Read the airline data into pandas dataframe
airline_data =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv', 
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str})
spacex_df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Randomly sample 500 data points. Setting the random state to be 42 so that we get same result.
data = airline_data.sample(n=500, random_state=42)
def gg(entered_site):
    if entered_site == 'ALL':
        b = spacex_df.groupby('Launch Site')['class'].mean()
        return b
    else :
        a = spacex_df[spacex_df['Launch Site']==entered_site]
        b = a.groupby('Launch Site')['class'].mean()
        return b

def fig1(a,entered_site):
    if entered_site == 'ALL':
        fig = px.pie(a, values=a.values, names=a.index, title='Distance group proportion by flights')
        return fig
    else :
        b = a.values
        fig = px.pie(a, values=[b[0],1-b[0]], names=[1,0], title='Distance group proportion by flights')
        return fig
 

# Pie Chart Creation
def fig2(entered_site,slider_range):
    low = slider_range[0]
    high = slider_range[1]
    b = spacex_df[spacex_df['Payload Mass (kg)']>low]
    b = b[b['Payload Mass (kg)']<high]
    if entered_site == 'ALL':
        fig1 = px.scatter(b,x='Payload Mass (kg)',y='class',color='Booster Version Category')
        return fig1
    else :
        a = b[b['Launch Site']==entered_site]
        fig1 = px.scatter(a,x='Payload Mass (kg)',y='class',color='Booster Version Category')
        return fig1

# Create a dash application
app = dash.Dash(__name__)

# Get the layout of the application and adjust it.
# Create an outer division using html.Div and add title to the dashboard using html.H1 component
# Add description about the graph using HTML P (paragraph) component
# Finally, add graph component.
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
                                html.P('Success rate check for every Launch Site', style={'textAlign':'center', 'color': '#F57241'}),
                                dcc.Dropdown(id='site-dropdown',
                                                options =[
                                                    {'label': 'All Sites', 'value': 'ALL'},
                                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                                ],
                                                value='ALL',
                                                placeholder = 'Select a Launch Site here',
                                                searchable = True),
                                html.Br(),
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),
                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                    min = 0, max = 10000, step = 1000,
                                                    value=[min_payload,max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),

                                               
                    ])


@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    a = gg(entered_site)
    fig = fig1(a,entered_site)
    return fig



@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart(entered_site,slider_range):
    fig = fig2(entered_site,slider_range)
    return fig

    


# Run the application                   
if __name__ == '__main__':
    app.run_server()