#  Techboy_ChatApp Documentation

### Overview
This project consists of two Python scripts, `romeo.py` and `juliet.py`, which set up a simple chat application using sockets. The server (`romeo.py`) listens for incoming connections, and the client (`juliet.py`) connects to the server. Once connected, the server and client can exchange messages until either party sends an "exit" message to close the connection.

### Modules Used
- **`socket`**: Provides low-level networking interface.
- **`threading`**: Used for running multiple threads (tasks) at once.
- **`os`**: Provides a way of using operating system-dependent functionality.

### `romeo.py` - Server Script

#### Purpose
The `romeo.py` script sets up a server that waits for a client to connect and facilitates message exchanges with the connected client.

#### Usage Instructions
1. Run `romeo.py`.
2. Enter the server's IP address and port number when prompted.
3. The server will wait for a client to connect.
4. Once connected, messages can be exchanged between the server and the client.
5. Type "exit" to close the connection and terminate the program.

- Example :
```bash
D:\>python Romeo.py
Enter Romeo IP address ex : 0.0.0.0 : 0.0.0.0
Enter Romeo port number ex : 4444 : 4444
Listening for connection on 0.0.0.0:4444...
```

#### Code
```python
import socket
import threading
import os

# Get server IP and port number from user input
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

# Function to send messages to the client
def send_msg():
    while True:
        msg = input()  # Read user input
        Kiran.send(msg.encode())  # Send the message to the client
        if msg.lower() == "exit":  # Check if the message is "exit"
            Kiran.close()  # Close the client socket
            Techboy.close()  # Close the server socket
            print("Connection closed.")
            os._exit(0)  # Exit the program immediately

# Function to receive messages from the client
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
```

#### Key Components
1. **Socket Creation**:
   ```python
   Techboy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   Techboy.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
   ```
   - `AF_INET`: Address family for IPv4.
   - `SOCK_STREAM`: Socket type for TCP.

2. **Binding and Listening**:
   ```python
   Techboy.bind((host, port))
   Techboy.listen(1)
   ```
   - `bind()`: Associates the socket with the provided host and port.
   - `listen()`: Enables the server to accept connections. `1` specifies the number of unaccepted connections the system will allow before refusing new connections.

3. **Accepting Connections**:
   ```python
   Kiran, adrr = Techboy.accept()
   ```
   - `accept()`: Blocks and waits for an incoming connection, returning a new socket and the address of the client.

4. **Sending Messages**:
   ```python
   def send_msg():
       while True:
           msg = input()
           Kiran.send(msg.encode())
           if msg.lower() == "exit":
               Kiran.close()
               Techboy.close()
               print("Connection closed.")
               os._exit(0)
   ```
- The `send_msg` function is responsible for sending messages from the server to the client. It operates in a loop and performs the following steps:
-  **Read User Input**:
   ```python
   msg = input()
   ```
   - This line waits for the user to type a message and press Enter.

-  **Send Message to Client**:
   ```python
   Kiran.send(msg.encode())
   ```
   - This line encodes the user's message into bytes and sends it over the socket to the client.

- **Check for Exit Condition**:
   ```python
   if msg.lower() == "exit":
       Kiran.close()
       Techboy.close()
       print("Connection closed.")
       os._exit(0)
   ```
   **`msg.lower()`**:
   - Converts the entire message string `msg` to lowercase.
   - Example: If `msg` is `"Exit"`, `msg.lower()` would be `"exit"`.

 - If the user types "exit", the server closes both the client and server sockets, prints a message indicating the connection is closed, and exits the program.

5. **Receiving Messages**:
   ```python
   def recv_msg():
       while True:
           received = Kiran.recv(1024)
           if not received or received.decode().lower() == "exit":
               print("Connection closed by juliet.")
               Kiran.close()
               Techboy.close()
               os._exit(0)
           print("juliet: ")
           print(received.decode())
           print("Romeo: ")
   ```
