import pandas as pd
import numpy as np
from pandas import Series, DataFrame
from pandas.core.apply import frame_apply
import glob
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
from natsort import natsorted, ns

app = Dash(__name__)

__name__ = "__main__"
path = "/Asteroids"

if __name__ == "__main__":
    asteroids = []
    file_list = glob.glob('*.csv')
    file_list = natsorted(file_list, key=lambda y: y.lower())
    for one_filename in file_list:
        print(f'Loading {one_filename}')
        new_df = pd.read_csv(one_filename)
        new_df = new_df.replace(0, np.nan)
        new_df = new_df.dropna()
        asteroids.append(new_df)
    def timeInterval(bitDepth,rate):
        time = []
        depth = bitDepth.diff(periods=1)
        depth = depth.replace(np.nan,0)
        time = depth / rate
        time = np.cumsum(time, axis=0)
        time = pd.Series(time,name='TIME')
        time = time.to_frame()
        return time
    res = []
    for asteroid in asteroids:
        time = timeInterval(asteroid.BIT_DEPTH, asteroid.RATE_OF_PENETRATION)
        asteroid = pd.concat([asteroid, time], axis=1)
        res.append(asteroid)
    asteroids = res

    def addCost(ast):
        conditions = [
            (ast['DRILL_BIT_NAME'] == 'Buzz Drilldrin'),
            (ast['DRILL_BIT_NAME'] == 'AstroBit'),
            (ast['DRILL_BIT_NAME'] == 'Apollo'),
            (ast['DRILL_BIT_NAME'] == 'ChallengDriller')]
        values = [5000,3000,1000,10000]
        ast['COST'] = np.select(conditions,values)
    for asteroid in asteroids:
        ast = asteroid
        addCost(ast)

    totalCost = []
    def cost(ast):
        conditions = [
            (ast['DRILL_BIT_NAME'] == 'Buzz Drilldrin'),
            (ast['DRILL_BIT_NAME'] == 'AstroBit'),
            (ast['DRILL_BIT_NAME'] == 'Apollo'),
            (ast['DRILL_BIT_NAME'] == 'ChallengDriller')]
        cost_per_ft = [1.5,1,4,0]
        cost_per_hr = [0,1500,2500,0]
        depth = ast.BIT_DEPTH
        hr = ast.TIME
        cRun = ast.COST
        cost = cRun + (depth * np.select(conditions,cost_per_ft) +
                        (hr * np.select(conditions,cost_per_hr)))
        totalCost = pd.Series(cost,name='TOTAL_COST')
        totalCost = totalCost.to_frame()
        return totalCost

    final=[]
    for asteroid in asteroids:
        fc = cost(asteroid)
        asteroid = pd.concat([asteroid, fc], axis=1)
        final.append(asteroid)
    asteroids = final
    asteroids


print(asteroids[0])

app.layout = html.Div(children=
    [html.Div([
        html.H4('Asteroid Data Analysis'),
        dcc.Graph(id="graph"),
        dcc.Checklist(
            options=["BIT_DEPTH", "RATE_OF_PENETRATION", "WEIGHT_ON_BIT","DRILL_BIT_ID","DRILL_BIT_NAME", "DIFFERENTIAL_PRESSURE"],
            value=["BIT_DEPTH", "RATE_OF_PENETRATION"],
            inline=True,
            id='checklist'
        ),
        dcc.RadioItems(
            ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19'],
                    '1',
                    id='asteroidid',
                    inline=True
        )
    ]),
    html.Div(
        dcc.Graph(figure={
        'data': [
            {'x': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19], 'y': [233971.909877,609026.922266,488656.763513,569287.259355,133697.196617,235712.394166,198644.069194,
                           79329.885,214638.025843,708214.839708,511026.119754,854611.416622,390798.382339,43220.184909,
                           48305.45,675429.316055,266143.44131,246137.065339,321643.911581], 'type': 'bar', 'name': 'Total Cost vs. Asteroid'}
            #{'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'MontrÃ©al'},
        ],
        'layout': {
            'title': 'Dash Data Visualization'
        }
    }),
        
    )

],
    
)



@app.callback(
    Output("graph", "figure"), 
    Input("checklist", "value"),
    Input('asteroidid', 'value'))
def update_line_chart(column, asteroid_name):
    df = asteroids[int(asteroid_name)]
    fig = px.line(df, 
        x="TIME", y=column)
    fig.update_layout(paper_bgcolor="#5BA5BD")
    fig.update_layout(legend_bgcolor='#A5C9D5')
    fig.add_layout_image(
    dict(
        source="https://raw.githubusercontent.com/ClassicSours/TheInterstellarAsteroidRush/main/logo.png",
        xref="paper", yref="paper",
        x=1, y=1.05,
        sizex=0.2, sizey=0.2,
        xanchor="right", yanchor="bottom"
    ) 
)  
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)  