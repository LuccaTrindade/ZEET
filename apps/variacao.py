import dash
import dash_core_components as dcc
import dash_html_components as html
import matplotlib.pyplot as plt
from dash.dependencies import Input, Output, State
import plotly.offline as py
from plotly.graph_objs import *   
import plotly.graph_objs as go 
import dash_bootstrap_components as dbc
import folium  
from folium import IFrame, FeatureGroup 

import re
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
from dash.dependencies import Output, Input
## Navbar
# from navbar import Navbar
from . import navbar
import base64
import io
from operator import itemgetter #Lembrar de Acrescentar
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from app import app
import unidecode as und

app.config.suppress_callback_exceptions = True  ## faz com que o app não mostre as execeções dash
####################
tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'font-size': '70%',
    'padding': '6px'
}

tab_style = { #Estilos das Tabs
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'font-size': '75%',
    'fontWeight': 'bold',
    'fontSize' : '13'
}
##################################

ListaCentros_variacao = ['Todos os centros', 'CCS -','CEAR -','CCEN -','CT -','CCM -','CBIOTEC -','CTDR -','CCHLA -','CCTA -','CCHSA -','CCSA -','CI -','CCAE -','CCJ -','CCA -','CE -']
Lista_Centros = ['CCS','CEAR','CCEN','CT','CCM','CBIOTEC','CTDR','CCHLA','CCTA','CCHSA','CCSA','CI','CCAE','CCJ','CCA','CE']
anos = ['Todos os anos','2017','2018','2019','2020','2021','2022']
nav = navbar.Navbar()

## Secção que  mostra os dropdowns da página
card_content = [
    dbc.CardHeader("Entendendo o gráfico",style={'font-size':24, 'textAlign':'center'}),
    dbc.CardBody(
        [
            html.P(
                className="card-text",id='relatorio_estudo_vocabular',style={'text-align':'justify'}
            ),
        ]
    ),
]
jumbotron = dbc.Card(card_content,  outline=True)


## Card que contém os dropdowns da página, com as opções separadas por 'tabs'
card_content_2 = [
    dbc.CardHeader("Opções de Filtro",style={'font-size':24, 'textAlign':'center'}),
    dbc.CardBody(
        [

        dcc.Tabs(id='tab_escolha_grafico', value='variabilidade_vocabular',children=[
                 dcc.Tab(label= 'Variabilidade Vocabular', value='variabilidade_vocabular',children=[
                 	html.Div(html.Br()),
				        html.H4("Escolha os anos que deseja analisar:", style={'font-size':19}),
				        dcc.Dropdown(
				        id = 'dropdown_anos_variacao',  
				        options=[{'label': "Todos os anos", 'value': 'todos'},
				            {'label': "2017", 'value': anos[1]},
				            {'label': "2018", 'value': anos[2]},
				            {'label': "2019", 'value': anos[3]},
										{'label': "2020", 'value': anos[4]},
										{'label': "2021", 'value': anos[5]},
										{'label': "2022", 'value': anos[6]},
				        ],
				        value= None,   
				        multi=True,
				        placeholder = "Selecione os anos",
				    	searchable=False,
				        style={'margin-bottom':'10px'}
				        ),  

				        dcc.Checklist(
						options=[
						    {'label': 'Selecionar Todos os Anos', 'value': 'ta'}, #ta = todos os anos
						],
						id = 'checklist_anos_variacao',
						labelStyle={'display': 'none'}
						),
						html.Br(),
						  
				        html.H4("Escolha os centros desejados:", style={'font-size':19}),
				        dcc.Dropdown(
				        id = 'dropdown_centros_variacao', 
				         
				        options=[{'label': "Todos os Centros", 'value': 'todos'},
				                {'label': "CCS", 'value': ListaCentros_variacao[1]},
				                {'label': "CEAR", 'value': ListaCentros_variacao[2]},
				                {'label': "CCEN", 'value': ListaCentros_variacao[3]},
				                {'label': "CT", 'value': ListaCentros_variacao[4]},
				                {'label': "CCM", 'value': ListaCentros_variacao[5]},
				                {'label': "CBIOTEC", 'value': ListaCentros_variacao[6]},
				                {'label': "CTDR", 'value': ListaCentros_variacao[7]},
				                {'label': "CCHLA", 'value': ListaCentros_variacao[8]},
				                {'label': "CCTA", 'value': ListaCentros_variacao[9]},
				                {'label': "CCHSA", 'value': ListaCentros_variacao[10]},
				                {'label': "CCSA", 'value': ListaCentros_variacao[11]},
				                {'label': "CI", 'value': ListaCentros_variacao[12]},
				                {'label': "CCAE", 'value': ListaCentros_variacao[13]},
				                {'label': "CCJ", 'value': ListaCentros_variacao[14]},
				                {'label': "CCA", 'value': ListaCentros_variacao[15]},
				                {'label': "CE", 'value': ListaCentros_variacao[16]},
				            ], 
				        value=None,   
				        multi=True,
				        placeholder = "Selecione os centros",
				    	searchable=False,
				        style={'margin-bottom':'10px'}
				   

				    ),
				    dcc.Checklist(
				    options=[
				        {'label': 'Selecionar Todos os Centros', 'value': 'tc'}, #ta = todos os anos
				    ],
				    id = 'checklist_centros_variacao',
				    labelStyle={'display': 'none'}
					),
					html.Br(),
					html.H4("Escolha o campo desejado:", style={'font-size':19}),
				        dcc.Dropdown(
				        id = 'dropdown_modalidades_variacao', 
				         
				        options=[
				                {'label': "Resumo", 'value': "Resumo"},
				                {'label': "Justificativa", 'value': "Justificativa"},
				                {'label': "Metodologia", 'value': "Metodologia"},
				                {'label': "Objetivos", 'value': "Objetivos"},
				                {'label': "Fundamentação Teórica", 'value': "Fundamentacao"},
				            ], 
				        
				        value=None,   
				        multi=False,
				        placeholder = "Selecione a modalidade",
				    	searchable=False,
				        style={'margin-bottom':'10px'}
				   

				    ),  


				                 	], 



				                 	style=tab_style, selected_style=tab_selected_style),




                
                dcc.Tab(label= 'Análise Gramatical', value='analise_gramatical',children=[
                html.Div(html.Br()),
		                
		        #############################################



		        html.H4("Escolha as classes gramaticais que deseja analisar:", style={'font-size':18}),
		        dcc.Dropdown(
		        id = 'dropdown_classes_analise',  
		        options=[{'label': "Todos as classes", 'value': 'todos'},
		            {'label': "Substantivos", 'value': "Substantivos"},
		            {'label': "Adjetivos", 'value': "Adjetivos"},
		            {'label': "Verbos", 'value': "Verbos"},
		            

		                 
		        ],
		        value= None,   
		        multi=True,
		        placeholder = "Selecione as classes",
		    	searchable=False,
		        style={'margin-bottom':'10px'}
		   

		        ),  
		        dcc.Checklist(
				options=[
				    {'label': 'Selecionar Todas as classes', 'value': 'tc'}, #ta = todos os anos
				],
				id = 'checklist_classes_analise',
				labelStyle={'display': 'none'}
				),
				html.Br(),
				  
		        html.H4("Escolha os centros desejados:", style={'font-size':19}),
		        dcc.Dropdown(
		        id = 'dropdown_centros_analise', 
		         
		        options=[{'label': "Todos os Centros", 'value': 'todos'},
		                {'label': "CCS", 'value': ListaCentros_variacao[1]},
		                {'label': "CEAR", 'value': ListaCentros_variacao[2]},
		                {'label': "CCEN", 'value': ListaCentros_variacao[3]},
		                {'label': "CT", 'value': ListaCentros_variacao[4]},
		                {'label': "CCM", 'value': ListaCentros_variacao[5]},
		                {'label': "CBIOTEC", 'value': ListaCentros_variacao[6]},
		                {'label': "CTDR", 'value': ListaCentros_variacao[7]},
		                {'label': "CCHLA", 'value': ListaCentros_variacao[8]},
		                {'label': "CCTA", 'value': ListaCentros_variacao[9]},
		                {'label': "CCHSA", 'value': ListaCentros_variacao[10]},
		                {'label': "CCSA", 'value': ListaCentros_variacao[11]},
		                {'label': "CI", 'value': ListaCentros_variacao[12]},
		                {'label': "CCAE", 'value': ListaCentros_variacao[13]},
		                {'label': "CCJ", 'value': ListaCentros_variacao[14]},
		                {'label': "CCA", 'value': ListaCentros_variacao[15]},
		                {'label': "CE", 'value': ListaCentros_variacao[16]}, 

		            ], 
		        
		        value=None,   
		        multi=True,
		        placeholder = "Selecione os centros",
		    	searchable=False,
		        style={'margin-bottom':'10px'}
		   

		    ),
		    dcc.Checklist(
		    options=[
		        {'label': 'Selecionar Todos os Centros', 'value': 'tc'}, #ta = todos os anos
		    ],
		    id = 'checklist_centros_analise',
		    labelStyle={'display': 'none'}
			),
			html.Br(),
			html.H4("Escolha o campo desejado:", style={'font-size':19}),
		        dcc.Dropdown(
		        id = 'dropdown_modalidades_analise', 
		         
		        options=[
		                {'label': "Resumo", 'value': "Resumo"},
		                {'label': "Justificativa", 'value': "Justificativa"},
		                {'label': "Metodologia", 'value': "Metodologia"},
		                {'label': "Objetivos", 'value': "Objetivos"},
		                {'label': "Fundamentação Teórica", 'value': "Fundamentacao"},
		            ], 
		        
		        value=None,   
		        multi=False,
		        placeholder = "Selecione o campo",
		    	searchable=False,
		        style={'margin-bottom':'10px'}
		   

		    ),  



                ], style=tab_style, selected_style=tab_selected_style),  
                dcc.Tab(label= 'Nuvem de Palavras', value='nuvem_palavras',children=[
                		html.Div(html.Br()),
        
				        html.H4("Escolha os anos que deseja analisar:", style={'font-size':19}),
				        dcc.Dropdown(
				        id = 'dropdown_anos_nuvem',  
				        options=[{'label': "Todos os Anos", 'value': 'todos'},
				            {'label': "2017", 'value': anos[1]},
				            {'label': "2018", 'value': anos[2]},
				            {'label': "2019", 'value': anos[3]},
				            {'label': "2020", 'value': anos[4]},
										{'label': "2021", 'value': anos[5]},
										{'label': "2022", 'value': anos[6]},

				                 
				        ],
				        value= None,   
				        multi=True,
				        placeholder = "Selecione os anos",
				    	searchable=False,
				        style={'margin-bottom':'10px'}
				        ),
				        dcc.Checklist(
						options=[
						    {'label': 'Selecionar Todos os Anos', 'value': 'ta'}, #ta = todos os anos
						],
						id = 'checklist_anos_nuvem',
						labelStyle={'display': 'none'}
						),
						html.Br(),
				   
						  
				        html.H4("Escolha os centros desejados:", style={'font-size':19}),
				        dcc.Dropdown(
				        id = 'dropdown_centros_nuvem', 
				         
				        options=[{'label': "Todos os Centros", 'value': 'todos'},
				                {'label': "CCS", 'value': ListaCentros_variacao[1]},
				                {'label': "CEAR", 'value': ListaCentros_variacao[2]},
				                {'label': "CCEN", 'value': ListaCentros_variacao[3]},
				                {'label': "CT", 'value': ListaCentros_variacao[4]},
				                {'label': "CCM", 'value': ListaCentros_variacao[5]},
				                {'label': "CBIOTEC", 'value': ListaCentros_variacao[6]},
				                {'label': "CTDR", 'value': ListaCentros_variacao[7]},
				                {'label': "CCHLA", 'value': ListaCentros_variacao[8]},
				                {'label': "CCTA", 'value': ListaCentros_variacao[9]},
				                {'label': "CCHSA", 'value': ListaCentros_variacao[10]},
				                {'label': "CCSA", 'value': ListaCentros_variacao[11]},
				                {'label': "CI", 'value': ListaCentros_variacao[12]},
				                {'label': "CCAE", 'value': ListaCentros_variacao[13]},
				                {'label': "CCJ", 'value': ListaCentros_variacao[14]},
				                {'label': "CCA", 'value': ListaCentros_variacao[15]},
				                {'label': "CE", 'value': ListaCentros_variacao[16]},
				                


				            ], 
				        
				        value=None,   
				        multi=True,
				        placeholder = "Selecione o centro",
				    	searchable=False,
				        style={'margin-bottom':'10px'}
				   

				    ),
				    dcc.Checklist(
				    options=[
				        {'label': 'Selecionar Todos os Centros', 'value': 'tc'}, #ta = todos os anos
				    ],
				    id = 'checklist_centros_nuvem',
				    labelStyle={'display': 'none'}
					),
				    html.Br(),
				    html.H4("Escolha o campo desejado:", style={'font-size':19}),
				    dcc.Dropdown(
				        id = 'dropdown_modalidades_nuvem', 
				         
				        options=[
				                {'label': "Resumo", 'value': "Resumo"},
				                {'label': "Justificativa", 'value': "Justificativa"},
				                {'label': "Metodologia", 'value': "Metodologia"},
				                {'label': "Objetivos", 'value': "Objetivos"},
				                {'label': "Fundamentação Teórica", 'value': "Fundamentacao"},
				               
				            ], 
				        
				        value=None,   
				        multi=False,
				        placeholder = "Selecione a modalidade",
				    	searchable=False,
				        style={'margin-bottom':'10px'}
				   

				    ),
			
                ], style=tab_style, selected_style=tab_selected_style), 
		
		
		
                dcc.Tab(label= 'Contagem de Palavras', value='contagem_palavras',children=[
                html.Div(html.Br()),
				html.H4("Escolha os anos que deseja analisar:", style={'font-size':19}),
				dcc.Dropdown(
				id = 'dropdown_anos_contagem',  
				options=[{'label': "Todos os anos", 'value': 'todos'},
				    {'label': "2017", 'value': anos[1]},
				    {'label': "2018", 'value': anos[2]},
				    {'label': "2019", 'value': anos[3]},
						{'label': "2020", 'value': anos[4]},
						{'label': "2021", 'value': anos[5]},
						{'label': "2022", 'value': anos[6]},
	                 
				],
		        value= None,   
				multi=True,
		        placeholder = "Selecione os anos",
		    	searchable=False,
				style={'margin-bottom':'10px'}
                ),
				dcc.Checklist(
				    options=[
				        {'label': 'Selecionar Todos Anos', 'value': 'ta'}, #ta = todos os anos
				    ],
				    id = 'checklist_anos_contagem',
				    labelStyle={'display': 'none'}
					),
				html.Br(),  
		        html.H4("Escolha os centros desejados:", style={'font-size':19}),
		        dcc.Dropdown(
		        id = 'dropdown_centros_contagem', 
		         
		        options=[{'label': "Todos os Centros", 'value': 'todos'},
		                {'label': "CCS", 'value': Lista_Centros[0]},
		                {'label': "CEAR", 'value': Lista_Centros[1]},
		                {'label': "CCEN", 'value': Lista_Centros[2]},
		                {'label': "CT", 'value': Lista_Centros[3]},
		                {'label': "CCM", 'value': Lista_Centros[4]},
		                {'label': "CBIOTEC", 'value': Lista_Centros[5]},
		                {'label': "CTDR", 'value': Lista_Centros[6]},
		                {'label': "CCHLA", 'value': Lista_Centros[7]},
		                {'label': "CCTA", 'value': Lista_Centros[8]},
		                {'label': "CCHSA", 'value': Lista_Centros[9]},
		                {'label': "CCSA", 'value': Lista_Centros[10]},
		                {'label': "CI", 'value': Lista_Centros[11]},
		                {'label': "CCAE", 'value': Lista_Centros[12]},
		                {'label': "CCJ", 'value': Lista_Centros[13]},
		                {'label': "CCA", 'value': Lista_Centros[14]},
		                {'label': "CE", 'value': Lista_Centros[15]}, 
		                


		            ], 
		        
		        value=None,   
		        multi=True,
		        placeholder = "Selecione os centros",
		    	searchable=False,
		        style={'margin-bottom':'10px'}
		   

		    ),
		    dcc.Checklist(
		    options=[
		        {'label': 'Selecionar Todos os Centros', 'value': 'tc'}, #ta = todos os anos
		    ],
		    id = 'checklist_centros_contagem',
		    labelStyle={'display': 'none'}
			),
			html.Br(),
			html.H4("Digite a(s) palavra(s) que deseja contar\nseparadas por vírgula:", style={'font-size':19}),
                html.H4("Para plurais com o mesmo radical da palavra no singular exemplo 'pesquisa - pesquisas' deve ser considerada apenas a versão da palavra no singular, caso contrário o plural será contabilizado duas vezes", style={'font-size':13}),
                dcc.Input(
                    id='palavra_contagem',
                    placeholder='Escreva a(s) palavra(s)',
                    type='text',
                    value = '',
                    style={'margin-bottom':'10px'}
                ),
                
                        
            ], style=tab_style, selected_style=tab_selected_style),



                ]),

        
        ]
    ),
]

