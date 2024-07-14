from app.config import ColoredBoxLayout, Button, Label, TextInput, StackLayout, BoxLayout, ScrollView, Screen
from app.config import TOP_BAR_COLOR, BUTTON_COLOR, TITLE_COLOR,  TITLE_FONT_SIZE, TEXT_COLOR,  HIGHLIGHTED_TEXT_COLOR, BACKGROUND_COLOR
from app.config import Clock, Window
from network.client import ContactBase, Contact, Message


class ChatScreen(Screen):
    """
    Экран чата, отображающий переписку с выбранным контактом.
    """
    
    def __init__(self, contact_base: ContactBase, **kwargs):
        super(ChatScreen, self).__init__(**kwargs)
        self.contact_name_label = None
        self.contact = None
        self.contact_base = contact_base
        self.build_ui()
        Clock.schedule_interval(self.update_messages, 1)  # Обновляем сообщения каждую секунду

    def build_ui(self) -> None:
        """
        Создает пользовательский интерфейс экрана чата.
        """
        screen_width = Window.width
        screen_height = Window.height

        padding = [screen_width * 0.025, screen_height * 0.025, screen_width * 0.025, screen_height * 0.025]
        spacing = screen_height * 0.02

        root = ColoredBoxLayout(orientation='vertical', padding=padding, bg_color=BACKGROUND_COLOR)

        # Верхняя панель с ником собеседника и кнопкой меню
        top_bar = ColoredBoxLayout(size_hint_y=0.1, orientation='horizontal', bg_color=TOP_BAR_COLOR, padding=[screen_width * 0.025, screen_height * 0.025, screen_width * 0.025, screen_height * 0.025], spacing=screen_width * 0.025)
        menu_button = Button(text='Меню', size_hint_x=0.1, background_normal='', background_color=[0.1, 0.1, 0.1, 1], color=BUTTON_COLOR)
        menu_button.bind(on_press=self.open_contacts)
        top_bar.add_widget(menu_button)
        self.contact_name_label = Label(text='Ник собеседника', size_hint_x=0.8, color=TITLE_COLOR, font_size=screen_height * 0.03, bold=True, halign='center', valign='middle')
        top_bar.add_widget(self.contact_name_label)
        top_bar.add_widget(Label(size_hint_x=0.1))  # Пустое пространство для выравнивания
        root.add_widget(top_bar)

        # ScrollView для сообщений
        self.messages_layout = StackLayout(size_hint_y=None, spacing=spacing, padding=padding)
        self.messages_layout.bind(minimum_height=self.messages_layout.setter('height'))

        self.scroll_view = ScrollView(size_hint=(1, 0.8))
        self.scroll_view.add_widget(self.messages_layout)
        root.add_widget(self.scroll_view)

        # Нижняя панель с текстовым полем, кнопкой прикрепить и кнопкой отправить
        bottom_bar = ColoredBoxLayout(size_hint_y=0.1, orientation='horizontal', padding=[10, 2])

        attach_button = Button(text='+', size_hint_x=0.1, background_normal='', background_color=[0.1, 0.1, 0.1, 1], color=BUTTON_COLOR)
        attach_button.bind(on_press=self.attach_file)
        bottom_bar.add_widget(attach_button)

        self.text_input = TextInput(size_hint_x=0.7, multiline=False, hint_text='Введите сообщение...', background_color=[0.3, 0.3, 0.3, 1], foreground_color=TITLE_COLOR, font_size=screen_height * 0.025, padding=[screen_width * 0.025, screen_height * 0.025])
        bottom_bar.add_widget(self.text_input)

        send_button = Button(text='Send', size_hint_x=0.2, background_normal='', background_color=BUTTON_COLOR, color=HIGHLIGHTED_TEXT_COLOR, font_size=screen_height * 0.025, bold=True, padding=[screen_width * 0.025, screen_height * 0.025])
        send_button.bind(on_press=self.send_message)
        bottom_bar.add_widget(send_button)

        root.add_widget(bottom_bar)

        self.add_widget(root)

    def send_message(self, instance) -> None:
        """
        Отправляет сообщение и добавляет его в список сообщений.

        Args:
            instance: Экземпляр кнопки отправки сообщения.
        """
        message = self.text_input.text
        if message and self.contact:
            self.contact_base.send_message(self.contact.name, message)
            self.text_input.text = ""

    def display_message(self, message: Message):
        try:
            screen_width = Window.width
            screen_height = Window.height
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=Window.height * 0.07, padding=[screen_width * 0.025, screen_height * 0.025, screen_width * 0.025, screen_height * 0.025])
            label = Label(text=f"{message.sender} {message.time}:\n{message.text}", color=message.color, size_hint_y=None, height=Window.height * 0.07, halign=message.position, valign='middle')
            box.add_widget(label)
            label.bind(size=label.setter('text_size'))  # Ensure text wraps within the label
            self.messages_layout.add_widget(box)
        except Exception as e:
            print(str(e))

    def update_messages(self, dt=None) -> None:
        """
        Обновляет список сообщений.
        """
        if not self.contact:
            return

        self.messages_layout.clear_widgets()
        for msg in self.contact.messages:
            self.display_message(msg)

    def attach_file(self, instance) -> None:
        """
        Обработчик для кнопки прикрепления файла.

        Args:
            instance: Экземпляр кнопки прикрепления файла.
        """
        print("Attach file")

    def open_contacts(self, instance) -> None:
        """
        Открывает экран контактов.

        Args:
            instance: Экземпляр кнопки меню.
        """
        self.manager.transition.direction = 'right'
        self.manager.current = 'contacts'

    def set_contact(self, contact: Contact) -> None:
        """
        Устанавливает текущий контакт и обновляет экран сообщений.

        Args:
            contact (Contact): Текущий контакт.
        """
        self.contact = contact
        self.contact_name_label.text = contact.name
        self.update_messages()


