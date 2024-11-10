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
    for msg_S in msg_L:
        print("Sent Message: " + msg_S)
        swrdt.swrdt_send(msg_S)

        # try to receive message before timeout
        received_msg = None
        while received_msg is None:
            received_msg = swrdt.swrdt_receive()
            if received_msg is None:
                if time_of_last_data + timeout < time.time():
                    print(f"Timeout! Resend message {swrdt.seq_num}")
                    swrdt.swrdt_send(msg_S)
                    time_of_last_data = time.time()
                else:
                    continue
        time_of_last_data = time.time()

        # print the result
        if received_msg:
            print("Received Message: " + received_msg + "\n")
        else:
            print("No reply received for: " + msg_S + "\n")

    swrdt.disconnect()
