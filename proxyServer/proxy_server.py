# 柯宇翰 b10505048
# 羅世朋 b09505029
import socket

# Set the server IP address and port
# TODO Start
HOST, PORT = "127.0.0.1", 6028
HOST2, PORT2 = "127.0.0.1", 9999
# TODO end

# Create a server socket, bind it to the specified IP and port, and start listening
# TODO Start
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((HOST2, PORT2))
serverSocket.listen()
# TODO end

while True:
    print('Ready to serve...')
    # Accept an incoming connection and get the client's address
    # TODO Start

    client_socket, client_address = serverSocket.accept()
    # TODO end
    print('Received a connection from:', client_address)

    try:
        # Receive request from the client
        # TODO Start
        request = client_socket.recv(1024).decode()
        # TODO end
        print(request)

        # Extract the filename from the request
        if request == "":
            request = "/ /"
        filename = request.split()[1].partition("/")[2]
        print(filename)
        file_path = "/" + filename
        print(file_path)

        file_exist = "false"
        try:
            # Check whether the file exists in the cache
            with open(file_path[1:], "r") as cache_file:
                output_data = cache_file.readlines()
            file_exist = "true"

            # ProxyServer finds a cache hit and generates a response message
            # Send the file data to the client
            client_socket.send("HTTP/1.1 200 OK\r\n".encode('utf-8'))
            client_socket.send("Content-Type:text/html\r\n\r\n".encode('utf-8'))
            # TODO Start
            for line in output_data:
                client_socket.send(line.encode())
            # TODO End
            print('Read from cache')

        # Error handling if the file is not found in cache
        except FileNotFoundError:

            # Create a socket on the proxy server
            # TODO Start
            proxy_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # TODO End

            host_name = filename.replace("www.", "", 1)
            print("Host name is " + host_name)

            try:
                print("Trying to connect to the web server")
                # Connect the socket to the web server port
                # TODO Start
                proxy_server_socket.connect((HOST, PORT))
                # TODO End
                print("Connected successfully")
                # Create a temporary file on this socket
                file_obj = proxy_server_socket.makefile('rw', None)

                # Create the HTTP GET request message to fetch the file from the web server
                # Write the request to the file-like object
                request_message = f"GET {file_path} HTTP/1.1\r\n"
                print(request_message)
                proxy_server_socket.send(request_message.encode())
                # file_obj.write(request_message)  # Write the request to the file-like object
                # file_obj.flush()
                # proxy_server_socket.send(file_obj.encode())
                print("Sent the request to the web server successfully")

                # Read the response into buffer
                # TODO Start
                s = ""
                i = 0
                while True:
                    server_message = proxy_server_socket.recv(1024).decode()
                    s = server_message + s

                    if not server_message:
                        break
                    if s == "HTTP/1.1 404 Not Found\r\n" + "Content-Type: text/html\r\n\r\n":
                        break


                if s:
                    s = s.replace("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n", "")
                    s = s.replace("<html><body><h1> 404 Not Found </h1></body></html>\r\n\r\n", "")
                    s = s.replace("HTTP/1.1 404 Not Found\r\n\r\n", "")

                if s == "HTTP/1.1 404 Not Found\r\n" + "Content-Type: text/html\r\n\r\n":
                    print("HTTP/1.1 404 Not Found\r\n\r\n")
                    client_socket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
                    print("HTTP/1.1 404 Not Found\r\n\r\n")
                    client_socket.send("<html><body><h1> 404 Not Found </h1></body></html>\r\n\r\n".encode())
                    client_socket.close()
                    break

                # TODO End
                print("Read the file from the web server successfully")

                # Create a new file in the cache for the requested file
                # TODO Start
                with open(filename, 'w') as logFile:
                    for i in s:
                        logFile.write(i)
                # TODO End
                print("Wrote the file to the cache successfully")

                # Send the response to the client socket
                # TODO Start
                info = "HTTP/1.1 200 OK\r\n" + "Content-Type: text/html\r\n\r\n"
                client_socket.send(info.encode())
                with open(filename, 'r') as logFile:
                    line = logFile.readlines()
                for lin in line:
                    client_socket.send(lin.encode())
                # TODO End
                print("Sent the data from the web server to the client")
            except:
                print("Illegal request")


    finally:
        # Close the client socket
        client_socket.close()

# Close the server socket
serverSocket.close()
