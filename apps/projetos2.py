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
import plotly.express as px

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

import plotly.io as pio
pio.templates.default = "plotly_white"


ano = [2017,2018,2019,2020,2021,'Todos os anos']
centro = ['Todos os centros','CCHLA','CCS','CCA','CT','CCEN','CCTA','CCAE','CEAR','CCM','CTDR','CE','CBIOTEC','CCHSA','CCSA','CI','CCJ']
nav = navbar.Navbar()    
graf_rel = make_subplots(rows=1, cols=1,row_titles = ['Razão Alunos/Professores'],  shared_yaxes=True)
##########
tab_selected_style = {
    'font-size': '66%',
    'padding': '6px',
    'font-weight': 'bold'
}

tab_style = { #Estilos das Tabs
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'font-size': '68%',
    'font-weight': 'bold'
}

##### opções de tabs na página discentes
tabs = html.Div([
    dcc.Tabs(id='tabs-proj2', value='tab-1', children=[
        dcc.Tab(label='Evolutivo de Projetos de Extensão', value='tab-1', style=tab_style, selected_style=tab_selected_style),

        dcc.Tab(label='Evolutivo Projetos de Pesquisa', value='tab-2', style=tab_style, selected_style=tab_selected_style),

        dcc.Tab(label='Razão entre Projetos de Pesquisa e Projetos de Extensão', value='tab-3', style=tab_style, selected_style=tab_selected_style),

        dcc.Tab(label='Relação entre Projetos de Pesquisa e Projetos de Extensão', value='tab-4', style=tab_style, selected_style=tab_selected_style),

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
                em projetos de extensão nos anos de 2017, 2018, 2019, 2020 e 2021. Podemos analisar que, como escolhido, está sendo filtrado em apenas 
                os centros: CEAR para serem visualizados. Esses dados foram representados em um grafico de barras. Com esses resultados pode-se 
                analisar os centros que possuem mais docentes que discentes, quando os valores obtidos forem menores que 1, e os que possuem 
                mais alunos que professores, para valores maiores que 1.''',
                className="card-text",id='relatorio_discentes_proj2',style={'text-align':'justify'}
            ),
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
        id = 'ano-proj2',  
        options=[
            {'label': j, 'value': j} for j in ano  
        ],
        value=[2017,2018,2019,2020,2021],   
        multi=True,
    searchable=False,
         style={'margin-bottom':'10px'}
   

        ),        
        html.H4("Escolha os centros desejados", style={'font-size':19}),
        dcc.Dropdown(
        id = "centro-proj2",  
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
    dbc.CardHeader(id='card_proj2',style={'font-size':24, 'textAlign':'center'}),
    dbc.CardBody(
        [
            html.Div(id='graph_discentes_proj2',
            style={'display':'flex','align-items':'center','justify-content':'center'}
            #esse style é o estilo com que a figura é mostrada
            )
        ],style={'display':'flex','align-items':'center','justify-content':'center'}
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
modal_5_proj2 = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader("ERROR"),
                dbc.ModalBody("Escolha pelo menos um centro como parâmetro de entrada de centros"),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close_3", className="ml-auto")
                ),
            ],
            id="modal_5_proj2",
        ),
    ]
)

modal_6_proj2 = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader("ERROR"),
                dbc.ModalBody("Escolha pelo menos um ano como parâmetro de entrada de anos"),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close_4", className="ml-auto")
                ),
            ],
            id="modal_6_proj2",
        ),
    ]
)
#############################


### Até essa parte temos apenas o layout da nossa página que é guardada na variável layout para depois ser importada no arquivo index.py que chama o layout de acordo com a url esoclhida.
layout = html.Div([
    nav,
    body_rel,
    modal_5_proj2,
    modal_6_proj2
])


## Essa parte de baixo é a referente a interatividade do site, através das callbacks
    # os códigos abaixo dizem respeito a confecção de cada gráfico

#mostra os gráficos de acordo com a escolha da tab, ano e centro, escolhidos pelo usuário
@app.callback(
	Output("graph_discentes_proj2", "children"),
	[Input("centro-proj2", "value"),
	Input("ano-proj2", "value"), Input("tabs-proj2","value")],
)
def update_graph_discentes_proj2(centro, ano, tab):
    if tab == 'tab-1':        
        df_rel = (pd.read_csv("apps/Apoio/docentesextensao.csv").sort_values(by=str(ano[0]))) if len(ano) == 1 else pd.read_csv("apps/Apoio/docentesextensao.csv")
        graf_rel = make_subplots(rows=1, cols=1,row_titles = ['Número de Projetos'],  shared_yaxes=True)
        for a in ano: 
            graf_rel.add_trace(go.Bar(x=df_rel[df_rel['centro'].isin(centro)]['centro'].to_list(), y=df_rel[df_rel['centro'].isin(centro)][str(a)].to_list(), name=str(a), text=df_rel[df_rel['centro'].isin(centro)][str(a)].to_list(), textposition='auto',),1,1)
            #graf_rel.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=True)
            #graf_rel.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))
            #graf_rel.update_layout(yaxis = dict(tickmode = 'linear', tick0 = 0, dtick = 0.5))
            graf_rel.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))

        graf_rel.update_layout(
            height = 500,
            width = 920,
        )

        return dcc.Graph(figure=graf_rel)


    elif tab == 'tab-2':
        df_rel = (pd.read_csv("apps/Apoio/docentespesquisa.csv").sort_values(by=str(ano[0]))) if len(ano) == 1 else pd.read_csv("apps/Apoio/docentespesquisa.csv")
        graf_rel = make_subplots(rows=1, cols=1,row_titles = ['Número de Projetos'],  shared_yaxes=True)
        for a in ano: 
            graf_rel.add_trace(go.Bar(x=df_rel[df_rel['centro'].isin(centro)]['centro'].to_list(), y=df_rel[df_rel['centro'].isin(centro)][str(a)].to_list(), name=str(a), text=df_rel[df_rel['centro'].isin(centro)][str(a)].to_list(), textposition='auto',),1,1)
            #graf_rel.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=True)
            #graf_rel.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))
            #graf_rel.update_layout(yaxis = dict(tickmode = 'linear', tick0 = 0, dtick = 0.5))

            graf_rel.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))
        
        graf_rel.update_layout(
            height = 500,
            width = 920,
        )

        return dcc.Graph(figure=graf_rel)

    elif tab == 'tab-3':
        df_rel = (pd.read_csv("apps/Apoio/docentesrelacao.csv").sort_values(by=str(ano[0]))) if len(ano) == 1 else pd.read_csv("apps/Apoio/docentesrelacao.csv")
        graf_rel = make_subplots(rows=1, cols=1,row_titles = ['Razão de Projetos'],  shared_yaxes=True)
        for a in ano: 
            graf_rel.add_trace(go.Bar(x=df_rel[df_rel['centro'].isin(centro)]['centro'].to_list(), y=df_rel[df_rel['centro'].isin(centro)][str(a)].to_list(), name=str(a), text=df_rel[df_rel['centro'].isin(centro)][str(a)].to_list(), textposition='auto',),1,1)
            graf_rel.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))

        graf_rel.update_layout(
            height = 500,
            width = 920,
        )
            
            #graf_rel.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=True)
            #graf_rel.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))
            #graf_rel.update_layout(yaxis = dict(tickmode = 'linear', tick0 = 0, dtick = 0.5))
        return dcc.Graph(figure=graf_rel)

    elif tab == 'tab-4':
        df_extproj = (pd.read_csv("apps/Apoio/docentesextensao.csv").sort_values(by=str(ano[0]))) if len(ano) == 1 else pd.read_csv("apps/Apoio/docentesextensao.csv")

        df_pesqproj = (pd.read_csv("apps/Apoio/docentespesquisa.csv").sort_values(by=str(ano[0]))) if len(ano) == 1 else pd.read_csv("apps/Apoio/docentespesquisa.csv")

        fig = make_subplots(
            rows=1, cols=1,
        )

        x = df_extproj[df_extproj['centro'].isin(centro)].sort_index()['centro'].to_list()

        if(len(ano) == 1):
            x_scatter = df_extproj[df_extproj['centro'].isin(centro)].sort_index()[str(ano[0])].to_list()
            y_scatter = df_pesqproj[df_pesqproj['centro'].isin(centro)].sort_index()[str(ano[0])].to_list()
            fig.add_trace(
                go.Scatter(x=x_scatter, y=y_scatter, text = x, name=ano[0], mode='markers'),
                row=1, col=1
            )

        else:
            for a in ano:
                y_sct = df_pesqproj[df_pesqproj['centro'].isin(centro)].sort_index()[str(a)].to_list()
                x_sct = df_extproj[df_extproj['centro'].isin(centro)].sort_index()[str(a)].to_list()
                fig.add_trace(
                    #go.Scatter(x=x_scatter, y=y_scatter, text = x, color=x, size_max=60),
                    go.Scatter(x=x_sct, y=y_sct, text = x, name=a, mode='markers'),
                    row=1, col=1
                )

        fig.add_trace(
            go.Scatter(x=[0,400],y=[0,400],name="reta Y = X",mode="lines",line=dict(color='black', width=1,dash='solid')),
            row=1, col=1
        )  

        fig.update_traces(textposition='top center')
        
        fig.update_layout(
            height = 580,
            width = 580,
            #title="Plot Title",
            xaxis_title="Quantidade de Projetos de Extensão",
            yaxis_title="Quantidade de Projetos de Pesquisa",
            #legend_title="",
            #font=dict(
            #family="Courier New, monospace",
            #size=18,
            #color="RebeccaPurple"
            #)
        )

        fig.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=True)
    
        fig.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))

        return dcc.Graph(figure=fig)
    

## Os dois próximos callbacks dizem respeito à seleção de todos os anos/todos os centros nos dropdowns
@app.callback(
	[Output("centro-proj2", "value"),Output("modal_5_proj2", "is_open")],
	[Input("ano-proj2", "value"), Input("close_3", "n_clicks")],
	[State("centro-proj2", "value"),State("modal_5_proj2", "is_open")],
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
	[Output("ano-proj2", "value"),Output("modal_6_proj2", "is_open")],
	[Input("centro-proj2", "value"),Input("close_4", "n_clicks")],
	[State("ano-proj2", "value"),State("modal_6_proj2", "is_open")],

)

def flag(centro,n_rel, ano, is_open_rel):
        if 'Todos os anos' in ano:
                return [[2017,2018,2019,2020,2021],is_open_rel]
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
	Output("relatorio_discentes_proj2", "children"),
	[Input("centro-proj2", "value"),Input("ano-proj2", "value"),
         Input("tabs-proj2","value")]
)

def relatorio_discentes_proj2(centro,ano,tab):
        centro=", ".join(str(x) for x in centro)
        ano=", ".join(str(x) for x in sorted(ano))
        if tab == 'tab-1':
                return f'''O gráfico ao lado exibe o evolutivo de projetos de extensão por centro, nos seguintes centros: {centro}. Além da visualização dessa quantidade de professores envolvidos em extensão nos seguintes anos: {ano}'''

        elif tab == 'tab-2':
                return f'''O gráfico ao lado exibe o evolutivo de projetos de pesquisa por centro, nos seguintes centros: {centro}. Além da visualização dessa quantidade de professores envolvidos em pesquisa nos seguintes anos: {ano}'''
                            
        elif tab == 'tab-3':
                return f'''O gráfico ao lado exibe o quantitativo de atividades de pesquisa e extensão desenvolvidas pelo(s) centro(s):  {centro}. No(s) ano(s) de {ano}. A exibição dessa gráfico é relevante porque existe a noção intuitiva de que a quantidade de projetos de extensão é consideravelmente menor dos que os de pesquisa (tendo em vista que a extensão é relativamente recente quando comparada a pesquisa), além disso pode-se observar se ocorreu uma modificação dessa 'tendência' durante o período de pandemia, o qual dificultou e vem dificultando o desenvolvimento de pesquisas em função da estrutura física necessária.'''
        elif tab == 'tab-4':
                return f'''O gráfico ao lado exibe uma relação gráfica entre a quantidade de projetos de extensão (eixo x)  e a quantidade de projetos de extensão (eixo y). Os centros considerados foram: {centro}, nos anos de {ano}.'''
   
## Modifica o título do gráfico mostrado de acordo com a tab escolhida.
@app.callback(
	Output("card_proj2", "children"),
	[Input("tabs-proj2","value")]
)

def graf_tit(tab):
        if tab == 'tab-1':
                return 'Evolutivo de Projetos de Extensão por Centro e Ano'
        elif tab == 'tab-2':
                return 'Evolutivo de Projetos de Pesquisa por Centro e Ano'
        elif tab == 'tab-3':
                return 'Razão entre Projetos de Pesquisa e Projetos de Extensão'
        elif tab == 'tab-4':
                return 'Relação entre Projetos de Pesquisa e Projetos de Extensão'