- The `recv_msg` function is responsible for receiving messages from the client. It operates in a loop and performs the following steps:

   - **Receive Message from Client**:
   ```python
   received = Kiran.recv(1024)
   ```
   - This line waits for a message from the client. The `1024` specifies the maximum amount of data to be received at once (1 KB).

   - **Check for Exit Condition**:
   ```python
   if not received or received.decode().lower() == "exit":
       print("Connection closed by juliet.")
       Kiran.close()
       Techboy.close()
       os._exit(0)
   ```
   - If the message is empty (indicating the client has closed the connection) or if the message is "exit", the server closes both the client and server sockets, prints a message indicating the connection is closed by the client, and exits the program.

   - **Print Received Message**:
   ```python
   print("juliet: ")
   print(received.decode())
   print("Romeo: ")
   ```
   - This block decodes the received message from bytes to a string, prints the message indicating it is from the client, and prompts the user to input the next message.

6. **Threading**:
   ```python
   t1 = threading.Thread(target=send_msg)
   t1.start()
   recv_msg()
   ```
   - Creates a new thread to handle sending messages so that receiving messages can be handled simultaneously in the main thread.

### `juliet.py` - Client Script

#### Purpose
The `juliet.py` script sets up a client that connects to the server and facilitates message exchanges with the connected server.

#### Usage Instructions
1. Run `juliet.py`.
2. Enter the server's IP address and port number when prompted.
3. The client will attempt to connect to the server.
4. Once connected, messages can be exchanged between the client and the server.
5. Type "exit" to close the connection and terminate the program.

 ```bash
D:\>python Juliet.py
Enter Romeo IP address - ex: 0.tcp.ngrok.io : 0.tcp.ngrok.io
Enter Romeo port number - ex: 13005  : 13005
```


#### Code
```python
import socket
import threading
import os

# Create a socket for the client
Kiran = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get server IP and port number from user input
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

# Function to send messages to the server
def send_msg():
    while True:
        msg = input()  # Read user input
        Kiran.send(msg.encode())  # Send the message to the server
        if msg.lower() == "exit":  # Check if the message is "exit"
            Kiran.close()  # Close the client socket
            print("Connection closed.")
            os._exit(0)  # Exit the program immediately

# Function to receive messages from the server
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
```

#### Key Components
1. **Socket Creation**:
   ```python
   Kiran = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   ```

2. **Connecting to the Server**:
   ```python
   while True:
       try:
           Kiran.connect((host, port))
           break
       except ConnectionRefusedError:
           continue
   ```
   -  **Infinite Loop**:
   ```python
   while True:
   ```
   - The loop runs indefinitely until it is explicitly broken out of with the `break` statement.

   - **Attempt to Connect**:
   ```python
   try:
       Kiran.connect((host, port))
   ```
   - The `connect` method tries to establish a connection to the specified host and port.

   - **Successful Connection**:
   ```python
   break
   ```
   - If the connection is successful, the `break` statement exits the loop.

   - **Exception Handling**:
   ```python
   except ConnectionRefusedError:
       continue
   ```
   - If a `ConnectionRefusedError` exception is raised (indicating that the connection attempt was refused), the `continue` statement causes the loop to restart, retrying the connection.

3. ***Sending Messages***:
   ```python
   def send_msg():
       while True:
           msg = input()
           Kiran.send(msg.encode())
           if msg.lower() == "exit":
               Kiran.close()
               print("Connection closed.")
               os._exit(0)
   ```

4. **Receiving Messages**:
   ```python
   def recv_msg():
       while True:
           received = Kiran.recv(1024)
           if not received or received.decode().lower() == "exit":
               print("Connection closed by Romeo.")
               Kiran.close()
               os._exit(0)
           print("Romeo: ")
           print(received.decode())
           print("juliet: ")
   ```

5. **Threading**:
   ```python
   t1 = threading.Thread(target=send_msg)
   t1.start()
   recv_msg()
   ```

### Summary
- **Modules Used**: `socket`, `threading`, `os`
- **`romeo.py`**:
  - Sets up the server.
  - Handles connections and message exchanges.
  - Uses threading to handle simultaneous sending and receiving of messages.
- **`juliet.py`**:
  - Sets up the client.
  - Connects to the server.
  - Handles message exchanges with the server.
  - Uses threading to handle simultaneous sending and receiving of messages.
- **Termination**: Typing "exit" in either the server or client will close the connection and terminate the program.
