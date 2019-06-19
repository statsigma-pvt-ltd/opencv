# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 18:41:12 2019

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
def nodes_edges_graph(input1):
    global i
    consumer_key = 'GLAoztDURqBu9OMbCWxuspsin'
    consumer_secret = 'z3FW6l5zdlnZV6zVOVGJPfyH12aODRcU5VhSJCdWvWeFAv8p4O'
    access_token = '1118074022309183488-qQVBylY6qfUj3ygNKpWdswOPbfw35r'
    access_token_secret = 'RiwVxQnbtw18MwO5MEx4nr6Ktz5g5YJOKpy2RRgvDDPbj'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
    user_node=[]
    friend_node=[]
    main_person=input1
    user = api.get_user(main_person)
    main_person_id=user.id
    no_of_hops=3
    # no_of_hops=no_of_h
    try:
        ids1=[]
        for items in tweepy.Cursor(api.friends_ids, screen_name=main_person).items(2):
            user_node.append(main_person_id)
            friend_node.append(items)
            ids1.append(items)
        #print(ids1)
        try:
            ids_old_hops=[]
            id_hops=[]
            for hops in range(no_of_hops):
                if hops==0:
                    id_hops=ids1
                else:
                    id_hops=ids_old_hops
                ids_old_hops=[]
                def carbike(i):
                    for items in tweepy.Cursor(api.friends_ids,user_id=id_hops[i]).items(2):
                        user_node.append(id_hops[i])
                        friend_node.append(items)
                        ids_old_hops.append(items)
                #print(id_old_hops)
                print(hops)
                for i in range(len(id_hops)):
                    carbike(i)
        except tweepy.TweepError as e:
                if str(e)=='Not authorized.':
                    #print('akhil')
                    i=i+1
                    carbike(i)
        user_node1=[]
        friend_node1=[]
        for ik in user_node:
                user = api.get_user(ik)
                user_node1.append(user.screen_name)
        for ik in friend_node:
                user = api.get_user(ik)
                friend_node1.append(user.screen_name)
    except tweepy.TweepError as e:
        if str(e)=='Not authorized.':
            print('the main person is protected')

    import csv
    with open("C:/Users/akhil/Downloads/nodes_finally156.txt", 'w') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerows(list(zip(user_node1, friend_node1)))
    G = nx.read_edgelist("C:/Users/akhil/Downloads/nodes_finally156.txt", create_using = nx.Graph())
    pos=nx.fruchterman_reingold_layout(G)
    Xn=[pos[k][0] for k in pos]
    Yn=[pos[k][1] for k in pos]
    labels=[k for k in pos]
    parts = community.best_partition(G)
    values = [parts.get(node) for node in G.nodes()]
    sizes=[x[1]*10 for x in G.degree()]
    trace_nodes=dict(type='scatter',
                 x=Xn, 
                 y=Yn,
                 mode='markers',
                 marker=dict(size=sizes, color=values),
                 text=labels,
                 hoverinfo='text')
    Xe=[]
    Ye=[]
    for e in G.edges():
        Xe.extend([pos[e[0]][0], pos[e[1]][0], None])
        Ye.extend([pos[e[0]][1], pos[e[1]][1], None])
    trace_edges=dict(type='scatter',
                 mode='lines',
                 x=Xe,
                 y=Ye,
                 line=dict(width=1, color='rgb(25,25,25)'),
                 hoverinfo='none' 
                )
    axis=dict(showline=False, # hide axis line, grid, ticklabels and  title
          zeroline=False,
          showgrid=False,
          showticklabels=False,
          title='' 
          )
    layout=dict(title= 'My Graph',  
            font= dict(family='Balto'),
            width=1800,
            height=1000,
            autosize=False,
            showlegend=False,
            xaxis=axis,
            yaxis=axis,
    hovermode='closest',
    plot_bgcolor='#efecea', #set background color            
    )
    fig= dict(data=[trace_edges, trace_nodes], layout=layout)
    return(fig)