jumbotron_2 = dbc.Card(card_content_2,  outline=True)

#Local em que os gráficos são exibidos
card_content_3 = [
	############
    dbc.CardHeader(id='texto_grafico_nuvem',style={'font-size':24, 'textAlign':'center'}),
    ############
    dbc.CardBody(
        [
            #html.Div(id='grafico_variacao_vocabular',
            #style={'display':'block', 'max-width': '100%', 'margin-left': 'auto', 'margin-right': 'auto'}
            html.Div(id='grafico_variacao_vocabular'),
            html.Div(id='grafico_analise_gramatical'),
			html.Div(id='grafico_contagem_palavras'),
            html.Img(id='grafico_nuvem_palavras', style={'display':'block', 'max-width': '100%', 'margin-left': 'auto', 'margin-right': 'auto','width':'90%','height':'90%'})
            
            
        ]
    ),
]

jumbotron_3 = dbc.Card(card_content_3,  outline=True)

body_1 =html.Div([  

    

        dbc.Row(
           [
               dbc.Col(
                  [jumbotron_2,
                        jumbotron]

        , md=4

               ),
              dbc.Col([
						jumbotron_3
                #html.Iframe(id='mapa', srcDoc=open('apps/Apoio/venn.svg', 'r').read(),width='100%',height='500px'),  

                    ], md=8 ),

                ],no_gutters=True
            ),
              
])


#esses modais abaixo são referentes a erros que podem ocorrer de acordo com a seleção de parâmetros (que não existe até agora nessa na página variação, mas caso precisem existir, a sua formatação já está pronta)
modal = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader("ERROR"),
                dbc.ModalBody("Escolha pelo menos um centro como parâmetro de entrada de centros"),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close", className="ml-auto")
                ),
            ],
            id="modal",
        ),
    ]
)

modal2 = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader("ERROR"),
                dbc.ModalBody("Escolha pelo menos dois anos como parâmetro de entrada de anos"),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close_2", className="ml-auto")
                ),
            ],
            id="modal",
        ),
    ]
)


# layout da página
layout = html.Div([
	nav,
	body_1,
	modal,
	modal2
])


##Abaixo temos o trecho referente a interatividade do site
@app.callback(
	Output("grafico_variacao_vocabular", "style"),
	[Input("tab_escolha_grafico","value")],
)
def update_layout_docentes(abas):
	print(abas,flush=True)
	if abas != 'variabilidade_vocabular':
		return {'display':'none', 'max-width': '100%', 'margin-left': 'auto', 'margin-right': 'auto'}
		
	else:
		return {'display':'block', 'max-width': '100%', 'margin-left': 'auto', 'margin-right': 'auto'}


@app.callback(
	Output("grafico_analise_gramatical", "style"),
	[Input("tab_escolha_grafico","value")],
)
def update_layout_docentes(abas):
	print(abas,flush=True)
	if abas != 'analise_gramatical':
		return {'display':'none', 'max-width': '100%', 'margin-left': 'auto', 'margin-right': 'auto'}
		
	else:
		return {'display':'block', 'max-width': '100%', 'margin-left': 'auto', 'margin-right': 'auto'}

@app.callback(
	Output("grafico_nuvem_palavras", "style"),
	[Input("tab_escolha_grafico","value")],
)
def update_layout_docentes(abas):
	print(abas,flush=True)
	if abas != 'nuvem_palavras':
		return {'display':'none', 'max-width': '100%', 'margin-left': 'auto', 'margin-right': 'auto','width':'90%','height':'90%'}
		
	else:
		return {'display':'block', 'max-width': '100%', 'margin-left': 'auto', 'margin-right': 'auto','width':'90%','height':'90%'}


@app.callback(
	Output("grafico_contagem_palavras", "style"),
	[Input("tab_escolha_grafico","value")],
)
def update_layout_docentes(abas):
	print(abas,flush=True)
	if abas != 'contagem_palavras':
		return {'display':'none', 'max-width': '100%', 'margin-left': 'auto', 'margin-right': 'auto'}
		
	else:
		return {'display':'block', 'max-width': '100%', 'margin-left': 'auto', 'margin-right': 'auto'}


@app.callback(
	Output("checklist_centros_variacao", "value"),
	[Input("dropdown_centros_variacao","value")]
)

def todos(valor):
	if ('todos' in valor):
		return 'tc'
	else:
		return ''

@app.callback(
	Output("checklist_anos_variacao", "value"),
	[Input("dropdown_anos_variacao","value")]
)

def todos(valor):
	if ('todos' in valor):
		return 'ta'
	else:
		return ''


@app.callback(
	Output("checklist_classes_analise", "value"),
	[Input("dropdown_classes_analise","value")]
)

def todos(valor):
	if ('todos' in valor):
		return 'tc'
	else:
		return ''

@app.callback(
	Output("checklist_centros_analise", "value"),
	[Input("dropdown_centros_analise","value")]
)

def todos(valor):
	if ('todos' in valor):
		return 'tc'
	else:
		return ''


@app.callback(
	Output("checklist_anos_nuvem", "value"),
	[Input("dropdown_anos_nuvem","value")]
)

def todos(valor):
	if ('todos' in valor):
		return 'ta'
	else:
		return ''


@app.callback(
	Output("checklist_centros_nuvem", "value"),
	[Input("dropdown_centros_nuvem","value")]
)

def todos(valor):
	if ('todos' in valor):
		return 'tc'
	else:
		return ''


@app.callback(
	Output("checklist_anos_contagem", "value"),
	[Input("dropdown_anos_contagem","value")]
)

def todos(valor):
	if ('todos' in valor):
		return 'ta'
	else:
		return ''

@app.callback(
	Output("checklist_centros_contagem", "value"),
	[Input("dropdown_centros_contagem","value")]
)

def todos(valor):
	if ('todos' in valor):
		return 'tc'
	else:
		return ''
######################################################3


