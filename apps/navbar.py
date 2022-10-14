import dash_bootstrap_components as dbc

import dash_html_components as html 

import base64

items = [
    dbc.DropdownMenuItem("Item 1"),
    dbc.DropdownMenuItem("Item 2"),
    dbc.DropdownMenuItem("Item 3"),
]

ode = base64.b64encode(open('apps/Apoio/ode.png', 'rb').read()) #logo do ODE
# try running the app with one of the Bootswatch themes e.g.
# app = dash.Dash(external_stylesheets=[dbc.themes.JOURNAL])
# app = dash.Dash(external_stylesheets=[dbc.themes.SKETCHY])

# make a reuseable navitem for the different examples

# make a reuseable dropdown for the different examples
dropdown = dbc.DropdownMenu(  #opções que são mostradas no menu
    children=[
                dbc.DropdownMenuItem("Mapa Geral", href="/mapa-ufpb"),       
                dbc.DropdownMenuItem("Análise Vocabular", href="/estudo-vocabular"),
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem("Dados discentes", href="/discente"),
                dbc.DropdownMenuItem("Dados docentes", href="/docente"),
                dbc.DropdownMenuItem(divider=True),
            
                dbc.DropdownMenu(
                    label = 'Desenvolvendo',
                    children = [    
                        dbc.DropdownMenuItem("docentes", href="/novo-docentes", style={'width': '100%','display': 'flex', 'align-items':'center', 'justify-content':'center'}),
                        dbc.DropdownMenuItem(divider=True),
                        dbc.DropdownMenuItem("projetos", href="/novo-projetos", style={'width': '100%','display': 'flex', 'align-items':'center', 'justify-content':'center'}),  
                        dbc.DropdownMenuItem(divider=True),
                        dbc.DropdownMenuItem("novos alunos", href="/novos-alunos", style={'width': '100%','display': 'flex', 'align-items':'center', 'justify-content':'center'}),
                        dbc.DropdownMenuItem(divider=True),
                        dbc.DropdownMenuItem("Dados docentes 2022", href="/docentes2022", style={'width': '100%','display': 'flex', 'align-items':'center', 'justify-content':'center'}),  
                    ],
                    nav=True,
                    in_navbar=True,
                    toggle_style={"color": "#212529", "background-color":'white'},
                    style={'background-color':'white','width': '100%','display': 'flex', 'align-items':'center', 'justify-content':'center'},
                    
                ),

                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem("Projetos", href="/projetos"),
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem("Quem somos?", href="/quemsomos"),
                html.A(dbc.DropdownMenuItem('Sair'),href='/'),             
    ],

    nav=True,
    in_navbar=True,
    label="Menu",
    toggle_style={"color": "white", "background-color":'#04383f'},
    color="primary",

    style={'background-color':'#022327', 'width': '100%', 'display': 'flex', 'align-items':'center', 'justify-content':'center'}
)
# this is the default navbar style created by the NavbarSimple component

# here's how you can recreate the same thing using Navbar


# this example that adds a logo to the navbar brand




def Navbar():

    navbar = dbc.Navbar(
        dbc.Container(
            [
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row(  #logo do ode que fica na navbar
                        [
                            dbc.Col(html.Img(src='data:image/png;base64,{}'.format(ode.decode()), height="50px")),
                            dbc.Col(dbc.NavbarBrand('Home', className="ml-2",href='/home',style={'color':'white'})),
                        ],
                        align="center",
                        no_gutters=True,
                        style={'background-color':'#04383f','fontColor':'white'}
                    ),
                    
                ),
                dbc.NavbarToggler(id="navbar-toggler2"),
                dbc.Collapse(
                    dbc.Nav(
                        [dropdown], className="ml-auto", navbar=True
                    ),
                    id="navbar-collapse2",
                    navbar=True,
                    style={'background-color':'#04383f', 'fontColor':'white'}
                ),
            ]
        ),
        color = '#04383f',
        sticky='top',
    )

    return navbar




