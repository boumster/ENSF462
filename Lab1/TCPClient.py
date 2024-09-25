from socket import *
serverName = 'localhost'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
name = input('Input your name: ')
clientSocket.send(name.encode())

while True:
    try:
        modifiedSentence = clientSocket.recv(1024)
        print(modifiedSentence.decode())
        if 'bye' in modifiedSentence.decode():
            break
        sentence = input(f'{name}: ')
        clientSocket.send(sentence.encode())
        if sentence == "bye":
            break
    except Exception as e:
        print(f"An error occurred: {e}")
        break

clientSocket.close()