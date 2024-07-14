from app.config import ColoredBoxLayout, Button, Label, TextInput, Screen
from app.config import TOP_BAR_COLOR, BUTTON_COLOR, TITLE_COLOR, TITLE_FONT_SIZE, BACKGROUND_COLOR, TEXT_COLOR, ICON_COLOR, HIGHLIGHTED_TEXT_COLOR, Clock, Window
from network.client import ContactBase

class SettingsScreen(Screen):
    """
    Экран настроек, позволяющий изменять ник пользователя.
    """
    
    def __init__(self, contact_base: ContactBase, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        self.contact_base = contact_base
        self.build_ui()

    def build_ui(self) -> None:
        """
        Создает пользовательский интерфейс экрана настроек.
        """
        screen_width = Window.width
        screen_height = Window.height

        padding = [screen_width * 0.05, screen_height * 0.05, screen_width * 0.05, screen_height * 0.05]
        spacing = screen_height * 0.02

        root = ColoredBoxLayout(orientation='vertical', padding=padding, spacing=spacing, bg_color=BACKGROUND_COLOR)

        # Верхняя панель с кнопкой назад
        top_bar = ColoredBoxLayout(size_hint_y=0.1, orientation='horizontal', bg_color=TOP_BAR_COLOR, padding=[screen_width * 0.025, screen_height * 0.025, screen_width * 0.025, screen_height * 0.025], spacing=screen_width * 0.025)
        back_button = Button(text='Назад', size_hint_x=0.1, background_normal='', background_color=[0.1, 0.1, 0.1, 1], color=BUTTON_COLOR)
        back_button.bind(on_press=self.go_back)
        top_bar.add_widget(back_button)
        title = Label(text='Настройки', size_hint_x=0.8, color=TITLE_COLOR, font_size=screen_height * 0.03, bold=True, halign='center', valign='middle')
        top_bar.add_widget(title)
        top_bar.add_widget(Label(size_hint_x=0.1))  # Пустое пространство для выравнивания
        root.add_widget(top_bar)

        # Создание функции для добавления поля ввода с меткой
        def add_input_field(layout, label_text, base = ""):
            field_layout = ColoredBoxLayout(size_hint_y=None, height=screen_height * 0.07, orientation='horizontal', spacing=screen_width * 0.025)
            label = Label(text=label_text, color=TEXT_COLOR, font_size=screen_height * 0.02, halign='left', valign='middle', size_hint_x=0.3)
            input_field = TextInput(
                size_hint=(0.7, None),
                height=screen_height * 0.05,
                background_color=[0.2, 0.2, 0.2, 1],
                foreground_color=TEXT_COLOR,
                padding=[10,2],
                font_size=screen_height * 0.025,
                hint_text_color=ICON_COLOR
            )
            
            field_layout.add_widget(label)
            field_layout.add_widget(input_field)

            layout.add_widget(field_layout)
            Clock.schedule_once(lambda dt: input_field.insert_text(base))
            return input_field

        # Поля ввода для настроек
        input_layout = ColoredBoxLayout(orientation='vertical', padding=[10, 0])
        self.nickname_input = add_input_field(input_layout, 'Никнейм', base = self.contact_base.client.username)
        self.status_input = add_input_field(input_layout, 'Статус', base = "Онлайн")

        # 6 дополнительных пустых полей
        self.additional_fields = []
        for i in range(5):
            self.additional_fields.append(add_input_field(input_layout, f'Поле {i+1}'))

        root.add_widget(input_layout)

        # Кнопка сохранения
        save_button = Button(
            text='Сохранить', 
            size_hint=(1, None), 
            height=screen_height * 0.07,
            background_normal='', 
            background_color=BUTTON_COLOR, 
            color=HIGHLIGHTED_TEXT_COLOR,
            font_size=screen_height * 0.025,
            bold=True,
            padding=[screen_width * 0.025, screen_height * 0.025]
        )
        save_button.bind(on_press=self.save_nickname)
        root.add_widget(save_button)

        self.add_widget(root)

    def go_back(self, instance) -> None:
        """
        Возвращается к экрану контактов.

        Args:
            instance: Экземпляр кнопки назад.
        """
        self.manager.transition.direction = 'left'
        self.manager.current = 'contacts'

    def save_nickname(self, instance) -> None:
        """
        Сохраняет новый ник пользователя.

        Args:
            instance: Экземпляр кнопки сохранения.
        """
        new_nickname = self.nickname_input.text
        new_status = self.status_input.text
        if new_nickname:
            # print(f'Новый ник: {new_nickname}')
            self.contact_base.rename(new_nickname)
            self.contact_base.client.username = new_nickname
        if new_status:
            # print(f'Новый статус: {new_status}')
            pass

if __name__ == "__main__":
    pass