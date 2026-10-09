import os
import socket
import threading
import shutil
from pathlib import Path
from PIL import Image


def recv_image_data(client_socket, file_name, file_data_len):
    """
    receive the image data and save the image
    :param client_socket: the client socket
    :param file_name:  the image file name
    :param file_data_len: the length of the image data
    :return:None
    """

    folder = "file_dest"
    if not os.path.exists("img_server/file_dest"):#folder destination of images
        os.mkdir("img_server/file_dest")

    data = b''
    while len(data) < file_data_len:
        slice = file_data_len - len(data)
        if slice > 1024:
            data += client_socket.recv(1024)
        else:
            data += client_socket.recv(slice)
            break



    # create the image file
    with open (file_name, "wb") as f:
        f.write(data)

    shutil.copy(file_name, folder)
    im = Image.open(file_name)
    im.show()

server_soc = socket.socket()
server_soc.bind(("0.0.0.0", 1450))
server_soc.listen(3)


while True:
    client_socket, addr = server_soc.accept()
    print(f"{addr[0]} - connected")

    while True:
        try:

            file_name_len = int(client_socket.recv(2).decode())
            file_name = client_socket.recv(file_name_len).decode()
            file_data_len = int(client_socket.recv(6).decode())




            recv_image_data(client_socket, file_name, file_data_len)

        except Exception as e:
            print(f"client {addr[0]} disconnected due to {str(e)}")
            client_socket.close()
            break

