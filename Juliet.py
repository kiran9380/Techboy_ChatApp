import socket
import threading
import os

# Create a socket for the client
Kiran = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = input("Enter Romeo IP address: ")
port = int(input("Enter Romeo port number: "))

# Attempt to connect to the server
while True:
    try:
        Kiran.connect((host, port))
        break
    except ConnectionRefusedError:
        continue

print(f"Connected to Romeo {host}:{port}")
print("juliet : ")

def send_msg():
    while True:
        msg = input()  # Read user input
        Kiran.send(msg.encode())  # Send the message to the server
        if msg.lower() == "exit":  # Check if the message is "exit"
            Kiran.close()  # Close the client socket
            print("Connection closed.")
            os._exit(0)  # Exit the program immediately

def recv_msg():
    while True:
        received = Kiran.recv(1024)  # Receive message from the server
        if not received or received.decode().lower() == "exit":  # Check if the connection is closed or the message is "exit"
            print("Connection closed by Romeo.")
            Kiran.close()  # Close the client socket
            os._exit(0)  # Exit the program immediately
        print("Romeo: ")
        print(received.decode())  # Print the received message
        print("juliet : ")

# Create and start the send_msg thread
t1 = threading.Thread(target=send_msg)
t1.start()

# Run the recv_msg function in the main thread
recv_msg()
