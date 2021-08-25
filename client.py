from datetime import datetime

import requests
from questionary import Choice, Separator, text, select

server_endpoint = 'http://127.0.0.1:5000/api/v1/'


# TASK 1
def ask_username():
    print("Username still missing...")
    return ""


# TASK 2
def ask_chat_action():
    return -1


# TASK 3
def ask_send_message():
    print("Still missing...")


# TASK 4
# Use the method fetch_all_messages() to get all chat messages
# Use the method print_message(message) to get print message to console
def print_all_chat_messages():
    print("Still missing...")


# TASK 4
def print_chat_messages_by_user(username):
    print("Still missing...")


# TASK 4
# Use get_message_datetime() to get the data and time for a message
# Use create_datetime_from_time() to add the current data to the time that will be entered by the user
def print_chat_messages_by_time():
    print("Still missing...")


def chat(username):
    while True:
        action = ask_chat_action()
        if action == 1:
            send_message(username)
        elif action == 2:
            # TASK 4
            print ("Still missing...")
        elif action == 3:
            # TASK 4
            print ("Still missing...")
        elif action == 4:
            # TASK 4
            print("Still missing...")
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
    username = ask_username()
    response = requests.post(server_endpoint + 'users/{username}'.format(username=username))
    if response.status_code == 200:
        return response
    else:
        print("Invalid username")
        return None


def main():
    response = join_chat()
    if response is not None:
        username = response.json()['user']['username']
        print('Hello, {username}'.format(username=username))
        chat(username)


if __name__ == '__main__':
    main()
