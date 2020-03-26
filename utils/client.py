import requests


def send_message(username, password, text):
    message = {'username': username, 'password': password, 'text': text}
    response = requests.post('http://127.0.0.1:5000/send', json=message)
    return response.status_code == 200


def authorization(username, password):
    user = {'username': username, 'password': password}
    response = requests.post('http://127.0.0.1:5000/authorization', json=user)
    code = response.status_code
    if code != 200:
        if code == 401:
            print("Не правильный логин или пароль!")
        elif code == 201:
            print(f"Автоматическая регистрация прошла успешно! Имя:{username} Пароль:{password}")
        else:
            print(f"Неизвестная ошибка({code})!")
    return code == 200 or code == 201


while True:
    status = False
    while status is False:
        username = input('Введите имя: ')
        password = input('Введите пароль: ')
        status = authorization(username, password)
    print("Вы авторизовались!")

    while True:
        text = input()
        result = send_message(username, password, text)
        if result is False:
            print('Ошибка проверки авторизации!')
            break
