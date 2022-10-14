# 📋 Repositório Principal do ODE

A página dash do ODE é constituída por 4 elementos principais: o arquivo app.py,o arquivo index.py, a pasta apps,  e o arquivo login.py.

- O arquivo app.py diz respeito apenas a crição do template da aplicação em si, porém não é ele quem incializa a aplicação, ficando apenas como espécie de coadjuvante para atender a sintaxe imposta pelo dash.

- O arquivo index.py é o nosso arquivo principal, é ele o responsável por iniciar a aplicação (o server flask, nesse caso em específico), além de redirecionar o layout da página desejada de acordo com a url escolhida.

- a pasta apps é o local que contém todos os nossos templates e callbacks da aplicação, sendo compsota por arquivos diferentes referentes a cada uma de suas funções. Por exemplo, o arquivo variacao.py contém o layout e as callbacks referentes a aba de estudo vocabular, e assim ocorre também para as páginas discentes, docentes, etc.

- O arquivo login é o responsável por iniciar o servidor que suporta o nosso site, nesse caso utilizando a bilioteca flask. Sendo esse arquivo responsável por colocar uma tela de login antes de abrir a tela principal, além de gerenciar o que acontece depois e durante esse procedimento.
