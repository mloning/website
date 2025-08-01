---
title: "Network Engineering"
date: 2025-07-24T23:07:58+02:00
last_modified: .Lastmod
draft: true
---

## Overview

[Open System Interconnection] (OSI) layer model:

| Layer            | Protocol Data Unit (PDU) | Function                                                                                                                                            | Diagnostic tools                          |
| ---------------- | ------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------- |
| **Host layers**  |                          |                                                                                                                                                     |                                           |
| 7 Application    | Data                     | High-level protocols such as for resource sharing or remote file access (e.g. HTTP, SMTP, LDAP, DNS)                                                | logging, debugging                        |
| 6 Presentation   | Data                     | Translation of data between a networking service and an application; including character encoding, data compression, and encryption/decryption      | logging, debugging                        |
| 5 Session        | Data                     | Managing communication sessions, i.e. continuous information exchange in the form of multiple back-and-forth transmissions between two nodes        | logging, debugging                        |
| 4 Transport      | Segment                  | Reliable transmission of data segments between points on a network, including segmentation, acknowledgement, and multiplexing (e.g. TCP, UDP, ICMP) | `netstat`, `nc` (netcat), `tcpdump`       |
| **Media layers** |                          |                                                                                                                                                     |                                           |
| 3 Network        | Packet, Datagram         | Multi-node network communication, including addressing, routing, and traffic control (IPv4, IPv6, ICMP)                                             | `ifconfig`, `route`, `ping`, `traceroute` |
| 2 Data link      | Frame                    | Transmission of data frames between two nodes connected by a physical layer (e.g. Ethernet)                                                         | `arp`, `ndp`, `tcpdump`                   |
| 1 Physical       | Bit, Symbol              | Transmission and reception of raw streams over a physical medium (e.g. wires, WiFi/radio waves)                                                     | Link status, hardware lights, `ifconfig`  |

For a high-level understanding, the differences between layers 5 - 7 are not critical, they all concern the application.

[Open System Interconnection]: https://en.wikipedia.org/wiki/OSI_model

## Physical layer (hardware)

- TODO network interfaces
- TODO switches
- network address translation (NAT) devices

### Router

- convert one physical layer into another, e.g. home Ethernet to internet service provider (ISP) fibre cable
- send traffic from one IP subset to another
- default gateway for sending traffic to hosts outside LAN

## Data link layer

### Ethernet

- [Local area network] (LAN) protocol
- broadcast protocol: any frame transmitted can go to any other host in the LAN (broadcast domain)
- every device has unique identifier: media access control (MAC) address
- maximum transmission unit (MTU)
- [Address Resolution Protocol] (ARP): mapping physical machine MAC addresses to IP addresses in LAN

[Local area network]: https://en.wikipedia.org/wiki/Local_area_network
[Address Resolution Protocol]: https://en.wikipedia.org/wiki/Address_Resolution_Protocol

### Virtual LAN (VLAN)

- all hosts on LAN can see each other
- a virtual LAN is a logical sub-group within a LAN that group together devices as if they were on the same physical network
- virtual LANs allow to separate LANs into multiple segments
- adds extra tag to Ethernet frames indicating the VLAN they belong to
- separate IP configuration
- set up by network engineers on switches

## Network layer

### IPv4

- 32-bit address, consisting of 4 dot-separated groups of 3 decimal numbers (e.g. `203.0.113.84`), omitting leading zeros, allowing a total of 2^32 distinct addresses from `0.0.0.0` to `255.255.255.255` (represented as all ones in binary)
- dynamic host configuration protocol (DHCP)
- to connect a host to a network, it needs a valid IP address and a subnet mask
- to communicate beyond the LAN, it needs a default gateway
- hosts can only communicate directly with hosts on the same IP subnet
- to communicate with hosts on a different subnet, hosts must go through a router, even if they are on the same Ethernet
- last IP address in a subnet is reserved for broadcasting (i.e. `255.255.255.255`)
- every host has a logical loopback interface (not hardware) with IP address `127.0.0.1` (`localhost`)

#### Private IP addresses

- 3 subnets reserved for private networks, cannot be used on the public internet:
  - `10.0.0.0/8`
  - `172.16.0.0/12`
  - `192.168.0.0/16`

- proxy accepts requests for internet resources on behalf of a client
- firewalls usually involve some combination of proxy and NAT

### IPv6

- 128-bit address, consisting of 8 colon-separated groups of 4 hexadecimal characters, omitting leading zeros (e.g. `2001:0db8:85a3:0000:0000:8a2e:0370:7334` or shortened to `2001:db8:85a3::8a2e:370:7334`)
- uses neighbor discovery (ND) instead of ARP
- `::1` (`localhost`) for logical loopback interface

### Internet control message protocol (ICMP)

- used for routing and probing availability and status (e.g. `ping`)

## Transport layer

### TCP/IP

- encompasses protocols like user datagram protocol (UDP), transmission control protocol (TCP), and ICMP
- a single chunk of data, called a segment, is wrapped in a IPv4 or IPv6 packet for transmission
- IPv4/IPv6 packet add source and destination IP address, which then in turn is wrapped in a data link frame

#### UDP

- connectionless, no connection is established for transmitting packets
- each packet is considered a discrete entity and has no relationship to other packets
- unreliable
  - no packet ordering
  - no packet loss or error detection or correction
- low overhead due to simplicity (compare TCP)
- UDP packets are usually filtered out at the network boundary due to security concerns (e.g. [IP address spoofing])
- used in applications where speed is more important than reliability, e.g. voice over IP or real-time audio/video streaming
- supports unicast, broadcast and [multicast] messaging

