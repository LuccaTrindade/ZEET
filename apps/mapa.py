from logging import PlaceHolder
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
from dash.dependencies import Output, Input
## Navbar
# from navbar import Navbar
from . import navbar
from app import app

style1 = {'fillColor': '#00FFFFFF', 'lineColor': '#00FFFFFF','zoom_on_click':'False'}

nav = navbar.Navbar()    

retval = os.getcwd()

grupos = ['CCHLA','CEAR','CCSA','CE','CCJ','CT','CBIOTEC','CCTA','CCEN','CCS','CCM'] 
dados = ['Quantidade de projetos em 2017','Quantidade de projetos em 2018','Quantidade de projetos em 2019','Quantidade de projetos em 2020','Quantidade de projetos em 2021','Quantidade de projetos em 2022'] 

dict_csv = {'Quantidade de projetos em 2017' : 'apps/Apoio/dados/dataset_2017.csv',
            'Quantidade de projetos em 2018' : 'apps/Apoio/dados/dataset_2018.csv',
    		'Quantidade de projetos em 2019' : 'apps/Apoio/dados/dataset_2019.csv',
            'Quantidade de projetos em 2020' : 'apps/Apoio/dados/dataset_2020.csv',
            'Quantidade de projetos em 2021' : 'apps/Apoio/dados/dataset_2021.csv',
            'Quantidade de projetos em 2022' : 'apps/Apoio/dados/dataset_2022.csv'
}

def escala_mapa(max):
    step = (max/9)
    myscale=np.arange(1, max, step).tolist()
    myscale.extend([max])
    return myscale

dict_ajeita_ano = {'Quantidade de projetos em 2017': '2017', 'Quantidade de projetos em 2018': '2018', 'Quantidade de projetos em 2019': '2019','Quantidade de projetos em 2020':'2020','Quantidade de projetos em 2021':'2021','Quantidade de projetos em 2022':'2022'}

#state_data=pd.read_csv('C:\\Users\\gabri\\OneDrive\\??rea de Trabalho\\Pasta de backup\\ODE\\dados\\projetos_2017.csv', engine='python')
#geo_data = 'C:\\Users\\gabri\\OneDrive\\??rea de Trabalho\\Pasta de backup\\ODE\\ufpb_centros.json'   

state_data=pd.read_csv('apps/Apoio/Projetos_2017.csv', engine='python')
geo_data = 'apps/Apoio/ufpb_centros.json'  


professores_envolvidos ={
'CBIOTEC2017': 7,
 'CBIOTEC2018': 13,
 'CBIOTEC2019': 12,
 'CBIOTEC2020': 8,
 'CBIOTEC2021': 8, #mudar os 2021 e 2022 de todos!!!
 'CBIOTEC2022': 9,
 'CCA2017': 64,
 'CCA2018': 75,
 'CCA2019': 79,
 'CCA2020': 75,
 'CCA2021': 56,
 'CCA2022': 52,
 'CCAE2017': 56,
 'CCAE2018': 74,
 'CCAE2019': 97,
 'CCAE2020': 101,
 'CCAE2021': 78,
 'CCAE2022': 41,
 'CCEN2017': 43,
 'CCEN2018': 49,
 'CCEN2019': 54,
 'CCEN2020': 72,
 'CCEN2021': 63,
 'CCEN2022': 48,
 'CCHLA2017': 90,
 'CCHLA2018': 129,
 'CCHLA2019': 141,
 'CCHLA2020': 168,
 'CCHLA2021': 147,
 'CCHLA2022': 103,
 'CCHSA2017': 44,
 'CCHSA2018': 59,
 'CCHSA2019': 60,
 'CCHSA2020': 66,
 'CCHSA2021': 60,
 'CCHSA2022': 51,
 'CCJ2017': 26,
 'CCJ2018': 37,
 'CCJ2019': 57,
 'CCJ2020': 48,
 'CCJ2021': 45,
 'CCJ2022': 33,
 'CCM2017': 26,
 'CCM2018': 37,
 'CCM2019': 57,
 'CCM2020': 48,
 'CCM2021': 45,
 'CCM2022': 39,
 'CCS2017': 238,
 'CCS2018': 296,
 'CCS2019': 395,
 'CCS2020': 335,
 'CCS2021': 293,
 'CCS2022': 222,
 'CCSA2017': 54,
 'CCSA2018': 85,
 'CCSA2019': 112,
 'CCSA2020': 92,
 'CCSA2021': 74,
 'CCSA2022': 53,
 'CCTA2017': 108,
 'CCTA2018': 139,
 'CCTA2019': 171,
 'CCTA2020': 177,
 'CCTA2021': 117,
 'CCTA2022': 101,
 'CE2017': 67,
 'CE2018': 92,
 'CE2019': 104,
 'CE2020': 102,
 'CE2021': 125,
 'CE2022': 91,
 'CEAR2017': 11,
 'CEAR2018': 17,
 'CEAR2019': 20,
 'CEAR2020': 17,
 'CEAR2021': 19,
 'CEAR2022': 16,
 'CI2017': 15,
 'CI2018': 18,
 'CI2019': 34,
 'CI2020': 19,
 'CI2021': 14,
 'CI2022': 11,
 'CT2017': 68,
 'CT2018': 64,
 'CT2019': 62,
 'CT2020': 68,
 'CT2021': 56,
 'CT2022': 44,
 'CTDR2017': 24,
 'CTDR2018': 27,
 'CTDR2019': 33,
 'CTDR2020': 40,
 'CTDR2021': 35,
 'CTDR2022': 24
 }

