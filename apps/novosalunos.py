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
from plotly.subplots import make_subplots     
import os  
import glob  
import pandas as pd 
from folium.plugins import MarkerCluster   
from dash.dependencies import Input, Output, State
from app import app

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

ano = [2017,2018,2019,2020,2021,2022,'Todos os anos']
centro = ['Todos os centros','CCHLA','CCS','CCA','CT','CCEN','CCTA','CCAE','CEAR','CCM','CTDR','CE','CBIOTEC','CCHSA','CCSA','CI','CCJ']
nav = navbar.Navbar()    
graf_rel = make_subplots(rows=1, cols=1,row_titles = ['Razão Alunos/Professores'],  shared_yaxes=True)
##########
tab_selected_style = {
    'font-size': '70%',
    'padding': '6px'
}

tab_style = { #Estilos das Tabs
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'font-size': '75%',
    'fontSize' : '13'
    }

##### opções de tabs na página discentes
#old-id = tabs-example
tabs = html.Div([
    dcc.Tabs(id='tabs-novos-alunos', value='tab-1', children=[
        dcc.Tab(label='Adriel', value='tab-1', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Lucca', value='tab-2', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Davi', value='tab-3', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Gabriel', value='tab-4', style=tab_style, selected_style=tab_selected_style),
])
    ,html.Br()])

####

#Campo responsável por mostrar a descrição geral dos gráficos, utilizando a biblioteca fstring para mudar textos durante a execução da aplicação
card_content = [
    dbc.CardHeader("Entendendo o gráfico",style={'font-size':24, 'textAlign':'center'}),
    dbc.CardBody(
        [
            html.P(
                children=f'''O gráfico analisado é a relação entre Discentes/Docentes, a fim de visualizar o envolvimento dos discentes 
                em projetos de extensão nos anos de 2017, 2018, 2019, 2020, 2021 e 2022. Podemos analisar que, como escolhido, está sendo filtrado em apenas 
                os centros: CEAR para serem visualizados. Esses dados foram representados em um grafico de barras. Com esses resultados pode-se 
                analisar os centros que possuem mais docentes que discentes, quando os valores obtidos forem menores que 1, e os que possuem 
                mais alunos que professores, para valores maiores que 1.''',
                className="card-text",id='relatorio-novos-discentes',style={'text-align':'justify'}
            ),
            #old-id = relatorio_discentes
        ]
    ),
]

jumbotron = dbc.Card(card_content,  outline=True)

### Parte da página que contém os dropdowns
card_content_2 = [
    dbc.CardHeader("Parâmetros do Gráfico",style={'font-size':24, 'textAlign':'center'}),
    dbc.CardBody(
        [
        tabs,
        html.H4("Escolha os anos que deseja analisar", style={'font-size':19}),
        dcc.Dropdown(
        id = 'ano-novos-alunos',  
        options=[
            {'label': j, 'value': j} for j in ano  
        ],
        value=[2017,2018,2019,2020,2021,2022],   
        multi=True,
    searchable=False,
         style={'margin-bottom':'10px'}
   

        ),        
        html.H4("Escolha os centros desejados", style={'font-size':19}),
        dcc.Dropdown(
        id = 'centro-novos-alunos',  
        options=[
            {'label': j, 'value': j} for j in centro  
        ],
        value=['CEAR'],   
        multi=True,
    searchable=True,
         style={'margin-bottom':'10px'}
   

    ),
        ]
    ),
]
#######

### Parte da página em que aparece a figura
jumbotron_2 = dbc.Card(card_content_2,  outline=True)
card_content_3 = [
    dbc.CardHeader(id='card-novos-alunos',style={'font-size':24, 'textAlign':'center'}),
    dbc.CardBody(
        [
            html.Div(id='graph-discentes-novos-alunos',
            style={'display':'block', 'max-width': '100%', 'margin-left': 'auto', 'margin-right': 'auto'}
            #esse style é o estilo com que a figura é mostrada
            )
        ]
    ),
]

jumbotron_3 = dbc.Card(card_content_3,  outline=True)



body_rel =html.Div([  

    

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

#esses modais são templates para mostrar erros de acordo com a escolha errada do usuário
modal_3 = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader("ERROR"),
                dbc.ModalBody("Escolha pelo menos um centro como parâmetro de entrada de centros"),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close_3-novos-alunos", className="ml-auto")
                ),
            ],
            id="modal_3-novos-alunos",
        ),
    ]
)

