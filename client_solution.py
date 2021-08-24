from datetime import datetime

import requests
from questionary import Choice, Separator, text, select

server_endpoint = 'http://127.0.0.1:5000/api/v1/'


# TASK 1
def ask_username():
    return input("Enter username: ")


# TASK 2
def ask_chat_action():
    print("Select option:")
    print("1. Send a message")
    print("2. Get all messages")
    print("3. Get messages by user")
    print("4. Get messages after hour and minute")
    print("5. Get messages cost by user")

    option = input()
    if option == '':
        return None

    option = int(option)
    while option < 1 or option > 5:
        print("Invalid option. Choose from 1 to 5...")
        option = int(input())

    return option


# TASK 3
def ask_send_message():
    return input("Send message: ")


# TASK 4
def print_all_chat_messages():
    messages = fetch_all_messages()
    if messages:
        for message in messages:
            print_message(message)
    else:
        print("No messages gave been sent yet...")


# TASK 4
def print_chat_messages_by_username():
    username = input("Get messages by username: ")
    messages = fetch_all_messages()
    for message in messages:
        if message['username'] == username:
            print_message(message)


# TASK 4
def print_chat_messages_by_time():
    time = input("Time: ")
    messages = fetch_all_messages()

    for message in messages:
        if get_message_datetime(message) > create_datetime_from_time(time):
            print_message(message)


def chat(username):
    while True:
        action = ask_chat_action()
        if action == 1:
            send_message(username)
        elif action == 2:
            # TASK 4
            print_all_chat_messages()
        elif action == 3:
            # TASK 4
            print_chat_messages_by_username()
        elif action == 4:
            # TASK 4
            print_chat_messages_by_time()
        elif action == 5:
            get_total_cost(username)
        else:
            print("Exiting...")
            exit(0)


# ------------------ DO NOT MODIFY UNLESS YOU ARE A PRO ------------------
def send_message(username):
    message = ask_send_message()
    response = requests.post(server_endpoint + 'messages', {'username': username, 'message': message})
    if response.status_code == 200:
        return response
    else:
        print("Response from server is: ", response)


def print_message(message):
    timestamp_date = datetime.strptime(message['timestamp'], '%Y-%m-%dT%H:%M:%S.%f')
    timestamp_formatted = timestamp_date.strftime('%H:%M:%S')
    print('🕒 {timestamp} 👤 {username} 💬 {message}'.format(timestamp=timestamp_formatted,
                                                             username=message['username'],
                                                             message=message['message']))


def fetch_all_messages():
    response = requests.get(server_endpoint + 'messages')
    messages = []
    if response.status_code == 200:
        messages = response.json()['messages']

    return messages


def get_message_datetime(message):
    return datetime.strptime(message['timestamp'], '%Y-%m-%dT%H:%M:%S.%f')


def create_datetime_from_time(time):
    hour = int(time[:2])
    minute = int(time[3:])
    return datetime.today().replace(hour=hour, minute=minute, second=0)


def get_total_cost(username):
    response = requests.get(server_endpoint + 'billing-cost', params={'username': username})
    if response.status_code == 200:
        cost = response.json()['cost']
        print('Total cost: {total_cost}'.format(total_cost=cost['total_cost']))


def join_chat():
    while True:
        username = ask_username()
        response = requests.post(server_endpoint + 'users/{username}'.format(username=username))
        if response.status_code == 200:
            return response


def main():
    response = join_chat()
    username = response.json()['user']['username']
    print('Hello, {username}'.format(username=username))
    chat(username)


if __name__ == '__main__':
    main()
