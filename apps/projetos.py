import dash
import dash_core_components as dcc
import dash_html_components as html
import matplotlib.pyplot as plt
from dash.dependencies import Input, Output
import plotly.offline as py
from plotly.graph_objs import *   
import plotly.graph_objs as go 
import dash_bootstrap_components as dbc
import folium  
from folium import IFrame, FeatureGroup 
import numpy as np
from PIL import Image
import json
import os  
import base64 
import glob  
import pandas as pd 
from folium.plugins import MarkerCluster   

### Data
import pandas as pd
import pickle
### Graphing
import plotly.graph_objects as go
### Dash
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State
## Navbar
from . import navbar
from app import app

nav = navbar.Navbar() 
  

centros = ['Todos os Centros','CCS','CEAR','CCEN','CT','CCM','CBIOTEC','CTDR','CCHLA','CCTA','CCHSA','CCSA','CI','CCAE','CCJ','CCA','CE']
anos = ['Todos os Anos', 2017,2018,2019]


card_content = [
    dbc.CardHeader("Opções de filtro",style={'font-size':24, 'textAlign':'center'}),
    dbc.CardBody(
        [


    html.H4("Escolha o ano desejado:", style={'font-size':19}),
        dcc.Dropdown(
        id = 'anos_projetos',
        placeholder="Selecione o(s) ano(s)",
        options=[
            {'label': j, 'value': j} for j in anos  
        ],
        value=['2019'],   
        multi=True,
    searchable=False
    ),


    html.Div(html.Br()),

        html.H4("Escolha o centro desejado:", style={'font-size':19}),
        dcc.Dropdown(
        id = 'centros_projetos',
        placeholder="Selecione o(s) centro(s)",  
        options=[
            {'label': j, 'value': j} for j in centros  
        ],
        value=['CEAR'],   
        multi=True,
    searchable=False
    ),
    

html.Br(),
html.H4("Digite a palavra-chave do projeto desejado:", style={'font-size':19}),
dcc.Input(
        id='entrada_titulo_projetos',
        placeholder='Escreva o título do projeto',
        type='text',
        value = '',
        style={'margin-bottom':'10px'}
),

   
html.Button('Pesquisar', id='btn-nclicks-1', n_clicks=0),

html.Div(html.Br()),
html.H4("Escolha um projeto para ver o resumo:", style={'font-size':19}),
        dbc.Select(
        id = 'projetos_projetos',  
        options=[
            {'label': j, 'value': j} for j in []  
        ],
        value=[''],   
        ),




        ]
    ),
]

jumbotron = dbc.Card(card_content,  outline=True)

card_content_3 = [
    dbc.CardHeader("Resumo do projeto",style={'font-size':24, 'textAlign':'center'}),
    dbc.CardBody(
        [
        dcc.Textarea(
        id='textarea_example',
        readOnly=True,
        value='',
        style={'display':'block', 'max-width': '100%', 'margin-left': 'auto', 'margin-right': 'auto','width':'90%','height':'580px','textAlign':'justify', 'font-size':20},
    ),
    #html.Div(id='textarea_example_output', style={'whiteSpace': 'pre-line'})
        ]
    ),
]

jumbotron_2 = dbc.Card(card_content_3,  outline=True)

body_1 =html.Div([  


        dbc.Row(
           [
               dbc.Col(
                  [

                jumbotron,



                   ], md=4

               ),
              dbc.Col([
              jumbotron_2 

                    ], md=8 ),

                ],no_gutters=True
            ),
              
])

modal_6 = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader("ERROR"),
                dbc.ModalBody("Escolha pelo menos um ano como parâmetro de entrada de anos"),
                dbc.ModalFooter(
                dbc.Button("Close", id="close_10", className="ml-auto")
                ),
            ],
            id="modal_10",
        ),
    ]
)

modal_7 = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader("ERROR"),
                dbc.ModalBody("Escolha pelo menos um centro como parâmetro de entrada de centros"),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close_7", className="ml-auto")
                ),
            ],
            id="modal_7",
        ),
    ]
)

layout = html.Div([
  nav,
  body_1,
  modal_6,
  modal_7
])

@app.callback(
	[Output("centros_projetos", "value"),Output("modal_7", "is_open")],
	[Input("anos_projetos", "value"), Input("close_7", "n_clicks")],
	[State("centros_projetos", "value"),State("modal_7", "is_open")],
)
def limite_centros(ano,n_rel, centro,is_open_rel):
	if 'Todos os Centros' in centro:
		return [['CCHLA','CCS','CCA','CT','CCEN','CCTA','CCAE','CEAR','CCM','CTDR','CE','CBIOTEC','CCHSA','CCSA','CI','CCJ'],is_open_rel]
	if len(centro) == 0:
		return [['CEAR'], not is_open_rel]
	else:
		if n_rel:
			if is_open_rel == True:
				return [centro, not is_open_rel]
			return [centro, is_open_rel]
		return [centro, is_open_rel]