# parte que retorna o gráfico de acordo com a seleção nos dropdowns para a VARIABILIDADE VOCABULAR
@app.callback(
	Output("grafico_variacao_vocabular", "children"),
	[Input("dropdown_anos_variacao", "value"),
	Input("dropdown_centros_variacao", "value"),
	Input("dropdown_modalidades_variacao", "value"),
	Input("tab_escolha_grafico","value")] #
)
def update_grafico_variacao_vocabular(dropdown_anos_variacao, dropdown_centros_variacao, dropdown_modalidades_variacao, tab_escolha_grafico):
   
	#return tab_escolha_grafico (variabilidade_vocabular e analise_gramatical)
	if tab_escolha_grafico == "variabilidade_vocabular":

		if('Resumo' in dropdown_modalidades_variacao):
			informacao = "Resumos"
		if('Justificativa' in dropdown_modalidades_variacao):
			informacao = "Justificativas" 
		if('Metodologia' in dropdown_modalidades_variacao):
			informacao = "Metodologias"   

		if('Fundamentacao' in dropdown_modalidades_variacao):
			informacao = "Fundamentacões Teóricas" 

		if('Objetivo' in dropdown_modalidades_variacao):
			informacao = "Objetivos"  

		if(tab_escolha_grafico == "variabilidade_vocabular"):
			if(informacao == "Resumos"):    
				df_resumo_2017 = pd.read_csv('apps/Apoio/Dataframes/df_resumo_2017.csv')
				df_resumo_2018 = pd.read_csv('apps/Apoio/Dataframes/df_resumo_2018.csv')
				df_resumo_2019 = pd.read_csv('apps/Apoio/Dataframes/df_resumo_2019.csv')
				df_resumo_2020 = pd.read_csv('apps/Apoio/Dataframes/df_resumo_2020.csv')
				df_resumo_2021 = pd.read_csv('apps/Apoio/Dataframes/df_resumo_2021.csv')
				df_resumo_2022 = pd.read_csv('apps/Apoio/Dataframes/df_resumo_2022.csv')

			elif(informacao == "Justificativas"):   
				df_resumo_2017 = pd.read_csv('apps/Apoio/Dataframes/justificativa_2017.csv')
				df_resumo_2018 = pd.read_csv('apps/Apoio/Dataframes/justificativa_2018.csv')
				df_resumo_2019 = pd.read_csv('apps/Apoio/Dataframes/justificativa_2019.csv')
				df_resumo_2020 = pd.read_csv('apps/Apoio/Dataframes/justificativa_2020.csv')
				df_resumo_2021 = pd.read_csv('apps/Apoio/Dataframes/justificativa_2021.csv')
				df_resumo_2022 = pd.read_csv('apps/Apoio/Dataframes/justificativa_2022.csv')

			elif(informacao == "Metodologias"):
				df_resumo_2017 = pd.read_csv('apps/Apoio/Dataframes/metodologia_2017.csv')
				df_resumo_2018 = pd.read_csv('apps/Apoio/Dataframes/metodologia_2018.csv')
				df_resumo_2019 = pd.read_csv('apps/Apoio/Dataframes/metodologia_2019.csv')
				df_resumo_2020 = pd.read_csv('apps/Apoio/Dataframes/metodologia_2020.csv')
				df_resumo_2021 = pd.read_csv('apps/Apoio/Dataframes/metodologia_2021.csv')
				df_resumo_2022 = pd.read_csv('apps/Apoio/Dataframes/metodologia_2022.csv')

			elif(informacao == "Fundamentacões Teóricas"):   
				df_resumo_2017 = pd.read_csv('apps/Apoio/Dataframes/fundamentacao_2017.csv')
				df_resumo_2018 = pd.read_csv('apps/Apoio/Dataframes/fundamentacao_2018.csv')
				df_resumo_2019 = pd.read_csv('apps/Apoio/Dataframes/fundamentacao_2019.csv')
				df_resumo_2020 = pd.read_csv('apps/Apoio/Dataframes/fundamentacao_2020.csv')
				df_resumo_2021 = pd.read_csv('apps/Apoio/Dataframes/fundamentacao_2021.csv')
				df_resumo_2022 = pd.read_csv('apps/Apoio/Dataframes/fundamentacao_2022.csv')

			elif(informacao == "Objetivos"):
				df_resumo_2017 = pd.read_csv('apps/Apoio/Dataframes/objetivo_2017.csv')
				df_resumo_2018 = pd.read_csv('apps/Apoio/Dataframes/objetivo_2018.csv')
				df_resumo_2019 = pd.read_csv('apps/Apoio/Dataframes/objetivo_2019.csv')
				df_resumo_2020= pd.read_csv('apps/Apoio/Dataframes/objetivo_2020.csv')
				df_resumo_2021 = pd.read_csv('apps/Apoio/Dataframes/objetivo_2021.csv')
				df_resumo_2022 = pd.read_csv('apps/Apoio/Dataframes/objetivo_2022.csv')

			else:
				informacao = "Resumos"    
				df_resumo_2017 = pd.read_csv('apps/Apoio/Dataframes/df_resumo_2017.csv')
				df_resumo_2018 = pd.read_csv('apps/Apoio/Dataframes/df_resumo_2018.csv')
				df_resumo_2019 = pd.read_csv('apps/Apoio/Dataframes/df_resumo_2019.csv')
				df_resumo_2020 = pd.read_csv('apps/Apoio/Dataframes/df_resumo_2020.csv')
				df_resumo_2021 = pd.read_csv('apps/Apoio/Dataframes/df_resumo_2021.csv')
				df_resumo_2022 = pd.read_csv('apps/Apoio/Dataframes/df_resumo_2022.csv')

		else:
			None
		
		tamanho_anos = 0
		df_resumos = [0,0,0,0,0,0,0]
		df_resumos[0] = df_resumo_2017
		df_resumos[1] = df_resumo_2018
		df_resumos[2] = df_resumo_2019
		df_resumos[3] = df_resumo_2020
		df_resumos[4] = df_resumo_2021
		df_resumos[5] = df_resumo_2022

		df_consulta = [0,0,0,0,0,0]
		centros_variacao = []
		qtd_palavras_2017 =[]
		qtd_palavras_2018 =[]
		qtd_palavras_2019 =[]
		qtd_palavras_2020 =[]
		qtd_palavras_2021 =[]
		qtd_palavras_2022 =[]
		anos = []
		centros = []
		anos.clear()
		
		df_consulta.clear()

		for i in dropdown_centros_variacao: 
				if(i in ListaCentros_variacao[1:]):
					centros.append(i)

		if('2017' in dropdown_anos_variacao):
			anos.append('2017')
			tamanho_anos += 1
			df_consulta.append(df_resumo_2017.loc['PALAVRAS'])
			for i in dropdown_centros_variacao: 
				if(i in ListaCentros_variacao[1:]):
					qtd_palavras_2017.append(df_resumo_2017.loc['PALAVRAS'][i])

		if('2018' in dropdown_anos_variacao):
			anos.append('2018')
			tamanho_anos += 1
			df_consulta.append(df_resumo_2018.loc['PALAVRAS'])
			for i in dropdown_centros_variacao: 
				if(i in ListaCentros_variacao[1:]):
					qtd_palavras_2018.append(df_resumo_2018.loc['PALAVRAS'][i])

		if('2019' in dropdown_anos_variacao):
			anos.append('2019')
			tamanho_anos += 1
			df_consulta.append(df_resumo_2019.loc['PALAVRAS'])
			for i in dropdown_centros_variacao: 
				if(i in ListaCentros_variacao[1:]):
					qtd_palavras_2019.append(df_resumo_2019.loc['PALAVRAS'][i])

		if('2020' in dropdown_anos_variacao):
			anos.append('2020')
			tamanho_anos += 1
			df_consulta.append(df_resumo_2020.loc['PALAVRAS'])
			for i in dropdown_centros_variacao: 
				if(i in ListaCentros_variacao[1:]):
					qtd_palavras_2020.append(df_resumo_2020.loc['PALAVRAS'][i])

		if('2021' in dropdown_anos_variacao):
			anos.append('2021')
			tamanho_anos += 1
			df_consulta.append(df_resumo_2021.loc['PALAVRAS'])
			for i in dropdown_centros_variacao: 
				if(i in ListaCentros_variacao[1:]):
					qtd_palavras_2021.append(df_resumo_2021.loc['PALAVRAS'][i])

		if('2022' in dropdown_anos_variacao):
			anos.append('2022')
			tamanho_anos += 1
			df_consulta.append(df_resumo_2022.loc['PALAVRAS'])
			for i in dropdown_centros_variacao: 
				if(i in ListaCentros_variacao[1:]):
					qtd_palavras_2022.append(df_resumo_2022.loc['PALAVRAS'][i])


			for i in range(0,len(centros)):
				centros[i] = centros[i].split('-')[0]

			x = centros

			


  
		if(tamanho_anos == 1):
			qtdPalavras = qtd_palavras_2017 + qtd_palavras_2018 + qtd_palavras_2019 + qtd_palavras_2020 + qtd_palavras_2021 + qtd_palavras_2022 
			dc_total_2017 = dict(zip(centros_variacao,qtdPalavras)) #Ordena do menor para o maior
			dc_total_2017 = dict(sorted(dc_total_2017.items(), key=itemgetter(1)))
			df_total_2017 = pd.DataFrame(data=dc_total_2017,index=['PALAVRAS'])
			
			x = centros
			y = qtdPalavras

			print("\n ")
			print('x = ' + str(x))
			print('y = ' + str(y))
			print("\n ")
			return dcc.Graph(
				id='g1_variacao_vocabular',
				figure={
					'data': [
						{'x': x , 'y': y, 'type': 'bar', 'name': int(anos[0])},
					],
					'layout': {
						'title': 'Gráfico da Variabilidade Vocabular por Centro - {} - ({})'.format(informacao, anos)
					}
				})
				
		if(tamanho_anos == 2):
			palavras = []
			if(sum(qtd_palavras_2017) > 0):
				palavras.append(qtd_palavras_2017)
			if(sum(qtd_palavras_2018) > 0):
				palavras.append(qtd_palavras_2018)
			if(sum(qtd_palavras_2019) > 0):
				palavras.append(qtd_palavras_2019)
			if(sum(qtd_palavras_2020) > 0):
				palavras.append(qtd_palavras_2020)
			if(sum(qtd_palavras_2021) > 0):
				palavras.append(qtd_palavras_2021)
			if(sum(qtd_palavras_2022) > 0):
				palavras.append(qtd_palavras_2022)

			x = centros
			y1 = palavras[0]
			y2 = palavras[1]

			return dcc.Graph(
				id='g1_variacao_vocabular',
				figure={
					'data': [
						{'x': x , 'y': y1, 'type': 'bar', 'name': int(anos[0])},
						{'x': x , 'y': y2, 'type': 'bar', 'name': int(anos[1])},
					],
			'layout': {
				'title': 'Gráfico da Variabilidade Vocabular por Centro - {} - ({})'.format(informacao, anos)
				}
			})
				
				
		if(tamanho_anos == 3):
			palavras = []
			if(sum(qtd_palavras_2017) > 0):
				palavras.append(qtd_palavras_2017)
			if(sum(qtd_palavras_2018) > 0):
				palavras.append(qtd_palavras_2018)
			if(sum(qtd_palavras_2019) > 0):
				palavras.append(qtd_palavras_2019)
			if(sum(qtd_palavras_2020) > 0):
				palavras.append(qtd_palavras_2020)
			if(sum(qtd_palavras_2021) > 0):
				palavras.append(qtd_palavras_2021)
			if(sum(qtd_palavras_2022) > 0):
				palavras.append(qtd_palavras_2022)

			print(palavras)
			y1 = palavras[0]
			y2 = palavras[1]
			y3 = palavras[2]

			return dcc.Graph(
				id='g1_variacao_vocabular',
				figure={
					'data': [
						{'x': x , 'y': y1, 'type': 'bar', 'name': int(anos[0])},
						{'x': x , 'y': y2, 'type': 'bar', 'name': int(anos[1])},
						{'x': x , 'y': y3, 'type': 'bar', 'name': int(anos[2])},
					],
			'layout': {
				'title': 'Gráfico da Variabilidade Vocabular por Centro - {} - ({})'.format(informacao, anos)
				}
			})

	if(tamanho_anos == 4):
			palavras = []
			if(sum(qtd_palavras_2017) > 0):
				palavras.append(qtd_palavras_2017)
			if(sum(qtd_palavras_2018) > 0):
				palavras.append(qtd_palavras_2018)
			if(sum(qtd_palavras_2019) > 0):
				palavras.append(qtd_palavras_2019)
			if(sum(qtd_palavras_2020) > 0):
				palavras.append(qtd_palavras_2020)
			if(sum(qtd_palavras_2021) > 0):
				palavras.append(qtd_palavras_2021)
			if(sum(qtd_palavras_2022) > 0):
				palavras.append(qtd_palavras_2022)

			x = centros
			print(palavras)
			y1 = palavras[0]
			y2 = palavras[1]
			y3 = palavras[2]
			y4 = palavras[3]
			
			return dcc.Graph(
				id='g1_variacao_vocabular',
				figure={
					'data': [
						{'x': x , 'y': y1, 'type': 'bar', 'name': int(anos[0])},
						{'x': x , 'y': y2, 'type': 'bar', 'name': int(anos[1])},
						{'x': x , 'y': y3, 'type': 'bar', 'name': int(anos[2])},
						{'x': x , 'y': y4, 'type': 'bar', 'name': int(anos[3])},
					],
			'layout': {
				'title': 'Gráfico da Variabilidade Vocabular por Centro - {} - ({})'.format(informacao, anos)
				}
			})

	if(tamanho_anos == 5):
			palavras = []
			if(sum(qtd_palavras_2017) > 0):
				palavras.append(qtd_palavras_2017)
			if(sum(qtd_palavras_2018) > 0):
				palavras.append(qtd_palavras_2018)
			if(sum(qtd_palavras_2019) > 0):
				palavras.append(qtd_palavras_2019)
			if(sum(qtd_palavras_2020) > 0):
				palavras.append(qtd_palavras_2020)
			if(sum(qtd_palavras_2021) > 0):
				palavras.append(qtd_palavras_2021)
			if(sum(qtd_palavras_2022) > 0):
				palavras.append(qtd_palavras_2022)

			x = centros
			print(palavras)
			y1 = palavras[0]
			y2 = palavras[1]
			y3 = palavras[2]
			y4 = palavras[3]
			y5 = palavras[4]
			

			return dcc.Graph(
				id='g1_variacao_vocabular',
				figure={
					'data': [
						{'x': x , 'y': y1, 'type': 'bar', 'name': int(anos[0])},
						{'x': x , 'y': y2, 'type': 'bar', 'name': int(anos[1])},
						{'x': x , 'y': y3, 'type': 'bar', 'name': int(anos[2])},
						{'x': x , 'y': y4, 'type': 'bar', 'name': int(anos[3])},
						{'x': x , 'y': y5, 'type': 'bar', 'name': int(anos[4])},
					],
			'layout': {
				'title': 'Gráfico da Variabilidade Vocabular por Centro - {} - ({})'.format(informacao, anos)
				}
			})


	if(tamanho_anos == 6):
			palavras = []
			if(sum(qtd_palavras_2017) > 0):
				palavras.append(qtd_palavras_2017)
			if(sum(qtd_palavras_2018) > 0):
				palavras.append(qtd_palavras_2018)
			if(sum(qtd_palavras_2019) > 0):
				palavras.append(qtd_palavras_2019)
			if(sum(qtd_palavras_2020) > 0):
				palavras.append(qtd_palavras_2020)
			if(sum(qtd_palavras_2021) > 0):
				palavras.append(qtd_palavras_2021)
			if(sum(qtd_palavras_2022) > 0):
				palavras.append(qtd_palavras_2022)

			x = centros
			
			y1 = palavras[0]
			y2 = palavras[1]
			y3 = palavras[2]
			y4 = palavras[3]
			y5 = palavras[4]
			y6 = palavras[5]
			

			return dcc.Graph(
				id='g1_variacao_vocabular',
				figure={
					'data': [
						{'x': x , 'y': y1, 'type': 'bar', 'name': int(anos[0])},
						{'x': x , 'y': y2, 'type': 'bar', 'name': int(anos[1])},
						{'x': x , 'y': y3, 'type': 'bar', 'name': int(anos[2])},
						{'x': x , 'y': y4, 'type': 'bar', 'name': int(anos[3])},
						{'x': x , 'y': y5, 'type': 'bar', 'name': int(anos[4])},
						{'x': x , 'y': y6, 'type': 'bar', 'name': int(anos[5])},
					],
			'layout': {
				'title': 'Gráfico da Variabilidade Vocabular por Centro - {} - ({})'.format(informacao, anos)
				}
			})




