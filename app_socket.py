from socket import AF_INET, SO_REUSEADDR, SOCK_STREAM, SOL_SOCKET, socket
from threading import Thread

HOST = '127.0.0.1'
PORT = 20000
BUFFER_SIZE = 1024

class AppClientSocket:

  def __init__(self) -> None:
    try:
      with socket(AF_INET, SOCK_STREAM) as socket:
        socket.connect((HOST, PORT))
        self.channel = socket

    except Exception as error:
      print(error)

  def send_data(self, msg, param: int | None = None) -> str:
    self.channel.send(msg.encode('utf-8'))
    data = socket.recv(BUFFER_SIZE)
    echo_text = repr(data)
    echo_text = data.decode('utf-8')
    return echo_text

  def get_instance(self):
    return self.channel

  def run(self):
    with self.channel as c:
      print(f"Servidor rodando na porta {PORT}")
      while True:
        text = input("Digite o texto a ser enviado ao servidor (Caso deseje terminar digite 'exit'):\n")
        echo_text = self.send_data(text)
        print('Recebido do servidor:', echo_text)
        if (text == 'exit'):
          print('Encerrando Socket_Client')
          c.close()
          break


class AppServerSocket:

  def __init__(self) -> None:
    try:
      with socket(AF_INET, SOCK_STREAM) as channel:
        self.channel = channel
        self.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.bind((HOST, PORT))
        self.VOWELS = ["A", "E", "I", "O", "U", "a", "e", "i", "o", "u"]
    except Exception as error:
      print(error)

  def on_new_client(self, client, addr):
    while True:
      client_ip, port = addr
      try:
        data = client.recv(BUFFER_SIZE)
        if not data:
          break

        received_text = data.decode('utf-8')
        if received_text == 'exit':
          print(f"O Socket do cliente {client_ip} foi encerrado!")
          client.close()
          return

        print(f"Mensagem '{received_text}' recebida pelo Cliente {client_ip} na porta {port}")
        new_word, total_vowals, total_consonants = self.process_word(received_text)
        self.channel.send(f"\nPalavra Reversa: {new_word}\nNúmero de Vogais: {total_vowals}\nNúmero de Consoantes: {total_consonants}".encode("utf-8"))

      except Exception as error:
        print("Erro no servidor!")
        print(error)

  def process_word(self, word, param = None) -> list:
    total_vowels = len([letter for letter in word if letter in self.VOWELS])
    total_consonants = len(word) - total_vowels

    print_result = lambda word: print(f"Resultado do processamento:\nForma de processamento: {param}\nPalavra processada: {word}\nNúmero de Vogais: {total_vowels}\nNúmero de Consoantes: {total_consonants}")
  
    if not param:
      reversed_word = word[::-1]
      print_result(reversed_word)
      return reversed_word, total_vowels, total_consonants

  def run(self):
    try:
      while True:
        self.channel.listen()
        client, addr = self.channel.accept()
        print(f"Conectado ao cliente no endereço: {addr}")
        t = Thread(target=self.on_new_client, args=(client, addr))
        t.start()
    except Exception as error:
      print("erro no runn")
      print(error)