chama_ano_criacao = {   
    'CCHLA': 1949
    ,'CEAR': 2011
    ,'CCSA': 1934
    ,'CE': 1978  
    ,'CCJ':1949
    ,'CT': 1974 
    ,'CBIOTEC':2011
    ,'CCTA':2012
    ,'CCEN': 1974
    ,'CCS': 1974
    ,'CCM': 2007
    ,'CCA': 1936
    ,'CCHSA': 2008
    ,'CCAE': 2006
    ,'CI':2012
    ,'CTDR': 2009
} 

chama_departamentos = {   
    'CCHLA': 11
    ,'CEAR': 2
    ,'CCSA': 6
    ,'CE': 7  
    ,'CCJ':5
    ,'CT': 7 
    ,'CBIOTEC':2
    ,'CCTA': 7
    ,'CCEN':9
    ,'CCS':13
    ,'CCM': 5
    ,'CCA': 7
    ,'CCHSA': 6
    ,'CCAE': 8
    ,'CTDR': 3
    ,'CI': 3
} 
  
chama_cursos = {   
    'CCHLA': ['Ci??ncias Sociais','Comunica????o em M??dias Digitais', 'Filosofia', 'Hist??ria', 'Letras', 'Letras / Ead', 'Letras - Libras', 'Letras(L??ngua Espanhola)','Letras(L??ngua Francesa)','Letras(L??nguas Cl??ssicas)','Letras(L??ngua Inglesa)','L??nguas Estrangeiras Aplicadas ??s Negocia????es Internacionais', 'Psicologia','Servi??o Social','Tradu????o']
    ,'CEAR': ['Engenharia El??trica', 'Engenharia de Energias Renovaveis']
    ,'CCSA': ['Admnistra????o', 'Admnistra????o P??blica','Arquivologia','Biblioteconomia', 'Ci??ncias Atuariais','Ci??ncias Cont??beis','Ci??ncias Econ??micas','Gest??o P??blica','Rela????es Internacionais','Tecnologia em Gest??o P??blica']
    ,'CE': ['Ci??ncias das Religi??es','Ci??ncias Naturais','Pedagogia','Pedagogia - EAD', 'Pedagogia(Educa????o Do Campo)','Pedagogia(MSC)','Psicopedagogia(BACH)']  
    ,'CCJ':['Direito']
    ,'CT': ['Arquitetura e Urbanismo','Engenharia Ambiental','Engenharia Civil','Engenharia De Alimentos','Engenharia De Materiais','Engenharia de Produ????o','Engenharia de Produ????o Mec??nica','Engenharia Mec??nica','Engenharia Qu??mica','Qu??mica Industrial']
    ,'CBIOTEC':['Biotecnologia']
    ,'CCTA': ['Artes Visuais','Cinema e Audiovisual','Comunica????o Social','Dan??a','Educa????o Art??stica','Hotelaria', 'Jornalismo','M??sica','M??sica - Bacharelado', 'M??sica Popular', 'Radialismo','Reg??ncia De bandas E Fanfarras','Rela????es P??blicas', 'Teatro(Bacharelado)','Teatro(Licenciatura)','Turismo']
    ,'CCEN':['Ciencias','Ci??ncias Biol??gicas','Ci??ncias Biol??gicas - EAD', 'Computa????o', 'Estat??stica','F??sica','Geografia','Matem??tica','Matem??tica - EAD', 'Qu??mica' ]
    ,'CCS':['Biomedicina','Educa????o F??sica','Educa????o F??sica - Licenciatura','Enfermagem','Farm??cia','Fisioterapia','Fonoaudiologia','Nutri????o','Odontologia','Terapia Ocupacional']
    ,'CCM': ['Medicina']
    ,'CCA': ['Agronomia','Ci??ncias biol??gicas', 'Medicina Veterinaria','Qu??mica','Zootecnia']
    ,'CCHSA': ['Admnistra????o','Agroecologia','Agroindustria','Ci??ncias Agr??rias','Curso Superior de Tecnologia em Cooperativismo','Pedagogia']
    ,'CCAE': ['Admnistra????o','Antropologia','Ci??ncia da Computa????o','Ci??ncias Cont??beis','Design','Ecologia','Hotelaria','Letras','Letras(Espanhol)','Letras(Ingl??s)','Matem??tica','Pedagogia','Secretariado Executivo Bil??ngue','Sistemas de Informa????o']
    ,'CTDR': ['Gastronomia','Tecnologia de Alimentos','Tecnologia em Produ????o Sucroaalcoleira']
    ,'CI': ['Ci??ncia da Computa????o','Ci??ncia de Dados e Intelig??ncia Artificial','Engenharia da Computa????o','Matem??tica Computacional']
}   

