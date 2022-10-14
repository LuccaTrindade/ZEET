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

import matplotlib_venn as vplt
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

import matplotlib
   

matplotlib.use('Agg')



anos = [2017,2018,2019,2020,2021,2022,'Todos os anos']
centros = ['Todos os centros','CCHLA','CCS','CCA','CT','CCEN','CCTA','CCAE','CEAR','CCM','CTDR','CE','CBIOTEC','CCHSA','CCSA','CI','CCJ'] 

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

##### opções de tabs na página docentes
abas = html.Div([
    dcc.Tabs(id='aba-example', value='aba-1', children=[
        dcc.Tab(label='Diagrama de Venn', value='aba-1', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Evolução docentes', value='aba-2', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Relação da Média de Docentes', value='aba-3', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Relação Docente/Projeto', value='aba-4', style=tab_style, selected_style=tab_selected_style),
])
    ,html.Br()])
####



nav = navbar.Navbar()    
venn = base64.b64encode(open('apps/Apoio/venn.png', 'rb').read())
card_content = [
    dbc.CardHeader("Entendendo o gráfico",style={'font-size':24, 'textAlign':'center'}),
    dbc.CardBody(
        [
        ###Esse f é da biblioteca fstring que substitui deterinado local por um texto durante a execução de uma callback
            html.P(
                children=f'''O gráfico analisado é uma análise de variabilidade, a fim de visualizar a quantidade de professores e alunos que 
                trabalharam em projetos de extensão apenas no ano de 2017, 2018 ou 2019, bem como suas respectivas intersecções. Podemos
                analisar que, como escolhido, está sendo filtrado em apenas os centros: CEAR para serem visualizados. Esses dados foram representados pelo diagrama de Venn.''',
                className="card-text",id='relatorio_docentes',style={'text-align':'justify'}
            ),
        ]
    ),
]



jumbotron = dbc.Card(card_content,  outline=True)

card_content_2 = [
    dbc.CardHeader("Filtros do Gráfico",style={'font-size':24, 'textAlign':'center'}),
    dbc.CardBody(
        [
        abas,
        html.H4("Escolha os anos que deseja analisar", style={'font-size':19}),
        dcc.Dropdown(
        id = 'anos',  
        options=[
            {'label': j, 'value': j} for j in anos  
        ],
        value=[2017,2018,2019],   
        multi=True,
    searchable=False,
         style={'margin-bottom':'10px'}
   

        ),        
        html.H4("Escolha os centros desejados", style={'font-size':19}),
        dcc.Dropdown(
        id = 'centros',  
        options=[
            {'label': j, 'value': j} for j in centros  
        ],
        value=['CEAR'],   
        multi=True,
    searchable=False,
         style={'margin-bottom':'10px'}
   

    ),
        ]
    ),
]

jumbotron_2 = dbc.Card(card_content_2,  outline=True)
card_content_3 = [
    dbc.CardHeader(id='card_doc',style={'font-size':24, 'textAlign':'center'}),
    dbc.CardBody(
        [
        ## Abaixo estão os ids onde os gráficos serão mostrados durante a execução da aplicação
            html.Img(id='graph_docentes',
            style={'display':'block', 'max-width': '100%', 'margin-left': 'auto', 'margin-right': 'auto'}
            ,src='data:image/png;base64,{}'.format(venn.decode())
                ),

            html.Div(id='graph_docentes_2',
            style={'display':'block', 'max-width': '100%', 'margin-left': 'auto', 'margin-right': 'auto'}
            )
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

#Em caso de exceção de escolha
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

#Em caso de exceção de escolha
modal_2 = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader("ERROR"),
                dbc.ModalBody("Escolha pelo menos dois anos como parâmetro de entrada de anos"),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close_2", className="ml-auto")
                ),
            ],
            id="modal_2",
        ),
    ]
)

modal_3a = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader("ERROR"),
                dbc.ModalBody("Escolha no máximo três anos como parâmetro de entrada de anos"),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close_3a", className="ml-auto")
                ),
            ],
            id="modal_3a",
        ),
    ]
)

