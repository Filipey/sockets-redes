from socket import AF_INET, SOCK_STREAM, socket

import dearpygui.dearpygui as dpg

HOST = '127.0.0.1'
PORT = 20000
BUFFER_SIZE = 1024

def main(): 
  try:
    with socket(AF_INET, SOCK_STREAM) as s:
      s.connect((HOST, PORT))
      print(f"Servidor rodando na porta {PORT}")
      while True:       
        text = input("Digite o texto a ser enviado ao servidor (Caso deseje terminar digite 'exit'):\n")
        s.send(text.encode())
        data = s.recv(BUFFER_SIZE)
        echo_text = repr(data)
        echo_text = data.decode('utf-8')
        print('Recebido do servidor:', echo_text)
        if (text == 'exit'):
          print('Encerrando Socket_Client')
          s.close()
          break
  except Exception as error:
    print("Exceção - Programa será encerrado!")
    print(error)
    return


if __name__ == "__main__":   
  main()