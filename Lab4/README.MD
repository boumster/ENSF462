# ENSF462 Lab 4

For lab 4 of ENSF 462, the focus is on implementing a reliable data transfer using SWRDT (Stop-and-Wait Reliable Data Transfer) protocol.

## Lab 4 Overview

In this lab, I implemented a reliable data transfer protocol using the Stop-and-Wait Reliable Data Transfer (SWRDT) method. I wrote Sender and Receiver programs that communicate over the network, ensuring each message is acknowledged before sending the next. The SWRDT class handles segment creation, corruption checking, retransmissions, and sequencing to guarantee reliable delivery.