layout = html.Div([
    nav,
    body_1,
    modal,
    modal_2,
    modal_3a
])

########## configuram a visualização dos gráficos (que são feitos como imagens, já que o módulo do diagrama de veen não é suportado nativamente pelo plotly)
@app.callback(
	Output("anos", "options"),
	[Input("aba-example","value")],
)
def update_layout_docentes(abas):
        if(abas == 'aba-1'):
                anos2 = [2017,2018,2019,2020]
                options=[{'label': j, 'value': j} for j in anos2  ]
                return options
        else:
                options=[{'label': j, 'value': j} for j in anos  ]
                return options

@app.callback(
	Output("graph_docentes_2", "style"),
	[Input("aba-example","value")],
)
def update_layout_docentes(abas):
	print(abas,flush=True)
	if abas == 'aba-1':
		return {'display':'none', 'max-width': '100%', 'margin-left': 'auto', 'margin-right': 'auto'}
	else:
		return {'display':'block', 'max-width': '100%', 'margin-left': 'auto', 'margin-right': 'auto'}

@app.callback(
	Output("graph_docentes", "style"),
	[Input("aba-example","value")],
)
def update_layout_docentes(abas):
	print(abas,flush=True)
	if abas == 'aba-1':
		return {'display':'block', 'max-width': '100%', 'margin-left': 'auto', 'margin-right': 'auto'}
	else:
		return {'display':'none', 'max-width': '100%', 'margin-left': 'auto', 'margin-right': 'auto'}

################

