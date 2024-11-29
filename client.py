import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except:
            print("Disconnected from server")
            break

def send_messages(client_socket):
    while True:
        message = input()
        client_socket.send(message.encode('utf-8'))

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 5555))

    thread_receive = threading.Thread(target=receive_messages, args=(client_socket,))
    thread_receive.start()

    thread_send = threading.Thread(target=send_messages, args=(client_socket,))
    thread_send.start()

start_client()
