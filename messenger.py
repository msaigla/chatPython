import datetime
import sys

import requests
from PyQt5 import QtWidgets, QtCore, uic
from processes import ProcessAuthorization, ProcessChats


class StartInterface(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = uic.loadUi("gui.ui", self)

        self.process_auth = ProcessAuthorization(main_window=self)
        self.process_chats = ProcessChats(main_window=self)

        self.after = 0
        self.stackedWidget.setCurrentWidget(self.authorization)
        self.process_auth.start()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_messages)
        self.timer.start(1000)

    def update_messages(self):
        try:
            response = requests.get(
                'http://127.0.0.1:5000/messages',
                params={'after': self.after}
            )
            data = response.json()
            for message in data['messages']:
                self.print_message(message)
                self.after = message['time']
        except:
            print('Connection Error!1')

    def print_message(self, message):
        user = message['username']
        message_time = message['time']
        text = message['text']
        dt = datetime.datetime.fromtimestamp(message_time)
        dt_beauty = dt.strftime('%d.%m.%Y %H:%M:%S')

        self.show_text(f'{dt_beauty} {user}\n{text}\n\n')

    def show_text(self, text):
        self.messagesAll.append(text)
        self.messagesAll.repaint()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = StartInterface()
    application.ui.show()
    sys.exit(app.exec())