##### Processo de confecção do gráfico
@app.callback(
        [Output("graph_docentes", "src"),Output("graph_docentes_2", "children")],
        [Input("centros", "value"),
        Input("anos", "value"),Input("aba-example","value")],
)
def update_graph_docentes(centros, anos,abas):
        print(abas,flush=True)
        if abas == 'aba-1':
                df_ = pd.read_csv("apps/Apoio/df_docentes_.csv")

                meio = 0
                sete_oito = 0
                sete_nove = 0
                oito_nove = 0 
                sete_vinte = 0 
                oito_vinte = 0
                nove_vinte = 0    
                result_df_2017 = []
                result_df_2018 = []
                result_df_2019 = []
                result_df_2020 = []
                result_df_2021 = []
                result_df_2022 = []

                df_ = df_[df_.a.isin(centros)]

                if 2017 in anos: 
                        df_2017 = df_[df_['ano']==2017] 
                        result_df_2017 = df_2017.drop_duplicates(subset=['id_pessoa'], keep='last') 
                if 2018 in anos:
                        df_2018 = df_[df_['ano']==2018]
                        result_df_2018 = df_2018.drop_duplicates(subset=['id_pessoa'], keep='last')
                if 2019 in anos:
                        df_2019 = df_[df_['ano']==2019]
                        result_df_2019 = df_2019.drop_duplicates(subset=['id_pessoa'], keep='last')
                if 2020 in anos:
                        df_2020 = df_[df_['ano']==2020]
                        result_df_2020 = df_2020.drop_duplicates(subset=['id_pessoa'], keep='last')

                if 2020 in anos:
                        df_2020 = df_[df_['ano']==2021]
                        result_df_2020 = df_2020.drop_duplicates(subset=['id_pessoa'], keep='last')
                                 
                if 2017 in anos and 2018 in anos and 2019 in anos:
                        meio = len(list(set(list(result_df_2017['id_pessoa'])) & set(list(result_df_2018['id_pessoa'])) & set(list(result_df_2019['id_pessoa']))))
                if 2017 in anos and 2018 in anos and 2020 in anos:
                        meio = len(list(set(list(result_df_2017['id_pessoa'])) & set(list(result_df_2018['id_pessoa'])) & set(list(result_df_2020['id_pessoa']))))
                if 2018 in anos and 2019 in anos and 2020 in anos:
                        meio = len(list(set(list(result_df_2018['id_pessoa'])) & set(list(result_df_2019['id_pessoa'])) & set(list(result_df_2020['id_pessoa']))))
                if 2017 in anos and 2019 in anos and 2020 in anos:
                        meio = len(list(set(list(result_df_2017['id_pessoa'])) & set(list(result_df_2019['id_pessoa'])) & set(list(result_df_2020['id_pessoa']))))

                print(meio)


                if 2017 in anos and 2018 in anos: 
                        sete_oito = len(list(set(list(result_df_2017['id_pessoa'])) & set(list(result_df_2018['id_pessoa'])))) - meio
                if 2017 in anos and 2019 in anos: 
                        sete_nove = len(list(set(list(result_df_2017['id_pessoa'])) & set(list(result_df_2019['id_pessoa'])))) - meio
                if 2018 in anos and 2019 in anos:
                        oito_nove =  len(list(set(list(result_df_2018['id_pessoa'])) & set(list(result_df_2019['id_pessoa'])))) - meio  

                if 2017 in anos and 2020 in anos:
                        sete_vinte =  len(list(set(list(result_df_2017['id_pessoa'])) & set(list(result_df_2020['id_pessoa'])))) - meio 
                if 2018 in anos and 2020 in anos:
                        oito_vinte =  len(list(set(list(result_df_2018['id_pessoa'])) & set(list(result_df_2020['id_pessoa'])))) - meio 
                if 2019 in anos and 2020 in anos:
                        nove_vinte =  len(list(set(list(result_df_2019['id_pessoa'])) & set(list(result_df_2020['id_pessoa'])))) - meio 


                if 2017 in anos: 
                        sete = len(set(list(result_df_2017['id_pessoa']))) - meio - sete_oito - sete_nove - sete_vinte
                if 2018 in anos:
                        oito = len(set(list(result_df_2018['id_pessoa']))) - meio - sete_oito - oito_nove - oito_vinte
                if 2019 in anos:
                        nove = len(set(list(result_df_2019['id_pessoa']))) - meio - sete_nove - oito_nove - nove_vinte
                if 2020 in anos:
                        vinte = len(set(list(result_df_2020['id_pessoa']))) - meio - sete_vinte - oito_vinte - nove_vinte

                plt.clf()

                if 2017 in anos and 2018 in anos and 2019 in anos:
                        v = vplt.venn3(subsets=(sete, oito, sete_oito, nove, sete_nove, oito_nove, meio), set_labels = ('2017','2018', '2019'))
                        plt.savefig('apps/Apoio/venn.png',dpi=150)
                        venn = base64.b64encode(open('apps/Apoio/venn.png', 'rb').read())
                        return ['data:image/png;base64,{}'.format(venn.decode()),dcc.Graph()]

                if 2017 in anos and 2018 in anos and 2020 in anos:
                        v = vplt.venn3(subsets=(sete, oito, sete_oito, vinte, sete_vinte, oito_vinte, meio), set_labels = ('2017','2018', '2020'))
                        plt.savefig('apps/Apoio/venn.png',dpi=150)
                        venn = base64.b64encode(open('apps/Apoio/venn.png', 'rb').read())
                        return ['data:image/png;base64,{}'.format(venn.decode()),dcc.Graph()]

                if 2018 in anos and 2019 in anos and 2020 in anos:
                        v = vplt.venn3(subsets=(oito, nove, oito_nove, vinte, oito_vinte, nove_vinte, meio), set_labels = ('2018','2019', '2020'))
                        plt.savefig('apps/Apoio/venn.png',dpi=150)
                        venn = base64.b64encode(open('apps/Apoio/venn.png', 'rb').read())
                        return ['data:image/png;base64,{}'.format(venn.decode()),dcc.Graph()]

                if 2017 in anos and 2019 in anos and 2020 in anos:
                        v = vplt.venn3(subsets=(sete, nove, sete_nove, vinte, sete_vinte, nove_vinte, meio), set_labels = ('2017','2019', '2020'))
                        plt.savefig('apps/Apoio/venn.png',dpi=150)
                        venn = base64.b64encode(open('apps/Apoio/venn.png', 'rb').read())
                        return ['data:image/png;base64,{}'.format(venn.decode()),dcc.Graph()]


                if 2017 in anos and 2018 in anos:
                        v = vplt.venn2(subsets={'10': sete, '01': oito, '11': sete_oito}, set_labels = ('2017', '2018'))
                        plt.savefig('apps/Apoio/venn.png',dpi=150)
                        venn = base64.b64encode(open('apps/Apoio/venn.png', 'rb').read())
                        return ['data:image/png;base64,{}'.format(venn.decode()),dcc.Graph()]
                if 2017 in anos and 2019 in anos:
                        v = vplt.venn2(subsets={'10': sete, '01': nove, '11': sete_nove}, set_labels = ('2017', '2019'))
                        plt.savefig('apps/Apoio/venn.png',dpi=150)
                        venn = base64.b64encode(open('apps/Apoio/venn.png', 'rb').read())
                        return ['data:image/png;base64,{}'.format(venn.decode()),dcc.Graph()]
                if 2018 in anos and 2019 in anos:
                        v = vplt.venn2(subsets={'10': oito, '01': nove, '11': oito_nove}, set_labels = ('2018', '2019'))
                        plt.savefig('apps/Apoio/venn.png',dpi=150) 
                        venn = base64.b64encode(open('apps/Apoio/venn.png', 'rb').read())
                        return ['data:image/png;base64,{}'.format(venn.decode()),dcc.Graph()]
                 
                if 2017 in anos and 2020 in anos:
                        v = vplt.venn2(subsets={'10': sete, '01': vinte, '11': sete_vinte}, set_labels = ('2017', '2020'))
                        plt.savefig('apps/Apoio/venn.png',dpi=150) 
                        venn = base64.b64encode(open('apps/Apoio/venn.png', 'rb').read())
                        return ['data:image/png;base64,{}'.format(venn.decode()),dcc.Graph()]
                 
                 
                if 2018 in anos and 2020 in anos:
                        v = vplt.venn2(subsets={'10': oito, '01': vinte, '11': oito_vinte}, set_labels = ('2018', '2020'))
                        plt.savefig('apps/Apoio/venn.png',dpi=150) 
                        venn = base64.b64encode(open('apps/Apoio/venn.png', 'rb').read())
                        return ['data:image/png;base64,{}'.format(venn.decode()),dcc.Graph()]
                 
                if 2019 in anos and 2020 in anos:
                        v = vplt.venn2(subsets={'10': nove, '01': vinte, '11': nove_vinte}, set_labels = ('2019', '2020'))
                        plt.savefig('apps/Apoio/venn.png',dpi=150) 
                        venn = base64.b64encode(open('apps/Apoio/venn.png', 'rb').read())
                        return ['data:image/png;base64,{}'.format(venn.decode()),dcc.Graph()]


        elif abas == 'aba-2':
                df_rel = (pd.read_csv('apps/Apoio/evolucao_docentes.csv').sort_values(by=str(anos[0]))) if len(anos) == 1 else pd.read_csv('apps/Apoio/evolucao_docentes.csv')

                agraf_rel = make_subplots(rows=1, cols=1,row_titles = ['Quantidade de Docentes'],  shared_yaxes=True)
                if 2017 in anos:
                        agraf_rel.add_trace(go.Bar(x=df_rel[df_rel['centro'].isin(centros)]['centro'].to_list(), y=df_rel[df_rel['centro'].isin(centros)]['2017'].to_list(), name='2017', text=df_rel[df_rel['centro'].isin(centros)]['2017'].to_list(), textposition='auto',),1,1)
                        agraf_rel.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=True)
                        agraf_rel.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))
                if 2018 in anos:
                        agraf_rel.add_trace(go.Bar(x=df_rel[df_rel['centro'].isin(centros)]['centro'].to_list(), y=df_rel[df_rel['centro'].isin(centros)]['2018'].to_list(), name='2018', text=df_rel[df_rel['centro'].isin(centros)]['2018'].to_list(), textposition='auto',),1,1)
                        agraf_rel.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=True)
                        agraf_rel.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))
                if 2019 in anos:
                        agraf_rel.add_trace(go.Bar(x=df_rel[df_rel['centro'].isin(centros)]['centro'].to_list(), y=df_rel[df_rel['centro'].isin(centros)]['2019'].to_list(), name='2019', text=df_rel[df_rel['centro'].isin(centros)]['2019'].to_list(), textposition='auto',),1,1)
                        agraf_rel.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=True)
                        agraf_rel.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))
                if 2020 in anos:
                        agraf_rel.add_trace(go.Bar(x=df_rel[df_rel['centro'].isin(centros)]['centro'].to_list(), y=df_rel[df_rel['centro'].isin(centros)]['2020'].to_list(), name='2020', text=df_rel[df_rel['centro'].isin(centros)]['2020'].to_list(), textposition='auto',),1,1)
                        agraf_rel.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=True)
                        agraf_rel.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))
                if 2021 in anos:
                        agraf_rel.add_trace(go.Bar(x=df_rel[df_rel['centro'].isin(centros)]['centro'].to_list(), y=df_rel[df_rel['centro'].isin(centros)]['2021'].to_list(), name='2021', text=df_rel[df_rel['centro'].isin(centros)]['2021'].to_list(), textposition='auto',),1,1)
                        agraf_rel.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=True)
                        agraf_rel.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))
                if 2022 in anos:
                        agraf_rel.add_trace(go.Bar(x=df_rel[df_rel['centro'].isin(centros)]['centro'].to_list(), y=df_rel[df_rel['centro'].isin(centros)]['2022'].to_list(), name='2022', text=df_rel[df_rel['centro'].isin(centros)]['2022'].to_list(), textposition='auto',),1,1)
                        agraf_rel.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=True)
                        agraf_rel.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))



                venn = base64.b64encode(open('apps/Apoio/venn.png', 'rb').read())
                agraf_rel.update_layout(height=600)
                return ['data:image/png;base64,{}'.format(venn.decode()),dcc.Graph(figure=agraf_rel)]
                                    
        elif abas == 'aba-3':
                df_rel = (pd.read_csv('apps/Apoio/relacao_docente_projeto.csv').sort_values(by=str(anos[0]))) if len(anos) == 1 else pd.read_csv('apps/Apoio/relacao_docente_projeto.csv')

                agraf_rel = make_subplots(rows=1, cols=1,row_titles = ['Razão Docente/Projeto'],  shared_yaxes=True)
                if 2017 in anos:
                        agraf_rel.add_trace(go.Bar(x=df_rel[df_rel['centro'].isin(centros)]['centro'].to_list(), y=df_rel[df_rel['centro'].isin(centros)]['2017'].to_list(), name='2017', text=df_rel[df_rel['centro'].isin(centros)]['2017'].to_list(), textposition='auto',),1,1)
                        agraf_rel.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=True)
                        agraf_rel.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))
                if 2018 in anos:
                        agraf_rel.add_trace(go.Bar(x=df_rel[df_rel['centro'].isin(centros)]['centro'].to_list(), y=df_rel[df_rel['centro'].isin(centros)]['2018'].to_list(), name='2018', text=df_rel[df_rel['centro'].isin(centros)]['2018'].to_list(), textposition='auto',),1,1)
                        agraf_rel.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=True)
                        agraf_rel.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))
                if 2019 in anos:
                        agraf_rel.add_trace(go.Bar(x=df_rel[df_rel['centro'].isin(centros)]['centro'].to_list(), y=df_rel[df_rel['centro'].isin(centros)]['2019'].to_list(), name='2019', text=df_rel[df_rel['centro'].isin(centros)]['2019'].to_list(), textposition='auto',),1,1)
                        agraf_rel.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=True)
                        agraf_rel.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))
                if 2020 in anos:
                        agraf_rel.add_trace(go.Bar(x=df_rel[df_rel['centro'].isin(centros)]['centro'].to_list(), y=df_rel[df_rel['centro'].isin(centros)]['2020'].to_list(), name='2020', text=df_rel[df_rel['centro'].isin(centros)]['2020'].to_list(), textposition='auto',),1,1)
                        agraf_rel.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=True)
                        agraf_rel.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))

                if 2021 in anos:
                        agraf_rel.add_trace(go.Bar(x=df_rel[df_rel['centro'].isin(centros)]['centro'].to_list(), y=df_rel[df_rel['centro'].isin(centros)]['2021'].to_list(), name='2021', text=df_rel[df_rel['centro'].isin(centros)]['2021'].to_list(), textposition='auto',),1,1)
                        agraf_rel.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=True)
                        agraf_rel.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))

                if 2022 in anos:
                        agraf_rel.add_trace(go.Bar(x=df_rel[df_rel['centro'].isin(centros)]['centro'].to_list(), y=df_rel[df_rel['centro'].isin(centros)]['2022'].to_list(), name='2022', text=df_rel[df_rel['centro'].isin(centros)]['2022'].to_list(), textposition='auto',),1,1)
                        agraf_rel.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=True)
                        agraf_rel.update_traces(marker=dict(line=dict(color='#000000', width=0.5)))

                venn = base64.b64encode(open('apps/Apoio/venn.png', 'rb').read())
                agraf_rel.update_layout(height=600)
                return ['data:image/png;base64,{}'.format(venn.decode()),dcc.Graph(figure=agraf_rel)]
        elif abas == 'aba-4':
                df_rel = pd.read_csv('apps/Apoio/doc-pro.csv')
                agraf_rel = make_subplots(rows=1, cols=1,  shared_yaxes=True)
                for an in anos:
                        agraf_rel.add_trace(go.Scatter(x=df_rel[(df_rel['ano']==an)&(df_rel['centros'].isin(centros))].groupby(['projetos'])['docentes'].sum().reset_index(level=0)['projetos'].to_list(), y=df_rel[(df_rel['ano']==an)&(df_rel['centros'].isin(centros))].groupby(['projetos'])['docentes'].sum().reset_index(level=0)['docentes'].to_list(), name=str(an), mode='markers'),1,1)
                        agraf_rel.update_layout(coloraxis=dict(colorscale='Bluered_r'), showlegend=True)
                agraf_rel.update_layout(go.Layout(yaxis={'title':'Numero de Projetos'},xaxis={'title': 'Quantidade de Docentes'}))
                venn = base64.b64encode(open('apps/Apoio/venn.png', 'rb').read())
                agraf_rel.update_layout(height=600)
                return ['data:image/png;base64,{}'.format(venn.decode()),dcc.Graph(figure=agraf_rel)]




