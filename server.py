import _thread
from enum import Enum
from socket import AF_INET, SO_REUSEADDR, SOCK_STREAM, SOL_SOCKET, socket
from sys import exit

import dearpygui.dearpygui as dpg

HOST = "localhost"
PORT = 20000
BUFFER_SIZE = 1024
VOWELS = ["A", "E", "I", "O", "U", "a", "e", "i", "o", "u"]

MAX_WIDTH = 720
MAX_HEIGHT = 540


class MessageEncode(Enum):
    REVERSE = 0
    SPLIT = 1
    REPLACE = 2


def init_server():
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()

    return conn, addr


def send_message(msg):
    processed_word, vowels, consonants, log = process_word(msg)
    conn.send(
        f"\n    Palavra Processada: {processed_word}\n    Número de Vogais: {vowels}\n    Número de Consoantes: {consonants}\n".encode(
            "utf-8"
        )
    )
    draw_log(log + f"\n    Processamento resultante: {processed_word}")


def recieve_message():
    while True:
        try:
            data = conn.recv(BUFFER_SIZE)
            message = data.decode("utf-8")
            if message == "exit":
                print(f"O Socker com o client {addr[0]} foi encerrado!")
                conn.close()
                exit()
                return
            send_message(message)
        except Exception as error:
            print("Erro na conexão com o client!")
            print(error)


def process_word(word: str, param=0) -> list:
    total_vowels = len([letter for letter in word if letter in VOWELS])
    total_consonants = len(word) - total_vowels

    log = f"Client: {addr[0]}\nPorta: {addr[1]}\nResultado do processamento:\n    Forma de apuração: {MessageEncode(param).name}\n    Palavra recebida: {word}\n    Número de Vogais: {total_vowels}\n    Número de Consoantes: {total_consonants}"

    if param == 0:
        reversed_word = word[::-1]
        return reversed_word, total_vowels, total_consonants, log


def draw_log(msg: str):
    dpg.add_text(msg, parent="logs", before="logs")


def GUI():
    _thread.start_new_thread(recieve_message, ())
    dpg.create_context()
    dpg.create_viewport(
        title="Apuracao de Strings - Filipe Augusto Santos de Moura",
        width=MAX_WIDTH,
        height=MAX_HEIGHT,
        max_width=MAX_WIDTH,
        max_height=MAX_HEIGHT,
        min_width=MAX_WIDTH,
        min_height=MAX_HEIGHT,
    )

    with dpg.window(
        label="Python + TCP --- SERVER LOGS",
        width=MAX_WIDTH,
        height=MAX_HEIGHT,
        no_move=True,
        no_close=True,
        no_collapse=True,
    ):
        dpg.add_text("", tag="logs")

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    conn, addr = init_server()
    GUI()
