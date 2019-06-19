# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 18:41:16 2019

@author: akhil
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import tweepy
import re
import pickle
#from wordcloud import WordCloud, STOPWORDS
import plotly.graph_objs as go
import plotly.plotly as py
import networkx as nx
import community
import platform
import plotly.plotly as py
import plotly
from plotly.offline import download_plotlyjs, init_notebook_mode,  iplot, plot
init_notebook_mode(connected=True)
from twitter_nodes_edges import nodes_edges_graph

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Input(id='input-1-submit', type='text', value=' '),
    html.Button(id='submit-button', n_clicks=0, children='Submit'),
    html.Div([dcc.Graph(id='output-submit')])
])
@app.callback(Output('output-submit', 'figure'),
              [Input('submit-button', 'n_clicks')],
              [State('input-1-submit', 'value')])
def update_output(n_clicks, input1):
    fig123=nodes_edges_graph(input1)
    return fig123
    
    
    
    
if __name__ == '__main__':
    app.run_server()