chama_assessor = {   
    'CCHLA': 'N??via Pereira'
    ,'CEAR': 'Jose Mauricio Ramos de Souza Neto'
    ,'CCSA': 'Danielle Vieira'
    ,'CE': 'Qu??zia Furtado, M?? da Concei????o Miranda'
    ,'CCJ':'Ludmila Cerqueira'
    ,'CT': 'Aur??lia Idrogo, Luzia Camboim'
    ,'CBIOTEC':'Elis??ngela A. de Moura Kretzschmar'
    ,'CCTA': 'Luceni Caetano' 
    ,'CCEN':'Jane Torelli'
    ,'CCS': 'Rosen??s Lima'
    ,'CCM': 'Andr?? Bonif??cio'
    ,'CCA': 'F??bio Mielezrsk'  
    ,'CCHSA': 'Vivian Galdino'
    ,'CCAE': 'Joc??lio de Oliveira'
    ,'CI': 'Jos?? Miguel Aroztegui'
    ,'CTDR': 'Ana Braga'
} 



chama_diretor = {   
    'CCHLA': 'Rodrigo Freire de Carvalho e Silva'
    ,'CEAR': ' Euler C??ssio Tavares de Mac??do'
    ,'CCSA': 'Walmir Rufino Da Silva'
    ,'CE': 'Wilson Honorato Arag??o'
    ,'CCJ':'Fredys Orlando Souto'
    ,'CT': 'Ant??nio de Mello Villar'
    ,'CBIOTEC':'Valdir de Andrade Braga'
    ,'CCTA': 'Jos?? David Campos Fernandes'
    ,'CCEN':'Jos?? Roberto Soares do Nascimento'
    ,'CCS':'Jo??o Euclides Fernandes Braga'
    ,'CCM': 'Eduardo S??rgio Moura Souza'
    ,'CCA': 'Manuel Bandeira de Albuquerque'
    ,'CCHSA': 'Terezinha Domiciano Martins'
    ,'CCAE': 'Maria Angeluce Soares Per??nico Barbotin'
    ,'CI': 'Hamilton Soares da Silva'
    ,'CTDR': 'Jos?? Marcelino Oliveira Cavalheiro'
} 

