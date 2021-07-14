import time
from pprint import pp

import requests
import threading
from PyInquirer import prompt, Separator

server_endpoint = 'http://127.0.0.1:5000/api/v1/'


def ask_username():
    username_prompt = {
        'type': 'input',
        'name': 'username',
        'message': '👤 Enter username:'
    }
    answer = prompt(username_prompt)

    return answer['username']


def join_chat():
    while True:
        username = ask_username()
        response = requests.post(server_endpoint + 'users/{username}'.format(username=username))
        if response.status_code == 200:
            return response


def ask_chat_action():
    chat_action_prompt = {
        'type': 'list',
        'name': 'action',
        'message': 'What do you want to do?',
        'choices': [
            {'value': 'send', 'name': '➡️ 💬 Send a message'},
            {'value': 'get', 'name': '🔄 💬 Get all messages'},
            Separator(),
            'Check messages by user',
            'Check messages after specific timestamp',
            'Check messages cost by user'
        ]
    }
    answer = prompt(chat_action_prompt)

    return answer['action']


def ask_send_message():
    chat_send_message_prompt = {
        'type': 'input',
        'name': 'message',
        'message': '💬 Message:'
    }
    answer = prompt(chat_send_message_prompt)

    return answer['message']


def send_message(username):
    while True:
        message = ask_send_message()
        response = requests.post(server_endpoint + 'messages', {'username': username, 'message': message})
        if response.status_code == 200:
            return response
        else:
            pp(response)


def chat(username):
    # fetch_chat_messages_thread = threading.Thread(target=fetch_chat_messages)
    # fetch_chat_messages_thread.start()

    while True:
        action = ask_chat_action()
        if action == 'send':
            send_message(username)
        elif action == 'get':
            fetch_chat_messages()
        else:
            print('🚧')


def fetch_chat_messages():
    response = requests.get(server_endpoint + 'messages')
    if response.status_code == 200:
        messages = response.json()['messages']
        for message in messages:
            print('🕒{timestamp} 👤{username}: 💬{message}'.format(timestamp=message['timestamp'], username=message['username'], message=message['message']))


def main():
    response = join_chat()
    username = response.json()['user']['username']
    print('Hello {username}'.format(username=username))
    chat(username)


if __name__ == '__main__':
    main()
