import socket
import threading

clients = []
rooms = {}

def handle_client(client_socket, addr):
    print(f"New connection from {addr}")
    clients.append(client_socket)
    
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message.startswith('/join'):
                room_name = message.split(' ')[1]
                if room_name not in rooms:
                    rooms[room_name] = []
                rooms[room_name].append(client_socket)
                client_socket.send(f"You joined the room: {room_name}".encode('utf-8'))
            elif message.startswith('/msg'):
                room_name, msg = message.split(' ', 2)[1:]
                if room_name in rooms:
                    for client in rooms[room_name]:
                        if client != client_socket:
                            client.send(msg.encode('utf-8'))
            else:
                broadcast(message, client_socket)
        except:
            clients.remove(client_socket)
            break

def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            client.send(message.encode('utf-8'))

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5555))
    server.listen(5)
    print("Server started...")
    
    while True:
        client_socket, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

start_server()
