import datetime
import time

import requests
from PyQt5 import QtCore

username = ''
password = ''


class ProcessAuthorization(QtCore.QThread):

    def __init__(self, main_window):
        super().__init__()
        self.window = main_window

    def run(self):
        self.window.login_in.clicked.connect(self.button_pushed)

    def button_pushed(self):
        global username
        global password
        username = self.window.lineLogin.text()
        password = self.window.linePassword.text()

        self.authorization()

    def authorization(self):
        user = {'username': username, 'password': password}
        try:
            response = requests.post('http://127.0.0.1:5000/authorization', json=user)
            code = response.status_code
            print(code)
            if code == 200:
                self.window.process_chats.start()
                self.window.stackedWidget.setCurrentWidget(self.window.chats)
            elif code == 401:
                print("Не правильный логин или пароль!")
            elif code == 201:
                print(f"Автоматическая регистрация прошла успешно! Имя:{username} Пароль:{password}")
            else:
                print(f"Неизвестная ошибка({code})!")
        except:
            print('Connection Error!')


class ProcessChats(QtCore.QThread):

    def __init__(self, main_window):
        super().__init__()
        self.window = main_window

    def run(self):
        self.window.sendButton.pressed.connect(self.button_pushed)

    def button_pushed(self):
        text = self.window.message.toPlainText()
        self.send_message(text)
        self.window.message.setText('')
        self.window.message.repaint()

    def send_message(self, text):
        message = {'username': username, 'password': password, 'text': text}
        try:
            response = requests.post('http://127.0.0.1:5000/send', json=message)
            if response.status_code == 401:
                self.show_text('Bad password')
            elif response.status_code != 200:
                self.show_text('Connection Error!')
        except:
            self.show_text('Connection Error!')

    def show_text(self, text):
        self.window.messagesAll.append(text)
        self.window.messagesAll.repaint()

