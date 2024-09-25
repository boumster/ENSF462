from socket import *
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

user2 = input('Input your name: ')

print('The server is ready to receive')
while True:
    connectionSocket, addr = serverSocket.accept()
    user1 = connectionSocket.recv(1024).decode()
    print(f'{user1} has connected')
    connectionSocket.send(f'{user2} is connected'.encode())
    while True:
        try:
            sentence = connectionSocket.recv(1024).decode()
            print('Received a message')
            print(f'{user1}: {sentence}')
            if 'bye' in sentence:
                break
            modifiedSentence = input(f'{user2}: ')
            modifiedSentence = f'{user2}: {modifiedSentence}'
            connectionSocket.send(modifiedSentence.encode())
            if "bye" in modifiedSentence:
                break
        except Exception as e:
            print(f"An error occurred: {e}")
            break
    connectionSocket.close()
