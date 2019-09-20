#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 15:27:48 2019

@author: moi
"""
#Import des librairies
import dash
import dash_table
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import requests
from pandas.io.json import json_normalize
import pandas as pd
from sqlalchemy import create_engine
import os,configparser

config = configparser.ConfigParser()
config.read_file(open(os.path.expanduser("~/.datalab.cnf")))
print(config.sections())

#Mise en place des coordonnées de la base et chargement des données
BDD = "Media_alex_cyp"

engine = create_engine("mysql://%s:%s@%s/%s" % (config['myBDD']['user'], config['myBDD']['password'], config['myBDD']['host'], BDD))

df = pd.read_sql(sql='SELECT * FROM Main_media', con=engine)
#Nettoyage des données
df.rename({'FilmRef':'Ref','Film_Nom':'Titre','Film_Ann':'Année','FR_nom':'Réalisateur','FP_nom':'Producteur', 'FS_nom':'Studio'}, axis=1, inplace=True)
if (True):
    df.replace('S:\s*', '', inplace=True, regex=True)
    df.replace('SU:\s*', '', inplace=True, regex=True)
    df.replace('PU:\s*', '', inplace=True, regex=True)
    df.replace('PN:\s*', '', inplace=True, regex=True)
    df.replace('D:\s*', '', inplace=True, regex=True)
    df.replace('P:\s*', '', inplace=True, regex=True)
    df.replace('St:\s*', '', inplace=True, regex=True)

# Création de la disposition de l'application
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([   
    
# Titre de l'application
    html.H1(
        children="Films de la médiathèque",
        style={'textAlign': 'center'}
    ),      

# Slider années
     html.Br(),
     html.Hr(),
     html.Label('Choix de la période', style={'fontSize': 25, 'marginTop': 40, 'textAlign':'center'}),
     dcc.RangeSlider(
        id='input-years',
        min=df['Année'].min(),
        max=df['Année'].max(),
        value=[df['Année'].min(), df['Année'].max()],
        
        #Création des marqueurs du slider
        marks={
        1891: {'label': '1891','style': {'color': 'black'}},
        1900: {'label': '1900','style': {'color': 'black'}},
        1910: {'label': '1910','style': {'color': 'black'}},
        1920: {'label': '1920','style': {'color': 'black'}},
        1930: {'label': '1930','style': {'color': 'black'}},
        1940: {'label': '1940','style': {'color': 'black'}},
        1950: {'label': '1950','style': {'color': 'black'}},
        1960: {'label': '1960','style': {'color': 'black'}},
        1970: {'label': '1970','style': {'color': 'black'}},
        1980: {'label': '1980','style': {'color': 'black'}},
        1990: {'label': '1990','style': {'color': 'black'}},
        2000: {'label': '2000','style': {'color': 'black'}}
        },
        
        step=None
        ),
             
    html.Br(),
    html.Br(),
    html.Div(id='output-years'),
    
# Affichage de la table de recherche
    html.Br(),
    html.Hr(),
    html.Label('Table de recherche', style={'fontSize': 25, 'marginTop': 40}
    ),
    
    html.Br(),
    html.Hr(),
    html.Div(id='output-table'),
    
                     
            
])
# Mise en place de l'interactivité
    #Slider années modifiable
@app.callback(Output('output-years', 'children'), # LIRE : "ma sortie à modifier est 'output-years' (identifiant de la 'Div html') et concerne la propriété 'children'
              [Input('input-years', 'value')]) # LIRE : "mon entrée à utiliser est 'input-years' (identifiant du SliderRange) et concerne la propriété 'value'
def update_years(input):
    return u'Période sélectionnée : {}'.format(input)   

# Table dynamique
@app.callback(Output('output-table', 'children'),
              [Input('input-years', 'value')])
def update_table(years):
    # Création d'une nouvelle dataframe (dff) qui est la mise à jour de la dataframe initiale (df) selon les paramètres utilisateurs
    dff = df[(df['Année'] >= years[0]) & (df['Année'] <= years[1])]
    table = html.Div([
            dash_table.DataTable(
                data=dff.to_dict('rows'),
                columns=[{'name': i, 'id': i} for i in dff.columns],
                editable=True,
                filtering=False,
                sorting=True,
                sorting_type="multi",
                row_selectable="multi",
                row_deletable=False,
                pagination_mode="fe",
                pagination_settings={
                        "current_page": 0,
                        "page_size": 20}
                )
            ])
    return table


#Lancement de l'application
if __name__ == '__main__':
    app.run_server(debug=True)
