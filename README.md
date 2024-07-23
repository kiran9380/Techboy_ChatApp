#  `Techboy_ChatApp` Project Documentation

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

### 4. **Sending Messages**:
   ```python
   def send_msg():
       while True:
           msg = input()
           Kiran.send(msg.encode())
           
5. **Sending Files**

Certainly! Let’s break down this segment of code in detail, explaining its purpose and functionality step-by-step. This segment is designed to handle the sending of files or text messages based on user input.

### Code Segment

```python
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
    Kiran.send(msg.encode())
```

### Detailed Explanation

1. **Checking for File Transfer Command**:
   ```python
   if msg.startswith("sendfile "):
   ```
   - **Purpose**: Checks if the message (`msg`) starts with the keyword `"sendfile "`. This keyword indicates that the user intends to send a file.
   - **Functionality**: This allows the code to distinguish between regular text messages and file transfer commands.

2. **Extracting the File Path**:
   ```python
   filepath = msg.split(" ", 1)[1]
   ```
   Certainly! Let's break down the line `filepath = msg.split(" ", 1)[1]` and understand what it does:

1. **`msg`**: This presumably is a string variable that contains the entire message received or processed in some context.

2. **`split(" ", 1)`**: This method call splits the string `msg` into a list of substrings based on the delimiter `" "` (a space), but only splits it once. The result of this operation is a list where the first element is everything before the first space, and the second element is everything after the first space.

   - Example: If `msg` is `"sendfile /path/to/file.txt"`, then `msg.split(" ", 1)` would result in `['sendfile', '/path/to/file.txt']`.

3. **`[1]`**: This index access `[1]` is used to retrieve the second element of the list returned by `split(" ", 1)`. In our example above, `msg.split(" ", 1)[1]` would give `'/path/to/file.txt'`.

Therefore, `filepath = msg.split(" ", 1)[1]` effectively extracts the file path from the message `msg` that starts with `"sendfile "`. It assumes that the message `msg` is structured such that the command `"sendfile "` is followed by a space and then the actual file path.

- **Purpose**: To extract the file path from a message that starts with `"sendfile "`.
- **Assumption**: The message format is `"sendfile <file_path>"`, where `<file_path>` is the absolute or relative path to the file you want to send.
- **Result**: `filepath` will contain the extracted file path, which is then used to check if the file exists (`os.path.isfile(filepath)`) and to open and read the file for sending over a network connection (`with open(filepath, "rb") as file:`).

3. **Checking if the File Exists**:
   ```python
   if os.path.isfile(filepath):
   ```
   - **Purpose**: Verifies if the file specified by `filepath` exists in the file system.
   - **Functionality**: Ensures that only existing files are sent. If the file does not exist, it prints an error message.

4. **Sending the File**:
   ```python
   Kiran.send(f"SENDFILE {os.path.basename(filepath)}".encode())
   ```
   - **Purpose**: Sends a command to the client indicating that a file transfer is about to begin. The command includes the file name.
   - **Functionality**: Encodes the command into bytes and sends it to the client using `Kiran.send()`.

5. **Reading and Sending the File in Chunks**:
   Certainly! Let's break down the code snippet:

```python
with open(filepath, "rb") as file:
    while True:
        data = file.read(4096)
        if not data:
            break
        Kiran.sendall(data)