chama_vice = {   
    'CCHLA': 'Marcelo Sitcovsky Santos Pereira'
    ,'CEAR': 'Marcal Rosas F. Lima Filho'
    ,'CCSA': 'Aldo Leonardo Cunha Callado'
    ,'CE': 'Swamy de Paula Lima Soares'
    ,'CCJ': 'Valfredo de Andrade Aguiar Filho'
    ,'CT': 'Tarciso Cabral da Silva' 
    ,'CBIOTEC': 'Fab??ola da Cruz Nunes'
    ,'CCTA': 'Ulisses Carvalho da Silva'
    ,'CCEN': 'Severino Francisco de Oliveira'
    ,'CCS':'Fabiano Gonzaga Rodrigues'
    ,'CCM': 'Eut??lia Freire'
    ,'CCA': 'Ricardo Rom??o Guerra'
    ,'CCHSA': 'Pedro Germano Antonio Nunes'
    ,'CCAE': 'Alexandre Scaico'
    ,'CI': 'Luc??dio dos Anjos Formiga Cabral'
    ,'CTDR': 'Jo??o Andrade da Silva'
} 

centro_extenso = {   
    'CCHLA': 'Centro de Ci??ncias Humanas, Letras e Artes'
    ,'CEAR': 'Centro de Energias Alternativas e Renov??veis'
    ,'CCSA': 'Centro de Ci??ncias Sociais Aplicadas'
    ,'CE': 'Centro de Educa????o'
    ,'CCJ': 'Centro de Ci??ncias Jur??dicas'
    ,'CT': 'Centro de Tecnologia' 
    ,'CBIOTEC': 'Centro de Biotecnologia'
    ,'CCTA': 'Centro de Comunica????o, Turismo e Artes'
    ,'CCEN': 'Centro de Ci??ncias Exatas e da Natureza'
    ,'CCS':'Centro de Ci??ncias da Sa??de'
    ,'CCM': 'Centro de Ci??ncias M??dicas'
    ,'CCA': 'Centro de Ciencias Agr??rias'
    ,'CCHSA': 'Centro de Ci??ncias Humanas, Sociais e Agr??rias'
    ,'CCAE': 'Centro de Ci??ncias Aplicadas e Educa????o'
    ,'CI': 'Centro de Inform??tica'
    ,'CTDR': 'Centro de Tecnologia e Desenvolvimento Regional'
} 


def chama_projetos(file,dado):
    state_data_1=pd.read_csv(dict_csv[dado], engine='python')
    filtered = [file]
    state_data_1 = state_data_1[state_data_1['centros'].isin(filtered)]
    lista= list(state_data_1['qtd_projeto'])
    return lista[0]

dict_coordenadas = {
    'cbiotec' : [-7.140993, -34.846455],
    'ccen'  : [-7.139640, -34.845020],    
    'cchla' : [-7.139370, -34.850374], 
    'ccj' :  [-7.141978, -34.848935], 
    'ccm' : [-7.136423, -34.840567 ],    
    'ccs' :  [-7.135673, -34.841516],  
    'ccsa' :  [-7.141069, -34.849936],   
    'ccta' : [-7.137422, -34.849572],  
    'ce' : [-7.139994, -34.850124],  
    'cear' : [-7.141625, -34.850556],  
    'ct' : [-7.142505, -34.850309],
    'cca'  : [-6.973692, -35.716273],   
    'ccae'  : [-6.829091, -35.118770],
    'cchsa'  : [-6.752077, -35.647532],
    'ci':[-7.162211,-34.817228],
    'ctdr':[-7.163018,-34.817989]
} 

#folder ='C:\\Users\\gabri\\OneDrive\\??rea de Trabalho\\Pasta de backup\\ODE\\logos'    
folder ='apps/Apoio/logos'    

extension = '*'                               
separator = ','                                    
extension = '*.' + extension  
os.chdir(folder)             
files_logos= glob.glob(extension)   

os.chdir(retval)             

#folder_1 ='C:\\Users\\gabri\\OneDrive\\??rea de Trabalho\\Pasta de backup\\ODE\\arquivos_json' 
#folder_1 ='C:Apoio\\arquivos_json' 
folder_1='apps/Apoio/arquivos_json'
os.chdir(folder_1)             
files_json= glob.glob(extension)   
os.chdir(retval)             

#folder_2 ='C:\\Users\\gabri\\OneDrive\\??rea de Trabalho\\Pasta de backup\\ODE\\dados' 
folder_2 ='apps/Apoio/dados' 
os.chdir(folder_2)             
files_dados= glob.glob(extension)   
os.chdir(retval)             

