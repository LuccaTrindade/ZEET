from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
    redirect,
    flash
    # flash serve para criar um tipo de mensagem, que pode ser resgatada do
    # arquivo .html, nesse caso utilizamos quando o usuário coloca o
    # usuário/senha inválidos.
)

####para operações com e-mail
from flask_mail import Mail,Message
from itsdangerous import SignatureExpired, URLSafeSerializer #responsável pelo token e da validade da confirmação do email.
####

import mysql.connector ##Estamos usando MySql para o nosso Banco de Dados

from logging import FileHandler, WARNING
import pandas as pd

import os #para pegar a variável de ambiente

#variáveis de ambiente
key = str( os.environ.get("KEY") )

key = bytes(key, 'utf-8') #converte a key para binário

email_local = str( os.environ.get("EMAIL") )
senha_local = str( os.environ.get("SENHA") )
senha_database = str( os.environ.get("SENHA_DATABASE") )
id_database = str( os.environ.get("ID_DATABASE") )
app_secret_key = str( os.environ.get("APP_SECRET_KEY") )

app = Flask(__name__)
app.secret_key = app_secret_key #essa secret_key é um parâmetro utilizado para criptografia do site, ela não é utilizada diretamente, mas o flash a utiliza em seus métodos, de modo a proteger o site contra ataques.

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = email_local
app.config['MAIL_PASSWORD'] = senha_local
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


'''conn = mysql.connector.connect(
    host='sql10.freemysqlhosting.net',
    user='sql10514081',
    passwd='tFANMR9IfU',
    port='3306',
    database="sql10514081"
)'''

'''mycursor = conn.cursor()'''

mail = Mail(app)

# print apenas para depuração.
flag_debug = False
def debug_print(*args, **kwargs):
    if flag_debug:
        print(*args, **kwargs)

class User:
    def __init__(self, username, password, email, status,nome,matricula,membro,descricao):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.status = status
        self.nome = nome
        self.matricula = matricula
        self.membro = membro
        self.descricao = descricao


    def __repr__(self):
        return f'<User: {self.username},Password: {self.password},Email: {self.email},status:{self.status}>'

def carrega_df(cursor):


    cursor.execute("select * from  registro")

    myresult= mycursor.fetchall()
    colnames = [desc[0] for desc in cursor.description]
    """
    print("COLNAMES - REMOVE")
    print(colnames)
    print("itens")
    print(myresult)
    """
    df = pd.DataFrame(data=myresult, columns=colnames)  #carrega a tabela da base de dados carregada
    return df


from cryptography.fernet import Fernet

def criptografar(var):
    f = Fernet(key)
    usuario_escondido = f.encrypt( bytes(var, 'utf-8') )
    usuario_escondido_salvar = usuario_escondido.decode('utf-8') #converte de binário para texto
    return usuario_escondido_salvar
def descriptografar(var):
    f = Fernet(key)
    ler = bytes(var, 'utf-8')
    visivel = f.decrypt(ler)
    return visivel.decode('utf-8')


def carrega_users(cursor):
    '''
    Lê a lista "users" do BD.
    '''
    df = carrega_df(cursor)

    global users
    users=[]

    for _,row in df.iterrows():
        users.append(User(username=row['usuario'], password=row['senha'], email=row['senha'], status=row['confirmado'],nome=row['nome'],matricula=row['matricula'],membro=row['membro'],descricao=row['descricao']))


    print("DEPURAÇÃO \n")
    # depuração
    for item in users:
        debug_print(item)
    debug_print('-----\n')

    return users

s = URLSafeSerializer(app.config['SECRET_KEY'])

def confirmar_email(status,email,username, nome, matricula, sim_nao,descricao):
    print("Confirmando emails... "*3)
    if(status!=1):
        with app.app_context():
            t = s.dumps (email,salt="email-confirm") #token
            print("O token eh : " + str(t))
            link = url_for('confirm_email', token=t,_external=True)

            descricao = str( descricao[0]  )

            global mensagem
            if(sim_nao=='sim'):
                mensagem = Message(subject="Confirmação de Email",
                        sender=app.config.get("MAIL_USERNAME"),
                        recipients=["j.guilherme.s.oliveira3@gmail.com"], # email de destino
                        body='{} soliciou o cadastramento no sistema do ODE, ele é membro da universidade, sob matrícula/siap {}, e registrou o seguinte interesse:"{}". O nome de usuário que ele deseja ter como cadastrado é "{}". O link para confirmação do cadastro é:{}.'.format(nome,matricula,descricao,username,link)
                    )

            else:
                mensagem = Message(subject="Confirmação de Email",
                    sender=app.config.get("MAIL_USERNAME"),
                    recipients=["j.guilherme.s.oliveira3@gmail.com"], # email de destino
                    body='{} soliciou o cadastramento no sistema do ODE, ele não é membro da universidade, mas registrou o seguinte interesse:"{}". O nome de usuário que ele deseja para cadastro é "{}". O link para confirmação do cadastro é:{}.'.format(nome,matricula,descricao,username,link)
                )
            try:
                mail.send(mensagem)
            except:
                print("exceção detectada, faça a confirmação manual xD")