```

This code snippet is part of a file-sending mechanism in Python using sockets, assuming `Kiran` represents a socket object capable of sending data.

### Explanation:

1. **`with open(filepath, "rb") as file:`**:
   - This line opens the file specified by `filepath` in binary read mode (`"rb"`). The `with` statement ensures that the file is properly closed after its suite (indented block of code) finishes, even if an exception occurs.

2. **`while True:`**:
   - This starts an infinite loop which will read the file in chunks until the entire file is read and sent.

3. **`data = file.read(4096)`**:
   - Inside the loop, `file.read(4096)` reads up to 4096 bytes of data from the file and stores it in `data`.

4. **`if not data:`**:
   - This condition checks if `data` is empty. In Python, an empty byte string (`b""`) evaluates to `False`, so `if not data` will be true when the end of the file is reached.

5. **`break`**:
   - If `data` is empty (end of file), the loop breaks, meaning all data has been read and sent.

6. **`Kiran.sendall(data)`**:
   - This sends the `data` chunk over the socket represented by `Kiran`. `sendall()` ensures that all data is sent; it continues sending data until either all data has been sent or an error occurs.

### Summary:

- **Purpose**: To read a file (`filepath`) in chunks of 4096 bytes and send each chunk over a network socket (`Kiran`).
- **Mechanism**: 
  - The file is opened in binary read mode (`"rb"`).
  - A loop reads chunks of up to 4096 bytes (`data = file.read(4096)`).
  - Each chunk (`data`) is sent over the socket using `Kiran.sendall(data)`.
  - The loop continues until all data from the file has been read and sent (`if not data` evaluates to true when `file.read(4096)` returns an empty byte string).

This approach is efficient for sending potentially large files over a network, as it minimizes memory usage by reading and sending the file in manageable chunks.

6. **Sending End-of-File (EOF) Marker**:
   ```python
   Kiran.send(b"EOF")  # Send EOF marker
   ```
   - **Purpose**: Sends a special marker (`EOF`) to indicate the end of the file transfer.
   - **Functionality**: Allows the client to know when the file has been fully transmitted, so it can stop expecting more data.

7. **Printing Confirmation**:
   ```python
   print(f"File '{filepath}' sent.")
   ```
   - **Purpose**: Provides feedback to the sender that the file has been successfully sent.
   - **Functionality**: Prints a confirmation message with the file name.

8. **Handling File Not Found**:
   ```python
   else:
       print("File not found.")
   ```
   - **Purpose**: Provides feedback if the file specified in the command does not exist.
   - **Functionality**: Prints an error message indicating that the file could not be found.

9. **Sending Regular Text Messages**:
   ```python
   else:
       Kiran.send(msg.encode())
   ```
   - **Purpose**: Handles messages that are not file transfer commands.
   - **Functionality**: Encodes the text message into bytes and sends it directly to the client using `Kiran.send()`.
   
This code segment is designed to handle two types of user input:
- **File Transfers**: If the input starts with `"sendfile "`, the code extracts the file path, checks if the file exists, and sends the file in chunks with an end-of-file marker.
- **Text Messages**: If the input does not start with `"sendfile "`, it is treated as a regular text message and sent directly.

The code ensures efficient file transfer by sending files in manageable chunks and provides feedback to the user about the status of the file transfer.

10. **Check for Exit Condition**:
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

11. **Exception Handling**

Certainly! Let's break down and explain the exception handling code segment:

##### Code Segment

```python
except Exception as e:
    print(f"Error sending message: {e}")
    break
```

##### Detailed Explanation

1. **Exception Handling Block**:
   ```python
   except Exception as e:
   ```
   - **Purpose**: Catches any exceptions that may occur during the execution of the code within the `try` block.
   - **Functionality**:
     - `except`: This keyword is used to handle exceptions. It catches exceptions that match the specified type.
     - `Exception`: This is the base class for all built-in exceptions in Python. By catching `Exception`, the code is designed to catch all types of exceptions, ensuring that any error during execution is handled.
     - `as e`: This part assigns the caught exception to the variable `e`. It allows access to the exception object, which contains information about the error that occurred.

2. **Printing the Error Message**:
   ```python
   print(f"Error sending message: {e}")
   ```
   - **Purpose**: Provides feedback about the error that occurred.
   - **Functionality**:
     - `print()`: This function outputs the specified message to the console.
     - `f"Error sending message: {e}"`: This is an f-string (formatted string literal) that includes the error message. The `e` variable, which contains the exception object, is included in the string, providing details about the error.
   - **Output Example**: If an error occurs, such as a network disconnection, the output might be: `Error sending message: [Errno 32] Broken pipe`.

3. **Breaking the Loop**:
   ```python
   break
   ```
   - **Purpose**: Exits the loop in which this code resides.
   - **Functionality**:
     - `break`: This statement terminates the nearest enclosing loop. In this context, it stops the `while True` loop that is responsible for sending messages.
   - **Effect**: By breaking out of the loop, the code stops attempting to send more messages. This is crucial in the event of an error, as continuing to send messages could lead to further complications or repeated errors.

##### Context

This exception handling code is typically found within a `while True` loop used for continuously sending messages. The relevant `try` block might look something like this:

```python
def send_msg():
    while True:
        try:
            msg = input()  # Read user input
            # Additional code to handle sending the message or file
        except Exception as e:
            print(f"Error sending message: {e}")
            break
