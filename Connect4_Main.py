import socket
import threading
from connect4 import Connect4

# Connect to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 55555))

# Type nickname
nickname = input("Enter your nickname: ")

# Send to server
client.send(f"{nickname}".encode("ascii"))

# Server sends back if you're player 1 or 2
message = client.recv(1024).decode("ascii")
index = int(message)

# Initialise board and current player
connect = Connect4(index+1)
current = 1

# Server sends whether both players have joined
message = client.recv(1024).decode("ascii")
if message.startswith("START"):
    print(" ".message.split(" ")[1:])

# Loop until server sends winner
while True:
    
    # Play move if current player
    if current == index:
        col = connect.play(index)
    
        # Send move to server
        message = f"{col} {index}"
        client.send(message.encode("ascii"))

        

    # Receive reply from server
    message = client.recv(1024).decode("ascii")

    # Win or draw after your move
    if message.startswith("RESULT"):
        print(message)
        client.send("QUIT".encode("ascii"))
        break

    # Win or draw after opponent's move
    elif message.startswith("MOVERESULT"):
        col = message.split(" ")[1]
        player = message.split(" ")[2]

        connect.updateBoard(col, player)

        print(" ".join(message[3:]))
        client.send("QUIT".encode("ascii"))
        break
    
    # No result
    elif message.startswith("MOVE"):
        col = message.split(" ")[1]
        player = message.split(" ")[2]

        connect.updateBoard(col, player)

        current = (current % 2) + 1

client.close()
    
    

        




    

