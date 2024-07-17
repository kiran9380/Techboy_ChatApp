import socket
import threading
import os

host = input("Enter Romeo IP address ex : 0.0.0.0 : ")
port = int(input("Enter Romeo port number ex : 4444 : "))

# Create a socket for the server
Techboy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Techboy.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to the provided host and port
Techboy.bind((host, port))
print(f"Listening for connection on {host}:{port}...")

# Listen for incoming connections
Techboy.listen(1)

# Accept a connection from a client
Kiran, adrr = Techboy.accept()
print(f"Connected to juliet  {adrr}")
print("Romeo: ")

def send_msg():
    while True:
        msg = input()  # Read user input
        Kiran.send(msg.encode())  # Send the message to the client
        if msg.lower() == "exit":  # Check if the message is "exit"
            Kiran.close()  # Close the client socket
            Techboy.close()  # Close the server socket
            print("Connection closed.")
            os._exit(0)  # Exit the program immediately

def recv_msg():
    while True:
        received = Kiran.recv(1024)  # Receive message from the client
        if not received or received.decode().lower() == "exit":  # Check if the connection is closed or the message is "exit"
            print("Connection closed by juliet .")
            Kiran.close()  # Close the client socket
            Techboy.close()  # Close the server socket
            os._exit(0)  # Exit the program immediately
        print("juliet : ")
        print(received.decode())  # Print the received message
        print("Romeo: ")

# Create and start the send_msg thread
t1 = threading.Thread(target=send_msg)
t1.start()

# Run the recv_msg function in the main thread
recv_msg()
