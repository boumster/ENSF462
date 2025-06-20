# ENSF462 Lab 5

Lab 5 for ENSF 462 works on routing algorithm implementation.

## Routing Algorithm

In this lab, I implemented a link-state routing protocol where each router exchanges its link-state information with neighbors and computes the shortest paths using Dijkstra's algorithm. The router reads its configuration, sends and receives link-state updates, and periodically updates its forwarding table based on the current network topology.