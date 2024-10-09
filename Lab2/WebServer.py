#import socket module
from socket import *
import threading

serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 6789
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

def handle_client(connectionSocket, addr):
    try:
        message =  connectionSocket.recv(1024).decode()
        filename = message.split()[1]
        filename = filename[1:]  # Remove the leading '/'
        print(f"Requested filename: {filename}")
        
        # Open and read the requested file
        with open(filename, 'r') as f:
            outputdata = f.read()
        #Send one HTTP header line into socket
        connectionSocket.send('HTTP/1.1 200 OK\r\n\r\n'.encode())
        #Send the content of the requested file to the client
        connectionSocket.send(outputdata.encode())
        
        connectionSocket.close()
    except IOError:
        #Send response message for file not found
        connectionSocket.send('HTTP/1.1 404 Not Found\r\n\r\n'.encode())
        connectionSocket.send('<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n'.encode())
        #Close client socket
        connectionSocket.close()

while True:
    #Establish the connection
    print('Ready to serve...')
    connectionSocket, addr =  serverSocket.accept()
    
    print(f"Accepted connection from {addr[0]}:{addr[1]}")
    # start a new thread to handle the client
    thread = threading.Thread(target=handle_client, args=( connectionSocket, addr,))
    thread.start()

serverSocket.close()