##### Seleção de centros e anos nos dropdowns.
@app.callback(
	[Output("centros", "value"),Output("modal", "is_open")],
	[Input("anos", "value"), Input("close", "n_clicks")],
	[State("centros", "value"),State("modal", "is_open")],

)
def limite_centros(anos,n2, centros,is_open):
	if 'Todos os centros' in centros:
		return [['CCHLA','CCS','CCA','CT','CCEN','CCTA','CCAE','CEAR','CCM','CTDR','CE','CBIOTEC','CCHSA','CCSA','CI','CCJ'],is_open]
	if len(centros) == 0:
		return [['CEAR'], not is_open]
	else:
		if n2:
			if is_open == True:
				return [centros, not is_open]
			return [centros, is_open]
		return [centros, is_open]


@app.callback(
	[Output("anos", "value"),Output("modal_2", "is_open"),Output("modal_3a", "is_open")],
	[Input("centros", "value"),Input("close_2", "n_clicks"),Input("close_3a", "n_clicks"),Input("aba-example","value")],
	[State("anos", "value"),State("modal_2", "is_open"),State("modal_3a", "is_open")],

)

def flag(centros,n2,n3, abas, anos, is_open,is_open2):
        if len(anos) > 3:
                if abas != 'aba-1':
                        if abas != 'aba-1':
                                if("Todos os anos" in anos):
                                        return [[2017,2018,2019,2020,2021,2022],is_open,is_open2]
                        
                        if("Todos os anos" in anos and abas == 'aba-1'):
                                return [[2018,2019,2029],is_open,not is_open2]

                        return [anos,is_open,is_open2]
                return [[2018,2019,2029],is_open,not is_open2]
                
        if len(anos) < 2:
                if abas != 'aba-1':
                        if("Todos os anos" in anos):
                                return [[2017,2018,2019,2020,2021,2022],is_open,is_open2]
                        return [anos,is_open,is_open2]

                return [[2018,2019], not is_open,is_open2]
        else:
                if abas != 'aba-1':
                        if("Todos os anos" in anos):
                                return [[2017,2018,2019,2020,2021,2022],is_open,is_open2]
                if n3:
                        if is_open2 == True:
                                return [anos,is_open, not is_open2]
                        return [anos, is_open,is_open2]
                if n2:
                        if is_open == True:
                                return [anos, not is_open,is_open2]
                        return [anos, is_open,is_open2]
                return [anos, is_open,is_open2]

