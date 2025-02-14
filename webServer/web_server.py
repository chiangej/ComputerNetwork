# 柯宇翰 b10505048
# 羅世朋 b09505029
import socket
import sys

# Server setup
# Specify the IP address and port number (Use "127.0.0.1" for localhost on local machine)
# TODO Start
HOST, PORT = "127.0.0.1", 6028
# TODO end


# 1. Create a socket
# 2. Bind the socket to the address
# TODO Start
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((HOST, PORT))
# TODO End

# Listen for incoming connections (maximum of 1 connection in the queue)
# TODO Start
serverSocket.listen()
# TODO End

# Start an infinite loop to handle incoming client requests
while True:
    print('Ready to serve...')

    # Accept an incoming connection and get the client's address
    # TODO Start
    connectionSocket, address = serverSocket.accept()
    # TODO End
    print(str(address) + " connected")

    try:
        # Receive and decode the client's request
        # TODO Start
        message = connectionSocket.recv(1024).decode()
        # TODO End

        # If the message is empty, set it to a default value
        if message == "":
            message = "/ /"

        # Print the client's request message
        print(f"client's request message: \n {message}")

        # Extract the filename from the client's request
        # TODO Start
        filename = message.split(" ")[1].replace("/","")

        # TODO End
        print(f"Extract the filename: {filename}")

        # Open the requested file
        # Read the file's content and store it in a list of lines
        f = open(filename)
        outputdata = f.readlines()
        f.close()

        # 1. Send an HTTP response header to the client
        # 2. Send the content of the requested file to the client line by line
        # 3. Close the connection to the client
        # TODO Start
        info = "HTTP/1.1 200 OK\r\n"+"Content-Type: text/html\r\n\r\n"
        connectionSocket.send(info.encode())
        for line in outputdata:
            connectionSocket.send(line.encode())
        connectionSocket.close()
        # TODO End

    except IOError:
        # If the requested file is not found, send a 404 Not Found response
        # TODO Start
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        connectionSocket.send("<html><body><h1> 404 Not Found </h1></body></html>\r\n\r\n".encode())
        pass
        # TODO End
