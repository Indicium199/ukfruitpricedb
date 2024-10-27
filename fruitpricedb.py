# Import packages
import sys
print(sys.path)

from dash import Dash, dcc, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np  # Import NumPy
import plotly.io as pio

pio.renderers.default = 'notebook_connected'  # or 'notebook_connected'

# Load the dataset directly from the website
url = 'https://assets.publishing.service.gov.uk/media/67121ccf386bf0964853d787/fruitvegprices-20241028.csv'
col_names = ['category', 'item', 'variety', 'date', 'price', 'unit']
df = pd.read_csv(url, sep=',', usecols=col_names)

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
        yaxis_title="Price in £",
        xaxis_title="Date",
        legend_title_text='Berry Variety'
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)