```

- **Purpose**: The `except Exception as e` block catches and handles all types of exceptions that occur within the `try` block.
- **Error Reporting**: The `print(f"Error sending message: {e}")` line provides feedback about the error, helping to diagnose issues.
- **Stopping Execution**: The `break` statement exits the loop, preventing further attempts to send messages after an error occurs, thereby maintaining the stability of the program.

### 12. Receiving Messages 

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
   
13. **Receiving Files**

Let's break down and explain the specific portion of the code you've highlighted:

##### Code Segment

```python
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
```

##### Detailed Explanation

1. **Decoding the Received Message**:
   ```python
   decoded_message = received.decode()
   ```
   - **Purpose**: Converts the received byte data into a string.
   - **Functionality**:
     - `received.decode()`: This method converts the received byte data (`received`) into a string using the default encoding (usually UTF-8).

2. **Checking for File Transfer Command**:
   ```python
   if decoded_message.startswith("SENDFILE "):
   ```
   - **Purpose**: Determines if the received message indicates the start of a file transfer.
   - **Functionality**:
     - `decoded_message.startswith("SENDFILE ")`: Checks if the string starts with "SENDFILE ", which is a custom protocol command indicating a file transfer initiation.

3. **Extracting the Filename**:
   ```python
   filename = decoded_message.split(" ", 1)[1]
   ```
   - **Purpose**: Extracts the filename from the "SENDFILE " command.
   - **Functionality**:
     - `decoded_message.split(" ", 1)`: Splits the string into two parts at the first space. The first part is "SENDFILE" and the second part is the filename.
     - `[1]`: Selects the second part, which is the filename.

4. **Opening the File for Writing**:
   ```python
   with open(filename, "wb") as file:
   ```
   - **Purpose**: Opens a new file to write the incoming data.
   - **Functionality**:
     - `open(filename, "wb")`: Opens the file in binary write mode ("wb").
     - `with`: Ensures the file is properly closed after the block is executed.

5. **Receiving and Writing File Data**:
  Certainly! Let's break down the code snippet you provided:

```python
while True:
    data = Kiran.recv(4096)
    if b"EOF" in data:
        data = data.replace(b"EOF", b"")
        if data:
            file.write(data)
        break
    file.write(data)
```

This code snippet is typically used to receive data over a network socket (`Kiran`) and write it to a file (`file`). Here's a detailed explanation:

#### Explanation:

1. **`while True:`**
   - This initiates an infinite loop which continues until explicitly broken.

2. **`data = Kiran.recv(4096)`**
   - `Kiran.recv(4096)` attempts to receive up to 4096 bytes of data from the socket `Kiran`. It stores the received data in the variable `data`.

3. **`if b"EOF" in data:`**
   - This checks if the byte sequence `b"EOF"` is present in the received `data`.

4. **`data = data.replace(b"EOF", b"")`**
   - If `b"EOF"` is found in `data`, it replaces all instances of `b"EOF"` with an empty byte sequence `b""`. This is to handle the marker indicating the end of the data transmission.

5. **`if data:`**
   - After removing `b"EOF"`, if `data` still contains any bytes, it writes these bytes to the `file`.

6. **`break`**
   - The `break` statement exits the `while` loop. This happens when `b"EOF"` is detected in the received `data`, indicating the end of the file transmission.

7. **`file.write(data)`**
   - If `b"EOF"` is not found in `data`, it writes the received `data` (or the modified `data` after replacing `b"EOF"`) to the `file`.

- **Purpose**: To receive data over a socket (`Kiran`) and write it to a file (`file`).
- **Mechanism**:
  - The loop continues to receive chunks of data (`Kiran.recv(4096)`).
  - It checks if the end-of-file marker (`b"EOF"`) is present in the received data.
  - If `b"EOF"` is found, it removes it and writes any remaining data to the file (`if data:`).
  - The loop exits (`break`) when `b"EOF"` is detected, indicating the end of the data transmission.
  - If `b"EOF"` is not found, it continues to write the received data to the file (`file.write(data)`).

This approach is commonly used for receiving files or large data streams over a network, where `b"EOF"` serves as a marker to signify the end of the data being transmitted.

6. **Printing the File Received Confirmation**:
   ```python
   print(f"File '{filename}' received.")
   ```
   - **Purpose**: Notifies that the file has been successfully received.
   - **Functionality**:
     - `print(f"File '{filename}' received.")`: Outputs a confirmation message with the filename.

7. **Handling Regular Messages**:
   ```python
   else:
       print("juliet : ")
       print(decoded_message)  # Print the received message
   print("Romeo: ")
   ```
   - **Purpose**: Handles regular chat messages that are not file transfers.
   - **Functionality**:
     - `else`: Executes if the received message does not start with "SENDFILE ".
     - `print("juliet : ")`: Indicates the message is from Juliet.
     - `print(decoded_message)`: Outputs the received chat message.
     - `print("Romeo: ")`: Prepares for the next input prompt from Romeo.

- **Exception Handling**:
```python
except Exception as e:
    print(f"Error sending message: {e}")
    break