[IP address spoofing]: https://en.wikipedia.org/wiki/IP_address_spoofing
[multicast]: https://en.wikipedia.org/wiki/Multicast

#### TCP

- connection-oriented, a connection is established between a sender and receiver for transmitting data
- reliable ("every packet is tracked and assembled"):
  - receiver acknowledges every packet it receives
  - sender re-sends packets that are not acknowledged
  - packet ordering is guaranteed at reception using packet numbering (packets may be scrambled during transmission but are checked for integrity at reception)
- controls data flow
- used where reliability is more important than speed, e.g. email (SMTP), web browing (HTTP/HTTPS) and file transfer (FTP)
- 3-way handshake to establish a connection (one SYN and ACK in each direction)
  - A: Send SYN - A (client) sends a request to initiate a connection to Host B (server), sent from a randomly assigned local port to the server's specific listening port.
  - B: Send SYN-ACK - B receives the SYN packet and, if it accepts the connection, responds to A with a packet containing both SYN and ACK flags.
  - A: Send ACK - A responds to B with an ACK packet, acknowledging the server's SYN-ACK message.
- 4-way handshake to close a connection (both client and server request and acknowledge tear down)

#### Other protocols

- HTTP/HTTPS
- SMTP
- FTP

### Ports

- logical address to identify multiple, simultaneuous connections on the same host
- 16-bit number, ranging from 0 to 65535, total of 65536 ports
- reserved port number ranges (see Internet Assigned Number Authority (IANA))
  - widely used services (0 - 1023), e.g. 21 FTP, 22 SSH, 80 HTTP, 443 HTTPS (privileged, require root access)
  - other services (1024 - 49151)
  - ephemeral ports for connections (49152 - 65535)
- every connection (or packet) goes from a source address (IP and port) to a destination address (IP and port); source and destination address uniquely identify connections
- server _binds_ to a port

monitoring and diagnostics:

- `netstat -n -a` (disable DNS lookup, filter active ports)
- `lsof -n -i` (disable DNS lookup, filter network ports)

### Sockets

- virtual, low-level programming abstraction representing an instance of a communication endpoint defined by an domain (e.g. `AF_INET` for IPv4), IP address, port number, and transport protocol (e.g. `SOCK_DGRAM` for UDP)
- defined by socket API (e.g. `socket()`, `connect()`, `send()`, `receive()`)
- exposed in high-level languages, e.g. see [Python socket guide]
- a process can open multiple sockets
- a socket can accept multiple connections (as long as they are unique in terms of source and destination IP address and port number)
- sockets are non-competing consumers, when creating multiple socket instances on the same host and port number, each socket will receive a copy of the message sent to that port
- besides network sockets, Unix Domain sockets (`AF_UNIX` or `AF_LOCAL`) are used for inter-process communication using the file system, bypassing the network stack

[Python socket guide]: https://docs.python.org/3.13/howto/sockets.html

### Domain name system (DNS)

- maps human-readable domain names (e.g. `www.mloning.com`) to an IP address
- authorative lists, recursive by zone, cached (changes take time to propagate)
- local `/etc/hosts` file
- types of records
  - A: maps a domain name to an IP address
  - CNAME: maps a domain name to an alias domain name
  - PTR: maps an IP address to a domain name (reverse of an A record)

monitoring and diagnostics:

- `host <name>`
- `dig`

## Monitoring, diagnostics and debugging

### Packet sniffing

- capture and analyze network packets as they are transmitted across a network

`tcpdump` usage:

- `tcpdump -i eth0` to filter by interface
- `tcpdump net 192.168.1.0/24` to filter by network IP range
- `tcpdump host 192.168.1.10` to filter packets to and from host
- `tcpdump src host 192.168.1.10` to filter by source host
- `tcpdump dst host 192.168.1.10` to filter by destination host
- `tcpdump tcp` to filter by protocol
- `tcpdump port 80` to filter by port
- `tcpdump -i eth0 host 192.168.1.10 and port 80` combining filters
- `-n` to disable DNS lookup
- `-v` for verbosity
- `-w <file>.pcap` write captured packets to file for later analysis
- `-r <file>.pcap` read captured packets from file

### Creating traffic

- read and send packets using TCP or UDP

`nc` (netcat) usage:

- `nc <ip> <port>` connect to server (client mode)
- `nc -l <port> > out.txt` bind to port (server mode) and write received data into file
- `echo "Hello, Netcat" | nc <ip> <port>` to send to destination `<ip>` and `<port>`
- `nc -u <ip> <port>` for UDP

## Tools

### macOS

- `whois`
- `ifconfig`
- `arp`
- `ndp`
- `ipconfig`
- `netstat` - established connections
- `lsof` - processes and files
- `route` - where traffic is being sent
- `tcpdump` - traffic to and from server
- `Wireshark`
- `nc` (netcat) - receive and send traffic
- `traceroute` - show route that traffic takes between hosts
- `host`
- `dig`
- `drill`

### Linux

Many of the above macOS tools are also available on Linux.

- `ip`
- `ethtool`

## Resources

Books and guides

- Networking for System Administrators (intro level)
- https://beej.us/guide/bgnet/ (intro level)
- Computer Networking: A Top-Down Approach by James Kurose (standard textbook)
- TCP/IP Illustrated: The Protocols, Volume 1 (classic text)
- The Illustrated Network: How TCP/IP Works in a Modern Network (modern adaptation)

For more recommendations, see this (https://news.ycombinator.com/item?id=38918418).

Courses:

- CS 144: Introduction to Computer Networking ([current course](https://cs144.github.io/), [website](https://online.stanford.edu/courses/cs144-introduction-computer-networking))

Other resources

- Python guide https://docs.python.org/3.13/howto/sockets.html
