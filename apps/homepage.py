import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
# from navbar import Navbar
from . import navbar
import base64
from dash.dependencies import Output, Input, State

##ESSA É A PÁGINA INICIAL DO SITE QUE APARECE APÓS O LOGIN

nav = navbar.Navbar()

#importa as imagens dos parceiros da ufpb
cear = base64.b64encode(open('apps/Apoio/cear.png', 'rb').read())
ufpb = base64.b64encode(open('apps/Apoio/ufpb.png', 'rb').read())
proex = base64.b64encode(open('apps/Apoio/proex.png', 'rb').read())
prac = base64.b64encode(open('apps/Apoio/prac.png', 'rb').read())
sti = base64.b64encode(open('apps/Apoio/sti.png', 'rb').read()) 
back='data:image/png;base64,{}'.format(cear.decode())
ode = base64.b64encode(open('apps/Apoio/ode.png', 'rb').read())


#Formtatação e conteúdo que a página exibe
jumbotron =dbc.Jumbotron(
    [
        html.Div(
        [    
            html.H3("Bem vindo(a) ao Observatório de Dados da Extensão", id="titulo-homepage"),
            html.Img(id='img_logo_ode',srcSet='data:image/png;base64,{}'.format(ode.decode())),
        
       ], id="divBoasVindas", className='back'),

    ], id="jumbotron-boas-vindas"
    )



jumbotron_2 =html.Div([dbc.Jumbotron(
    [
        
        html.H2("O que é o ODE?",id="titulo-def-ode"),
            
        html.Hr(className="my-2",style={'color':'white'}),
              
        html.P(['A extensão universitária tem como objetivo promover o desenvolvimento social e a difusão de conhecimentos para a universidade. Muitas são as ações desenvolvidas na UFPB com este objetivo, onde, por enquanto, existem poucas ferramentas sendo implementadas para avaliar dados gerados e permitir um acompanhamento de tais atividades. Esse projeto visa apresentar os dados da extensão de forma quantitativa, usando ferramentas de análise de dados e propondo métricas que auxiliam sua gestão dentro da UFPB, por meio da PRAC ou até mesmo das Assessorias de Extensão. Esta iniciativa é batizada de Observatório de Dados da Extensão e fornece informações estratégicas para um melhor conhecimento das ações de extensão desenvolvidas na UFPB.'],className="descricao-homepage"),

    ],
    className="descricao-forma-jumbotron",
)], className="descricao-forma")



jumbotron_3 =html.Div([dbc.Jumbotron(
    [
        

            html.H1("Parceiros", className="titulo-parceiros"),
            html.Hr(id="my-hr-parceiros"),

            html.Div([
                html.A([
                        html.Img(className="img-homepage elemento-quem-somos", srcSet='data:image/png;base64,{}'.format(ufpb.decode()) ),],href="https://www.ufpb.br/",id="logo-ufpb-homepage"),
                    

                html.A([
                    html.Img(className="img-homepage elemento-quem-somos",id='img_logo_cear',srcSet='data:image/png;base64,{}'.format(cear.decode()) ),],href="http://www.cear.ufpb.br/", id="logo-cear-homepage"),

                
                html.A([
                html.Img(className="img-homepage elemento-quem-somos",id='img_logo_proex',srcSet='data:image/png;base64,{}'.format(proex.decode()) ),],href="http://www.prac.ufpb.br/", id="logo-proex-homepage"),
                    
                html.A([
                html.Img(className="img-homepage elemento-quem-somos",id='img_logo_sti',srcSet='data:image/png;base64,{}'.format(sti.decode()) ),],href="https://www.sti.ufpb.br/", id="logo-sti-homepage"),

            
            #####
            ], className="flex-centros")


        

          
],className="descricao-forma2-jumbotron"),
],className="descricao-forma2", id="teste-loading")



           
body = dbc.Col([
              jumbotron, 
              jumbotron_2,
              jumbotron_3
			], style={'margin':'0','padding':'0'})


#O layout da página é constituído do seu conteúdo (body) mas a navbar que mostra os menus
layout = html.Div([
    nav,
    body
])    



