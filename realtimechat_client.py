import socket
import threading

HOST = '127.0.0.1'
PORT = 12345

def receive_messages(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            print("An error occurred!")
            client.close()
            break

def send_messages(client):
    while True:
        message = input()
        if message.lower() == 'exit':
            client.close()
            break
        client.send(f"{nickname}: {message}".encode('utf-8'))

if __name__ == "__main__":
    nickname = input("Choose your nickname: ")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    send_thread = threading.Thread(target=send_messages, args=(client,))
    send_thread.start()