tooltip = "Clique para abrir a imagem"     
html1 = '<img src="data:image/png;base64,{}">'.format  

def limpa_nome_arquivo_json(logo):   
    files=logo.replace('json','')      
    files=files.replace('.','') 
    return files 

def limpa_nome_arquivo(logo):  
    files=logo.replace('jpeg','')      
    files=files.replace('jpg','')  
    files=files.replace('png','')  
    files=files.replace('.','') 
    return files 

def gera_cloropleth(geo_data,state_data,files_dados,mapa_,dado,grupos):

    state_data_1=[] 
    state_data_1=pd.read_csv(dict_csv[dado], engine='python')
    #print(str(state_data_1)*100)
    #geo_data = 'C:\\Users\\Pessoal\\Desktop\\ODE\\choropleth\\gp_1.json'      
    #geo_data = 'apps/Apoio/choropleth/json_divisao_centros.json'  
    with open('apps/Apoio/choropleth/json_divisao_centros.json') as jsonfile:
        input_dict = json.load(jsonfile)

    lista_features = [x for x in input_dict['features'] if x['id'] in grupos]

    #geo_data = json.dumps(lista_features)
    geo_data ={'type': 'FeatureCollection','features': lista_features}

    filtered = grupos
    state_data_1 = state_data_1[state_data_1['centros'].isin(filtered)]  

    #myscale = (state_data_1['qtd_projeto'].quantile((0,0.12,0.22,0.32,0.42,0.52,0.72,0.82,0.92,1))).tolist()
    maxi=max(list(state_data_1['qtd_projeto']))
    myscale=escala_mapa(maxi)
    myscale=[float(i) for i in myscale]
    try:
        folium.Choropleth(   
                geo_data = geo_data, 
                name='Choropleth',
                data=state_data_1,    
                columns=['centros', 'qtd_projeto'],   
                key_on='feature.id', 
                fill_color='YlGn',    
                fill_opacity=0.7,   
                line_opacity=0.2,
                legend_name='Quantidade de projetos',   
                threshold_scale=myscale,
                #show=False,
                #overlay=False         
            ).add_to(mapa_) 
    except KeyError:
        pass

  

        
    #folium.LayerControl().add_to(map)
  
  

def gera_camadas_ufpb(arquivo_json,mapa_,logo):    
    #AQUIII
    picture1 = base64.b64encode(open('apps/Apoio/logos/' + logo ,'rb').read()).decode()
    #img = Image.open('apps/Apoio/logos/' + logo)

    iframe1 = IFrame(html1(picture1), width=200+20, height=200+20)   
    #icon1 = folium.features.CustomIcon('C:\\Users\\gabri\\OneDrive\\??rea de Trabalho\\Pasta de backup\\ODE\\logos\\' + logo, icon_size=(20,20))
    #camadas_ufpb = os.path.join('C:\\Users\\gabri\\OneDrive\\??rea de Trabalho\\Pasta de backup\\ODE\\arquivos_json\\' + arquivo_json)
    camadas_ufpb = os.path.join('apps/Apoio/arquivos_json/' + arquivo_json)

    arquivo_json=limpa_nome_arquivo_json(arquivo_json)

    camada=folium.GeoJson(camadas_ufpb,name=arquivo_json, tooltip='Clique para abrir a imagem',style_function=lambda x:style1).add_to(mapa_)    

    #camada.add_child(folium.Popup(dict_centros[arquivo_json]))
    camada.add_child(folium.Popup(iframe1,width=200+20,height=200+20))
    
    camada.add_to(mapa_)    




