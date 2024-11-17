from socket import *
import time

serverName = 'localhost'
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_DGRAM)  # Create a UDP socket
clientSocket.settimeout(1)  # Set the timeout to 1 second

sequence_number = 1
rtts = []
num_lost_packets = 0

for sequence_number in range(1, 11):
    send_time = time.time()
    message = f"Ping {sequence_number} {send_time}"
    clientSocket.sendto(message.encode(), (serverName, serverPort))
    
    try:
        response, serverAddress = clientSocket.recvfrom(1024)
        receive_time = time.time()
        rtt = receive_time - send_time
        rtts.append(rtt)
        print(f"Response from server: {response.decode()}")
        print(f"RTT: {rtt:.6f} seconds")
    except timeout:
        print("Request timed out")
        num_lost_packets += 1

# Calculate statistics
if rtts:
    min_rtt = min(rtts)
    max_rtt = max(rtts)
    avg_rtt = sum(rtts) / len(rtts)
else:
    min_rtt = max_rtt = avg_rtt = 0

packet_loss_rate = (num_lost_packets / 10) * 100

print(f"\nMinimum RTT: {min_rtt:.6f} seconds")
print(f"Maximum RTT: {max_rtt:.6f} seconds")
print(f"Average RTT: {avg_rtt:.6f} seconds")
print(f"Packet loss rate: {packet_loss_rate:.2f}%")

clientSocket.close()