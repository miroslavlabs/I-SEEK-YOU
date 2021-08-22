from datetime import datetime
from pprint import pp

import requests
from questionary import Choice, Separator, text, select

server_endpoint = 'http://127.0.0.1:5000/api/v1/'


def ask_username():
    return text('👤 What\'s your username:').ask()


def join_chat():
    while True:
        username = ask_username()
        response = requests.post(server_endpoint + 'users/{username}'.format(username=username))
        if response.status_code == 200:
            return response


def ask_chat_action():
    return select(
        'What do you want to do?',
        choices=[
            Choice(title='Send a message', value=1),
            Choice(title='Get all messages', value=2),
            Separator(),
            Choice(title='Get total cost for my user', value=3),
        ], use_shortcuts=True, use_arrow_keys=False, show_selected=False, use_indicator=False
    ).ask()


def ask_send_message():
    return text('Message').ask()


def send_message(username):
    message = ask_send_message()
    response = requests.post(server_endpoint + 'messages', {'username': username, 'message': message})
    if response.status_code == 200:
        return response
    else:
        pp(response)


def chat(username):
    while True:
        action = ask_chat_action()
        if action == 1:
            send_message(username)
        elif action == 2:
            fetch_chat_messages()
        elif action == 3:
            get_total_cost(username)
        elif action is None:
            exit(0)
        else:
            print('🚧')


def fetch_chat_messages():
    response = requests.get(server_endpoint + 'messages')
    if response.status_code == 200:
        messages = response.json()['messages']
        for message in messages:
            timestamp_date = datetime.strptime(message['timestamp'], '%Y-%m-%dT%H:%M:%S.%f')
            timestamp_formatted = timestamp_date.strftime('%H:%M:%S')
            print('🕒 {timestamp} 👤 {username} 💬 {message}'.format(timestamp=timestamp_formatted, username=message['username'], message=message['message']))
        print()


def get_total_cost(username):
    response = requests.get(server_endpoint + 'billing-cost', params={'username': username})
    if response.status_code == 200:
        cost = response.json()['cost']
        print('Total cost: {total_cost}'.format(total_cost=cost['total_cost']))


def main():
    response = join_chat()
    username = response.json()['user']['username']
    print('Hello, {username}'.format(username=username))
    chat(username)


if __name__ == '__main__':
    main()