def gera_icones_da_ufpb(logo,dict_logo,dict_coordenadas,html1,tooltip,mapa_,arquivo_json,dado): 
    #AQUIII
    #picture1 = base64.b64encode(open('C:\\Users\\gabri\\OneDrive\\??rea de Trabalho\\Pasta de backup\\ODE\\logos\\' + logo ,'rb').read()).decode()
    files=limpa_nome_arquivo(logo) 
    file = files.upper()
    cur=chama_cursos[file]

    if dado == 0:
        html1=f"""
    <h1> Informa????es sobre o {file}</h1>
    Nome do Centro: {centro_extenso[file]}<br><br>  
    Ano de cria????o: {chama_ano_criacao[file]}<br><br>  
    N??mero de departamentos: {chama_departamentos[file]}<br><br> 
    Cursos: {', '.join(str(x) for x in cur)}<br><br>
    Diretor: {chama_diretor[file]}<br><br>
    Vice-Diretor: {chama_vice[file]}<br><br>
    Assessor(es): {chama_assessor[file]}<br><br>
    """  
    else:
        html1=f"""
    <h1> Informa????es sobre o {file}</h1>
    Nome do Centro: {centro_extenso[file]}<br><br>  
    Ano de cria????o: {chama_ano_criacao[file]}<br><br>
    N??mero de departamentos: {chama_departamentos[file]}<br><br>
    Cursos: {', '.join(str(x) for x in cur)}<br><br>
    Diretor: {chama_diretor[file]}<br><br>
    Vice-Diretor: {chama_vice[file]}<br><br>
    Assessor(es): {chama_assessor[file]}<br><br>
    {dado}: {chama_projetos(file,dado)}<br><br>
    Quantidade de professores Envolvidos: {professores_envolvidos[file + dict_ajeita_ano[dado]]}<br><br>
    """
    #picture1 = base64.b64encode(open('apps/Apoio/logos/' + logo ,'rb').read()).decode()
    arquivo_json=limpa_nome_arquivo_json(arquivo_json)
    #iframe1 = IFrame(html1(picture1), width=200+20, height=200+20)   
    icon1 = folium.features.CustomIcon('apps/Apoio/logos/' + logo, icon_size=(20,20))
      

    ifr = IFrame(html=html1, width=500, height=300)
    popup1 = folium.Popup(ifr, max_width=2650)
    #popup1 = folium.Popup(dict_centros[arquivo_json],max_width=600)       
    folium.Marker(location=dict_coordenadas[files],popup= popup1,tooltip='Clique para um maior conhecimento sobre centro',icon=icon1).add_to(mapa_)
    
def mapa_da_ufpb(tooltip, files_logos,dict_coordenadas,files_json,geo_data,state_data, files_dados,mapa_,flag,grupos,dado):
    files_json = []   
    files_logos = []   
    if 'CTDR' in grupos:
        files_json.extend(['CTDR.json'])
        files_logos.extend([ 'ctdr.png'])
    if 'CI' in grupos:
        files_json.extend(['CI.json'])
        files_logos.extend([ 'ci.png'])
    if 'CCA' in grupos:
        files_json.extend(['CCA.json'])
        files_logos.extend([ 'cca.png'])
    if 'CCAE' in grupos:
        files_json.extend(['CCAE.json'])
        files_logos.extend([ 'ccae.png'])
    if 'CCHSA' in grupos:
        files_json.extend(['CCHSA.json'])
        files_logos.extend([ 'cchsa.png'])
    if 'CCJ' in grupos:
        files_json.extend(['CCJ.json'])
        files_logos.extend([ 'ccj.png'])
    if 'CT' in grupos:
        files_json.extend(['CT.json'])
        files_logos.extend([ 'ct.png'])
    if 'CBIOTEC' in grupos:
        files_json.extend(['CBIOTEC.json'])
        files_logos.extend(['cbiotec.png'])
    if 'CCHLA' in grupos:
        files_json.extend(['CCHLA.json'])
        files_logos.extend([ 'cchla.png'])
    if 'CEAR' in grupos:
        files_json.extend(['CEAR.json'])
        files_logos.extend([ 'cear.png'])
    if 'CCSA' in grupos:
        files_json.extend(['CCSA.json'])
        files_logos.extend([ 'ccsa.png'])
    if 'CE' in grupos:
        files_json.extend(['CE.json'])
        files_logos.extend(['ce.png'])
    if 'CCTA' in grupos:
        files_json.extend(['CCTA.json'])
        files_logos.extend(['ccta.png'])
    if 'CCEN' in grupos:
        files_json.extend(['CCEN.json'])
        files_logos.extend(['ccen.png'])
    if 'CCHLA' in grupos:
        files_json.extend(['CCHLA.json'])
        files_logos.extend([ 'cchla.png'])
    if 'CCS' in grupos:
        files_json.extend(['CCS.json'])
        files_logos.extend([ 'ccs.png'])
    if 'CCM' in grupos:
        files_json.extend(['CCM.json'])
        files_logos.extend(['ccm.png'])
  
    if flag == 'nao' or dado == 0: 
        for arquivo_json,logo in zip(files_json,files_logos):
            gera_camadas_ufpb(arquivo_json,mapa_,logo)  
    for arquivo_json,logo in zip(files_json,files_logos):    
        gera_icones_da_ufpb(logo,logo,dict_coordenadas,html1,tooltip,mapa_,arquivo_json,dado)
    if flag == 'sim' and grupos != [] and dado != 0:
        print('cheguei',flush=True)  
        gera_cloropleth(geo_data,state_data,files_dados,mapa_,dado,grupos)    
    #mapa_.save("C:\\Users\\gabri\\OneDrive\\??rea de Trabalho\\Pasta de backup\\ODE\\mapa_ufpb_centros.html") 
    mapa_.save("apps/Apoio/mapa_ufpb_centros.html") 
