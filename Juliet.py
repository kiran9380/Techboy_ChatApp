import socket
import threading
import os

# Create a socket for the client
Kiran = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = input("Enter Romeo IP address - ex: 0.tcp.ngrok.io : ")
port = int(input("Enter Romeo port number - ex: 13005  : "))

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
                Kiran.send(msg.encode())  # Send the message to the server
            if msg.lower() == "exit":  # Check if the message is "exit"
                Kiran.close()  # Close the client socket
                print("Connection closed.")
                os._exit(0)  # Exit the program immediately
        except Exception as e:
            print(f"Error sending message: {e}")
            break

def recv_msg():
    while True:
        try:
            received = Kiran.recv(4096)  # Receive message from the server
            if not received or received.decode().lower() == "exit":  # Check if the connection is closed or the message is "exit"
                print("Connection closed by Romeo.")
                Kiran.close()  # Close the client socket
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
                print("Romeo: ")
                print(decoded_message)  # Print the received message
            print("juliet : ")
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

# Create and start the send_msg thread
t1 = threading.Thread(target=send_msg)
t1.start()

# Run the recv_msg function in the main thread
recv_msg()