@app.callback(
	Output("dropdown_anos_variacao","value"),
	[Input("checklist_anos_variacao", "value")],[State("dropdown_anos_variacao", "value")]

)
def retornar_anos_dropdown(value,estado):
	print(value)
	if('ta' in value):
		return ["2017", "2018", "2019","2020","2021","2022"]
	else:
		return estado
		


@app.callback(
	Output("dropdown_centros_variacao","value"),
	[Input("checklist_centros_variacao", "value")],[State("dropdown_centros_variacao", "value")]
)
def retornar_anos_dropdown(value,estado):
	if('tc' in value):
		return ListaCentros_variacao[1:]
	else:
		return estado


########################
######################
#######################
################
# parte que retorna o gráfico de acordo com a seleção nos dropdowns para a ANÁLISE GRAMATICAL

@app.callback(
	Output("grafico_analise_gramatical", "children"), #o gráfico independe dos cards
	[Input("dropdown_classes_analise", "value"),
	Input("dropdown_centros_analise", "value"),
	Input("dropdown_modalidades_analise", "value"),
	Input("tab_escolha_grafico","value")] #######################
)
def update_grafico_analise_vocabular(dropdown_classes_analise, dropdown_centros_analise, dropdown_modalidades_analise, tab_escolha_grafico):
	if tab_escolha_grafico == "analise_gramatical":
		informacao = []
		informacao.clear()
		if('Substantivos' in dropdown_classes_analise):
			informacao.append("Substantivos")
		if('Adjetivos' in dropdown_classes_analise):
			informacao.append("Adjetivos") 
		if('Verbos' in dropdown_classes_analise):
			informacao.append("Verbos")   
		
		if("Substantivos" in informacao and "Adjetivos" in informacao and "Verbos" in informacao):
			cont = 3
			if("Resumo" in dropdown_modalidades_analise):
				df1 = pd.read_csv('apps/Apoio/Dataframes/substantivos_resumo.csv')
				df2 = pd.read_csv('apps/Apoio/Dataframes/adjetivos_resumo.csv')
				df3 = pd.read_csv('apps/Apoio/Dataframes/verbos_resumo.csv')
				info = "Resumo"
			elif("Justificativa" in dropdown_modalidades_analise):
				df1 = pd.read_csv('apps/Apoio/Dataframes/substantivos_justificativa.csv')
				df2 = pd.read_csv('apps/Apoio/Dataframes/adjetivos_justificativa.csv')
				df3 = pd.read_csv('apps/Apoio/Dataframes/verbos_justificativa.csv')
				info = "Justificativa"
			elif("Metodologia" in dropdown_modalidades_analise):
				df1 = pd.read_csv('apps/Apoio/Dataframes/substantivos_metodologia.csv')
				df2 = pd.read_csv('apps/Apoio/Dataframes/adjetivos_metodologia.csv')
				df3 = pd.read_csv('apps/Apoio/Dataframes/verbos_metodologia.csv')
				info = "Metodologia"
			elif("Fundamentacao" in dropdown_modalidades_analise):
				df1 = pd.read_csv('apps/Apoio/Dataframes/substantivos_fundamentacao.csv')
				df2 = pd.read_csv('apps/Apoio/Dataframes/adjetivos_fundamentacao.csv')
				df3 = pd.read_csv('apps/Apoio/Dataframes/verbos_fundamentacao.csv')
				info = "Fundamentação Teórica"
			elif("Objetivo" in dropdown_modalidades_analise):
				df1 = pd.read_csv('apps/Apoio/Dataframes/substantivos_objetivos.csv')
				df2 = pd.read_csv('apps/Apoio/Dataframes/adjetivos_objetivos.csv')
				df3 = pd.read_csv('apps/Apoio/Dataframes/verbos_objetivos.csv')
				info = "Objetivo"

		elif("Substantivos" in informacao and "Adjetivos" in informacao):
			cont = 2
			if("Resumo" in dropdown_modalidades_analise):
				df1 = pd.read_csv('apps/Apoio/Dataframes/substantivos_resumo.csv')
				df2 = pd.read_csv('apps/Apoio/Dataframes/adjetivos_resumo.csv')
				info = "Resumo"
			elif("Justificativa" in dropdown_modalidades_analise):
				df1 = pd.read_csv('apps/Apoio/Dataframes/substantivos_justificativa.csv')
				df2 = pd.read_csv('apps/Apoio/Dataframes/adjetivos_justificativa.csv')
				info = "Justificativa"
			elif("Metodologia" in dropdown_modalidades_analise):
				df1 = pd.read_csv('apps/Apoio/Dataframes/substantivos_metodologia.csv')
				df2 = pd.read_csv('apps/Apoio/Dataframes/adjetivos_metodologia.csv')
				info = "Metodologia"
			elif("Fundamentacao" in dropdown_modalidades_analise):
				df1 = pd.read_csv('apps/Apoio/Dataframes/substantivos_fundamentacao.csv')
				df2 = pd.read_csv('apps/Apoio/Dataframes/adjetivos_fundamentacao.csv')
				info = "Fundamentação Teórica"
			elif("Objetivo" in dropdown_modalidades_analise):
				df1 = pd.read_csv('apps/Apoio/Dataframes/substantivos_objetivos.csv')
				df2 = pd.read_csv('apps/Apoio/Dataframes/adjetivos_objetivos.csv')
				info = "Objetivo"


		elif("Substantivos" in informacao and "Verbos" in informacao):
			cont =2
			if("Resumo" in dropdown_modalidades_analise):
				df1 = pd.read_csv('apps/Apoio/Dataframes/substantivos_resumo.csv')
				df2 = pd.read_csv('apps/Apoio/Dataframes/verbos_resumo.csv')
				info = "Resumo"
			elif("Justificativa" in dropdown_modalidades_analise):
				df1 = pd.read_csv('apps/Apoio/Dataframes/substantivos_justificativa.csv')
				df2 = pd.read_csv('apps/Apoio/Dataframes/verbos_justificativa.csv')
				info = "Justificativa"
			elif("Metodologia" in dropdown_modalidades_analise):
				df1 = pd.read_csv('apps/Apoio/Dataframes/substantivos_metodologia.csv')
				df2 = pd.read_csv('apps/Apoio/Dataframes/verbos_metodologia.csv')
				info = "Metodologia"
			elif("Fundamentacao" in dropdown_modalidades_analise):
				df1 = pd.read_csv('apps/Apoio/Dataframes/substantivos_fundamentacao.csv')
				df2 = pd.read_csv('apps/Apoio/Dataframes/verbos_fundamentacao.csv')
				info = "Fundamentação Teórica"
			elif("Objetivo" in dropdown_modalidades_analise):
				df1 = pd.read_csv('apps/Apoio/Dataframes/substantivos_objetivos.csv')
				df2 = pd.read_csv('apps/Apoio/Dataframes/verbos_objetivos.csv')
				info = "Objetivo"

		elif("Adjetivos" in informacao and "Verbos" in informacao):
			cont =2
			if("Resumo" in dropdown_modalidades_analise):
				df1 = pd.read_csv('apps/Apoio/Dataframes/adjetivos_resumo.csv')
				df2 = pd.read_csv('apps/Apoio/Dataframes/verbos_resumo.csv')
				info = "Resumo"
			elif("Justificativa" in dropdown_modalidades_analise):
				df1 = pd.read_csv('apps/Apoio/Dataframes/adjetivos_justificativa.csv')
				df2 = pd.read_csv('apps/Apoio/Dataframes/verbos_justificativa.csv')
				info = "Justificativa"
			elif("Metodologia" in dropdown_modalidades_analise):
				df1 = pd.read_csv('apps/Apoio/Dataframes/adjetivos_metodologia.csv')
				df2 = pd.read_csv('apps/Apoio/Dataframes/verbos_metodologia.csv')
				info = "Metodologia"
			elif("Fundamentacao" in dropdown_modalidades_analise):
				df1 = pd.read_csv('apps/Apoio/Dataframes/adjetivos_fundamentacao.csv')
				df2 = pd.read_csv('apps/Apoio/Dataframes/verbos_fundamentacao.csv')
				info = "Fundamentação Teórica"
			elif("Objetivo" in dropdown_modalidades_analise):
				df1 = pd.read_csv('apps/Apoio/Dataframes/adjetivos_objetivos.csv')
				df2 = pd.read_csv('apps/Apoio/Dataframes/verbos_objetivos.csv')
				info = "Objetivo"

		elif("Substantivos" in informacao):
			cont = 1
			if("Resumo" in dropdown_modalidades_analise):
				df1 = pd.read_csv('apps/Apoio/Dataframes/substantivos_resumo.csv')
				info = "Resumo"
			elif("Justificativa" in dropdown_modalidades_analise):
				df1 = pd.read_csv('apps/Apoio/Dataframes/substantivos_justificativa.csv')
				info = "Justificativa"
			elif("Metodologia" in dropdown_modalidades_analise):
				df1 = pd.read_csv('apps/Apoio/Dataframes/substantivos_metodologia.csv')
				info = "Metodologia"
			elif("Fundamentacao" in dropdown_modalidades_analise):
				df1 = pd.read_csv('apps/Apoio/Dataframes/substantivos_fundamentacao.csv')
				info = "Fundamentação Teórica"
			elif("Objetivo" in dropdown_modalidades_analise):
				df1 = pd.read_csv('apps/Apoio/Dataframes/substantivos_objetivos.csv')
				info = "Objetivo"

		elif("Adjetivos" in informacao):
			cont = 1
			if("Resumo" in dropdown_modalidades_analise):
				df1 = pd.read_csv('apps/Apoio/Dataframes/adjetivos_resumo.csv')
				info = "Resumo"
			elif("Justificativa" in dropdown_modalidades_analise):
				df1 = pd.read_csv('apps/Apoio/Dataframes/adjetivos_justificativa.csv')
				info = "Justificativa"
			elif("Metodologia" in dropdown_modalidades_analise):
				df1 = pd.read_csv('apps/Apoio/Dataframes/adjetivos_metodologia.csv')
				info = "Metodologia"
			elif("Fundamentacao" in dropdown_modalidades_analise):
				df1 = pd.read_csv('apps/Apoio/Dataframes/adjetivos_fundamentacao.csv')
				info = "Fundamentação Teórica"
			elif("Objetivos" in dropdown_modalidades_analise):
				df1 = pd.read_csv('apps/Apoio/Dataframes/adjetivos_objetivos.csv')
				info = "Objetivo"

		elif("Verbos" in informacao):
			cont = 1
			if("Resumo" in dropdown_modalidades_analise):
				df1 = pd.read_csv('apps/Apoio/Dataframes/verbos_resumo.csv')
				info = "Resumo"
			elif("Justificativa" in dropdown_modalidades_analise):
				df1 = pd.read_csv('apps/Apoio/Dataframes/verbos_justificativa.csv')
				info = "Justificativa"
			elif("Metodologia" in dropdown_modalidades_analise):
				df1 = pd.read_csv('apps/Apoio/Dataframes/verbos_metodologia.csv')
				info = "Metodologia"
			elif("Fundamentacao" in dropdown_modalidades_analise):
				df1 = pd.read_csv('apps/Apoio/Dataframes/verbos_fundamentacao.csv')
				info = "Fundamentação Teórica"
			elif("Objetivo" in dropdown_modalidades_analise):
				df1 = pd.read_csv('apps/Apoio/Dataframes/verbos_objetivos.csv')
				info = "Objetivo"	
		
		centros_variacao = []
		df_consulta1 = []
		df_consulta2 = []
		df_consulta3 = []

		if(cont==1):
			for i in dropdown_centros_analise: 
				if(i in ListaCentros_variacao[1:]):
					centros_variacao.append(i)
					df_consulta1.append(df1.loc['PALAVRAS'][i])

			for j,i in enumerate(centros_variacao):
				if i not in dropdown_centros_analise:
					del centros_variacao[j]
					del df_consulta1[j]

		elif(cont==2):
			for i in dropdown_centros_analise: 
				if(i in ListaCentros_variacao[1:]):
					centros_variacao.append(i)
					df_consulta1.append(df1.loc['PALAVRAS'][i])
					df_consulta2.append(df2.loc['PALAVRAS'][i])

			for j,i in enumerate(centros_variacao):
				if i not in dropdown_centros_analise:
					del centros_variacao[j]
					del df_consulta1[j]
					del df_consulta2[j]

		elif(cont==3):
			for i in dropdown_centros_analise: 
				if(i in ListaCentros_variacao[1:]):
					centros_variacao.append(i)
					df_consulta1.append(df1.loc['PALAVRAS'][i])
					df_consulta2.append(df2.loc['PALAVRAS'][i])
					df_consulta3.append(df3.loc['PALAVRAS'][i])

			for j,i in enumerate(centros_variacao):
				if i not in dropdown_centros_analise:
					del centros_variacao[j]
					del df_consulta1[j]
					del df_consulta2[j]
					del df_consulta3[j]


		for j,i in enumerate(centros_variacao):
			centros_variacao[j] = i.split(' -')[0]


		if(cont == 1):
			dc_total1 = dict(zip(centros_variacao,df_consulta1)) #Ordena do menor para o maior
			dc_total1 = dict(sorted(dc_total1.items(), key=itemgetter(1)))
			df_total1 = pd.DataFrame(data=dc_total1,index=['PALAVRAS'])
			x1=df_total1.columns.to_list()
			y1 = df_total1.loc['PALAVRAS']
			   
		
			return dcc.Graph(
				id='g1_variacao_vocabular',
				figure={
					'data': [
						{'x': x1 , 'y': y1, 'type': 'bar', 'name': "Nome qualquer"},
					],
			'layout': {
				'title': 'Gráfico da Análise Gramatical do(a) {} por Centro (média de 2017,2018, 2019, 2020, 2021 e 2022)'.format(info)
				}
			})


		if(cont == 2):
			dc_total1 = dict(zip(centros_variacao,df_consulta1)) #Ordena do menor para o maior
			dc_total1 = dict(sorted(dc_total1.items(), key=itemgetter(1)))
			df_total1 = pd.DataFrame(data=dc_total1,index=['PALAVRAS'])
			x1=df_total1.columns.to_list()
			y1 = df_total1.loc['PALAVRAS']

			dc_total2 = dict(zip(centros_variacao,df_consulta2)) #Ordena do menor para o maior
			dc_total2 = dict(sorted(dc_total2.items(), key=itemgetter(1)))
			df_total2 = pd.DataFrame(data=dc_total2,index=['PALAVRAS'])
			x2=df_total2.columns.to_list()
			y2 = df_total2.loc['PALAVRAS']

			return dcc.Graph(
				id='g1_variacao_vocabular',
				figure={
					'data': [
						{'x': x1 , 'y': y1, 'type': 'bar', 'name': informacao[0]},
						{'x': x2 , 'y': y2, 'type': 'bar', 'name': informacao[1]},
					],
			'layout': {
				'title': 'Gráfico da Análise Gramatical do(a) {} por Centro (média de 2017,2018 e 2019)'.format(info)
		
				}
			})


		if(cont == 3):
			dc_total1 = dict(zip(centros_variacao,df_consulta1)) #Ordena do menor para o maior
			dc_total1 = dict(sorted(dc_total1.items(), key=itemgetter(1)))
			df_total1 = pd.DataFrame(data=dc_total1,index=['PALAVRAS'])
			x1=df_total1.columns.to_list()
			y1 = df_total1.loc['PALAVRAS']

			dc_total2 = dict(zip(centros_variacao,df_consulta2)) #Ordena do menor para o maior
			dc_total2 = dict(sorted(dc_total2.items(), key=itemgetter(1)))
			df_total2 = pd.DataFrame(data=dc_total2,index=['PALAVRAS'])
			x2=df_total2.columns.to_list()
			y2 = df_total2.loc['PALAVRAS']

			dc_total3 = dict(zip(centros_variacao,df_consulta3)) #Ordena do menor para o maior
			dc_total3 = dict(sorted(dc_total3.items(), key=itemgetter(1)))
			df_total3 = pd.DataFrame(data=dc_total3,index=['PALAVRAS'])
			x3=df_total3.columns.to_list()
			y3 = df_total3.loc['PALAVRAS']

			return dcc.Graph(
				id='g1_variacao_vocabular',
				figure={
					'data': [
						{'x': x1 , 'y': y1, 'type': 'bar', 'name': informacao[0]},
						{'x': x2 , 'y': y2, 'type': 'bar', 'name': informacao[1]},
						{'x': x3 , 'y': y3, 'type': 'bar', 'name': informacao[2]},
					],
			'layout': {
				'title': 'Gráfico da Análise Gramatical do(a) {} por Centro (média de 2017,2018 e 2019)'.format(info)
				}
			})