```
-`except Exception as e`: Catches any exceptions that occur during message receiving.
    - `print(f"Error receiving message: {e}")`: Prints the error message.
    - `break`: Exits the loop.


#### Summary

This code segment is part of the `recv_msg` function that continuously receives data from the connected client (Juliet). It decodes the received data and checks if it indicates the start of a file transfer. If so, it extracts the filename and writes the received file data to a new file, handling an "EOF" marker to signify the end of the file. If the message is a regular chat message, it prints it out for the user. This ensures seamless handling of both file transfers and chat messages in the application.


### 14. **Threading**:
  Certainly! Let's break down the provided code snippet:

```python
t1 = threading.Thread(target=send_msg)
t1.start()
recv_msg()
```

##### Explanation:

1. **`t1 = threading.Thread(target=send_msg)`**:
   - This line creates a new thread (`t1`) that will execute the `send_msg` function concurrently. The `target=` parameter specifies the function (`send_msg`) that the thread will run.
   - Threads in Python are used to achieve concurrent execution, allowing multiple functions to run simultaneously or in parallel.

2. **`t1.start()`**:
   - This starts the execution of the thread `t1`. When `t1.start()` is called, Python initiates a new operating system-level thread that will invoke `send_msg()` concurrently with any other threads running in the program.
   - `send_msg()` function will start executing in its own thread, independent of the main thread (where `recv_msg()` might be called).

3. **`recv_msg()`**:
   - This function is called immediately after starting the `t1` thread. Since this call is not inside a thread itself, `recv_msg()` will execute in the main thread (unless it also starts another thread internally).

- **Purpose**: The code aims to achieve concurrent execution of `send_msg()` and `recv_msg()` functions, likely for handling communication tasks concurrently.
- **Threads**: 
  - `t1` is used to run `send_msg()` concurrently with the main program flow.
  - `recv_msg()` is called directly in the main thread or any other thread it might start internally.

##### Notes:

- Using threads (`threading.Thread`) allows for parallel execution of functions that might perform I/O-bound operations (like sending and receiving messages over a network) without blocking each other.
- Care should be taken with thread synchronization and resource sharing (like shared variables or data structures) to avoid potential issues such as race conditions.

# `juliet.py` - Client Script

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

```

Sure, let's break down and explain each part of the `juliet.py` code.

### Full Code Explanation

```python
import socket
import threading
import os
```

- **Imports**:
  - `socket`: This module provides access to the BSD socket interface. It's used for network communication.
  - `threading`: This module constructs higher-level threading interfaces on top of the lower-level `_thread` module. It's used to run multiple threads (functions) concurrently.
  - `os`: This module provides a way of using operating system-dependent functionality like reading or writing to the file system.

```python
# Create a socket for the client
Kiran = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```

- **Socket Creation**:
  - `Kiran`: This is the client socket object.
  - `socket.AF_INET`: Specifies the address family for the socket (IPv4).
  - `socket.SOCK_STREAM`: Specifies that the socket is a TCP socket.

```python
host = input("Enter Romeo IP address - ex: 0.tcp.ngrok.io : ")
port = int(input("Enter Romeo port number - ex: 13005  : "))
```

