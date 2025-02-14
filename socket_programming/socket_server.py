# 柯宇翰 b10505048
# 羅世朋 b09505029
import socket
import time
from datetime import datetime


# Function to calculate the expression
def calculate_expression(expression):
    # TODO: Implement this function
    if expression != "Y" and expression != "N":
        return float(eval(expression))
    else:
        return expression
    pass


# Server setup
# Specify the IP address and port number (Use "127.0.0.1" for localhost on local machine)
# TODO Start
# HOST, PORT = '140.112.42.104', 7777
HOST, PORT = "127.0.0.1", 6028
# TODO end

with open('./server_log.txt', 'w') as logFile:
    # 1. Create a socket
    # 2. Bind the socket to the address
    # TODO Start
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((HOST, PORT))
    # TODO End

    while True:
        # Listen to a new request with the socket
        # TODO Start
        serverSocket.listen()
        # TODO End

        now = datetime.now()
        print("The Server is running..")
        logFile.write(now.strftime("%H:%M:%S ") + "The Server is running..\n")
        logFile.flush()

        # Accept a new request and admit the connection
        # TODO Start
        client, address = serverSocket.accept()
        # TODO End

        client.settimeout(15)
        print(str(address) + " connected")
        now = datetime.now()
        logFile.write(now.strftime("%H:%M:%S ") + "connected " + str(address) + '\n')
        logFile.flush()

        try:
            while True:

                client.send(("Please input a question for calculation").encode())

                # Recieve the data from the client
                # TODO Start
                question = client.recv(1024).decode()
                # TODO End

                now = datetime.now()
                logFile.write(now.strftime("%H:%M:%S ") + question + '\n')
                logFile.flush()

                # TODO: Call the calculate_expression function here
                if question.lower() != 'n' or question.lower() != 'y':
                    ans = str(calculate_expression(question))
                if question.lower() == 'y':
                    question = client.recv(1024).decode()
                    ans = str(calculate_expression(question))

                # Ask if the client want to terminate the process
                message = f"{ans}\nDo you wish to continue? (Y/N)"

                # Send the answer back to the client
                # TODO Start
                if question.lower() != 'n' and question.lower() != 'y':
                    client.send(message.encode())
                    continue
                # TODO End

                # Terminate the process or continue
                if question.lower() == 'n':
                    break

        except ConnectionResetError:
            print("Connection reset by peer")
            logFile.write("Connection reset by peer\n")
            logFile.flush()
        except Exception as e:
            print("An error occurred:", e)
            logFile.write(f"An error occurred: {e}\n")
            logFile.flush()

        client.close()

logFile.close()
