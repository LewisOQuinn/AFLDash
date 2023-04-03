import requests
import pandas as pd
import dash
from dash import dash_table
from dash import html
from dash import dcc
from bs4 import BeautifulSoup

# Download website
url = 'https://www.afl.com.au/'
data = requests.get(url).text

# Create BeautifulSoup object
soup = BeautifulSoup(data, 'html.parser')

# Extract ladder table
table = soup.find('table', {'class': 'sidebar-ladder__table'})

# Use Pandas to read the table into a DataFrame
df = pd.read_html(str(table))[0]

# Keep only the 3rd and 5th columns
df = df.iloc[:, [2, 4]]

# Rename columns
df.columns = ['Team', 'Points']

# Remove the last row with NaN values
df.dropna(inplace=True)

# Create a dictionary mapping each team to its respective custom ladder
custom_ladder_dict = {
    'Lew': ['Brisbane Lions', 'Sydney Swans', 'Essendon', 'Gold Coast Suns', 'St Kilda', 'North Melbourne'],
    'Tom': ['Melbourne', 'Carlton', 'Port Adelaide', 'Western Bulldogs', 'GWS Giants', 'Adelaide Crows'],
    'JBFM': ['Geelong Cats', 'Fremantle', 'Collingwood', 'Richmond', 'Hawthorn', 'West Coast Eagles']
}

# Create an empty DataFrame to store the custom ladder
custom_ladder = pd.DataFrame(columns=['Rank', 'Team', 'Points'])

# Iterate over the custom_ladder_dict to populate the custom_ladder DataFrame
rank = 1
for custom_team, teams in custom_ladder_dict.items():
    points_sum = df.loc[df['Team'].isin(teams), 'Points'].sum()
    custom_ladder = pd.concat([custom_ladder, pd.DataFrame({'Rank': [rank], 'Team': [custom_team], 'Points': [points_sum]})])
    rank += 1

# Initialize the app
app = dash.Dash(__name__)

# Set the app layout
app.layout = html.Div(children=[
    html.H1(children='3 year AFL Bet - $2000 Prize', style={'text-align': 'center', 'fontWeight': 'bold'}),
    
    dash_table.DataTable(
        id='custom-ladder',
        columns=[{"name": i, "id": i} for i in custom_ladder.columns],
        data=custom_ladder.to_dict('records'),
        style_as_list_view=True,
        style_header={'backgroundColor': 'rgb(237, 23, 31)', 'color': 'white', 'fontWeight': 'bold'},
        style_cell={'backgroundColor': 'rgb(32, 54, 105)', 'color': 'white', 'textAlign': 'center', 'fontSize': '20px'}
    ),
    
    html.Br(), # Add two lines of blank space here
    
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        style_as_list_view=True,
        style_header={'backgroundColor': 'rgb(237, 23, 31)', 'color': 'white', 'fontWeight': 'bold'},
        style_cell={'backgroundColor': 'rgb(32, 54, 105)', 'color': 'white', 'textAlign': 'center', 'fontSize': '20px'}
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
