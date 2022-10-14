import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from app import app

# apps é uma pasta na raiz do nosso diretório e nela estão contidas todos as 
# páginas do nosso site
from apps import novosalunos,docentes2, homepage, variacao, mapa, discentes, docentes, quem_somos, projetos2,projetos ,docentes2022

server = app.server

# faz com que o app não mostre as execeções dash
app.config.suppress_callback_exceptions = True  

app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')
    ]
)

# callback responsável pelo roteamento de endereços do site
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):

    if pathname == '/estudo-vocabular':
        return variacao.layout

    elif pathname == '/mapa-ufpb':
        return mapa.layout

    elif pathname == '/novo-docentes':
        return docentes2.layout

    elif pathname == '/novo-projetos':
        return projetos2.layout

    elif pathname == '/discente':
        return discentes.layout

    elif pathname == '/docente':
        return docentes.layout

    elif pathname == '/quemsomos':
        return quem_somos.layout
    
    elif pathname == '/projetos':
        return projetos.layout
    
    elif pathname == '/novos-alunos':
        return novosalunos.layout

    elif pathname == '/docentes2022':
        return docentes2022.layout

    else:
        return dbc.Spinner(children=[homepage.layout], fullscreen=True,debounce=1000, spinnerClassName="loader-homepage",type=None),


# inicia o flask server, por isso ele é linkado no Procfile (arquivo do heroku)
if __name__ == '__main__':
    server.run(debug=True)
