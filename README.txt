Atividade Prática - Filipe Augusto Santos de Moura (20.2.8079)

Tecnologias Escolhidas:
O jogo foi desenvolvido utilizando a linguagem Python (3.10.6), a bibliteca de GUI Dearpygui e o protocolo TCP.

A fim de preservar a máquina do usuário, foi criado um ambiente virtual para que a biblioteca não permaneça instalada no computador após o fim da avaliação. Cabe ao usuário querer utilizá-lo ou não. O 		ambiente virtual facilita na compatibilidade de versões, permitindo que as versões utilizadas durante o desenvolvimento sejam as mesmas para o usuário que irá utilizar o script.

Comandos para execução:

source venv/bin/activate (Caso queira utilzar o ambiente virtual, caso contrário ignore este passo)
pip install -r requirements.txt (Instalar as dependencias de GUI)

python app.py (Executar a aplicação com o servidor e cliente em background, mantendo somente a GUI visível ao usuário)
python app.py --logs (Executar a aplicação com a janelas de GUI, cliente e servidor visíveis ao usuário)


*Foi implementado o desafio proposto, onde o usuário possui algumas opções de análise da String digitada.
*Em ambientes Linux sem um alias no bash, é necessário trocar o comando "python" para "python3"
