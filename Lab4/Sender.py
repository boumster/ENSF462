import argparse
import SWRDT
import time

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Quotation sender talking to a receiver."
    )
    parser.add_argument("receiver", help="receiver.")
    parser.add_argument("port", help="Port.", type=int)
    args = parser.parse_args()

    msg_L = [
        "sending message - 1",
        "sending message - 2",
        "sending message - 3",
        "sending message - 4",
        "sending message - 5",
        "sending message - 6",
        "sending message - 7",
        "sending message - 8",
        "sending message - 9",
        "sending message - 10",
    ]

    timeout = 2  # send the next message if no response
    time_of_last_data = time.time()

    swrdt = SWRDT.SWRDT("sender", args.receiver, args.port)
    for i, msg_S in enumerate(msg_L):
        print("Sent Message: " + msg_S)
        swrdt.swrdt_send(msg_S)

        # Wait for ACK
        ack_received = False
        while not ack_received:
            ack = swrdt.network.network_receive()
            if ack:
                try:
                    ack_segment = SWRDT.Segment.from_byte_S(ack)
                    if ack_segment.msg_S == "ACK" and ack_segment.seq_num == swrdt.seq_num - 1:
                        print(f"Receive ACK {ack_segment.seq_num}. Proceed to next message.")
                        ack_received = True
                except RuntimeError:
                    print(f"Corruption detected in ACK. Resend message {swrdt.seq_num - 1}")
            if time_of_last_data + timeout < time.time():
                print(f"Timeout! Resend message {swrdt.seq_num - 1}")
                swrdt.swrdt_send(msg_S)
                time_of_last_data = time.time()

        # Stop after the last message
        if i == len(msg_L) - 1:
            break

    swrdt.disconnect()
