import socket
import threading
import json
import time
import secrets
import struct
import sympy

from kivy.utils import get_color_from_hex


GREEN = get_color_from_hex('#056162')
BLUE = get_color_from_hex('#262D31')
LIGHTBLUE = get_color_from_hex('#0088cc')



class IP:
    @staticmethod
    def get_local():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # не подключаясь, просто попытаться подключиться к адресу (без использования интернет-соединения)
            s.connect(("10.254.254.254", 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()

        return IP
    

hostname = socket.gethostname()
# print("IP Address:",socket.gethostbyname(hostname))