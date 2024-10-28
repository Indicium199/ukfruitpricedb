# Import libraries & components for Dash application
from dash import Dash, dcc, Output, Input  # Core components & callback utilities
import dash_bootstrap_components as dbc  # Bootstrap components for styling
import plotly.express as px  # Plotly Express for easy plotting
import pandas as pd  # Pandas for data manipulation
import numpy as np  # Import NumPy
import plotly.io as pio  # Plotly IO to configure rendering settings

# Set the default renderer for Plotly to 'notebook_connected' 
pio.renderers.default = 'notebook_connected'  

# Load the dataset directly from the website
url = 'https://assets.publishing.service.gov.uk/media/67121ccf386bf0964853d787/fruitvegprices-20241028.csv'
col_names = ['category', 'item', 'variety', 'date', 'price', 'unit']  # Specify the column names to be used from the CSV file
df = pd.read_csv(url, sep=',', usecols=col_names)  # Read the CSV file into a Pandas DataFrame, using only the specified columns

# Convert columns to appropriate data types
df['category'] = df['category'].astype('category')
df['variety'] = df['variety'].astype('category')
df['date'] = pd.to_datetime(df['date'])

# Create a DataFrame for apples and another for berries
applesdf = df[df['item'].str.contains('apple', case=False, na=False)].copy()  # Filtering apples
dfBerry = df[df['item'].isin(['blackberries', 'raspberries', 'blueberries', 'strawberries', 'cherries', 'gooseberries', 'currants'])].copy()  # Filtering berries

# Create 'Berry Variety' column using .loc[] to avoid the SettingWithCopyWarning
dfBerry['berryVariety'] = dfBerry['variety'].str.replace('_', ' ').str.capitalize()

# Modify the berry variety names specifically for currants and cherries
# Add a 'berryVariety' column to handle display names
dfBerry['berryVariety'] = dfBerry['variety'].str.replace('_', ' ').str.capitalize()

# Custom replacements for currants and cherries
dfBerry.loc[(dfBerry['variety'].str.contains('red', case=False)) & (dfBerry['item'] == 'currants'), 'berryVariety'] = 'Red Currants'
dfBerry.loc[(dfBerry['variety'].str.contains('black', case=False)) & (dfBerry['item'] == 'currants'), 'berryVariety'] = 'Black Currants'
dfBerry.loc[dfBerry['item'] == 'cherries', 'berryVariety'] = 'Cherries'  # Explicitly set to "Cherries"

# Pears DataFrame
dfPears = df[df['item'].str.contains('pear', case=False, na=False)].copy()

# Plums DataFrame
dfPlums = df[df['item'].str.contains('plum', case=False, na=False)].copy()

# Instantiate the App
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# App Layout
app.layout = dbc.Container([
    dcc.Markdown("### The Price of UK Homegrown Apples and Berries Over Time"),
    
    # Apple Section
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='appleVariety',
                options=[{'label': x, 'value': x} for x in applesdf.variety.unique()],
                placeholder="Select an Apple Variety",
                multi=True,
                value=[applesdf.variety.unique()[0]]  # Default value
            )
        ], width=8)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='figure1')
        ], width=8)
    ]),

    # Berry Section
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='berryVariety',
                options=[{'label': x, 'value': x} for x in dfBerry.berryVariety.unique()],
                placeholder="Select a Berry Variety",
                multi=True,
                value=[dfBerry.berryVariety.unique()[0]]  # Default value
            )
        ], width=8)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='figure2')
        ], width=8)
    ]),

# Pear Section
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='pearVariety',
                options=[{'label': x, 'value': x} for x in dfPears['variety'].unique()],
                placeholder="Select a Pear Variety",
                multi=True,
                value=[dfPears['variety'].unique()[0]]  # Default selection
            )
        ], width=8)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='figure3')
        ], width=8)
    ]),
# Plum Section
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='plumVariety',
                options=[{'label': x, 'value': x} for x in dfPlums['variety'].unique()],
                placeholder="Select a Plum Variety",
                multi=True,
                value=[dfPlums['variety'].unique()[0]]
            )
        ], width=8)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='figure4')
        ], width=8)
    ])
])


# Configure Callbacks
@app.callback(
    Output('figure1', 'figure'),
    Input('appleVariety', 'value')
)
def update_apple_graph(apples_selected):
    df_filtered = applesdf[applesdf.variety.isin(apples_selected)]
    fig = px.line(df_filtered, x='date', y='price', color='variety')

    fig.update_layout(
        title="🍎 UK Homegrown Apple Price Trends Over Time",  # Add title to the chart
        yaxis_title="Price in £",
        xaxis_title="Date",
        legend_title_text='Apple Variety'
    )

    return fig

@app.callback(
    Output('figure2', 'figure'),
    Input('berryVariety', 'value')
)
def update_berry_graph(berry_selected):
    df_filtered = dfBerry[dfBerry.berryVariety.isin(berry_selected)]
    fig = px.line(df_filtered, x='date', y='price', color='variety')

    fig.update_layout(
        title="🍒 UK Homegrown Berry Price Trends Over Time",
        yaxis_title="Price in £",
        xaxis_title="Date",
        legend_title_text='Berry Variety'
    )

    return fig

@app.callback(
    Output('figure3', 'figure'),
    Input('pearVariety', 'value')
)
def update_pear_graph(pears_selected):
    df_filtered = dfPears[dfPears['variety'].isin(pears_selected)]
    fig = px.line(df_filtered, x='date', y='price', color='variety')
    fig.update_layout(
        title="🍐 UK Homegrown Pear Price Trends Over Time",
        yaxis_title="Price in £",
        xaxis_title="Date",
        legend_title_text='Pear Variety'
    )
    return fig

@app.callback(
    Output('figure4', 'figure'),
    Input('plumVariety', 'value')
)
def update_plum_graph(plums_selected):
    df_filtered = dfPlums[dfPlums['variety'].isin(plums_selected)]
    fig = px.line(df_filtered, x='date', y='price', color='variety')
    fig.update_layout(
        title="🍑 UK Homegrown Plum Price Trends Over Time",
        yaxis_title="Price in £",
        xaxis_title="Date",
        legend_title_text='Plum Variety'
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)


