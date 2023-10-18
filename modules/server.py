import socket   
import threading

# IP del equipo
host = '127.0.0.1'
port = 8080 

clients = []
usernames = []

def broadcast(message, _client):
    for client in clients:
        if client != _client:
            client.send(message)

def handle_messages(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message, client)
        except:
            index = clients.index(client)
            username = usernames[index]
            broadcast(f"ChatBot: {username} disconnected".encode('utf-8'), client)
            clients.remove(client)
            usernames.remove(username)
            client.close()
            break

def create_server():
    # Variables servidor
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"Server running on {host}:{port}")

    """
    while True:
        client, address = server.accept()

        client.send("@username".encode("utf-8"))
        username = client.recv(1024).decode('utf-8')

        clients.append(client)
        usernames.append(username)

        print(f"{username} is connected with {str(address)}")

        message = f"ChatBot: {username} joined the chat!".encode("utf-8")
        broadcast(message, client)
        client.send("Connected to server".encode("utf-8"))

        thread = threading.Thread(target=handle_messages, args=(client,))
        thread.start()
    """
    while True:
        client, address = server.accept()

        client.send("@username".encode("utf-8"))
        username = client.recv(1024).decode('utf-8')

        clients.append(client)
        usernames.append(username)

        print(f"{username} is connected with {str(address)}")

        # Enviar mensaje de bienvenida al cliente
        client.send("Connected to server".encode("utf-8"))

        message = f"ChatBot: {username} joined the chat!".encode("utf-8")
        broadcast(message, client)

        thread = threading.Thread(target=handle_messages, args=(client,))
        thread.start()



if __name__ == "__main__":
    create_server()