- **User Input**:
  - `host`: Takes the IP address or hostname of the server (Romeo) as input.
  - `port`: Takes the port number of the server as input.

```python
# Attempt to connect to the server
while True:
    try:
        Kiran.connect((host, port))
        break
    except ConnectionRefusedError:
        continue
```

- **Connection Attempt**:
  - The client (`Kiran`) attempts to connect to the server (`host` and `port`).
  - The `while True` loop ensures that the client keeps trying to connect until successful.
  - `Kiran.connect((host, port))`: Tries to establish a connection to the server.
  - `ConnectionRefusedError`: If the connection is refused, it catches the exception and continues to retry.

```python
print(f"Connected to Romeo {host}:{port}")
print("juliet : ")
```

- **Connection Confirmation**:
  - Prints a message indicating that the client is connected to the server.
  - Indicates that the prompt is ready for Juliet's (client's) input.

```python
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
```

- **Message Sending Function (`send_msg`)**:
  - **Infinite Loop**: Continuously waits for user input.
  - **Message Handling**:
    - **File Sending**:
      - `msg.startswith("sendfile ")`: Checks if the input starts with "sendfile ", indicating a file transfer.
      - `filepath = msg.split(" ", 1)[1]`: Extracts the file path from the input.
      - `os.path.isfile(filepath)`: Checks if the specified file exists.
      - `Kiran.send(f"SENDFILE {os.path.basename(filepath)}".encode())`: Sends a message to the server indicating the start of a file transfer with the file's name.
      - `with open(filepath, "rb") as file`: Opens the file in binary read mode.
      - `file.read(4096)`: Reads up to 4096 bytes from the file.
      - `Kiran.sendall(data)`: Sends the read data to the server.
      - `Kiran.send(b"EOF")`: Sends an EOF marker indicating the end of the file transfer.
      - `print(f"File '{filepath}' sent.")`: Confirms that the file has been sent.
    - **Regular Message**:
      - `Kiran.send(msg.encode())`: Sends the message to the server.
    - **Exit Command**:
      - `if msg.lower() == "exit"`: Checks if the message is "exit" (case insensitive).
      - `Kiran.close()`: Closes the client socket.
      - `print("Connection closed.")`: Prints a message indicating the connection is closed.
      - `os._exit(0)`: Exits the program immediately.
  - **Exception Handling**:
    - `except Exception as e`: Catches any exceptions that occur during message sending.
    - `print(f"Error sending message: {e}")`: Prints the error message.
    - `break`: Exits the loop.

```python
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
```

- **Message Receiving Function (`recv_msg`)**:
  - **Infinite Loop**: Continuously waits to receive messages from the server.
  - **Message Handling**:
    - **Receiving Data**:
      - `received = Kiran.recv(4096)`: Receives up to 4096 bytes of data from the server.
      - `if not received or received.decode().lower() == "exit"`: Checks if the connection is closed or if the received message is "exit".
      - `print("Connection closed by Romeo.")`: Prints a message indicating the server closed the connection.
      - `Kiran.close()`: Closes the client socket.
      - `os._exit(0)`: Exits the program immediately.
    - **File Receiving**:
      - `decoded_message = received.decode()`: Decodes the received data into a string.
      - `if decoded_message.startswith("SENDFILE ")`: Checks if the message indicates the start of a file transfer.
      - `filename = decoded_message.split(" ", 1)[1]`: Extracts the filename from the message.
      - `with open(filename, "wb") as file`: Opens a new file in binary write mode.
      - `data = Kiran.recv(4096)`: Receives file data from the server.
      - `if b"EOF" in data`: Checks for the end-of-file marker in the data.
      - `data.replace(b"EOF", b"")`: Removes the EOF marker from the data.
      - `file.write(data)`: Writes the data to the file.
      - `print(f"File '{filename}' received.")`: Confirms that the file has been received.
    - **Regular Message**:
      - `print("Romeo: ")`: Indicates the message is from Romeo.
      - `print(decoded_message)`: Prints the received message.
      - `print("juliet : ")`: Prepares for the next input prompt from Juliet.
  - **Exception Handling**:
    - `except Exception as e`: Catches any exceptions that occur during message receiving.
    - `print(f"Error receiving message: {e}")`: Prints the error message.
    - `break`: Exits the loop.

