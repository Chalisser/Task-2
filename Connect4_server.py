import threading
import socket
from connect4 import Connect4

host = "127.0.0.1"
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []
players = [0]
current = 1
connect = Connect4()

def broadcast(message):
    for client in clients:
        client.send(message)

def remove_client(client):
    index = clients.index(client)
    clients.remove(client)
    nickname = nicknames[index]
    nicknames.remove(nickname)
    return nickname

def handle(client):
    print(f"Handling client {players[0]}")
    while True:
        try:
            
            message = client.recv(1024).decode("ascii")
            print(message)
            if message == "QUIT":
                remove_client(client)
                
            # if(message.startswith('WIN')):
            #     player_won = int(message.split(" ")[1])
            #     if player_won == 0:
            #         broadcast("Match drawn!".encode("ascii"))
            #     else:
            #         player_won = nicknames[player_won - 1]
            #         broadcast(f"{player_won} wins!".encode("ascii"))
            # elif(message == "CONTINUE"):
            #     client.send("NOT OVER".encode("ascii"))
            # else:
            #     broadcast(message.encode("ascii"))
        except:
            index = clients.index(client)
            clients.remove(client)
            nickname = nicknames[index]
            print(f"{nickname} left the chat")
            nicknames.remove(nickname)

def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        nickname = client.recv(1024).decode("ascii")
        nicknames.append(nickname)
        clients.append(client)

        players[0] += 1

        client.send(f"{players[0]}".encode("ascii"))

        # while players[0] >= 2:
        #     pass
        # if players[0] == 2:
        #     broadcast("START".decode("ascii"))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server is listening....")
receive()
