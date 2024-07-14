from kivy.utils import get_color_from_hex
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, RoundedRectangle

import threading
import time

BACKGROUND_COLOR = get_color_from_hex('#2A2A2A')  # Немного светлее и с добавлением голубого оттенка
TOP_BAR_COLOR = get_color_from_hex('#3A3F44')  # Светлее и с легким голубым оттенком для контраста
TEXT_COLOR = get_color_from_hex('#D8D8D8')  # Светлее для улучшенной читабельности
HIGHLIGHTED_TEXT_COLOR = get_color_from_hex('#FFFFFF')  # Оставляем белый для выделенного текста
BUTTON_COLOR = get_color_from_hex('#1E90FF')  # Светлее с добавлением голубого оттенка
ICON_COLOR = get_color_from_hex('#B0B0B0')  # Светлее для лучшего контраста
LINK_COLOR = get_color_from_hex('#1E90FF')  # Соответствует цвету кнопок для консистентности
DIVIDER_COLOR = get_color_from_hex('#404040')  # Светлее и с добавлением голубого оттенка
USER_MESSAGE_COLOR = get_color_from_hex('#0E7373')  # Светлее для лучшего контраста с фоном
CONTACT_MESSAGE_COLOR = get_color_from_hex('#3A4447')  # Светлее для улучшенной видимости
TITLE_COLOR = get_color_from_hex('#1E90FF')  # Соответствует цвету кнопок и ссылок для консистентности
LABEL_COLOR = get_color_from_hex('#1E90FF')  # Соответствует цвету кнопок и ссылок для консистентности

ICON_COLOR = get_color_from_hex('#A3A3A3')
HIGHLIGHTED_TEXT_COLOR = get_color_from_hex('#FFFFFF')

# Настройки шрифта и размера
TITLE_FONT_SIZE = '20sp'
BUTTON_HEIGHT = 40

# Размер окна
WINDOW_SIZE = (360, 640)

# Контакты
CONTACTS = [
    'Alice',
    'Bob',
    'Charlie'
]


class ColoredBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        self.bg_color = kwargs.pop('bg_color', BACKGROUND_COLOR)
        super(ColoredBoxLayout, self).__init__(**kwargs)
        with self.canvas.before:
            Color(*self.bg_color)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos
  

if __name__ == "__main__":
    pass