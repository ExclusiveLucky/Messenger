from app.chat import ChatScreen
from app.contacts import ContactsScreen
from app.settings import SettingsScreen
from app.config import App, ScreenManager, SlideTransition
from app.config import Clock
from network.client import ContactBase

# python -m PyInstaller --onefile --name chat C:\python\P2P\main.py

class MessengerApp(App):
    """
    Основной класс приложения мессенджера.
    """
    
    def build(self) -> ScreenManager:
        """
        Создает и возвращает менеджер экранов приложения.

        Returns:
            ScreenManager: Менеджер экранов приложения.
        """
        self.contact_base = ContactBase("Denis")
        self.contact_base.registrate()
        self.contact_base.update()

        Clock.schedule_interval(self.contact_base.update, 1)  # Обновляем данные сервера

        self.sm = ScreenManager(transition=SlideTransition())
        self.sm.add_widget(ChatScreen(self.contact_base, name='chat'))
        self.sm.add_widget(ContactsScreen(self.contact_base, name='contacts'))
        self.sm.add_widget(SettingsScreen(self.contact_base,name='settings'))

        # Установка начального экрана
        self.sm.current = 'contacts'

        return self.sm
    
        
if __name__ == '__main__':
    MessengerApp().run()