@app.callback(
	[Output("anos_projetos", "value"),Output("modal_10", "is_open")],
	[Input("centros_projetos", "value"),Input("close_10", "n_clicks")],
	[State("anos_projetos", "value"),State("modal_10", "is_open")],
)

def flag(centro,n_rel, ano, is_open_rel):
	if 'Todos os Anos' in ano:
		return [[2017,2018,2019],is_open_rel]
	if len(ano) == 0:
		return [[2019], not is_open_rel]
	else:
		if n_rel:
			if is_open_rel == True:
				return [ano, not is_open_rel]
			return [ano, is_open_rel]
		return [ano, is_open_rel]


	
@app.callback(
    Output("textarea_example", "value"),
    [Input("projetos_projetos", "value"),Input('btn-nclicks-1', 'n_clicks')]
)
def atualiza_resumo(titulo,n):
	print(titulo)
	if titulo == ['']:
		#print('cheguei no test')
		return ''

	data_frame = pd.read_csv("apps/Apoio/definitivo2.csv", encoding='utf-8-sig') #trocar o arquivo csv

	#data_frame = data_frame.drop_duplicates(subset=['curso_nome'], keep='last')  #apagar essa linha foi so pra diminuir enquanto eu testava 

	data_frame = data_frame[data_frame['titulo']==titulo] #trocar --curso_nome-- para --titulo-- com o df certo
	print(data_frame['resumo'])
	return data_frame['resumo']  #trocar --plano_trabalho_objetivo-- para --resumo-- com o df certo


###improviso -p/ reunião prac
@app.callback(
    Output('projetos_projetos', 'value'),
    [Input('anos_projetos', 'value'),Input('centros_projetos', 'value'),Input('entrada_titulo_projetos', 'value'),Input('btn-nclicks-1', 'n_clicks')]
)
def update_output(anos,centros,titulo,btn1):
    flag = []
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'btn-nclicks-1' in changed_id:
        print(titulo)
        data_frame = pd.read_csv("apps/Apoio/definitivo2.csv", encoding='utf-8-sig') #trocar o arquivo csv
        #data_frame = data_frame.drop_duplicates(subset=['curso_nome'], keep='last')  #apagar essa linha foi so pra diminuir enquanto eu testava

        data_frame_flag = data_frame['ano'].isin(anos) #tirar o comentario quando tiver recebendo o df certo
        data_frame = data_frame[data_frame_flag]

        data_frame_flag = data_frame['unidade_proponente'].isin(centros) #tirar o comentario quando tiver recebendo o df certo
        data_frame = data_frame[data_frame_flag]

        pega_palavra = list(titulo.split(" ")) 

        lista_de_titulos = list(data_frame['titulo']) #trocar --curso_nome-- para --titulo-- com o df certo
        flag = list(lista_de_titulos)

        for x in pega_palavra:
            primeira = x.lower()
            for y in lista_de_titulos:
                segunda = y.lower()
                if primeira in segunda:
                    ok = ''
                else:
                    if y in flag:
                        flag.remove(y)
                    ok=''

        if(len(flag)<1):
            return ["SEM RESULTADOS PARA A PALAVRA-CHAVE"]
        else:
            return [{'label': j, 'value': j} for j in flag]       
###improviso

@app.callback(
    Output('projetos_projetos', 'options'),
    [Input('anos_projetos', 'value'),Input('centros_projetos', 'value'),Input('entrada_titulo_projetos', 'value'),Input('btn-nclicks-1', 'n_clicks')]
)
def update_output(anos,centros,titulo,btn1):
	flag = []
	changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
	if 'btn-nclicks-1' in changed_id:
		print(titulo)
		data_frame = pd.read_csv("apps/Apoio/definitivo2.csv", encoding='utf-8-sig') #trocar o arquivo csv
		#data_frame = data_frame.drop_duplicates(subset=['curso_nome'], keep='last')  #apagar essa linha foi so pra diminuir enquanto eu testava

		data_frame_flag = data_frame['ano'].isin(anos) #tirar o comentario quando tiver recebendo o df certo
		data_frame = data_frame[data_frame_flag]

		data_frame_flag = data_frame['unidade_proponente'].isin(centros) #tirar o comentario quando tiver recebendo o df certo
		data_frame = data_frame[data_frame_flag]

		pega_palavra = list(titulo.split(" ")) 

		lista_de_titulos = list(data_frame['titulo']) #trocar --curso_nome-- para --titulo-- com o df certo
		flag = list(lista_de_titulos)

		for x in pega_palavra:
			primeira = x.lower()
			for y in lista_de_titulos:
				segunda = y.lower()
				if primeira in segunda:
					ok = ''
				else:
					if y in flag:
						flag.remove(y)
					ok=''


		return [{'label': j, 'value': j} for j in flag]

		return [{'label': j, 'value': j} for j in flag]

		return [{'label': j, 'value': j} for j in flag_padrao]
	
	return []
