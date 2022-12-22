from socket import AF_INET, SO_REUSEADDR, SOCK_STREAM, SOL_SOCKET, socket
from threading import Thread

HOST = '127.0.0.1'
PORT = 20000
BUFFER_SIZE = 1024
VOWELS = ["A", "E", "I", "O", "U", "a", "e", "i", "o", "u"]

def on_new_client(client_socket, addr):
  while True:
    client, port = addr
    try:
      data = client_socket.recv(BUFFER_SIZE)
      if not data:
        break

      received_text = data.decode('utf-8')
      if (received_text == 'exit'):
        print(f"O Socket do Cliente {client} foi encerrado!")
        client_socket.close() 
        return
      
      print(f"Mensagem '{received_text}' recebida pelo Cliente {client} na porta {port}")
      processed_word, vowels, consonants = process_word(received_text)         
      client_socket.send(f"\nPalavra Reversa: {processed_word}\nNúmero de Vogais: {vowels}\nNúmero de Consoantes: {consonants}".encode("utf-8"))

    except Exception as error:
      print("Erro na conexão com o cliente!!")
      print(error)
      return

def process_word(word: str, param = None) -> list:
  total_vowels = len([letter for letter in word if letter in VOWELS])
  total_consonants = len(word) - total_vowels

  print_result = lambda word: print(f"Resultado do processamento:\nForma de processamento: {param}\nPalavra processada: {word}\nNúmero de Vogais: {total_vowels}\nNúmero de Consoantes: {total_consonants}")
  
  if not param:
    reversed_word = word[::-1]
    print_result(reversed_word)
    return reversed_word, total_vowels, total_consonants


def main():
  try:
    with socket(AF_INET, SOCK_STREAM) as server_socket:
      server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
      server_socket.bind((HOST, PORT))
      while True:
        server_socket.listen()
        client_socket, addr = server_socket.accept()
        print('Conectado ao cliente no endereço:', addr)
        t = Thread(target=on_new_client, args=(client_socket,addr))
        t.start()   
  except Exception as error:
    print("Erro na execução do servidor!!")
    print(error)        
    return             

if __name__ == "__main__":   
  main()