modal_4 = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader("ERROR"),
                dbc.ModalBody("Escolha pelo menos um ano como parâmetro de entrada de anos"),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close_4-novos-alunos", className="ml-auto")
                ),
            ],
            id="modal_4-novos-alunos",
        ),
    ]
)
#############################


### Até essa parte temos apenas o layout da nossa página que é guardada na variável layout para depois ser importada no arquivo index.py que chama o layout de acordo com a url esoclhida.
layout = html.Div([
nav,
body_rel,
modal_3,
modal_4
])


## Essa parte de baixo é a referente a interatividade do site, através das callbacks
    # os códigos abaixo dizem respeito a confecção de cada gráfico

#mostra os gráficos de acordo com a escolha da tab, ano e centro, escolhidos pelo usuário
@app.callback(
	Output("graph-discentes-novos-alunos", "children"),
	[Input("centro-novos-alunos", "value"),
	Input("ano-novos-alunos", "value"), Input("tabs-novos-alunos","value")],
)
def update_graph_discentes(centro, ano, tab):
    if tab == 'tab-1':        
        df_rel = (pd.read_csv("apps/Apoio/relacao_novo.csv").sort_values(by=str(ano[0]))) if len(ano) == 1 else pd.read_csv("apps/Apoio/relacao_novo.csv")
        graf_rel = make_subplots(rows=1, cols=1,row_titles = ['Razão Alunos/Professores'],  shared_yaxes=True)
        for a in ano: 
            graf_rel.add_trace(go.Bar(x=df_rel[df_rel['centro'].isin(centro)]['centro'].to_list(), y=df_rel[df_rel['centro'].isin(centro)][str(a)].to_list(), name=str(a), text=df_rel[df_rel['centro'].isin(centro)][str(a)].to_list(), textposition='auto',),1,1)
            graf_rel.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=True)
            graf_rel.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))
        graf_rel.update_layout(yaxis = dict(tickmode = 'linear', tick0 = 0, dtick = 0.5))
        return dcc.Graph(figure=graf_rel)
    elif tab == 'tab-2':
        df_rel = (pd.read_csv('apps/Apoio/evo.csv').sort_values(by=str(ano[0]))) if len(ano) == 1 else pd.read_csv('apps/Apoio/evo.csv')
        graf_rel = make_subplots(rows=1, cols=1,row_titles = ['Quantidade de Discentes'],  shared_yaxes=True)
        for a in ano:
                graf_rel.add_trace(go.Bar(x=df_rel[df_rel['centro'].isin(centro)]['centro'].to_list(), y=df_rel[df_rel['centro'].isin(centro)][str(a)].to_list(), name=str(a), text=df_rel[df_rel['centro'].isin(centro)][str(a)].to_list(), textposition='auto',),1,1)
                graf_rel.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=True)
                graf_rel.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))
        return dcc.Graph(figure=graf_rel)
    elif tab == 'tab-3':
        df_rel = (pd.read_csv('apps/Apoio/rel_dis_pro.csv').sort_values(by=str(ano[0]))) if len(ano) == 1 else pd.read_csv('apps/Apoio/rel_dis_pro.csv')
        graf_rel = make_subplots(rows=1, cols=1,row_titles = ['Razão Alunos/Projeto'],  shared_yaxes=True)
        for a in ano:
                graf_rel.add_trace(go.Bar(x=df_rel[df_rel['centro'].isin(centro)]['centro'].to_list(), y=df_rel[df_rel['centro'].isin(centro)][str(a)].to_list(), name=str(a), text=df_rel[df_rel['centro'].isin(centro)][str(a)].to_list(), textposition='auto',),1,1)
                graf_rel.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=True)
                graf_rel.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))
        return dcc.Graph(figure=graf_rel)
    elif tab == 'tab-4':
        df_rel = pd.read_csv('apps/Apoio/dis-pro.csv')
        graf_rel = make_subplots(rows=1, cols=1,  shared_yaxes=True)
        for a in ano:
                graf_rel.add_trace(go.Scatter(x=df_rel[(df_rel['ano']==a)&(df_rel['centros'].isin(centro))].groupby(['projetos'])['discentes'].sum().reset_index(level=0)['projetos'].to_list(), y=df_rel[(df_rel['ano']==a)&(df_rel['centros'].isin(centro))].groupby(['projetos'])['discentes'].sum().reset_index(level=0)['discentes'].to_list(), name=str(a), mode='markers'),1,1)
                graf_rel.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=True)
        graf_rel.update_layout(go.Layout(yaxis={'title':'Numero de Projetos'},xaxis={'title': 'Quantidade de discentes'}))
        return dcc.Graph(figure=graf_rel)