```python
# Create and start the send_msg thread
t1 = threading.Thread(target=send_msg)
t1.start()

# Run the recv_msg function in the main thread
recv_msg()
```

- **Thread Creation and Execution**:
  - **Sending Messages**:
    - `t1 = threading.Thread(target=send_msg)`: Creates a new thread to run the `send_msg` function.
    - `t1.start()`: Starts the thread.
  - **Receiving Messages**:
    - `recv_msg()`: Runs the `recv_msg` function in the main thread, ensuring that the program continuously receives messages.

### Summary

This code implements a simple chat client that can send and receive both text messages and files. It uses TCP sockets for communication and threading to handle sending and receiving messages concurrently. The `send_msg` function handles sending messages and files, while the `recv_msg` function handles receiving messages and files from the server. Proper exception handling ensures the program exits gracefully on errors.

Certainly! Here’s a detailed documentation for your project, including how you used ChatGPT in the development process. 

---
# References I used for this project.
I learned socket and threading with these videos,

`Socket` : https://youtu.be/MR_84xQlduc?si=eLfV9QSXkMIBPkCb

`Threading` : https://youtu.be/ZkzreM9ADeg?si=slrHiuun1m3Wzkr8

 With these videos I built a simple chatting app after that I modified this using AI (ChatGPT )

## How ChatGPT Was Used in This Project

### 1. **Code Explanation and Refinement**

ChatGPT was utilized to provide detailed explanations of various parts of the code, ensuring a clear understanding of how each component works. Key aspects include:

- **Understanding Socket Communication**: ChatGPT explained how socket objects are created and used to establish connections between the server and client, and how data is sent and received over these connections.
  
- **Error Handling**: Assistance was provided on how to handle exceptions gracefully, ensuring robust error reporting and control flow within the application.

- **File Transfer Logic**: Detailed explanations were given on implementing file transfer functionality, including encoding, sending, and receiving files using sockets.

### 2. **Documentation Creation**

ChatGPT helped in creating comprehensive documentation for the project, which includes:

- **Code Documentation**: Each function and critical code segment was explained, including parameters, return values, and the overall logic.

- **Markdown Formatting**: The documentation was formatted using Markdown to ensure readability and structure, including code blocks, headings, and detailed explanations.

### 3. **Code Optimization**

ChatGPT provided suggestions on optimizing code for handling various scenarios, such as large file transfers and efficient message handling. This included:

- **Buffer Size Management**: Guidance was offered on how to adjust buffer sizes for receiving data and handling large files effectively.

- **Connection Handling**: Recommendations were made for managing connections and handling disconnections properly.

## Detailed Code Documentation

### `romeo.py` (Server Script)

```python
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
```

- **Socket Setup**: Initializes a TCP socket, binds it to the specified address and port, and listens for incoming connections.
- **Connection Handling**: Accepts a single connection from the client and prints connection details.

#### `send_msg()` Function

```python
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
```

- **Message Handling**: Reads user input, checks if it’s a file transfer request or a regular message, and sends data accordingly.
- **Error Handling**: Prints error messages if something goes wrong during message sending.

#### `recv_msg()` Function

```python
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
```

- **Message Reception**: Receives and processes incoming messages from the client. Handles file transfers and regular messages.
- **File Handling**: Writes received file data to disk and prints a confirmation message.

### `juliet.py` (Client Script)

```python
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
```

- **Socket Setup**: Initializes a TCP socket and attempts to connect to the server specified by the user.
- **Connection Handling**: Keeps trying to connect until successful.

#### `send_msg()` Function

```python
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
```

- **Message Sending**: Handles sending both text and files to the server.
- **File Transfer**: Similar to the `send_msg` function in `romeo.py`, but in reverse (client-side).

#### `recv_msg()` Function

```python
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
```

- **Message Reception**: Receives and processes messages and files from the server.
- **File Handling**: Saves received files and prints confirmation.

### Summary

This project demonstrates a basic chat application with file transfer capabilities. The server (`romeo.py`) and client (`juliet.py`) use TCP sockets for communication. The ChatGPT assistant provided detailed explanations and documentation, helping to understand socket programming, message handling, and file transfers. Additionally,


