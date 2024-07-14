import socket
import threading
import json
import time
from typing import Dict, List

class IP:
    """
    Класс для получения локального IP-адреса.
    """

    @staticmethod
    def get_local() -> str:
        """
        Получает локальный IP-адрес.

        Returns:
            str: Локальный IP-адрес.
        """
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
    
class Container:
    """
    Класс для представления контейнера данных.

    Атрибуты:
        header (str): Заголовок сообщения.
        command (str): Команда.
        user (str): Имя пользователя.
        data (str): Данные.
    """

    header: str
    "Заголовок сообщения"

    command: str
    "Команда"

    user: str
    "Имя пользователя"

    data: str
    "Данные"

    def __init__(self, header: str = "", command: str = "", user: str = "", data: str = ""):
        """
        Инициализация контейнера данных.

        Args:
            header (str, optional): Заголовок сообщения. По умолчанию "".
            command (str, optional): Команда. По умолчанию "".
            user (str, optional): Имя пользователя. По умолчанию "".
            data (str, optional): Данные. По умолчанию "".
        """
        self.header = header
        self.command = command
        self.user = user
        self.data = data

class User:
    """
    Класс для представления пользователя.

    Атрибуты:
        name (str): Имя пользователя.
        public (str): Публичный ключ пользователя.
        status (bool): Статус пользователя (онлайн/оффлайн).
        status_time (float): Время последнего обновления статуса.
        messages (Dict[str, List[str]]): Словарь сообщений.
    """

    name: str
    "Имя пользователя"

    public: str
    "Публичный ключ пользователя"

    status: bool
    "Статус пользователя (онлайн/оффлайн)"

    status_time: float
    "Время последнего обновления статуса"

    messages: Dict[str, List[str]]
    "Словарь сообщений"

    def __init__(self, name: str, public: str):
        """
        Инициализация пользователя.

        Args:
            name (str): Имя пользователя.
            public (str): Публичный ключ пользователя.
        """
        self.name = name
        self.public = public
        self.status = False
        self.status_time = False
        self.messages = dict()

    def alert(self):
        """
        Оповещает пользователя.
        """
        pass
        
    def message(self, from_user: str, data: str):
        """
        Добавляет сообщение от другого пользователя.

        Args:
            from_user (str): Имя пользователя-отправителя.
            data (str): Сообщение.
        """
        if from_user not in self.messages:
            self.messages[from_user] = list()
        self.messages[from_user].append(data)

    def rename(self, name: str):
        """
        Переименовывает пользователя.

        Args:
            name (str): Новое имя пользователя.
        """
        self.name = name

    def online(self):
        """
        Устанавливает статус пользователя как онлайн.
        """
        self.status = True
        self.status_time = time.time()

    def update_status(self):
        """
        Обновляет статус пользователя.
        """
        if self.status and (time.time() - self.status_time > 10):
            self.status = False

class UserBase:
    """
    Класс для управления базой данных пользователей.
    """

    users: Dict[str, User]
    "Словарь пользователей"

    def __init__(self):
        """
        Инициализация базы данных пользователей.
        """
        self.users = {"test": User("test", "1234")}

    def update(self):
        """
        Обновляет статус всех пользователей в базе данных.
        """
        for user in list(self.users.values()):
            user.update_status()

class Session:
    """
    Класс для управления сессией клиента.

    Атрибуты:
        client_socket (socket.socket): Сокет клиента.
    """

    client_socket: socket.socket
    "Сокет клиента"

    def __init__(self, client_socket: socket.socket, userbase: UserBase):
        """
        Инициализация сессии клиента.

        Args:
            client_socket (socket.socket): Сокет клиента.
        """
        self.client_socket = client_socket
        self.userbase = userbase
        self.connect()

    def read(self) -> Container:
        """
        Читает сообщение от клиента.

        Returns:
            Container: Контейнер с данными.
        """
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                if message:
                    return Container(**dict(json.loads(message)))
            except:
                break

    def write(self, data: Container) -> bool:
        """
        Отправляет данные клиенту.

        Args:
            data (Container): Данные для отправки.

        Returns:
            bool: True, если отправка успешна, иначе False.
        """
        try:
            self.client_socket.send(json.dumps(data).encode())
            return True
        except Exception as e:
            # print(f"Send Error: {str(e)}")
            return False
        
    def connect(self):
        """
        Обрабатывает подключение клиента.

        Args:
            client_socket (socket.socket): Сокет клиента.
        """
        container = self.read()
        # print(container.header, container.command)
        if container.header == "system":
            if container.command == "add":
                self.userbase.users[container.user] = User(container.user, container.data)

            elif container.command == "rename":
                if container.data not in self.userbase.users:
                    user: User = self.userbase.users[container.user]
                    user.rename(container.data)
                    del self.userbase.users[container.user]
                    self.userbase.users[container.data] = user
                    result = True
                else:
                    result = False    

                container = Container(container.header, container.command, "", result).__dict__
                self.write(container)

            elif container.command == "update":
                self.userbase.users[container.user].online()
                data = {"messages": self.userbase.users[container.user].messages,
                        "keys": dict((user.name, [user.public, user.status]) for user in self.userbase.users.values())}
                
                self.userbase.users[container.user].messages = dict()
                container = Container(container.header, container.command, "", data).__dict__
                self.write(container)

            elif container.command == "get":
                data = list(self.userbase.users.keys())
                container = Container(container.header, container.command, "", data).__dict__
                self.write(container)

        elif container.header in self.userbase.users:
            if container.command == "info": 
                data = self.userbase.users[container.header].__dict__
                container = Container(container.header, container.command, "", data).__dict__
                self.write(container)
                pass
            elif container.command == "send":
                self.userbase.users[container.header].message(container.user, container.data)

class Server:
    """
    Класс для управления сервером.

    Атрибуты:
        host (str): Хост сервера.
        port (int): Порт сервера.
        max_peers (int): Максимальное количество подключений.
        userbase (UserBase): База данных пользователей.
    """

    host: str
    "Хост сервера"

    port: int
    "Порт сервера"

    max_peers: int
    "Максимальное количество подключений"

    userbase: UserBase
    "База данных пользователей"

    def __init__(self):
        """
        Инициализация сервера.
        """
        self.host = "0.0.0.0"
        self.port = 50001
        self.max_peers = 10
        self.userbase = UserBase()

        # print(f"Start server on IP {IP.get_local()}")

    def setup_networking(self):
        """
        Настройка сетевых параметров сервера.
        """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(self.max_peers)
        threading.Thread(target=self.accept_connections, daemon=True).start()

    def accept_connections(self):
        """
        Принимает подключения от клиентов.
        """
        while True:
            client, address = self.server_socket.accept()
            # print(f"Connect from peer: {address}")
            # print(self.userbase.users.keys())
            threading.Thread(target=Session, args=(client, self.userbase), daemon=True).start()

    




if __name__ == "__main__":
    server = Server()
    server.setup_networking()
    while True:
        server.userbase.update()
        time.sleep(1)