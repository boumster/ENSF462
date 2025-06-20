# ENSF462 Lab 2

Lab 2 for ENSF 462 was a focus on a simple Web Server and a UDP Pinger.

## Web Server

The web server was a simple implementation that continued to build on the concept of socket programming with TCP connections. The web server receives an HTTP request for a requested file and retrieves the file from the system.

## UDP Pinger

In this, the UDPPingerServer was provided, the client sends 10 pings to the server and the server responds with the time it took to receive the ping. The client then calculates the round trip time and displays it. Since UDP is an unreliable protocol, the client will also display if any pings were lost.