####################################


#Retorno do Texto de acordo com as escolhas de gráficos do usuário utilizando a biblioteca fstring para substiuir o termo em '{}' por uma string apropriada durante a execução do código
@app.callback(
	Output("relatorio_docentes", "children"),
	[Input("centros", "value"),Input("anos", "value"),Input("aba-example","value")]

)
def relatorio_docentes(centros,anos, abas):
	if abas == 'aba-1':
		centros=", ".join(str(x) for x in centros)
		anos=", ".join(str(x) for x in anos)
		return f'''O gráfico analisado é uma análise de variabilidade, a fim de visualizar a quantidade de professores e alunos que 
		trabalharam em projetos de extensão apenas no ano de {anos}, bem como suas respectivas intersecções. Podemos
		analisar que, como escolhido, está sendo filtrado em apenas os centros: {centros} para serem visualizados.
		Esses dados foram representados pelo diagrama de Venn.'''
	if abas == 'aba-2':
		centros=", ".join(str(x) for x in centros)
		anos=", ".join(str(x) for x in anos)
		return f'''O gráfico analisado é o evolutivo dos docentes por centro, a fim de visualizar o envolvimento dos docentes 
		em projetos de extensão nos anos de {anos}. Podemos analisar que, como escolhido, está sendo filtrado em apenas 
		os centros: {centros} para serem visualizados. Esses dados foram representados em um grafico de barras. Com esses resultados pode-se 
		analisar os centros que atraem mais docentes para projetos de estensão e nos permite fazer um comparativo com os outros centros.'''
	if abas == 'aba-3':
		centros=", ".join(str(x) for x in centros)
		anos=", ".join(str(x) for x in anos)
		return f'''O gráfico analisado é a média da quantidade de docentes envolvidos em ações de extensão, a fim de visualizar o envolvimento dos docentes 
		em projetos de extensão nos anos de {anos}. Podemos analisar que, como escolhido, está sendo filtrado em apenas 
		os centros: {centros} para serem visualizados. Esses dados foram representados em um grafico de barras. Com esses resultados pode-se 
		analisar os centros que possuem a maior média de docentes por projetos.'''
	if abas == 'aba-4':
		centros=", ".join(str(x) for x in centros)
		anos=", ".join(str(x) for x in anos)
		return f'''O gráfico analisado é a relação entre Docentes/Projeto, a fim de visualizar a quantidade de projetos que possuem apenas um docente,
                                dois docentes e assim sucessivamente, 
				nos anos de {anos}. Podemos analisar que, como escolhido, está sendo filtrado em apenas 
				os centros: {centros} para serem visualizados. Esses dados foram representados em um grafico de dispersão. Com esses resultados pode-se 
				analisar os projetos que possuem mais docentes.'''

        

#Retorna o nome do gráfico de acordo com a seleção do usuário, na parte superior.
@app.callback(
	Output("card_doc", "children"),
	[Input("aba-example","value")]
)

def graf_tit(abas):
        if abas == 'aba-1':
                return 'Gráfico de Variabilidade de Docentes'
        elif abas == 'aba-2':
                return 'Gráfico Evolutivo de Docentes por Centro'
        elif abas == 'aba-3':
                return 'Gráfico da Media de Docentes por Centro'
        elif abas == 'aba-4':
                return 'Gráfico da Relação Docente/Projeto'






