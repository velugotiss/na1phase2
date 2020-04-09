import socket
import json
import requests

HOST = ''
PORT = 4000


def connect():
    sock = socket.socket()
    server = sock.bind((HOST, PORT))
    sock.listen(1)
    print("Server is Listening.....")
    conn, addr = sock.accept()
    return conn


def send_messages(c):
    while True:
        msg = str(c.recv(1024).decode())
        msg = msg.lower()
        if msg == "bye":
            print(msg)
            c.send(str.encode("Server connection is closed"))
            c.close()
            c = connect()
            send_messages(c)
        elif msg == "weather":
            response = requests.get(
                'https://samples.openweathermap.org/data/2.5/forecast/hourly?q=kansascity&appid=b6907d289e10d714a6e88b30761fae22')
            json_response = response.json()
            repository = json_response['daily']['data']
            message = ''
            for i in range(3):
                message += str(repository[i]['temperatureLow']) + 'c/'
            message = 'Next  three Consecutive days temperature : ' + message
            c.send(str.encode(message))
        else:
            print(msg)
            c.send(str.encode(msg))


def main():
    c = connect()
    send_messages(c)


if __name__ == '__main__':
    main()
