from socket import *
import threading
import time
import sys
import json

serverName = 'localhost'

link_state = {}  # Link state vector
recieved_link_state = {}  # Link state vector received from neighbors
num_of_nodes = 0  # Number of nodes in the network
routerid = 0  # Router ID

def send_link_state(routerport):
    while True:
        if not link_state:
            print("Link state is empty")
        for neighbor in link_state:
            try:
                # Create a socket and send the link state information
                with socket(AF_INET, SOCK_DGRAM) as sock:
                    message = json.dumps(link_state).encode()
                    print(f'{neighbor}')
                    print(f'{link_state[neighbor]}')
                    port = link_state[neighbor][str(routerid)]['port']
                    print(f"Sending message : {neighbor} : {port}")
                    sock.sendto(message, (serverName, port))
            except Exception as e:
                print(f"Error sending to {neighbor}: {e}")
        time.sleep(5)

def receive_link_state(routerport):
    while True:
        # Code to receive link state information from neighbors
        with socket(AF_INET, SOCK_DGRAM) as sock:
            sock.bind(('', routerport))
            while True:
                data, addr = sock.recvfrom(1024)
                try:
                    neighbor_link_state = json.loads(data.decode())
                    recieved_link_state[addr] = neighbor_link_state
                    # Process the received link state as needed
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")

import heapq

def compute_paths():
    global forwarding_table
    while True:
        # Initialize distances and priority queue
        if not link_state:
            print("Link state is empty")
            time.sleep(10)
            continue
        distances = {node: float('inf') for node in link_state}
        distances[routerid] = 0
        priority_queue = [(0, routerid)]
        previous_nodes = {node: None for node in link_state}

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)

            if current_distance > distances[current_node]:
                continue

            for neighbor, info in link_state[current_node].items():
                distance = current_distance + info['cost']
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(priority_queue, (distance, neighbor))

        # Update forwarding table
        forwarding_table = {}
        for node in link_state:
            if node == routerid:
                continue
            path = []
            current = node
            while previous_nodes[current] is not None:
                path.append(current)
                current = previous_nodes[current]
            path.reverse()
            if path:
                forwarding_table[node] = path[0]

        print(f"Updated forwarding table: {forwarding_table}")
        time.sleep(10)  # Recompute paths periodically
        
def read_config(configfile):
    global link_state, num_of_nodes, routerid
    with open(configfile, 'r') as file:
        lines = file.readlines()
        total_nodes = int(lines[0].strip())
        print(f"Total nodes: {total_nodes}")
        num_of_nodes = total_nodes
        router_label = str(routerid)
        link_state[router_label] = {}
        for line in lines[1:]:
            parts = line.strip().split()
            if len(parts) != 4:
                return
            try:
                neighbor_label = parts[0]
                neighbor_id = int(parts[1])
                link_cost = int(parts[2])
                neighbor_port = int(parts[3])
                link_state[router_label][neighbor_label] = {
                    'id': neighbor_id,
                    'cost': link_cost,
                    'port': neighbor_port
                }
                if neighbor_label not in link_state:
                    link_state[neighbor_label] = {}
                link_state[neighbor_label][router_label] = {
                    'id': routerid,
                    'cost': link_cost,
                    'port': routerport
                }
            except ValueError as e:
                print(f"Error processing line: {line} - {e}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python Router.py <routerid> <routerport> <configfile>")
        sys.exit(1)

    routerid = sys.argv[1]
    routerport = int(sys.argv[2])
    configfile = sys.argv[3]

    read_config(configfile)

    # Start threads for sending and receiving link state information
    send_thread = threading.Thread(target=send_link_state, args=(routerport,))
    receive_thread = threading.Thread(target=receive_link_state, args=(routerport,))
    compute_thread = threading.Thread(target=compute_paths)

    send_thread.start()
    receive_thread.start()
    compute_thread.start()

    send_thread.join()
    receive_thread.join()
    compute_thread.join()