tabs = html.Div(
    [    
        dbc.Tabs(
            [
                dbc.Tab(label="Areia", tab_id="tab-1"),
                dbc.Tab(label="Bananeiras", tab_id="tab-2"),
                dbc.Tab(label="Jo??o Pessoa", tab_id="tab-3"),
                dbc.Tab(label="Mangabeira - JP", tab_id="tab-5"),
                dbc.Tab(label="Mamanguape", tab_id="tab-4"),
            ],
            id="tabs",
            active_tab="tab-3",
            card=True
        ),
        html.Div(id="content"),
    ]
)


card_content = [
    dbc.CardHeader("Filtros do Mapa",style={'font-size':24, 'textAlign':'center'}),
    dbc.CardBody(
        [
        tabs,
        html.Div(html.Br()),
        html.H4("Escolha o grupo desejado:", style={'font-size':19,'margin-top':'14px'}),
        dcc.Dropdown(
        id = 'grupos',  
        options=[
            {'label': j, 'value': j} for j in grupos  
        ],
        value=['Todos os centros'],   
        multi=True,
        searchable=False,
        placeholder="Selecione o(s) centro(s) desejados",
    ),
    

    html.Div(html.Br()),
    html.H4("Deseja analisar o mapa pelo quantitativo de projetos por ano?", style={'font-size':19}),

    dbc.RadioItems(
                    options=[  
                        {'label': 'Sim', 'value': 'sim'},
                        {'label': 'N??o', 'value': 'nao'},      

                    ],
                    id='flag',
                    value='1',
                    inline = True,
                    labelStyle={'display': 'inline-block','margin-bottom':'10px'}   
                ),
    html.Div([
    html.H4("Escolha o ano para visualizar o mapa:", style={'font-size':19}),

    dcc.Dropdown(
        id = 'dados',  
        options=[
            {'label': j, 'value': j} for j in dados  
        ],
        value=0,   
         multi=False,
    searchable=False,
         style={'margin-bottom':'10px'}

    ),],
    id='choropleth',
    style = {'display': 'none'}),
        ]
    ),
]

jumbotron = dbc.Card(card_content,  outline=True)

