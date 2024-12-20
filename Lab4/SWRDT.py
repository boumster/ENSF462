import Network
import argparse
from time import sleep
import hashlib
import time


class Segment:
    ## the number of bytes used to store segment length
    seq_num_S_length = 10
    length_S_length = 10
    ## length of md5 checksum in hex
    checksum_length = 32

    def __init__(self, seq_num, msg_S):
        self.seq_num = seq_num
        self.msg_S = msg_S

    @classmethod
    def from_byte_S(self, byte_S):
        if byte_S is None or Segment.corrupt(byte_S):
            raise RuntimeError("Cannot initialize Segment: byte_S is corrupt or None")
        # extract the fields
        seq_num = int(
            byte_S[
                Segment.length_S_length : Segment.length_S_length
                + Segment.seq_num_S_length
            ]
        )
        msg_S = byte_S[
            Segment.length_S_length + Segment.seq_num_S_length + Segment.checksum_length :
        ]
        return self(seq_num, msg_S)

    def get_byte_S(self):
        # convert sequence number of a byte field of seq_num_S_length bytes
        seq_num_S = str(self.seq_num).zfill(self.seq_num_S_length)
        # convert length to a byte field of length_S_length bytes
        length_S = str(
            self.length_S_length
            + len(seq_num_S)
            + self.checksum_length
            + len(self.msg_S)
        ).zfill(self.length_S_length)
        # compute the checksum
        checksum = hashlib.md5((length_S + seq_num_S + self.msg_S).encode("utf-8"))
        checksum_S = checksum.hexdigest()
        # compile into a string
        return length_S + seq_num_S + checksum_S + self.msg_S

    @staticmethod
    def corrupt(byte_S):
        # extract the fields
        length_S = byte_S[0 : Segment.length_S_length]
        seq_num_S = byte_S[
            Segment.length_S_length : Segment.length_S_length + Segment.seq_num_S_length
        ]
        checksum_S = byte_S[
            Segment.length_S_length + Segment.seq_num_S_length : Segment.length_S_length + Segment.seq_num_S_length + Segment.checksum_length
        ]
        msg_S = byte_S[
            Segment.length_S_length + Segment.seq_num_S_length + Segment.checksum_length :
        ]
        # compute the checksum locally
        checksum = hashlib.md5(str(length_S + seq_num_S + msg_S).encode("utf-8"))
        computed_checksum_S = checksum.hexdigest()
        # and check if the same
        return checksum_S != computed_checksum_S


class SWRDT:
    ## latest sequence number used in a segment
    seq_num = 1
    expected_seq_num = 1
    ## buffer of bytes read from network
    byte_buffer = ""

    def __init__(self, role_S, receiver_S, port):
        self.network = Network.NetworkLayer(role_S, receiver_S, port)

    def disconnect(self):
        self.network.disconnect()

    def swrdt_send(self, msg_S):
        p = Segment(self.seq_num, msg_S)
        while True:
            print(f"Send message {self.seq_num}")
            self.network.network_send(p.get_byte_S())
            start_time = time.time()
            while True:
                ack = self.network.network_receive()
                if ack:
                    try:
                        ack_segment = Segment.from_byte_S(ack)
                        if ack_segment.seq_num == self.seq_num:
                            print(f"Receive ACK {ack_segment.seq_num}. Message successfully sent!")
                            self.seq_num += 1
                            return
                        else:
                            print(f"Receive ACK {ack_segment.seq_num}. Resend message {self.seq_num}")
                            break
                    except RuntimeError:
                        # Occurs when the received segment is corrupt
                        print(f"Corruption detected in ACK. Resend message {self.seq_num}")
                        break
                if time.time() - start_time > 2:  # timeout after 2 seconds
                    print(f"Timeout! Resend message {self.seq_num}")
                    break

    def swrdt_receive(self):
        ret_S = None
        byte_S = self.network.network_receive()
        self.byte_buffer += byte_S
        while True:
            if len(self.byte_buffer) < Segment.length_S_length:
                return ret_S
            length = int(self.byte_buffer[: Segment.length_S_length])
            if len(self.byte_buffer) < length:
                return ret_S
            try:
                p = Segment.from_byte_S(self.byte_buffer[:length])
                
                if p.seq_num < self.expected_seq_num:
                    print(f"Received duplicate message {p.seq_num}. Send ACK {p.seq_num}")
                    ack_segment = Segment(p.seq_num, "ACK")
                    self.network.network_send(ack_segment.get_byte_S())
                    self.byte_buffer = self.byte_buffer[length:]
                    continue
                if p.seq_num == self.expected_seq_num:
                    print(f"Receive message {p.seq_num}. Send ACK {p.seq_num}")
                    ack_segment = Segment(p.seq_num, "ACK")
                    self.network.network_send(ack_segment.get_byte_S())
                    self.expected_seq_num += 1
                    ret_S = p.msg_S if (ret_S is None) else ret_S + p.msg_S
                    self.byte_buffer = self.byte_buffer[length:]
                    return ret_S
                else:
                    print(f"Received out-of-order message {p.seq_num}. Send ACK {self.expected_seq_num - 1}")
                    ack_segment = Segment(self.expected_seq_num - 1, "ACK")
                    self.network.network_send(ack_segment.get_byte_S())
                    self.byte_buffer = self.byte_buffer[length:]
                    continue
            except RuntimeError:
                print(f"Corruption detected! Send ACK {self.expected_seq_num - 1}")
                ack_segment = Segment(self.expected_seq_num - 1, "ACK")
                self.network.network_send(ack_segment.get_byte_S())
                self.byte_buffer = self.byte_buffer[length:]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SWRDT implementation.")
    parser.add_argument(
        "role",
        help="Role is either sender or receiver.",
        choices=["sender", "receiver"],
    )
    parser.add_argument("receiver", help="receiver.")
    parser.add_argument("port", help="Port.", type=int)
    args = parser.parse_args()

    swrdt = SWRDT(args.role, args.receiver, args.port)
    if args.role == "sender":
        swrdt.swrdt_send("MSG_FROM_SENDER")
        sleep(2)
        print(swrdt.swrdt_receive())
        swrdt.disconnect()

    else:
        sleep(1)
        print(swrdt.swrdt_receive())
        swrdt.swrdt_send("MSG_FROM_RECEIVER")
        swrdt.disconnect()