Atividade Prática - Filipe Augusto Santos de Moura (20.2.8079)

Tecnologias Escolhidas:
O jogo foi desenvolvido utilizando a linguagem Python (3.10.6), a bibliteca de GUI Dearpygui e o protocolo TCP.

A fim de preservar a máquina do usuário, foi criado um ambiente virtual para que a biblioteca não permaneça instalada no computador após o fim da avaliação. Cabe ao usuário querer utilizá-lo ou não. O ambiente virtual facilita na compatibilidade de versões, permitindo que as versões utilizadas durante o desenvolvimento sejam as mesmas para o usuário que irá utilizar o script.

Comandos para execução:

- Utilizando ambiente virtual (Caso não queira basta ignorar os 3 próximos passos):
  python3 -m pip install --user virtualenv (Caso nao tenha o virtualenv instalado. Para verificar: virtualenv --version)
  virtualenv venv
  source venv/bin/activate


pip install -r requirements.txt (Instalar as dependencias de GUI)
python3 server.py
python3 client.py

Após executar o Client e Servidor, duas janelas devem aparecer ao usuário, representando cada um dos processos.


*Foi implementado o desafio proposto, onde o usuário possui algumas opções de análise da String digitada.
*Para sair do ambiente virtual, basta digitar 'deactivate'