####### desativado *tudo com checklist está desativado por enquanto
@app.callback(
	Output("dropdown_classes_analise","value"),
	[Input("checklist_classes_analise", "value")],[State("dropdown_classes_analise", "value")]

)
def retornar_classes_dropdown(value,estado):
	if('tc' in value):
		return ["Substantivos", "Adjetivos", "Verbos"]
	else:
		return estado 

@app.callback(
	Output("dropdown_centros_analise","value"),
	[Input("checklist_centros_analise", "value")],[State("dropdown_centros_analise", "value")]
)
def retornar_centros_dropdown(value,estado):
	if('tc' in value):
		return ListaCentros_variacao[1:]
	else:
		return estado
#############################	
	
##############
##############
############## NUVEM DE PALAVRAS

# exibe o tipo de gráfico que está sendo mostrado, no topo da página
@app.callback(
	Output("texto_grafico_nuvem", "children"),
	[Input("tab_escolha_grafico","value")]
)

def graf_tit(tipo_grafico):
        if tipo_grafico == 'nuvem_palavras':
          return 'Nuvem de Palavras por Centro, Ano e Campo'

        elif tipo_grafico == 'variabilidade_vocabular':
          return 'Gráfico da Variabilidade Vocabular por Centro e Campo'

        elif tipo_grafico == 'analise_gramatical':
          return 'Gráfico da Análise Gramatical por Classe, Centro e Campo'

        elif tipo_grafico == 'contagem_palavras':
          return 'Contagem de Palavras por Ano'

@app.callback(
	Output("grafico_nuvem_palavras", "src"),
	[Input("dropdown_anos_nuvem", "value"),
	Input("dropdown_centros_nuvem", "value"),
	Input("tab_escolha_grafico","value"),
	Input("dropdown_modalidades_nuvem","value")] #######################
)
def update_grafico_variacao_vocabular(dropdown_anos_nuvem, dropdown_centros_nuvem, tab_escolha_grafico, dropdown_modalidades_nuvem):
	f= io.open("apps/Apoio/stopwords_portugues.txt", "r", encoding="utf8") #Importando as stopwords
	stopwords_portuguese = []
	stopwords_portuguese = f.readlines()
	for j,i in enumerate(stopwords_portuguese):
		if(" \n" in i):
			stopwords_portuguese[j] = stopwords_portuguese[j].split(" \n")[0]
		elif("\n" in i):
			stopwords_portuguese[j] = stopwords_portuguese[j].split("\n")[0]


	if(tab_escolha_grafico == "nuvem_palavras"):
		if( "Resumo" in dropdown_modalidades_nuvem):
			info = "Resumo"
			df_2017 = pd.read_csv("apps/Apoio/Dataframes/lista_palavras_resumo_2017.csv")
			df_2018 = pd.read_csv("apps/Apoio/Dataframes/lista_palavras_resumo_2018.csv")
			df_2019 = pd.read_csv("apps/Apoio/Dataframes/lista_palavras_resumo_2019.csv")
			df_2020 = pd.read_csv("apps/Apoio/Dataframes/lista_palavras_resumo_2020.csv")
			df_2021 = pd.read_csv("apps/Apoio/Dataframes/lista_palavras_resumo_2021.csv")
			df_2022 = pd.read_csv("apps/Apoio/Dataframes/lista_palavras_resumo_2022.csv")
			

		elif( "Metodologia" in dropdown_modalidades_nuvem):
			info = "Metodologia"
			df_2017 = pd.read_csv("apps/Apoio/Dataframes/lista_palavras_metodologia_2017.csv")
			df_2018 = pd.read_csv("apps/Apoio/Dataframes/lista_palavras_metodologia_2018.csv")
			df_2019 = pd.read_csv("apps/Apoio/Dataframes/lista_palavras_metodologia_2019.csv")
			df_2020 = pd.read_csv("apps/Apoio/Dataframes/lista_palavras_metodologia_2020.csv")
			df_2021 = pd.read_csv("apps/Apoio/Dataframes/lista_palavras_metodologia_2021.csv")
			df_2022 = pd.read_csv("apps/Apoio/Dataframes/lista_palavras_metodologia_2022.csv")

		elif( "Justificativa" in dropdown_modalidades_nuvem):
			info = "Justificativa"
			df_2017 = pd.read_csv("apps/Apoio/Dataframes/lista_palavras_justificativa_2017.csv")
			df_2018 = pd.read_csv("apps/Apoio/Dataframes/lista_palavras_justificativa_2018.csv")
			df_2019 = pd.read_csv("apps/Apoio/Dataframes/lista_palavras_justificativa_2019.csv")
			df_2020 = pd.read_csv("apps/Apoio/Dataframes/lista_palavras_justificativa_2020.csv")
			df_2021 = pd.read_csv("apps/Apoio/Dataframes/lista_palavras_justificativa_2021.csv")
			df_2022 = pd.read_csv("apps/Apoio/Dataframes/lista_palavras_justificativa_2022.csv")

		elif( "Objetivo" in dropdown_modalidades_nuvem):
			info = "Objetivo"
			df_2017 = pd.read_csv("apps/Apoio/Dataframes/lista_palavras_objetivo_2017.csv")
			df_2018 = pd.read_csv("apps/Apoio/Dataframes/lista_palavras_objetivo_2018.csv")
			df_2019 = pd.read_csv("apps/Apoio/Dataframes/lista_palavras_objetivo_2019.csv")
			df_2020 = pd.read_csv("apps/Apoio/Dataframes/lista_palavras_objetivo_2020.csv")
			df_2021 = pd.read_csv("apps/Apoio/Dataframes/lista_palavras_objetivo_2021.csv")
			df_2022 = pd.read_csv("apps/Apoio/Dataframes/lista_palavras_objetivo_2022.csv")

		elif("Fundamentacao" in dropdown_modalidades_nuvem):
			info = "Fundamentacão Teórica"
			df_2017 = pd.read_csv("apps/Apoio/Dataframes/lista_palavras_fundamentacao_2017.csv")
			df_2018 = pd.read_csv("apps/Apoio/Dataframes/lista_palavras_fundamentacao_2018.csv")
			df_2019 = pd.read_csv("apps/Apoio/Dataframes/lista_palavras_fundamentacao_2019.csv")
			df_2020 = pd.read_csv("apps/Apoio/Dataframes/lista_palavras_fundamentacao_2020.csv")
			df_2021 = pd.read_csv("apps/Apoio/Dataframes/lista_palavras_fundamentacao_2021.csv")
			df_2022 = pd.read_csv("apps/Apoio/Dataframes/lista_palavras_fundamentacao_2022.csv")

			print(df_2017)


		df_consulta1 = []
		df_consulta2 = []
		df_consulta3 = []
		df_consulta4 = []
		df_consulta5 = []
		df_consulta6 = []

		centros_variacao = []
		texto = ""
		centros = []
		anos = []
		tamanho_anos = 0

		for i in dropdown_centros_nuvem: 
			if(i in ListaCentros_variacao[1:]):
				centros.append(i)

		##Pegando os centros desejados
		if('2017' in dropdown_anos_nuvem):
			anos.append("2017")
			tamanho_anos += 1
			for i in dropdown_centros_nuvem: 
				if(i in ListaCentros_variacao[1:]):
					df_consulta1.append(df_2017.loc['PALAVRAS'][i])

		if('2018' in dropdown_anos_nuvem):
			anos.append("2018")
			tamanho_anos += 1
			for i in dropdown_centros_nuvem: 
				if(i in ListaCentros_variacao[1:]):
					df_consulta2.append(df_2018.loc['PALAVRAS'][i])

		if('2019' in dropdown_anos_nuvem):
			anos.append("2019")
			tamanho_anos += 1
			for i in dropdown_centros_nuvem: 
				if(i in ListaCentros_variacao[1:]):
					df_consulta3.append(df_2019.loc['PALAVRAS'][i])

		if('2020' in dropdown_anos_nuvem):
			anos.append("2020")
			tamanho_anos += 1
			for i in dropdown_centros_nuvem: 
				if(i in ListaCentros_variacao[1:]):
					df_consulta4.append(df_2020.loc['PALAVRAS'][i])

		if('2021' in anos):
			anos.append("2021")
			tamanho_anos += 1
			for i in dropdown_centros_nuvem: 
				if(i in ListaCentros_variacao[1:]):
					df_consulta5.append(df_2021.loc['PALAVRAS'][i])

		if('2022' in dropdown_anos_nuvem):
			anos.append("2022")
			tamanho_anos += 1
			for i in dropdown_centros_nuvem: 
				if(i in ListaCentros_variacao[1:]):
					df_consulta6.append(df_2022.loc['PALAVRAS'][i])

			#
			for j,i in enumerate(centros_variacao):
				if i not in dropdown_centros_nuvem:
					del centros[j]
					del df_consulta1[j]
					del df_consulta2[j]
					del df_consulta3[j]
					del df_consulta4[j]
					del df_consulta5[j]
					del df_consulta6[j]
					
		texto_nuvem = ""
		for i in df_consulta1:
			texto_nuvem += str(i)
		for i in df_consulta2:
			texto_nuvem += str(i)
		for i in df_consulta3:
			texto_nuvem += str(i)
		for i in df_consulta4:
			texto_nuvem += str(i)
		for i in df_consulta5:
			texto_nuvem += str(i)
		for i in df_consulta6:
			texto_nuvem += str(i)

		wordcloud = WordCloud(max_font_size=60, max_words=20, background_color="white", stopwords=stopwords_portuguese).generate(texto_nuvem)
		fig, ax = plt.subplots()
		ax.imshow(wordcloud, interpolation='bilinear')
		ax.set_axis_off()
		plt.savefig('apps/Apoio/nuvem/nuvem.png')
		encoded_image = base64.b64encode(open("apps/Apoio/nuvem/nuvem.png", 'rb').read())
		src='data:image/png;base64,{}'.format(encoded_image.decode())
		return src


