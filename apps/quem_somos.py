import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.Jumbotron import Jumbotron
import dash_core_components as dcc
import dash_html_components as html
# from navbar import Navbar
from . import navbar
import base64
from dash.dependencies import Output, Input, State

##Importa as imagens dos integrantes e o navbar da página
nav = navbar.Navbar()
mauricio = base64.b64encode(open('apps/Apoio/participantes/mauricio.jpeg', 'rb').read())
helon = base64.b64encode(open('apps/Apoio/participantes/helon.jpeg', 'rb').read())
rafael_m = base64.b64encode(open('apps/Apoio/participantes/rafael_m.jpeg', 'rb').read())
ademar = base64.b64encode(open('apps/Apoio/participantes/ademar.jpeg', 'rb').read())
joao = base64.b64encode(open('apps/Apoio/participantes/joao.jpeg', 'rb').read())
gabriel = base64.b64encode(open('apps/Apoio/participantes/gabriel.jpeg', 'rb').read())
yasmin = base64.b64encode(open('apps/Apoio/participantes/yasmin.jpeg', 'rb').read())
felipe = base64.b64encode(open('apps/Apoio/participantes/felipe.jpeg', 'rb').read())


jumbotron =dbc.Jumbotron(
    [
        html.H1("Equipe", id="titulo-quem-somos"),
        html.Div(
        [    
            html.Div(  #diz ao dash que só quero uma coluna da linha 
            [
                dbc.CardImg(src='data:image/png;base64,{}'.format(mauricio.decode()), top=True,className="imagens-quem-somos"),
                html.H3("Coordenador", className="funcao-quem-somos"),
                html.P(
                    "José Mauricio Ramos de Souza Neto",
                    className="nome-quem-somos"
                ),
                dbc.Button("Lattes", href='http://lattes.cnpq.br/6354668326581094', className="button-dbc"),
            ],className="elemento-quem-somos"),

            html.Div(  #diz ao dash que só quero uma coluna da linha 
            [
                dbc.CardImg(src='data:image/png;base64,{}'.format(helon.decode()), top=True,className="imagens-quem-somos"),
                html.H3("Coordenador Adjunto", className="funcao-quem-somos"),
                html.P(
                    "Helon David de Macedo Braz",
                    className="nome-quem-somos"
                ),
                dbc.Button('Lattes', href='http://lattes.cnpq.br/4756997631027455', className="button-dbc"),
            ],className="elemento-quem-somos"),

            

            html.Div([
                dbc.CardImg(src='data:image/png;base64,{}'.format(joao.decode()), top=True,className="imagens-quem-somos"),
                html.H3("Bolsista Probex", className="funcao-quem-somos"),       
                html.P(
                    "João Guilherme Sales de Oliveira",
                    className="nome-quem-somos"
                ),
                dbc.Button("Lattes", href='http://lattes.cnpq.br/9540990930501608', className="button-dbc"),
                    
            ],className="elemento-quem-somos"),

            html.Div([
                dbc.CardImg(src='data:image/png;base64,{}'.format(yasmin.decode()), top=True,className="imagens-quem-somos"),
                html.H3("Bolsista Probex", className="funcao-quem-somos"),
                html.P(
                    "Yasmin Kely Lucena de Medeiros",
                    className="nome-quem-somos"
                ),
                dbc.Button("Lattes", href='http://lattes.cnpq.br/5223289129574607', className="button-dbc"),
            ],className="elemento-quem-somos"),

            html.Div(
            [
                dbc.CardImg(src='data:image/png;base64,{}'.format(rafael_m.decode()), top=True,className="imagens-quem-somos"),
                
                html.H3("Colaborador", className="funcao-quem-somos"),
                html.P(
                    "Rafael de Sousa Marinho",
                    className="nome-quem-somos"
                ),
                dbc.Button("Lattes", href='http://lattes.cnpq.br/9229841711516369', className="button-dbc"),
                    
            ],className="elemento-quem-somos"),


            html.Div(
            [
                dbc.CardImg(src='data:image/png;base64,{}'.format(ademar.decode()), top=True,className="imagens-quem-somos"),
                
                html.H3("Colaborador", className="funcao-quem-somos"),
                html.P(
                    "Ademar Virgolino da Silva Netto",
                    className="nome-quem-somos"
                ),
                dbc.Button("Lattes", href='http://lattes.cnpq.br/5726596757497539', className="button-dbc"),
                    
            ],className="elemento-quem-somos"),

            html.Div([
                dbc.CardImg(src='data:image/png;base64,{}'.format(gabriel.decode()), top=True,className="imagens-quem-somos"),  
                
                html.H3("Voluntário", className="funcao-quem-somos"),
                html.P(
                    "Gabriel Murilo Santiago dos Anjos",
                    className="nome-quem-somos"
                ),
                dbc.Button("Lattes", href='http://lattes.cnpq.br/4579130098454805',className="button-dbc"),
                    
            ],className="elemento-quem-somos"),

            html.Div([
                dbc.CardImg(src='data:image/png;base64,{}'.format(felipe.decode()), top=True, className="imagens-quem-somos"),
                
                html.H3("Voluntário", className="funcao-quem-somos"),
                html.P(
                    "Felipe Silva Lima",
                    className="nome-quem-somos"
                ),
                dbc.Button("Lattes", href='https://www.linkedin.com/in/felipe-lima-9a1b40213',className="button-dbc"),
                    
            ],className="elemento-quem-somos"),

       ], id="quem-somos-grid"),

    ],id="jumbotron-quem-somos")



## A página retorna as duas partes de seu corpo bem como a navbar que exibe os menus
layout = html.Div([
    nav,
    jumbotron,
],id="layout-jumbotron-quem-somos")

 
