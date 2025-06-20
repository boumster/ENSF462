
# ENSF462 Lab 1

Lab 1 for ENSF 462, focuses on using Wireshark and Socket programming in Python.

## Wireshark

Wireshark was used to make simple packet captures and observations. We used wireshark to analyze the HTTP call that was made from our computer to the website `http://gaia.cs.umass.edu/wireshark-labs/INTRO-wireshark-file1.html`

## Socket Programming

Created a simple chat program relying on TCP as the transport protocol. The program consists of a server and a client. The server listens for incoming connections and the client connects to the server. Once connected, the client can send messages to the server, which will then print them out.