#import socket module
from socket import *
import sys # In order to terminate the program
serverSocket = socket(AF_INET, SOCK_STREAM) #Prepare a sever socket

port = 6004
serverSocket.bind(("", port))
serverSocket.listen()

#Fill in start
#Fill in end
while True:
#Establish the connection 
    print('Ready to serve...') 
    connectionSocket, addr = serverSocket.accept()

    try:
#Fill in start
#Fill in end
        message = connectionSocket.recv(1024).decode()
        print("Server received", repr(message))
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()
#Send one HTTP header line into socket
#Fill in start
#Fill in end
#Send the content of the requested file to the client 
        for i in range(0,len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
        print("Sent", repr(outputdata.encode()))
        connectionSocket.close() 
    except IOError:
#Send response message for file not found
#Fill in start
        message = "404 Error\r\n"
        connectionSocket.send(message.encode())
        print("Sent", repr(message.encode()))
#Fill in end
#Close client socket
#Fill in start
#Fill in end
serverSocket.close()
sys.exit()#Terminate the program after sending the corresponding data
