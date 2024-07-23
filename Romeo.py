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
        try:
            msg = input()  # Read user input
            if msg.startswith("sendfile "):
                filepath = msg.split(" ", 1)[1]
                if os.path.isfile(filepath):
                    Kiran.send(f"SENDFILE {os.path.basename(filepath)}".encode())
                    with open(filepath, "rb") as file:
                        while True:
                            data = file.read(4096)
                            if not data:
                                break
                            Kiran.sendall(data)
                    Kiran.send(b"EOF")  # Send EOF marker
                    print(f"File '{filepath}' sent.")
                else:
                    print("File not found.")
            else:
                Kiran.send(msg.encode())  # Send the message to the client
            if msg.lower() == "exit":  # Check if the message is "exit"
                Kiran.close()  # Close the client socket
                Techboy.close()  # Close the server socket
                print("Connection closed.")
                os._exit(0)  # Exit the program immediately
        except Exception as e:
            print(f"Error sending message: {e}")
            break

def recv_msg():
    while True:
        try:
            received = Kiran.recv(4096)  # Receive message from the client
            if not received or received.decode().lower() == "exit":  # Check if the connection is closed or the message is "exit"
                print("Connection closed by juliet.")
                Kiran.close()  # Close the client socket
                Techboy.close()  # Close the server socket
                os._exit(0)  # Exit the program immediately
            decoded_message = received.decode()
            if decoded_message.startswith("SENDFILE "):
                filename = decoded_message.split(" ", 1)[1]
                with open(filename, "wb") as file:
                    while True:
                        data = Kiran.recv(4096)
                        if b"EOF" in data:
                            data = data.replace(b"EOF", b"")
                            if data:
                                file.write(data)
                            break
                        file.write(data)
                print(f"File '{filename}' received.")
            else:
                print("juliet : ")
                print(decoded_message)  # Print the received message
            print("Romeo: ")
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

# Create and start the send_msg thread
t1 = threading.Thread(target=send_msg)
t1.start()

# Run the recv_msg function in the main thread
recv_msg()