# class ChatScreen(Screen):
#     """
#     Экран чата, отображающий переписку с выбранным контактом.
#     """
    
#     def __init__(self, contact_base: ContactBase, **kwargs):
#         super(ChatScreen, self).__init__(**kwargs)
#         self.contact_name_label = None
#         self.contact = None
#         self.contact_base = contact_base
#         self.build_ui()
#         Clock.schedule_interval(self.update_messages, 1)  # Обновляем сообщения каждую секунду

#     def build_ui(self) -> None:
#         """
#         Создает пользовательский интерфейс экрана чата.
#         """
#         root = ColoredBoxLayout(orientation='vertical', padding=[10, 10, 10, 10])

#         # Верхняя панель с ником собеседника и кнопкой меню
#         top_bar = ColoredBoxLayout(size_hint_y=0.1, orientation='horizontal', bg_color=TOP_BAR_COLOR)
#         menu_button = Button(text='Меню', size_hint_x=0.1, background_color=[0, 0, 0, 0], color=BUTTON_COLOR)
#         menu_button.bind(on_press=self.open_contacts)
#         top_bar.add_widget(menu_button)
#         self.contact_name_label = Label(text='Ник собеседника', size_hint_x=0.8, color=TITLE_COLOR, font_size=TITLE_FONT_SIZE)
#         top_bar.add_widget(self.contact_name_label)
#         top_bar.add_widget(Label(size_hint_x=0.1))  # Пустое пространство для выравнивания
#         root.add_widget(top_bar)

#         # ScrollView для сообщений
#         self.messages_layout = StackLayout(size_hint_y=None, spacing=10)
#         self.messages_layout.bind(minimum_height=self.messages_layout.setter('height'))

#         self.scroll_view = ScrollView(size_hint=(1, 0.8))
#         self.scroll_view.add_widget(self.messages_layout)
#         root.add_widget(self.scroll_view)

#         # Нижняя панель с текстовым полем, кнопкой прикрепить и кнопкой отправить
#         bottom_bar = ColoredBoxLayout(size_hint_y=0.1, orientation='horizontal', padding=[10, 0])

#         attach_button = Button(text='+', size_hint_x=0.1, background_color=[0, 0, 0, 0], color=BUTTON_COLOR)
#         attach_button.bind(on_press=self.attach_file)
#         bottom_bar.add_widget(attach_button)

#         self.text_input = TextInput(size_hint_x=0.7, multiline=False, hint_text='Введите сообщение...')
#         bottom_bar.add_widget(self.text_input)

#         send_button = Button(text='Send', size_hint_x=0.2, background_color=[0, 0, 0, 0], color=BUTTON_COLOR)
#         send_button.bind(on_press=self.send_message)
#         bottom_bar.add_widget(send_button)

#         root.add_widget(bottom_bar)

#         self.add_widget(root)

#     def send_message(self, instance) -> None:
#         # print(self.contact.name)
#         """
#         Отправляет сообщение и добавляет его в список сообщений.

#         Args:
#             instance: Экземпляр кнопки отправки сообщения.
#         """
#         message = self.text_input.text
#         if message and self.contact:
#             self.contact_base.send_message(self.contact.name, message)
#             self.text_input.text = ""


#     def display_message(self, message: Message):
#         try:
#             box = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
#             label = Label(text=f"{message.sender} {message.time}:\n{message.text}", color=message.color, size_hint_y=None, height=40, halign=message.position, valign='middle')
#             box.add_widget(label)
#             label.bind(size=label.setter('text_size'))  # Ensure text wraps within the label
#             self.messages_layout.add_widget(box)
#         except Exception as e:
#             print(str(e))

#         self.messages_layout.scroll_y = 100

#     def update_messages(self, dt=None) -> None:
#         """
#         Обновляет список сообщений.
#         """
#         if not self.contact:
#             return

#         self.messages_layout.clear_widgets()
#         for msg in self.contact.messages:
#             position = 'left'
#             self.display_message(msg)

#     def attach_file(self, instance) -> None:
#         """
#         Обработчик для кнопки прикрепления файла.

#         Args:
#             instance: Экземпляр кнопки прикрепления файла.
#         """
#         print("Attach file")

#     def open_contacts(self, instance) -> None:
#         """
#         Открывает экран контактов.

#         Args:
#             instance: Экземпляр кнопки меню.
#         """
#         self.manager.transition.direction = 'right'
#         self.manager.current = 'contacts'

#     def set_contact(self, contact: Contact) -> None:
#         """
#         Устанавливает текущий контакт и обновляет экран сообщений.

#         Args:
#             contact (Contact): Текущий контакт.
#         """
#         self.contact = contact
#         self.contact_name_label.text = contact.name
#         self.update_messages()

if __name__ == "__main__":
    pass
