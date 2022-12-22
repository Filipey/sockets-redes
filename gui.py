from socket import socket

import dearpygui.dearpygui as dpg
import dearpygui.demo as demo

from client import send_data

dpg.create_context()
dpg.create_viewport(title='Apuracao de Strings - Filipe Augusto Santos de Moura', width=540, height=720, max_width=540, max_height=540, min_width=540, min_height=540)

# def send_data(socket):
#   text = dpg.get_value("user_input")
#   dpg.set_value("user_input", "")

# def get_server_response(socket: socket):
#   res = socket

with dpg.window(label="Python + TCP", width=540, height=720, no_move=True, no_close=True, no_collapse=True):
  dpg.add_text("Digite uma String")
  dpg.add_input_text(tag="user_input")
  dpg.add_button(label="Enviar", callback=send_data)


# demo.show_demo()

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()