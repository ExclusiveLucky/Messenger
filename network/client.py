# from network.crypto import RSAcrypto
from network.config import socket, json, time
from network.config import GREEN, BLUE, LIGHTBLUE

class Container:
    def __init__(self, header: str = "", 
                 command: str = "", 
                 user: str = "", 
                 data: str = ""):
        
        self.header = header
        self.command = command
        self.user = user
        self.data = data


class Client():
    def __init__(self, username):
        self.server_ip = "84.38.183.57"
        # self.server_ip = "127.0.0.1"
        self.server_port = 50001
        self.users_base = {}
        self.username = username

    def request(self, container, response = False):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_ip, self.server_port))
        self.client_socket.send(json.dumps(container).encode())
        if response:
            response = self.read()

        time.sleep(.001)    
        self.client_socket.close()
        return response
    
    def read(self):
        while True:
            try:
                data = self.client_socket.recv(1024).decode()
                if data:
                    return Container(**dict(json.loads(data)))
            except:
                break


class Message:
    def __init__(self, text, time, sender = "You", position = "left", color = GREEN):
        self.text = text
        self.time = time
        self.status = True
        self.position = position
        self.color = color
        self.sender = sender

    def read(self):
        self.status = False
        self.color = LIGHTBLUE

class Contact:
    """
    Класс, представляющий контакт в мессенджере.

    """
    
    def __init__(self, name):
        """
        Инициализирует экземпляр класса Contact.

        """
        self.name = name
        self.public = ""
        self.messages = []
        self.status = False
        self.new = False
    
    def __str__(self):
        return f"Contact(name={self.name}, public={self.public}, status={self.status}, new={self.new})"


class ContactBase:
    def __init__(self, username):
        self.contacts = list()
        self.client = Client(username)

    def update(self, dt=None) -> None:
        def update_msg():
            if name in messages:
                for msg_text in messages[name]:
                    msg = Message(msg_text, time.strftime("%H:%M:%S"), sender=name)
                    contact.messages.append(msg)

        message = Container("system", "update", self.client.username).__dict__
        response = self.client.request(message, True).__dict__

        data = response.get('data', {})
        messages = data.get('messages', {})
        keys = data.get('keys', {})
        
        for name, data in keys.items():
            public_key, status = data
            contact = next((c for c in self.contacts if c.name == name), None)
            if not contact:
                contact = Contact(name)
                self.contacts.append(contact)

            contact.public = public_key
            contact.status = status
            update_msg()


    
    def send_message(self, contact_name, message: Message):
        """
        Отправляет сообщение указанному контакту.
        """
        container = Container(contact_name, "send", self.client.username, message).__dict__
        self.client.request(container)
        contact: Contact = next((c for c in self.contacts if c.name == contact_name), None)
        contact.messages.append(Message(message, time.strftime("%H:%M:%S"), position="right", color=LIGHTBLUE))
        # print(f"Сообщение отправлено контакту {contact_name}")

    def registrate(self):
        message = Container("system", "add", self.client.username, "1234").__dict__
        self.client.request(message)
        # print(f"Зарегестрировались в системе")

    def rename(self, new_name):
        message = Container("system", "rename", self.client.username, new_name).__dict__
        container = self.client.request(message, True)
        # if container.data:
        #     print(f"Зарегестрировались в системе.")
        # else:
        #     print(f"Имя уже занято.")

if __name__ == "__main__":
    pass
