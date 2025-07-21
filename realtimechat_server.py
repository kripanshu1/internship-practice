import socket
import threading

HOST = '127.0.0.1'
PORT = 12345

clients = []
nicknames = []

def broadcast(message, _client):
    for client in clients:
        if client != _client:
            try:
                client.send(message)
            except:
                client.close()
                remove_client(client)

def remove_client(client):
    if client in clients:
        index = clients.index(client)
        clients.remove(client)
        nickname = nicknames[index]
        nicknames.remove(nickname)
        broadcast(f"{nickname} left the chat.".encode('utf-8'), client)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            if message:
                broadcast(message, client)
        except:
            remove_client(client)
            break

def receive_connections():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server started on {HOST}:{PORT}")

    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname} joined the chat!".encode('utf-8'), client)
        client.send("Connected to the server.".encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

if __name__ == "__main__":
    receive_connections()
