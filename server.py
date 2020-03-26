from flask import Flask, request, abort, Response
import time
import datetime

app = Flask(__name__)

messages = [
    {'username': 'Nick', 'text': 'Hello', 'time': 0.0}
]

users = {
    'Nick': '12345'
}


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/status")
def status():

    return {
        'status': True,
        'name': "Saigla",
        'time': datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
        'users': len(users),
        'messages': len(messages)
    }


@app.route('/authorization', methods=['POST'])
def authorization():
    username = request.json['username']
    password = request.json['password']

    if username in users:  # зарегистрированный пользователь
        if password != users[username]:
            return abort(401)
    else:
        users[username] = password  # регистрируем
        return Response("{'a':'b'}", status=201, mimetype='application/json')
    return {"ok": True}


@app.route("/send", methods=['POST'])
def send():
    '''

    принимаем ?фаеук=адщфе
    :return: JSON {
        "messages": [
            {"username": str, "text: str "time": float}
        ]
    }
    :return:
    '''
    username = request.json['username']
    password = request.json['password']

    if password != users[username]:
        return abort(401)

    text = request.json['text']
    current_time = time.time()
    message = {'username': username, 'text': text, 'time': current_time}
    messages.append(message)
    print(messages)
    return {"ok": True}


@app.route("/messages")
def messages_view():
    after = float(request.args.get('after'))

    # filtered_messages = []
    # for message in messages:
    #     if message['time'] > after:
    #         filtered_messages.append(message)

    filtered_messages = [message for message in messages if message['time'] > after]

    return {
        'messages': filtered_messages
    }


app.run()