card_content_3 = [
    dbc.CardHeader("Mapa da UFPB",style={'font-size':24, 'textAlign':'center'}),
    dbc.CardBody(
        [
            html.Iframe(id='mapa', srcDoc=open('apps/Apoio/mapa_ufpb_centros.html', 'r').read(),width='100%',height='580px'), 
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


layout = html.Div([
nav,

body_1,
    html.Div([], id='value-container', style={'display': 'none'})

    #html.Iframe(id='mapa', srcDoc=open('C:\\Users\\gabri\\OneDrive\\??rea de Trabalho\\Pasta de backup\\ODE\\mapa_ufpb_centros.html', 'r').read(), width='100%', height='430'),  

    #html.Iframe(id='mapa', srcDoc=open('apps/Apoio/mapa_ufpb_centros.html', 'r').read(), width='100%', height='430'),  
])
    
@app.callback(
   dash.dependencies.Output('choropleth', 'style'),
	[dash.dependencies.Input('flag', 'value')])             

def some_o_grafico_para_aparecer_os_outros(valor):
	if valor == 'nao':
		return {'display': 'none'}
	if valor == 'sim':
		return {'display': 'block'} 
	else:
		return {'display': 'none'}         

@app.callback(
   dash.dependencies.Output('dados', 'value'),
	[dash.dependencies.Input('flag', 'value')])             

def some_o_grafico_para_aparecer_os_outros(valor):
	if valor == 'nao':
		return 0
	else:
		return dash.no_update


@app.callback(
   dash.dependencies.Output('value-container', 'style'),
	[dash.dependencies.Input('grupos', 'value')])

def some_o_grafico_para_aparecer_os_outros(grupos):
	return {'display': 'none'}



@app.callback(
   dash.dependencies.Output('grupos', 'value'),
	[dash.dependencies.Input('tabs', 'active_tab'),dash.dependencies.Input('value-container', 'style')],[dash.dependencies.State('grupos', 'value')])             

def some_o_grafico_para_aparecer_os_outros(tabs,flag,grupos):
	if 'Todos os centros' in grupos:
		valor = True
	else:
		valor = False
	if valor == False or tabs == 'tab-1' or tabs == 'tab-2' or tabs == 'tab-4':
		return grupos
	if valor == True and tabs =='tab-3':
		return ['CCHLA','CEAR','CCSA','CE','CCJ','CT','CBIOTEC','CCTA','CCEN','CCS','CCM']
	if valor == True and tabs =='tab-5':
		return ['CI','CTDR']           







@app.callback(
   dash.dependencies.Output('grupos', 'options'),
	[dash.dependencies.Input('tabs', 'active_tab')])             

def ajeita_entrada_valores(tabs):
	if tabs == 'tab-1':
		return [{'label': j, 'value': j} for j in ['CCA']]
	if tabs == 'tab-2':
		return [{'label': j, 'value': j} for j in ['CCHSA']]
	if tabs == 'tab-3':
		return [{'label': j, 'value': j} for j in ['Todos os centros','CCHLA','CEAR','CCSA','CE','CCJ','CT','CBIOTEC','CCTA','CCEN','CCS','CCM']]
	if tabs == 'tab-4':
		return [{'label': j, 'value': j} for j in ['CCAE']]
	if tabs == 'tab-5':
		return [{'label': j, 'value': j} for j in ['Todos os centros','CI','CTDR']]

@app.callback(
	dash.dependencies.Output('mapa', 'srcDoc'),
	[dash.dependencies.Input('grupos', 'value'),
	dash.dependencies.Input('dados', 'value'),
	dash.dependencies.Input('flag', 'value'),
	dash.dependencies.Input('tabs', 'active_tab')])

def update_map(grupos,dado,flag,tabs):
	print(tabs)
	if tabs == 'tab-5':
		base = os.path.join('apps/Apoio/base_mangabeira.json')
		mapa_ = folium.Map(location= [-7.162806, -34.817641], zoom_start=15,tiles='cartodbpositron')    
	if tabs == 'tab-3':
		base = os.path.join('apps/Apoio/base_ufpb.json')
		mapa_ = folium.Map(location= [-7.1385,-34.8464], zoom_start=15,tiles='cartodbpositron')
	if tabs == 'tab-1':
		base = os.path.join('apps/Apoio/base_areia.json')
		mapa_ = folium.Map(location= [-6.973741,-35.716276], zoom_start=15,tiles='cartodbpositron')
	if tabs == 'tab-2':
		base = os.path.join('apps/Apoio/base_bananeiras.json')
		mapa_ = folium.Map(location= [-6.751973,-35.647689], zoom_start=15,tiles='cartodbpositron')
	if tabs == 'tab-4':
		base = os.path.join('apps/Apoio/base_mamanguape.json')
		mapa_ = folium.Map(location= [-6.829537,-35.118103], zoom_start=15,tiles='cartodbpositron')
	folium.GeoJson(base, name='base').add_to(mapa_)

	mapa_da_ufpb(tooltip, files_logos,dict_coordenadas,files_json,geo_data,state_data, files_dados,mapa_,flag,grupos,dado)  
	#return open('C:\\Users\\gabri\\OneDrive\\??rea de Trabalho\\Pasta de backup\\ODE\\mapa_ufpb_centros.html', 'r').read()
	return open('apps/Apoio/mapa_ufpb_centros.html', 'r').read()  