'''users = carrega_users(mycursor)''' #carrega_users é uma função do prof Helon

## A página é baseada em um template do flask servidor para dash, ele
# basicamente vai redirecionando as urls de acordo com o sucesso/fracasso no
# login ou no cadastramento de um novo usuário.

# Essa parte abaixo diz respeito a uma tentativa de criar uma banco de dados
# para novos usuários, porém não obteve-se sucesso nesse processo.

if not app.debug:
    file_handler = FileHandler('errorlog.txt')
    file_handler.setLevel(WARNING) #o level WARNING não mostra mensagens de baixo nível, existe também o DEBUG que mostra todas as inforações de log. utilizamos o WARNING porque só queremos ter acesso aos erros.
    app.logger.addHandler(file_handler)
    #caso dê algum tipo de erro na execução do server, ele guarda as informações no arquivo errorlog.txt. O FileHandler é a classe responsável por fazer isso.


### A callback route faz com que dispare uma função toda vez que o usuário entre na url específicada
#Obs.: por padrão, a callback só responde a GET requests  (puxa dados remotos)
# POSTS requests são usados quando existem dados submetidos a serem processados (insere/atualiza dados remotos)


@app.route('/confirm_email/<token>')

def confirm_email(token):

    try:
        email = s.loads(token, salt="email-confirm") #sem max age (tempo)
        mycursor.execute("UPDATE registro SET confirmado=1 WHERE email = '%s'" %(email))
        conn.commit()

        carrega_users(mycursor)

        #https://pynative.com/python-sqlite-update-table/

        return redirect(url_for('login'))
    except SignatureExpired:
        print("Deu erro no cadastro :(")
        return redirect(url_for('login'))


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    global users
    # ele pega os dados de registro da função if e após isso, retorna o usuário
    # a url do login. Esse if é executado ao mesmo tempo do teplate registro.html,
    # fazendo com que o template de registro apareça.
    debug_print('route:/registro')
    #parte do registro (BANCO DE DADOS)
    if request.method == 'POST': #cadastro de novos usuários mydb
        print("REGISTRANDO NEW USER"*50)
        if (request.form['username_registro'] and request.form['email_registro'] and request.form['password_registro']):

            username = criptografar(request.form['username_registro'])
            password = criptografar(request.form['password_registro'])
            nome = criptografar(request.form['nome_registro'])
            matricula = criptografar(request.form['matricula_registro'])

            mycursor.execute(
                """
                INSERT INTO registro (usuario,nome,matricula,membro,descricao,email, senha,confirmado) VALUES (%s, %s, %s, %s,%s, %s, %s, %s)
                """,
                (
                    username,
                    nome,
                    matricula,
                    request.form['sim_nao'],
                    request.form["campo_descricao"],
                    request.form['email_registro'],
                    password,
                    0
                )
            )
            conn.commit()
            users = carrega_users(mycursor)

            status=0
            email = request.form['email_registro']
            username = request.form['username_registro']
            ###
            nome = request.form['nome_registro']
            matricula = request.form['matricula_registro']
            sim_nao = request.form['sim_nao']
            descricao = request.form["campo_descricao"],

            confirmar_email(status,email,username, nome, matricula, sim_nao,descricao)

            return redirect(url_for('login'))

    return render_template('registro.html')




@app.route('/login', methods=['GET', 'POST'])
def login():
    debug_print('route:/login')

    session['user_id']=None
    if request.method == 'POST':

        debug_print(f'request.method = {request.method}')
        session.pop('user_id', None)
        username = request.form['username']
        debug_print(username,flush=True)
        password = request.form['password']
        user = [x for x in users if descriptografar(x.username) == username and x.status==1]

        ##
        ##print("User------")
        ##print("\n")
        ##print(user)
        ##print("\n")
        ##print("User------")


        if user != []:
            user = user[0]
            try:
                user.password = descriptografar( str(user.password) )
                print(user.password)
                print("AQUI??"*100)
            except:
                None

        print(password)
        if user and user.password == password:
            #session['user_id'] = user.id
            return redirect(url_for('/home/_dash-update-component'))
        else:
            flash('Erro: \"Campo Usuario ou Senha: Inválido.\"')  #flash(mensagem,categoria) categoria={"error", "info" ou "warning"} (é um parâmetro opcional)

        return redirect(url_for('login'))

    return render_template('index.html') #isso é o que faz abrir o menu de login, quando entramos no site, ele é chamado pelo app.route('/')


@app.route('/home/') #esse é o caminho que fica no app.py, e quando ele é chamado, significa que o login foi feito, daí o usuário é direcionado para a homepage, para saber mais detalhes olhe também o arquivo index.py
def home():
    debug_print('route:/home')
    #time.sleep(3)
    #print('vamo ver2')
    return redirect(url_for('/home/_dash-update-component'))


@app.route('/')  # Quando a página ele, o usuário é redirecionado para /login
def inicio():
    debug_print('route:/inicio')


    #print('vamover3',flush=True)

    return redirect(url_for('/home/_dash-update-component'))

# if __name__ == '__main__':
#     server.run(port=1020)
