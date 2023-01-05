import _thread
from enum import Enum
from math import ceil
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
    CLEAR = 1
    CONCAT = 2
    STRIP = 3
    PARTITION = 4


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
        f"\n    Resultado processado: {processed_word}\n    Número de Vogais: {vowels}\n    Número de Consoantes: {consonants}\n".encode(
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
            if message:
                send_message(message)

        except Exception as error:
            print("Erro na conexão com o client!")
            print(error)


def process_word(word: str) -> list:
    word, protocol, selected_chars = word.split("&")
    total_vowels, total_consonants = get_vowels_and_consonants(word)

    log = generate_log(word, protocol, total_vowels, total_consonants)

    if protocol == "0":
        reversed_word = word[::-1]
        return reversed_word, total_vowels, total_consonants, log
    elif protocol == "1":
        splitted_word = word.split(selected_chars)
        total_vowels, total_consonants = get_vowels_and_consonants(splitted_word)
        log = generate_log(word, protocol, total_vowels, total_consonants)
        return splitted_word, total_vowels, total_consonants, log
    elif protocol == "2":
        concated_word = word + selected_chars
        total_vowels, total_consonants = get_vowels_and_consonants(concated_word)
        log = generate_log(word, protocol, total_vowels, total_consonants)
        return concated_word, total_vowels, total_consonants, log
    elif protocol == "3":
        stripped_word = word.replace(" ", "")
        return stripped_word, total_vowels, total_consonants, log
    elif protocol == "4":
        partitioned_word = divide_in_three(word)
        return partitioned_word, total_vowels, total_consonants, log


def get_vowels_and_consonants(word: str):
    total_vowels = len([letter for letter in word if letter in VOWELS])
    total_consonants = len([letter for letter in word if letter not in VOWELS and not letter.isnumeric()])
    return total_vowels, total_consonants


def generate_log(word, protocol, vowels, consonants):
    return f"Client: {addr[0]}\nPorta: {addr[1]}\nResultado do processamento:\n    Forma de apuração: {MessageEncode(int(protocol)).name}\n    Palavra recebida: {word}\n    Número de Vogais: {vowels}\n    Número de Consoantes: {consonants}"


def draw_log(msg: str):
    dpg.add_text(msg, parent="logs", before="logs")

def divide_in_three(word):
  equal_parts = ceil(len(word) / 3)
  if len(word) < 3:
    return "Não é possível dividir em três uma palavra com menos de três caracteres!"

  partitioned_word = [word[i:i+equal_parts] for i in range(0, len(word), equal_parts)]

  if len(word) == 4:
    replace_char = partitioned_word[1][1]
    partitioned_word.append(replace_char)
    replace = partitioned_word[1].replace(replace_char, "")
    partitioned_word[1] = replace
  return partitioned_word

def GUI():
    _thread.start_new_thread(recieve_message, ())
    dpg.create_context()
    dpg.create_viewport(
        title="Apuracao de Strings - Filipe Augusto Santos de Moura - SERVER",
        width=MAX_WIDTH,
        height=MAX_HEIGHT,
        max_width=MAX_WIDTH,
        max_height=MAX_HEIGHT,
        min_width=MAX_WIDTH,
        min_height=MAX_HEIGHT,
        x_pos=100,
        y_pos=200
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