#### desativado
@app.callback(
	Output("dropdown_anos_nuvem","value"),
	[Input("checklist_anos_nuvem", "value")],[State("dropdown_anos_nuvem", "value")]

)
def retornar_anos_dropdown(value,estado):
	if('ta' in value):
		return ["2017", "2018", "2019","2020","2021","2022"]
	else:
		return estado	


@app.callback(
	Output("dropdown_centros_nuvem","value"),
	[Input("checklist_centros_nuvem", "value")],[State("dropdown_centros_nuvem", "value")]
)
def retornar_anos_dropdown(value,estado):
	if('tc' in value):
		return ListaCentros_variacao[1:]
	else:
		return estado	
##################


##########
##########
########## CONTAGEM DE PALAVRAS
@app.callback(
	dash.dependencies.Output("grafico_contagem_palavras", "children"),
	[dash.dependencies.Input("dropdown_anos_contagem", "value"),
	dash.dependencies.Input("palavra_contagem", "value"),
	dash.dependencies.Input("dropdown_centros_contagem", "value"),
	dash.dependencies.Input("tab_escolha_grafico","value")] #######################
)
def grafico(dropdown_anos_contagem, palavra_contagem,dropdown_centros_contagem,tab_escolha_grafico):
	
	if tab_escolha_grafico == "contagem_palavras":
		centros_selecionados = []
		tamanho_anos = 0
		anos = []
		palavras_input_ = str(palavra_contagem)
		palavras_input = palavras_input_.lower()
		palavras_input = und.unidecode(palavras_input)
		palavras = palavras_input.split(',')
		#------------
		valores = []
		valores1 = []
		valores2 = []
		valores3 = []
		valores4 = []
		valores5 = []
		valores6 = []
		
		valores_arredondados = []
		x = ''
		y = ''

		df_17= pd.read_csv('apps/Apoio/dataset_2017.csv')
		df_18= pd.read_csv('apps/Apoio/dataset_2018.csv')
		df_19= pd.read_csv('apps/Apoio/dataset_2019.csv')
		df_20= pd.read_csv('apps/Apoio/dataset_2020.csv')
		df_21= pd.read_csv('apps/Apoio/dataset_2021.csv')
		df_22= pd.read_csv('apps/Apoio/dataset_2022.csv')

		textos_2017 = pd.read_csv('apps/Apoio/Dataframes/textos_contagem_2017.csv')
		textos_2018 = pd.read_csv('apps/Apoio/Dataframes/textos_contagem_2018.csv')
		textos_2019 = pd.read_csv('apps/Apoio/Dataframes/textos_contagem_2019.csv')
		textos_2020 = pd.read_csv('apps/Apoio/Dataframes/textos_contagem_2020.csv')
		textos_2021 = pd.read_csv('apps/Apoio/Dataframes/textos_contagem_2022.csv')
		textos_2022 = pd.read_csv('apps/Apoio/Dataframes/textos_contagem_2022.csv')


		encontrados_17 = []
		encontrados_18 = []
		encontrados_19 = []
		encontrados_20 = []
		encontrados_21 = []
		encontrados_22 = []

		normalizado_17 = []
		normalizado_18 = []
		normalizado_19 = []
		normalizado_20 = []
		normalizado_21 = []
		normalizado_22 = []


		for i in Lista_Centros:
			text = list(textos_2017[i])
			text = ' '.join(text)
			text1 = list(textos_2018[i])
			text1 = ' '.join(text1)
			text2 = list(textos_2019[i])
			text2 = ' '.join(text2)
			text3 = list(textos_2020[i])
			text3 = ' '.join(text3)
			text4 = list(textos_2021[i])
			text4 = ' '.join(text4)
			text5 = list(textos_2022[i])
			text5 = ' '.join(text5)

			

			for n in range(0, len(palavras)):
				palavra = re.compile(palavras[n])
				p = palavra.findall(text)
				tam = len(p)
				p1 = palavra.findall(text1)
				tam1 = len(p1)
				p2 = palavra.findall(text2)
				tam2 = len(p2)
				p3 = palavra.findall(text3)
				tam3 = len(p)
				p4 = palavra.findall(text4)
				tam4 = len(p1)
				p5 = palavra.findall(text5)
				tam5 = len(p2)

				encontrados_17.append(tam)
				encontrados_18.append(tam1)
				encontrados_19.append(tam2)
				encontrados_20.append(tam3)
				encontrados_21.append(tam4)
				encontrados_22.append(tam5)

			total  = sum(encontrados_17) # atribui o números de elementos da lista a uma variável
			total1 = sum(encontrados_18)
			total2 = sum(encontrados_19)
			total3 = sum(encontrados_20) # atribui o números de elementos da lista a uma variável
			total4 = sum(encontrados_21)
			total5 = sum(encontrados_22)

			quant = int(df_17[i])
			quant1 = int(df_18[i])
			quant2 = int(df_19[i])
			quant3 = int(df_20[i])
			quant4 = int(df_21[i])
			quant5 = int(df_22[i])

			normalizado_17.append(total/quant)
			normalizado_18.append(total1/quant1)
			normalizado_19.append(total2/quant2)
			normalizado_20.append(total3/quant3)
			normalizado_21.append(total4/quant4)
			normalizado_22.append(total5/quant5)



		if('2017' in dropdown_anos_contagem):
			anos.append('2017')
			tamanho_anos += 1

		if('2018' in dropdown_anos_contagem):
			anos.append('2018')
			tamanho_anos += 1

		if('2019' in dropdown_anos_contagem):
			anos.append('2019')
			tamanho_anos += 1

		if('2020' in dropdown_anos_contagem):
			anos.append('2020')
			tamanho_anos += 1

		if('2021' in dropdown_anos_contagem):
			anos.append('2021')
			tamanho_anos += 1

		if('2022' in dropdown_anos_contagem):
			anos.append('2022')
			tamanho_anos += 1
		
		for i in dropdown_centros_contagem :
			if (i in Lista_Centros[0:]):
				centros_selecionados.append(i)
			else:
				None
		

		if(tamanho_anos == 1):
			print(tamanho_anos)
			if('2017' in anos):
				data = dict(zip(Lista_Centros,normalizado_17))
				data = dict(sorted(data.items(),key=itemgetter(1)))
				dataframe_ = pd.DataFrame(data = data, index = ['numero'])
				dataframe = dataframe_[centros_selecionados]
				valores = list(dataframe.loc['numero'])
				valores_arredondados = []

			elif('2018' in anos):
				data = dict(zip(Lista_Centros,normalizado_18))
				data = dict(sorted(data.items(),key=itemgetter(1)))
				dataframe_ = pd.DataFrame(data = data, index = ['numero'])
				dataframe = dataframe_[centros_selecionados]
				valores = list(dataframe.loc['numero'])
				valores_arredondados = []

			elif('2019' in anos):
				data = dict(zip(Lista_Centros,normalizado_19))
				data = dict(sorted(data.items(),key=itemgetter(1)))
				dataframe_ = pd.DataFrame(data = data, index = ['numero'])
				dataframe = dataframe_[centros_selecionados]
				valores = list(dataframe.loc['numero'])
				valores_arredondados = []

			elif('2020' in anos):
				data = dict(zip(Lista_Centros,normalizado_20))
				data = dict(sorted(data.items(),key=itemgetter(1)))
				dataframe_ = pd.DataFrame(data = data, index = ['numero'])
				dataframe = dataframe_[centros_selecionados]
				valores = list(dataframe.loc['numero'])
				valores_arredondados = []

			elif('2021' in anos):
				data = dict(zip(Lista_Centros,normalizado_21))
				data = dict(sorted(data.items(),key=itemgetter(1)))
				dataframe_ = pd.DataFrame(data = data, index = ['numero'])
				dataframe = dataframe_[centros_selecionados]
				valores = list(dataframe.loc['numero'])
				valores_arredondados = []

			elif('2022' in anos):
				data = dict(zip(Lista_Centros,normalizado_22))
				data = dict(sorted(data.items(),key=itemgetter(1)))
				dataframe_ = pd.DataFrame(data = data, index = ['numero'])
				dataframe = dataframe_[centros_selecionados]
				valores = list(dataframe.loc['numero'])
				valores_arredondados = []
			
			

			for j in valores:
				val = round(j,2)
				valores_arredondados.append(val)
				x = dataframe.columns.to_list()
				y = valores_arredondados

			return dcc.Graph(
					id='g1_contagem_palavras',
					figure={
							'data': [
									{'x': x , 'y': y, 'type': 'bar', 'name': str(anos[0])},
									],
							'layout': {
									'title': 'Gráfico da quantidade das palavras - {} normalizadas por Centro - ({})'.format(palavras_input_, anos)
									}
							})

		elif(tamanho_anos == 2):
			valores_arredondados = []
			valores1 = []
			valores2 = []
			valores3 = []
			valores4 = []
			valores5 = []
			valores6 = []
			anos = []

			if('2017' in dropdown_anos_contagem):
					data = dict(zip(Lista_Centros,normalizado_17))
					data = dict(sorted(data.items(),key=itemgetter(1)))
					dataframe_ = pd.DataFrame(data = data, index = ['numero'])
					dataframe = dataframe_[centros_selecionados]
					valores1 = list(dataframe.loc['numero'])
					anos.append('2017')
					listaaux1 = []
					for j in valores1:
							val = round(j,2)
							listaaux1.append(val)
					valores_arredondados.append(listaaux1)
					
			if('2018' in dropdown_anos_contagem):
					data = dict(zip(Lista_Centros,normalizado_18))
					data = dict(sorted(data.items(),key=itemgetter(1)))
					dataframe_ = pd.DataFrame(data = data, index = ['numero'])
					dataframe = dataframe_[centros_selecionados]
					valores2 = list(dataframe.loc['numero'])
					anos.append('2018')
					listaaux2 = []
					for j in valores2:
							val = round(j,2)
							listaaux2.append(val)
					valores_arredondados.append(listaaux2)

			if('2019' in dropdown_anos_contagem):
					data = dict(zip(Lista_Centros,normalizado_19))
					data = dict(sorted(data.items(),key=itemgetter(1)))
					dataframe_ = pd.DataFrame(data = data, index = ['numero'])
					dataframe = dataframe_[centros_selecionados]
					valores3 = list(dataframe.loc['numero'])
					anos.append('2019')
					listaaux3 = []
					for j in valores3:
							val = round(j,2)
							listaaux3.append(val)
					valores_arredondados.append(listaaux3)

					
			if('2020' in dropdown_anos_contagem):
					data = dict(zip(Lista_Centros,normalizado_20))
					data = dict(sorted(data.items(),key=itemgetter(1)))
					dataframe_ = pd.DataFrame(data = data, index = ['numero'])
					dataframe = dataframe_[centros_selecionados]
					valores4 = list(dataframe.loc['numero'])
					anos.append('2020')
					listaaux4 = []
					for j in valores4:
							val = round(j,2)
							listaaux4.append(val)
					valores_arredondados.append(listaaux4)
							
			if('2021' in dropdown_anos_contagem):
					data = dict(zip(Lista_Centros,normalizado_21))
					data = dict(sorted(data.items(),key=itemgetter(1)))
					dataframe_ = pd.DataFrame(data = data, index = ['numero'])
					dataframe = dataframe_[centros_selecionados]
					valores5 = list(dataframe.loc['numero'])
					anos.append('2021')
					listaaux5 = []
					for j in valores5:
							val = round(j,2)
							listaaux5.append(val)
					valores_arredondados.append(listaaux5)

			if('2022' in dropdown_anos_contagem):
					data = dict(zip(Lista_Centros,normalizado_22))
					data = dict(sorted(data.items(),key=itemgetter(1)))
					dataframe_ = pd.DataFrame(data = data, index = ['numero'])
					dataframe = dataframe_[centros_selecionados]
					valores6 = list(dataframe.loc['numero'])
					anos.append('2022')
					listaaux6 = []
					for j in valores6:
							val = round(j,2)
							listaaux6.append(val)
					valores_arredondados.append(listaaux6)

			x = dataframe.columns.to_list()
			y1 = valores_arredondados[0]
			y2 = valores_arredondados[1]

			return dcc.Graph(
					id='g1_contagem_palavras',
					figure={
							'data': [
									{'x': x , 'y': y1, 'type': 'bar', 'name': str(anos[0])},
									{'x': x , 'y': y2, 'type': 'bar', 'name': str(anos[1])},
									],
							'layout': {
									'title': 'Gráfico da quantidade das palavras - {} normalizadas por Centro - ({})'.format(palavras_input_, anos)
									}
							})
		
		elif(tamanho_anos == 3):
			valores_arredondados = []
			valores1 = []
			valores2 = []
			valores3 = []
			valores4 = []
			valores5 = []
			valores6 = []
			anos = []

			if('2017' in dropdown_anos_contagem):
					data = dict(zip(Lista_Centros,normalizado_17))
					data = dict(sorted(data.items(),key=itemgetter(1)))
					dataframe_ = pd.DataFrame(data = data, index = ['numero'])
					dataframe = dataframe_[centros_selecionados]
					valores1 = list(dataframe.loc['numero'])
					anos.append('2017')
					listaaux1 = []
					for j in valores1:
							val = round(j,2)
							listaaux1.append(val)
					valores_arredondados.append(listaaux1)
					
			if('2018' in dropdown_anos_contagem):
					data = dict(zip(Lista_Centros,normalizado_18))
					data = dict(sorted(data.items(),key=itemgetter(1)))
					dataframe_ = pd.DataFrame(data = data, index = ['numero'])
					dataframe = dataframe_[centros_selecionados]
					valores2 = list(dataframe.loc['numero'])
					anos.append('2018')
					listaaux2 = []
					for j in valores2:
							val = round(j,2)
							listaaux2.append(val)
					valores_arredondados.append(listaaux2)

			if('2019' in dropdown_anos_contagem):
					data = dict(zip(Lista_Centros,normalizado_19))
					data = dict(sorted(data.items(),key=itemgetter(1)))
					dataframe_ = pd.DataFrame(data = data, index = ['numero'])
					dataframe = dataframe_[centros_selecionados]
					valores3 = list(dataframe.loc['numero'])
					anos.append('2019')
					listaaux3 = []
					for j in valores3:
							val = round(j,2)
							listaaux3.append(val)
					valores_arredondados.append(listaaux3)

					
			if('2020' in dropdown_anos_contagem):
					data = dict(zip(Lista_Centros,normalizado_20))
					data = dict(sorted(data.items(),key=itemgetter(1)))
					dataframe_ = pd.DataFrame(data = data, index = ['numero'])
					dataframe = dataframe_[centros_selecionados]
					valores4 = list(dataframe.loc['numero'])
					anos.append('2020')
					listaaux4 = []
					for j in valores4:
							val = round(j,2)
							listaaux4.append(val)
					valores_arredondados.append(listaaux4)
							
			if('2021' in dropdown_anos_contagem):
					data = dict(zip(Lista_Centros,normalizado_21))
					data = dict(sorted(data.items(),key=itemgetter(1)))
					dataframe_ = pd.DataFrame(data = data, index = ['numero'])
					dataframe = dataframe_[centros_selecionados]
					valores5 = list(dataframe.loc['numero'])
					anos.append('2021')
					listaaux5 = []
					for j in valores5:
							val = round(j,2)
							listaaux5.append(val)
					valores_arredondados.append(listaaux5)

			if('2022' in dropdown_anos_contagem):
					data = dict(zip(Lista_Centros,normalizado_22))
					data = dict(sorted(data.items(),key=itemgetter(1)))
					dataframe_ = pd.DataFrame(data = data, index = ['numero'])
					dataframe = dataframe_[centros_selecionados]
					valores6 = list(dataframe.loc['numero'])
					anos.append('2022')
					listaaux6 = []
					for j in valores6:
							val = round(j,2)
							listaaux6.append(val)
					valores_arredondados.append(listaaux6)

			x = dataframe.columns.to_list()
			y1 = valores_arredondados[0]
			y2 = valores_arredondados[1]
			y3 = valores_arredondados[2]

			return dcc.Graph(
					id='g1_contagem_palavras',
					figure={
							'data': [
									{'x': x , 'y': y1, 'type': 'bar', 'name': str(anos[0])},
									{'x': x , 'y': y2, 'type': 'bar', 'name': str(anos[1])},
									{'x': x , 'y': y3, 'type': 'bar', 'name': str(anos[2])},
									],
							'layout': {
									'title': 'Gráfico da quantidade das palavras - {} normalizadas por Centro - ({})'.format(palavras_input_, anos)
									}
							})

		elif(tamanho_anos == 4):
			valores_arredondados = []
			valores1 = []
			valores2 = []
			valores3 = []
			valores4 = []
			valores5 = []
			valores6 = []
			anos = []

			if('2017' in dropdown_anos_contagem):
					data = dict(zip(Lista_Centros,normalizado_17))
					data = dict(sorted(data.items(),key=itemgetter(1)))
					dataframe_ = pd.DataFrame(data = data, index = ['numero'])
					dataframe = dataframe_[centros_selecionados]
					valores1 = list(dataframe.loc['numero'])
					anos.append('2017')
					listaaux1 = []
					for j in valores1:
							val = round(j,2)
							listaaux1.append(val)
					valores_arredondados.append(listaaux1)
					
			if('2018' in dropdown_anos_contagem):
					data = dict(zip(Lista_Centros,normalizado_18))
					data = dict(sorted(data.items(),key=itemgetter(1)))
					dataframe_ = pd.DataFrame(data = data, index = ['numero'])
					dataframe = dataframe_[centros_selecionados]
					valores2 = list(dataframe.loc['numero'])
					anos.append('2018')
					listaaux2 = []
					for j in valores2:
							val = round(j,2)
							listaaux2.append(val)
					valores_arredondados.append(listaaux2)

			if('2019' in dropdown_anos_contagem):
					data = dict(zip(Lista_Centros,normalizado_19))
					data = dict(sorted(data.items(),key=itemgetter(1)))
					dataframe_ = pd.DataFrame(data = data, index = ['numero'])
					dataframe = dataframe_[centros_selecionados]
					valores3 = list(dataframe.loc['numero'])
					anos.append('2019')
					listaaux3 = []
					for j in valores3:
							val = round(j,2)
							listaaux3.append(val)
					valores_arredondados.append(listaaux3)

					
			if('2020' in dropdown_anos_contagem):
					data = dict(zip(Lista_Centros,normalizado_20))
					data = dict(sorted(data.items(),key=itemgetter(1)))
					dataframe_ = pd.DataFrame(data = data, index = ['numero'])
					dataframe = dataframe_[centros_selecionados]
					valores4 = list(dataframe.loc['numero'])
					anos.append('2020')
					listaaux4 = []
					for j in valores4:
							val = round(j,2)
							listaaux4.append(val)
					valores_arredondados.append(listaaux4)
							
			if('2021' in dropdown_anos_contagem):
					data = dict(zip(Lista_Centros,normalizado_21))
					data = dict(sorted(data.items(),key=itemgetter(1)))
					dataframe_ = pd.DataFrame(data = data, index = ['numero'])
					dataframe = dataframe_[centros_selecionados]
					valores5 = list(dataframe.loc['numero'])
					anos.append('2021')
					listaaux5 = []
					for j in valores5:
							val = round(j,2)
							listaaux5.append(val)
					valores_arredondados.append(listaaux5)

			if('2022' in dropdown_anos_contagem):
					data = dict(zip(Lista_Centros,normalizado_22))
					data = dict(sorted(data.items(),key=itemgetter(1)))
					dataframe_ = pd.DataFrame(data = data, index = ['numero'])
					dataframe = dataframe_[centros_selecionados]
					valores6 = list(dataframe.loc['numero'])
					anos.append('2022')
					listaaux6 = []
					for j in valores6:
							val = round(j,2)
							listaaux6.append(val)
					valores_arredondados.append(listaaux6)

			x = dataframe.columns.to_list()
			y1 = valores_arredondados[0]
			y2 = valores_arredondados[1]
			y3 = valores_arredondados[2]
			y4 = valores_arredondados[3]

			return dcc.Graph(
					id='g1_contagem_palavras',
					figure={
							'data': [
									{'x': x , 'y': y1, 'type': 'bar', 'name': str(anos[0])},
									{'x': x , 'y': y2, 'type': 'bar', 'name': str(anos[1])},
									{'x': x , 'y': y3, 'type': 'bar', 'name': str(anos[2])},
									{'x': x , 'y': y4, 'type': 'bar', 'name': str(anos[3])},
									],
							'layout': {
									'title': 'Gráfico da quantidade das palavras - {} normalizadas por Centro - ({})'.format(palavras_input_, anos)
									}
							})

		elif(tamanho_anos == 5):
			valores_arredondados = []
			valores1 = []
			valores2 = []
			valores3 = []
			valores4 = []
			valores5 = []
			valores6 = []
			anos = []

			if('2017' in dropdown_anos_contagem):
					data = dict(zip(Lista_Centros,normalizado_17))
					data = dict(sorted(data.items(),key=itemgetter(1)))
					dataframe_ = pd.DataFrame(data = data, index = ['numero'])
					dataframe = dataframe_[centros_selecionados]
					valores1 = list(dataframe.loc['numero'])
					anos.append('2017')
					listaaux1 = []
					for j in valores1:
							val = round(j,2)
							listaaux1.append(val)
					valores_arredondados.append(listaaux1)
					
			if('2018' in dropdown_anos_contagem):
					data = dict(zip(Lista_Centros,normalizado_18))
					data = dict(sorted(data.items(),key=itemgetter(1)))
					dataframe_ = pd.DataFrame(data = data, index = ['numero'])
					dataframe = dataframe_[centros_selecionados]
					valores2 = list(dataframe.loc['numero'])
					anos.append('2018')
					listaaux2 = []
					for j in valores2:
							val = round(j,2)
							listaaux2.append(val)
					valores_arredondados.append(listaaux2)

			if('2019' in dropdown_anos_contagem):
					data = dict(zip(Lista_Centros,normalizado_19))
					data = dict(sorted(data.items(),key=itemgetter(1)))
					dataframe_ = pd.DataFrame(data = data, index = ['numero'])
					dataframe = dataframe_[centros_selecionados]
					valores3 = list(dataframe.loc['numero'])
					anos.append('2019')
					listaaux3 = []
					for j in valores3:
							val = round(j,2)
							listaaux3.append(val)
					valores_arredondados.append(listaaux3)

					
			if('2020' in dropdown_anos_contagem):
					data = dict(zip(Lista_Centros,normalizado_20))
					data = dict(sorted(data.items(),key=itemgetter(1)))
					dataframe_ = pd.DataFrame(data = data, index = ['numero'])
					dataframe = dataframe_[centros_selecionados]
					valores4 = list(dataframe.loc['numero'])
					anos.append('2020')
					listaaux4 = []
					for j in valores4:
							val = round(j,2)
							listaaux4.append(val)
					valores_arredondados.append(listaaux4)
							
			if('2021' in dropdown_anos_contagem):
					data = dict(zip(Lista_Centros,normalizado_21))
					data = dict(sorted(data.items(),key=itemgetter(1)))
					dataframe_ = pd.DataFrame(data = data, index = ['numero'])
					dataframe = dataframe_[centros_selecionados]
					valores5 = list(dataframe.loc['numero'])
					anos.append('2021')
					listaaux5 = []
					for j in valores5:
							val = round(j,2)
							listaaux5.append(val)
					valores_arredondados.append(listaaux5)

			if('2022' in dropdown_anos_contagem):
					data = dict(zip(Lista_Centros,normalizado_22))
					data = dict(sorted(data.items(),key=itemgetter(1)))
					dataframe_ = pd.DataFrame(data = data, index = ['numero'])
					dataframe = dataframe_[centros_selecionados]
					valores6 = list(dataframe.loc['numero'])
					anos.append('2022')
					listaaux6 = []
					for j in valores6:
							val = round(j,2)
							listaaux6.append(val)
					valores_arredondados.append(listaaux6)

			x = dataframe.columns.to_list()
			y1 = valores_arredondados[0]
			y2 = valores_arredondados[1]
			y3 = valores_arredondados[2]
			y4 = valores_arredondados[3]
			y5 = valores_arredondados[4]

			return dcc.Graph(
					id='g1_contagem_palavras',
					figure={
							'data': [
									{'x': x , 'y': y1, 'type': 'bar', 'name': str(anos[0])},
									{'x': x , 'y': y2, 'type': 'bar', 'name': str(anos[1])},
									{'x': x , 'y': y3, 'type': 'bar', 'name': str(anos[2])},
									{'x': x , 'y': y4, 'type': 'bar', 'name': str(anos[3])},
									{'x': x , 'y': y5, 'type': 'bar', 'name': str(anos[4])},
									],
							'layout': {
									'title': 'Gráfico da quantidade das palavras - {} normalizadas por Centro - ({})'.format(palavras_input_, anos)
									}
							})


		elif(tamanho_anos == 6):
			valores_arredondados = []
			valores1 = []
			valores2 = []
			valores3 = []
			valores4 = []
			valores5 = []
			valores6 = []
			anos = []

			if('2017' in dropdown_anos_contagem):
					data = dict(zip(Lista_Centros,normalizado_17))
					data = dict(sorted(data.items(),key=itemgetter(1)))
					dataframe_ = pd.DataFrame(data = data, index = ['numero'])
					dataframe = dataframe_[centros_selecionados]
					valores1 = list(dataframe.loc['numero'])
					anos.append('2017')
					listaaux1 = []
					for j in valores1:
							val = round(j,2)
							listaaux1.append(val)
					valores_arredondados.append(listaaux1)
					
			if('2018' in dropdown_anos_contagem):
					data = dict(zip(Lista_Centros,normalizado_18))
					data = dict(sorted(data.items(),key=itemgetter(1)))
					dataframe_ = pd.DataFrame(data = data, index = ['numero'])
					dataframe = dataframe_[centros_selecionados]
					valores2 = list(dataframe.loc['numero'])
					anos.append('2018')
					listaaux2 = []
					for j in valores2:
							val = round(j,2)
							listaaux2.append(val)
					valores_arredondados.append(listaaux2)

			if('2019' in dropdown_anos_contagem):
					data = dict(zip(Lista_Centros,normalizado_19))
					data = dict(sorted(data.items(),key=itemgetter(1)))
					dataframe_ = pd.DataFrame(data = data, index = ['numero'])
					dataframe = dataframe_[centros_selecionados]
					valores3 = list(dataframe.loc['numero'])
					anos.append('2019')
					listaaux3 = []
					for j in valores3:
							val = round(j,2)
							listaaux3.append(val)
					valores_arredondados.append(listaaux3)

					
			if('2020' in dropdown_anos_contagem):
					data = dict(zip(Lista_Centros,normalizado_20))
					data = dict(sorted(data.items(),key=itemgetter(1)))
					dataframe_ = pd.DataFrame(data = data, index = ['numero'])
					dataframe = dataframe_[centros_selecionados]
					valores4 = list(dataframe.loc['numero'])
					anos.append('2020')
					listaaux4 = []
					for j in valores4:
							val = round(j,2)
							listaaux4.append(val)
					valores_arredondados.append(listaaux4)
							
			if('2021' in dropdown_anos_contagem):
					data = dict(zip(Lista_Centros,normalizado_21))
					data = dict(sorted(data.items(),key=itemgetter(1)))
					dataframe_ = pd.DataFrame(data = data, index = ['numero'])
					dataframe = dataframe_[centros_selecionados]
					valores5 = list(dataframe.loc['numero'])
					anos.append('2021')
					listaaux5 = []
					for j in valores5:
							val = round(j,2)
							listaaux5.append(val)
					valores_arredondados.append(listaaux5)

			if('2022' in dropdown_anos_contagem):
					data = dict(zip(Lista_Centros,normalizado_22))
					data = dict(sorted(data.items(),key=itemgetter(1)))
					dataframe_ = pd.DataFrame(data = data, index = ['numero'])
					dataframe = dataframe_[centros_selecionados]
					valores6 = list(dataframe.loc['numero'])
					anos.append('2022')
					listaaux6 = []
					for j in valores6:
							val = round(j,2)
							listaaux6.append(val)
					valores_arredondados.append(listaaux6)

			x = dataframe.columns.to_list()
			y1 = valores_arredondados[0]
			y2 = valores_arredondados[1]
			y3 = valores_arredondados[2]
			y4 = valores_arredondados[3]
			y5 = valores_arredondados[4]
			y6 = valores_arredondados[5]

			return dcc.Graph(
					id='g1_contagem_palavras',
					figure={
							'data': [
									{'x': x , 'y': y1, 'type': 'bar', 'name': str(anos[0])},
									{'x': x , 'y': y2, 'type': 'bar', 'name': str(anos[1])},
									{'x': x , 'y': y3, 'type': 'bar', 'name': str(anos[2])},
									{'x': x , 'y': y4, 'type': 'bar', 'name': str(anos[3])},
									{'x': x , 'y': y5, 'type': 'bar', 'name': str(anos[4])},
									{'x': x , 'y': y6, 'type': 'bar', 'name': str(anos[5])},
									],
							'layout': {
									'title': 'Gráfico da quantidade das palavras - {} normalizadas por Centro - ({})'.format(palavras_input_, anos)
									}
							})


