import argparse
import SWRDT
import time

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Uppercase conversion receiver.")
    parser.add_argument("port", help="Port.", type=int)
    args = parser.parse_args()

    timeout = 10  # close connection if no new data within 10 seconds
    time_of_last_data = time.time()

    swrdt = SWRDT.SWRDT("receiver", None, args.port)
    expected_messages = 10
    received_messages = 0

    while received_messages < expected_messages:
        # try to receive message before timeout
        msg_S = swrdt.swrdt_receive()
        if msg_S is None:
            if time_of_last_data + timeout < time.time():
                break
            else:
                continue
        time_of_last_data = time.time()

        # process the message (convert to uppercase)
        print(f"Received raw message: {msg_S}")  # Debug print
        try:
            identifier, msg_content = msg_S.split(":", 1)
        except ValueError:
            print(f"Error splitting message: {msg_S}")
            continue

        # Send ACK for the received message
        ack_segment = SWRDT.Segment(int(identifier), "ACK")
        swrdt.network.network_send(ack_segment.get_byte_S())
        print(f"Send ACK {identifier}")

        received_messages += 1

    swrdt.disconnect()
