from app.config import ColoredBoxLayout, Button, Label, StackLayout, ScrollView, Screen, time, threading
from app.config import TOP_BAR_COLOR, BUTTON_COLOR, TITLE_COLOR, TITLE_FONT_SIZE, BUTTON_HEIGHT, Clock, Window
from network.client import ContactBase, Contact, Message

class ContactsScreen(Screen):
    """
    Экран контактов, отображающий список всех контактов.
    """
    
    def __init__(self, contact_base: ContactBase, **kwargs):
        super(ContactsScreen, self).__init__(**kwargs)
        self.contact_base = contact_base
        self.build_ui()
        Clock.schedule_interval(self.update_contacts, 1)  # Обновляем список контактов каждую секунду

    def build_ui(self) -> None:
        """
        Создает пользовательский интерфейс экрана контактов.
        """
        screen_width = Window.width
        screen_height = Window.height

        padding = [screen_width * 0.025, screen_height * 0.025, screen_width * 0.025, screen_height * 0.025]
        spacing = screen_height * 0.02

        root = ColoredBoxLayout(orientation='vertical', padding=padding, spacing=spacing)

        # Верхняя панель с кнопкой настройки
        top_bar = ColoredBoxLayout(size_hint_y=0.1, orientation='horizontal', bg_color=TOP_BAR_COLOR, padding=[screen_width * 0.0125, screen_height * 0.0125, screen_width * 0.0125, screen_height * 0.0125], spacing=screen_width * 0.0125)
        settings_button = Button(text='Настройки', size_hint_x=0.1, background_normal='', background_color=[0.1, 0.1, 0.1, 1], color=BUTTON_COLOR)
        settings_button.bind(on_press=self.open_settings)
        top_bar.add_widget(settings_button)
        title = Label(text='Контакты', size_hint_x=0.8, color=TITLE_COLOR, font_size=screen_height * 0.03, bold=True)
        top_bar.add_widget(title)
        top_bar.add_widget(Label(size_hint_x=0.1))  # Пустое пространство для выравнивания
        root.add_widget(top_bar)

        # ScrollView для списка контактов
        self.contacts_layout = StackLayout(size_hint_y=None, spacing=screen_height * 0.02, padding=[screen_width * 0.0125, screen_height * 0.0125, screen_width * 0.0125, screen_height * 0.0125])
        self.contacts_layout.bind(minimum_height=self.contacts_layout.setter('height'))

        self.scroll_view = ScrollView(size_hint=(1, 0.9))
        self.scroll_view.add_widget(self.contacts_layout)
        root.add_widget(self.scroll_view)

        self.add_widget(root)
        self.update_contacts()

    def update_contacts(self, dt=None) -> None:
        """
        Обновляет список контактов.
        """
        screen_width = Window.width
        screen_height = Window.height
        self.contacts_layout.clear_widgets()
        button_height = Window.height * 0.07  # Высота кнопки контакта относительно высоты экрана

        for contact in self.contact_base.contacts:
            if contact.name != self.contact_base.client.username:
                contact_button = Button(
                    text=contact.name, 
                    size_hint_y=None, 
                    height=button_height, 
                    background_normal='', 
                    background_color=[0.2, 0.2, 0.2, 1], 
                    color=BUTTON_COLOR,
                    halign='center',
                    valign='middle',
                    text_size=(self.width, None),
                    font_size=Window.height * 0.025,  # Размер шрифта относительно высоты экрана
                    padding=[screen_width * 0.025, screen_height * 0.025]
                )
                contact_button.bind(on_press=lambda instance, c=contact: self.open_chat(c))
                self.contacts_layout.add_widget(contact_button)


    def open_chat(self, contact: Contact) -> None:
        """
        Открывает экран чата с выбранным контактом.

        Args:
            contact (Contact): Выбранный контакт.
        """
        chat_screen = self.manager.get_screen('chat')
        chat_screen.set_contact(contact)
        self.manager.transition.direction = 'left'
        self.manager.current = 'chat'
        for message in contact.messages:
            message: Message
            message.status = False

    def open_settings(self, instance) -> None:
        """
        Открывает экран настроек.

        Args:
            instance: Экземпляр кнопки настройки.
        """
        self.manager.transition.direction = 'right'
        self.manager.current = 'settings'

if __name__ == "__main__":
    pass