@app.callback(
	Output("dropdown_anos_contagem","value"),
	[Input("checklist_anos_contagem", "value")],[State("dropdown_anos_contagem", "value")]
)
def retornar_anos_dropdown(value,estado):
	if('ta' in value):
		return ["2017","2018","2019","2020","2021","2022"]
	else:
		return estado

@app.callback(
	Output("dropdown_centros_contagem","value"),
	[Input("checklist_centros_contagem", "value")],[State("dropdown_centros_contagem", "value")]
)
def retornar_anos_dropdown(value,estado):
	if('tc' in value):
		return ['CCS','CEAR','CCEN','CT','CCM','CBIOTEC','CTDR','CCHLA','CCTA','CCHSA','CCSA','CI','CCAE','CCJ','CCA','CE']
	else:
		return estado

#Parte que exibe a descrição dos gráficos na parte inferior esquerda da página
@app.callback(
	Output("relatorio_estudo_vocabular","children"),
	[Input("tab_escolha_grafico", "value"),
	Input("dropdown_anos_variacao","value"),
	Input("dropdown_centros_variacao","value"),
	Input("dropdown_modalidades_variacao","value"),
	Input("dropdown_classes_analise","value"),
	Input("dropdown_centros_analise","value"),
	Input("dropdown_modalidades_analise","value"),
	Input("dropdown_anos_nuvem", "value"),
	Input("dropdown_centros_nuvem", "value"),
	Input("dropdown_modalidades_nuvem","value"),
	Input("dropdown_anos_contagem", "value"),
	Input("dropdown_centros_contagem", "value"),
	Input("palavra_contagem","value")],
)
def relatorio_estudo_vocabular(value, dropdown_anos_variacao, dropdown_centros_variacao, dropdown_modalidades_variacao, dropdown_classes_analise, dropdown_centros_analise,dropdown_modalidades_analise, dropdown_anos_nuvem, dropdown_centros_nuvem,dropdown_modalidades_nuvem,dropdown_anos_contagem,dropdown_centros_contagem, palavra_contagem):
	#######variação vocabular
	try:
		dropdown_anos_variacao = sorted(dropdown_anos_variacao)
		anos_variacao = ""
		for i in dropdown_anos_variacao:
		    if('2017' not in anos_variacao and '2018' not in anos_variacao and '2019' not in anos_variacao):
		        anos_variacao = anos_variacao + str(i)
		    else:
		        anos_variacao = anos_variacao + "," + str(i)

		centros_variacao = ""
		for i in dropdown_centros_variacao:
		    if('C' not in centros_variacao):
		        centros_variacao = centros_variacao + str(i.split(' -')[0])
		    else:
		        centros_variacao = centros_variacao + "," + str(i.split(' -')[0])

		campo_variacao = dropdown_modalidades_variacao
		if(campo_variacao == None):
			campo_variacao = ""
	######Análise Gramatical
	except:
		None

	try:	
		classes_analise = ""

		for i in dropdown_classes_analise:
			if(classes_analise != ''):
				classes_analise = classes_analise + "," +i
			else:
				classes_analise = classes_analise + i


		centros_analise =""
		for i in dropdown_centros_analise:
		    if('C' not in centros_analise):
		        centros_analise = centros_analise + str(i.split(' -')[0])
		    else:
		        centros_analise = centros_analise + "," + str(i.split(' -')[0])

		modalidades_analise = ""
		for i in dropdown_modalidades_analise:
			modalidades_analise += i

		if(modalidades_analise == None):
			modalidades_analise = ""

	except:
		None



	#Nuvem de Palavras
	try:
		anos_nuvem = ""
		for i in dropdown_anos_nuvem:
		    if('2017' not in anos_nuvem and '2018' not in anos_nuvem and '2019' not in anos_nuvem and '2020' not in anos_nuvem and '2021' not in anos_nuvem and '2022' not in anos_nuvem):
		        anos_nuvem = anos_nuvem + str(i)
		    else:
		        anos_nuvem = anos_nuvem + "," + str(i)

		centros_nuvem = ""
		for i in dropdown_centros_nuvem:
		    if('C' not in centros_nuvem):
		        centros_nuvem = centros_nuvem + str(i.split(' -')[0])
		    else:
		        centros_nuvem = centros_nuvem + "," + str(i.split(' -')[0])

		campo_nuvem = ""
		for i in dropdown_modalidades_nuvem:
			campo_nuvem += i

		if(campo_nuvem == None):
			campo_nuvem = ""


	#Contagem de Palavras
	except:
		None

	try:
		anos_contagem = ""
		for i in dropdown_anos_contagem:
		    if('2017' not in anos_contagem and '2018' not in anos_contagem and '2019' not in anos_contagem and '2020' not in anos_contagem and '2021' not in anos_contagem and '2022' not in anos_contagem):
		        anos_contagem = anos_contagem + str(i)
		    else:
		        anos_contagem = anos_contagem + "," + str(i)


		centros_contagem = ""
		for i in dropdown_centros_contagem:
		    if('C' not in centros_contagem):
		        centros_contagem = centros_contagem + str(i.split(' -')[0])
		    else:
		        centros_contagem = centros_contagem + "," + str(i.split(' -')[0])

	except:
		None



			

	if value == 'variabilidade_vocabular':
		try:
			return f'''O Gráfico apresentado mostra a Varibilidade Vocabular dos projetos de extensão da UFPB por Centro(s), Ano(s) e Campo. A variabilidade vocabular consiste na quantidade média de palavras dos projetos dos centros escolhidos, isto é o total de palavras dividido pelo total de projetos considerados daquele centro. Nesse caso em específico, você está observando a Variabilidade Vocabular do(s) Ano(s): {anos_variacao}, no(s) Centro(s): {centros_variacao}, e no Campo {campo_variacao}'''
		except:
			return ""

	elif value == 'analise_gramatical' :
		try:
			return f'''O Gráfico apresentado mostra uma Análise Vocabular dos projetos de extensão da UFPB por Classe(s) de Palavra(s), Centro(s) e Campo. A análise gramatical consiste na quantidade média de elementos de uma determinada classe gramatical (a quantidade total daquela classe naquele centro dividida pela quantidade total de projetos daquele centro). Nesse caso em específico, você está observando uma Análise Gramatical da(s) classe(s): {classes_analise}, no(s) centro(s): {centros_analise}, e no campo {modalidades_analise}, considerando uma média dos anos de 2017, 2018 e 2019.'''
		except:
			return ""

	elif value == 'nuvem_palavras' :
		try:
			return f'''O gráfico apresentado mostra uma Nuvem de Palavras com as palavras mais relevantes de determinado(s) Centro(s) em determinado(s) Ano(s). A nuvem de palavras consiste nas 20 principais palavras dos centros escolhidos nos anos escolhidos, ou seja, se você escolheu mais de um centro em mais de um ano, todas as palavras foram consideradas para a confecção desta nuvem. Nesse caso em específico, você está observando a Nuvem de Palavras do(s) Ano(s): {anos_nuvem}, no(s) Centro(s): {centros_nuvem}, e no campo {campo_nuvem}'''
	
		except:
			return ""

	elif value == 'contagem_palavras':
		try:
			return f'''Este gráfico mostra o número de ocorrências das palavras pesquisadas normalizadas por centro, podendo nos apontar as tendências de área de envolvimento comparadas por centro. Os campos que foram levados em consideração para a contagem foram : Justificativa, Metodologia, Fundamentação Teórica e Objetivos. Nesse caso em específico, você está observando o gráfico referente a contagem da palavra "{palavra_contagem}", no(s) Ano(s) {anos_contagem}, e no(s) Centro(s): {centros_contagem}'''
		except:
			return ""
	else:
		return ""




