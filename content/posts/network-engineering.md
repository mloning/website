---
title: "Network engineering"
date: 2025-07-24T23:07:58+02:00
last_modified: .Lastmod
draft: false
---

## Intro

I recently had to think more about network engineering.
Here are my notes from reading [Beej's Guide to Network Programming] and [Computer Networking: A Top-Down Approach].

[Beej's Guide to Network Programming]: https://beej.us/guide/bgnet/
[Computer Networking: A Top-Down Approach]: https://gaia.cs.umass.edu/kurose_ross/

## Overview

Five-layer version of [Open System Interconnection] (OSI) model:

| Layer         | Protocol Data Unit (PDU) | Function                                                                                                                              | Diagnostic tools                          |
| ------------- | ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------- |
| 5 Application | Data                     | High-level protocols such as for continuous data exchange, resource sharing, or remote file access (e.g. HTTP, SMTP, LDAP, DNS)       | Loggers, debuggers                        |
| 4 Transport   | Segment                  | Reliable transmission of data segments between nodes, including segmentation, acknowledgement, and multiplexing (e.g. TCP, UDP, ICMP) | `netstat`, `nc` (netcat), `tcpdump`       |
| 3 Network     | Packet, Datagram         | Multi-node network communication, including addressing, routing, and traffic control (IPv4, IPv6, ICMP)                               | `ifconfig`, `route`, `ping`, `traceroute` |
| 2 Data link   | Frame                    | Transmission of data frames between two nodes connected by a physical layer (e.g. Ethernet, WiFi)                                     | `arp`, `ndp`, `tcpdump`                   |
| 1 Physical    | Bit, Symbol              | Transmission and reception of raw streams over a physical medium (e.g. copper/fibre wires, WiFi/radio waves)                          | Hardware status lights, `ifconfig`        |

Level 5 can be broken down further, but for a high-level understanding, the differences are not critical; they all concern the application.

Like a postal system, each layer passes its message (payload) down to the next layer, which wraps it in its own envelope, adding its own layer-specific information (headers) (see [encapsulation]).
At reception, the reverse happens.
Starting from the physical layer, each layer unwraps the message using the headers and passes it up to the next layer (de-encapsulation).
Each layer only acts on its layer-specific headers, leaving the rest untouched.
In practice, encapsulation and de-encapsulation is more complex because a message may be split up into multiple segments, which are then split up into multiple datagrams.

Most complexity is designed to be in the network-edge devices (end systems), including the application and transport layer.
Network-core devices, including everything from the network layer and below, are designed to be simple (complexity on edges).

Upper layers are constrained by services provided by lower layers (e.g. physical limitations like bandwith or transmission delay), but can build services on top to remedy lower-level limitations (e.g. TCP provides reliable data transfer on the transport layer even with IPv4 as an unreliable network layer protocol).

[Open System Interconnection]: https://en.wikipedia.org/wiki/OSI_model
[protocol stack]: https://en.wikipedia.org/wiki/Protocol_stack
[encapsulation]: https://en.wikipedia.org/wiki/Encapsulation_(networking)

## Physical layer

### Network interface

- a device (e.g. Ethernet cards or WiFi adapters) that connect a device to a network
- each interface has a unique MAC address and can be physical (e.g. an Ethernet card) or virtual (e.g. an interface for VMs)
- a host can have multiple interfaces

### Switch

- a device that connects multiple devices within a local network, forwarding data only to the device intended to receive it
- operate at the data link layer but are part of the physical infrastructure

## Data link layer

### Local area network (LAN)

- [LAN] is a network of trusted hosts

[LAN]: https://en.wikipedia.org/wiki/Local_area_network

### Ethernet

- LAN protocol
- broadcast protocol: any frame transmitted can go to any other host in the LAN (broadcast domain)
- every network interface has a unique identifier called the media access control (MAC) address
- maximum transmission unit (MTU), typically 1.5 Kb including headers, e.g. for a UDP datagram to fit into a single frame it should be smaller than 1.4 Kb
- if a frame exceeds the MTU, it may be fragmented into smaller pieces or dropped, depending on the protocol and device configuration, fragmentation increases the overhead
- [Address Resolution Protocol] (ARP): mapping MAC addresses to IP addresses in LAN, used when a device wants to communicate with another device on the same LAN and only knows its IP

[Address Resolution Protocol]: https://en.wikipedia.org/wiki/Address_Resolution_Protocol

### Virtual LAN (VLAN)

- a VLAN is a logical sub-group within a LAN that groups together devices as if they were on the same physical network
- all hosts on the same VLAN can see each other
- virtual LANs allow to separate LANs into multiple segments
- adds extra tag to Ethernet frames indicating the VLAN they belong to
- separate IP configuration
- set up by network engineers on switches
- useful for isolating network traffic for security (e.g. separating guest WiFi from internal company network)

## Network layer

- logical communication between network hosts

### Internet Protocol (IP)

- unreliable, best-effort protocol
  - no packet delivery guarantee
  - no in-order delivery
  - potential packet loss
  - potential packet error (corruption)
- every network host has at least one IP address

### Router

- a device that converts one physical layer into another, e.g. home Ethernet to internet service provider (ISP) fibre cable
- send traffic from one IP subset to another
- default gateway for sending traffic to hosts outside LAN, e.g. when your host wants to reach hosts on the internet, it sends traffic to the router’s IP

### IPv4

- 32-bit address, consisting of 4 dot-separated groups of a single byte (i.e. 3 decimals ranging from 0 - 255), e.g. `203.0.113.84`, omitting leading zeros, allowing a total of 2^32 distinct addresses from `0.0.0.0` to `255.255.255.255` (represented as all ones in binary)
- dynamic host configuration protocol (DHCP) automatically assigns IP addresses to devices on a network
- to connect a host to a network, it needs a valid IP address and a subnet mask
- subnet mask example: `255.255.255.0` means the first three numbers identify the network, and the last number identifies the host within that network (e.g. `192.168.1.42` is host `42` on network `192.168.1.0`)
- to communicate beyond the LAN, it needs a default gateway
- hosts can only communicate directly with hosts on the same IP subnet, otherwise they need to go through a router, e.g. if host A is on `192.168.1.x` and host B is on `192.168.2.x`, their subnet masks `255.255.255.0` mean they’re in different subnets, so their traffic must be go through a router
- to communicate with hosts on a different subnet, hosts must go through a router, even if they are on the same Ethernet
- last IP address in a subnet is reserved for broadcasting (i.e. `255.255.255.255`)
- every host has a logical loopback interface with IP address `127.0.0.1` (`localhost`), e.g. used for testing network software locally

Monitoring and diagnostics:

- `ipconfig getifaddr en0` to see your IP address for the `en0` network interface

### Private IP addresses

- 3 subnets reserved for private networks, cannot be used on the public internet:
  - `10.0.0.0/8`
  - `172.16.0.0/12`
  - `192.168.0.0/16`

### Network Address Translation (NAT) and Server Name Indication (SNI)

- publicly available IPv4 addresses are exhausted and IPv6 has not been fully adapted
- NAT allows multiple devices on a private network to share a single public IP address on the internet, and to hide internal network topologies
- the NAT device (usually a router) rewrites the source IP address and port of outgoing packets to its own public IP and keeps track of the mapping, so responses can be sent back to the correct device, e.g. at home your laptop (`192.168.0.2`) and phone (`192.168.0.3`) both connect to the internet through your router which uses NAT to translate their private IPs to its public IP (e.g. `203.0.113.5`), so websites only see requests coming from the router’s public address.
- SNI lets a client tell the server which host it is trying to reach during the TLS handshake, allowing multiple TLS-secured domains to share an IP address

### Proxies and firewalls

- proxy accepts requests for internet resources on behalf of a client
- firewalls usually involve some combination of proxy and NAT

### IPv6

- not enough available public addresses under IPv4
- 128-bit address, consisting of 8 colon-separated groups of 4 hexadecimal characters, omitting leading zeros (e.g. `2001:0db8:85a3:0000:0000:8a2e:0370:7334` or shortened to `2001:db8:85a3::8a2e:370:7334`)
- uses neighbor discovery (ND) instead of ARP
- ND is a set of protocols used in IPv6 to discover other devices on the same network, determine their link-layer addresses, find routers, and automatically configure addresses
- `::1` (`localhost`) for logical loopback interface (equivalent to `127.0.0.1` in IPv4)

### Internet control message protocol (ICMP)

- used for routing, network control, probing of availability and status, and error reporting, e.g. `ping` or `traceroute` (e.g. "destination unreachable")
- not used for transmitting application data

## Transport layer

- logical communication between processes (on different network hosts)
- extend host-to-host communication (network layer) to process-to-process communication (multiplexing)

### Principles for choosing transport layer protocols

- reliability (reliable data transfer)
- throughput guarantees: bandwith-sensitive vs adaptive applications
- timing guarantees (latency, transmission delay)
- security

### TCP/IP

- a single chunk of data, called a segment, is wrapped in a IPv4 or IPv6 packet for transmission which add source and destination IP address, which in turn is wrapped in a data link frame (i.e. "envelopes in envelopes")
- encompasses common protocols including:
  - Internet control message protocol (ICMP)
  - User Datagram Protocol (UDP)
  - Transmission Control Protocol (TCP), with security via [Transport Layer Security] (TLS)

[Transport Layer Security]: https://en.wikipedia.org/wiki/Transport_Layer_Security

### UDP

- connectionless: no connection is established for transmitting packets
- UDP packet is fully identified by its 2-tuple of destination IP address and port
- each packet is considered a discrete entity and has no relationship to other packets
- unreliable
  - no in-order delivery (packets may not arrive in the order they were sent)
  - potential packet loss
  - error detection using checksums, but no automatic error correction
- low overhead due to simplicity (compared to TCP)
- used when speed is more important than reliability, e.g. in application tolerant to packet loss including DNS, DHCP, voice over IP or real-time streaming (video, audio, gaming)
- UDP packets are usually filtered out at the network boundary due to security concerns (e.g. [IP address spoofing])
- Ethernet frame fragmentation can occur if UDP packets exceed the MTU, potentially leading to packet loss and application issues
- supports unicast, broadcast and [multicast] messaging

[IP address spoofing]: https://en.wikipedia.org/wiki/IP_address_spoofing
[multicast]: https://en.wikipedia.org/wiki/Multicast

### TCP

- connection-oriented: a connection is established between a sender and receiver for transmitting data
- TCP packet is fully identified by its 4-tuple of source and destination IP address and port
- two-way communication (duplex connection)
- reliable ("every packet is tracked and assembled"):
  - receiver acknowledges every packet it receives and checks packet integrity using checksum
  - sender re-sends packets that are not acknowledged
  - packet ordering is guaranteed at reception using packet numbering (the packet sequence may be scrambled during transmission is restored at reception)
- network congestion control, matching sender and receiver speed
- 3-way handshake to establish a connection (one SYN and ACK in each direction)
  - A: Send SYN - A (client) sends a request to initiate a connection to Host B (server), sent from a randomly assigned local port to the server's specific listening port.
  - B: Send SYN-ACK - B receives the SYN packet and, if it accepts the connection, responds to A with a packet containing both SYN and ACK flags.
  - A: Send ACK - A responds to B with an ACK packet, acknowledging the server's SYN-ACK message.
- 4-way handshake to close a connection (both client and server request and acknowledge tear down)
- used when reliability is more important than speed, e.g. in higher-level protocols:
  - SSH (Secure Shell protocol): encrypted remote login and command execution over a network
  - HTTP/HTTPS (Hypertext Transfer Protocol): transferring web pages and resources, HTTPS adds encryption for security
  - SMTP (Simple Mail Transfer Protocol): transmitting emails between servers
  - FTP (File Transfer Protocol): transferring files between network hosts
  - other data messaging and streaming protocols (e.g. ZMQ)
- security via [TLS]

### Ports

> If the subnet mask is like the street name or zip code and the IP address like the house number, then the port is like a room number.

- logical address to identify a (receiving or sending) process on a host, and to enable multiple, simultaneous connections on the same host
- 16-bit number, ranging from 0 to 65535, total of 65536 ports
- reserved port number ranges (see Internet Assigned Number Authority ([IANA]))
  - well-known ports (0 - 1023), e.g. 21 FTP, 22 SSH, 80 HTTP, 443 HTTPS (privileged, require root access)
  - other services (1024 - 49151)
  - dynamically assigned ports for user applications/connections (49152 - 65535)
- every connection (or packet) goes from a source address (both IP and port) to a destination address
- source and destination address uniquely identify connections

Monitoring and diagnostics:

- `netstat -n -a` (disable DNS lookup, filter active ports)
- `lsof -n -i` (disable DNS lookup, filter network ports)

[IANA]: https://en.wikipedia.org/wiki/Internet_Assigned_Numbers_Authority

## Application layer

### Network application design

#### Client-server

- Client: host process initiating the communication
- Server: host process waiting to begin communication with a client

Server is

- always on
- fixed IP known to the client(s)
- no client-to-client communication

For example, HTTP web servers.

#### Peer-to-peer (P2P)

- intermittently connected hosts
- no central server with fixed IP, peers discover and connect to each other
- direct client-to-client communication

For example, [BitTorrent].

[BitTorrent]: https://en.wikipedia.org/wiki/BitTorrent

### Sockets

- software interface between application and transport layer
- virtual, low-level programming abstraction representing an instance of a communication endpoint defined by a domain (e.g. `AF_INET` for IPv4), IP address, port number, and transport protocol (e.g. `SOCK_DGRAM` for UDP)
- defined by the [socket API] (e.g. `socket()`, `connect()`, `listen()`, `accept()`, `send()`, `receive()`)
- used to implement higher-level protocols (e.g. TCP or UDP)
- exposed in higher-level languages, e.g. see [Python socket guide]
- a process can open multiple sockets
- a socket can accept multiple connections (as long as they are unique in terms of source and destination IP address and port number)
- sockets are non-competing consumers of broadcast messages, when creating multiple socket instances on the same host and port number, each socket will receive a copy of the broadcast message sent to that port
- besides network sockets, Unix Domain sockets (`AF_UNIX` or `AF_LOCAL`) are used for inter-process communication using the file system, bypassing the network stack

[Python socket guide]: https://docs.python.org/3.13/howto/sockets.html
[socket API]: https://en.wikipedia.org/wiki/Berkeley_sockets

#### Bind (server) and connect (client)

- a server binds to a particular port to specify where it will listen for incoming client connections (`bind()`), making its service available for clients under a specific address; after binding, it will listen for incoming connection requests (`listen()`)
- a client connects to a server using the server's IP address and bound port (`connect()`)

### Domain name system (DNS)

- maps human-readable domain names (e.g. `www.google.com`) to an IP address
- authoritative lists, recursive by zone, cached (changes take time to propagate)
- local `/etc/hosts` file
- types of records
  - `A`: maps a domain name to an IP address
  - `CNAME`: maps a domain name to an alias domain name
  - `PTR`: maps an IP address to a domain name (reverse of an `A` record)
- usually uses UDP

Monitoring and diagnostics:

- `host <name>`
- `dig`

### Hypertext Transfer Protocol (HTTP)

- based on TCP
- stateless: no persistent information about clients, but use of cookies to identify returning clients
- persistent (default) or non-persistent connections

### MPEG-DASH

- adaptive streaming over HTTP

### QUIC-HTTP/2

- TODO

### Content Distribution Network (CDN)

- TODO

## Security

- put malware into a host
- disrupt servers and network infrastructure (denial of service, or distributed denial of service attacks)
- sniff packets
- IP spoofing

## Monitoring, diagnostics and debugging

### Packet sniffing

- capture and analyze network packets as they are transmitted across a network
- used for troubleshooting connectivity, analysing traffic and detecting anomalies

#### `tcpdump` usage

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

Alternatively, use `Wireshark`.

### Creating traffic

- read and send packets using TCP or UDP
- useful for testing open ports and simulating network services

`nc` (netcat) usage:

- `nc <ip> <port>` connect to server (client mode)
- `nc -l <port> > out.txt` bind to port (server mode) and write received data into file
- `echo "Hello, Netcat" | nc <ip> <port>` to send to destination `<ip>` and `<port>`
- `nc -u <ip> <port>` for UDP

### Tracking traffic across the network

- `traceroute <host>`
- `-n` to disable DNS lookup

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
- `traceroute`, or `mtr` (My Traceroute) - show route that traffic takes between hosts
- `host`
- `dig`
- `drill`
- `nmap` - port scanning, sends TCP SYN requests to find ports with listening processes

### Linux

Many of the above macOS tools are also available on Linux.

- `ip`
- `ethtool`

## Resources

- [Beej's Guide to Network Programming] (intro level)
- [Computer Networking: A Top-Down Approach] by James Kurose and Keith Ross (standard textbook)
- Networking for System Administrators by Michael Lucas (intro level)
- TCP/IP Illustrated: The Protocols, Volume 1 (classic text), or The Illustrated Network: How TCP/IP Works in a Modern Network (modern adaptation)
- CS 144: Introduction to Computer Networking ([current course](https://cs144.github.io/), [website](https://online.stanford.edu/courses/cs144-introduction-computer-networking))

For more recommendations, see this [HackerNews thread](https://news.ycombinator.com/item?id=38918418).
