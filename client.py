import _thread
from socket import AF_INET, SOCK_STREAM, socket
from sys import exit

import dearpygui.dearpygui as dpg

HOST = "localhost"
PORT = 20000
BUFFER_SIZE = 1024

MAX_WIDTH = 720
MAX_HEIGHT = 540


def init_client():
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((HOST, PORT))

    return s


def send_message():
    msg = dpg.get_value("user_input")
    char_selected = dpg.get_value("char_field")
    msg = msg + "&" + str(select_string_protocol()) + "&" + char_selected
    s.send(msg.encode("utf-8"))
    dpg.set_value("user_input", "")
    dpg.set_value("char_field", "")

    if msg == "exit":
        s.close()
        exit()


def recieve_message():
    while True:
        try:
            data = s.recv(BUFFER_SIZE)
            message: str = data.decode("utf-8")
            if message:
                update_response(message)

        except Exception as error:
            print("Erro na conxeão com o server!")
            print(error)


def update_response(msg):
    dpg.set_value("response_text", f"Resposta do servidor: {msg}")


def select_string_protocol():
    protocol = dpg.get_value("string_protocol")

    if (
        not protocol
        or protocol == "Reverter"
        or protocol == "Remover espaços"
        or protocol == "Particionar em 3"
    ):
        dpg.hide_item("char_filter")
        dpg.hide_item("char_field")
        if protocol == "Reverter":
            return 0
        if protocol == "Remover espaços":
            return 3
        if protocol == "Particionar em 3":
            return 4

    dpg.show_item("char_filter")
    dpg.show_item("char_field")

    if protocol == "Remover letras":
        return 1
    if protocol == "Concatenar":
        return 2


def GUI():
    _thread.start_new_thread(recieve_message, ())
    list_items = [
        "Reverter",
        "Remover letras",
        "Concatenar",
        "Remover espaços",
        "Particionar em 3",
    ]
    dpg.create_context()
    dpg.create_viewport(
        title="Apuracao de Strings - Filipe Augusto Santos de Moura - CLIENT",
        width=MAX_WIDTH,
        height=MAX_HEIGHT,
        max_width=MAX_WIDTH,
        max_height=MAX_HEIGHT,
        min_width=MAX_WIDTH,
        min_height=MAX_HEIGHT,
        x_pos=1000,
        y_pos=200
    )

    with dpg.window(
        label="Python + TCP --- CLIENT",
        width=MAX_WIDTH,
        height=MAX_HEIGHT,
        no_move=True,
        no_close=True,
        no_collapse=True,
    ):
        dpg.add_text(
            "Digite o texto a ser enviado ao servidor (Caso deseje terminar clique no 'x')"
        )
        dpg.add_input_text(tag="user_input")
        dpg.add_button(label="Enviar", callback=send_message, tag="send_button")
        dpg.add_text("Forma de Apuração")
        dpg.add_listbox(
            items=list_items,
            tag="string_protocol",
            callback=select_string_protocol,
        )
        dpg.add_text("Digite os caracteres para filtragem", tag="char_filter")
        dpg.add_input_text(tag="char_field")
        dpg.add_text("Resposta do servidor: ", tag="response_text")
        dpg.hide_item("char_filter")
        dpg.hide_item("char_field")

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    s = init_client()
    GUI()