## Os dois próximos callbacks dizem respeito à seleção de todos os anos/todos os centros nos dropdowns
@app.callback(
	[Output("centro-novos-alunos", "value"),Output("modal_3-novos-alunos", "is_open")],
	[Input("ano-novos-alunos", "value"), Input("close_3-novos-alunos", "n_clicks")],
	[State("centro-novos-alunos", "value"),State("modal_3-novos-alunos", "is_open")],
)
def limite_centros(ano,n_rel, centro,is_open_rel):
	if 'Todos os centros' in centro:
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
	[Output("ano-novos-alunos", "value"),Output("modal_4-novos-alunos", "is_open")],
	[Input("centro-novos-alunos", "value"),Input("close_4-novos-alunos", "n_clicks")],
	[State("ano-novos-alunos", "value"),State("modal_4-novos-alunos", "is_open")],

)

def flag(centro,n_rel, ano, is_open_rel):
        if 'Todos os anos' in ano:
                return [[2017,2018,2019,2020,2021,2022],is_open_rel]
        if len(ano) == 0:
                return [[2020], not is_open_rel]
        else:
                if n_rel:
                        if is_open_rel == True:
                                return [ano, not is_open_rel]
                        return [ano, is_open_rel]
                return [ano, is_open_rel]


# parte da página em que a descrição é atualizada de acordo com a escolha do usuário, utilizando a bilioteca fstring.
@app.callback(
    Output("relatorio-novos-discentes", "children"),
	[Input("centro-novos-alunos", "value"),Input("ano-novos-alunos", "value"),
         Input("tabs-novos-alunos","value")]

)

def relatorio_discentes(centro,ano,tab):
        centro=", ".join(str(x) for x in centro)
        ano=", ".join(str(x) for x in sorted(ano))
        if tab == 'tab-1':
                return f'''O gráfico analisado é a relação entre Discentes/Docentes, a fim de visualizar o envolvimento dos discentes 
                                em projetos de extensão nos anos de {ano}. Podemos analisar que, como escolhido, está sendo filtrado em apenas 
                                os centros: {centro} para serem visualizados. Esses dados foram representados em um grafico de barras. Com esses resultados pode-se 
                                analisar os centros que possuem mais docentes que discentes, quando os valores obtidos forem menores que 1, e os que possuem 
                                mais alunos que professores, para valores maiores que 1.'''
        elif tab == 'tab-2':
                return f'''O gráfico analisado é o evolutivo dos discentes por centro, a fim de visualizar o envolvimento dos discentes 
                                em projetos de extensão nos anos de {ano}. Podemos analisar que, como escolhido, está sendo filtrado em apenas 
                                os centros: {centro} para serem visualizados. Esses dados foram representados em um grafico de barras. Com esses resultados pode-se 
                                analisar os centros que atraem mais alunos para projetos de estensão e nos permite fazer um comparativo com os outros centros.'''
        elif tab == 'tab-3':
                return f'''O gráfico analisado é a relação entre Discentes/Projeto, a fim de visualizar o envolvimento dos discentes 
                                em projetos de extensão nos anos de {ano}. Podemos analisar que, como escolhido, está sendo filtrado em apenas 
                                os centros: {centro} para serem visualizados. Esses dados foram representados em um grafico de barras. Com esses resultados pode-se 
                                analisar os centros que possuem a maior média de discentes por projetos.'''
        elif tab == 'tab-4':
                return f'''O gráfico analisado é a relação entre Discentes/Projeto, a fim de visualizar a quantidade de projetos que possuem apenas um discente,
                                dois discentes e assim sucessivamente, 
                                nos anos de {ano}. Podemos analisar que, como escolhido, está sendo filtrado em apenas 
                                os centros: {centro} para serem visualizados. Esses dados foram representados em um grafico de dispersão. Com esses resultados pode-se 
                                analisar os projetos que possuem mais discentes envolvidos.'''

        
        
## Modifica o título do gráfico mostrado de acordo com a tab escolhida.
@app.callback(
	Output("card-novos-alunos", "children"),
	[Input("tabs-novos-alunos","value")]
)

def graf_tit(tab):
        if tab == 'tab-1':
                return 'Gráfico da Relação de Discentes/Docentes por Centro'
        elif tab == 'tab-2':
                return 'Gráfico Evolutivo de Discentes por Centro'
        elif tab == 'tab-3':
                return 'Gráfico da Media de Discentes por Centro'
        elif tab == 'tab-4':
                return 'Gráfico da Relação de Discentes/Projeto por Centro'

