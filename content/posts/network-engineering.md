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

### Data link switches

- link-layer devices forwarding packets based on link-layer information

### Local area network (LAN)

- [LAN] is a network of trusted hosts

[LAN]: https://en.wikipedia.org/wiki/Local_area_network

### Ethernet

- LAN protocol
- broadcast protocol: any frame transmitted can go to any other host in the LAN (broadcast domain)
- every network interface has a unique identifier called the media access control (MAC) address
- maximum transmission unit (MTU), typically 1.5 Kb including headers
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
- network management
  - control vs data plane
  - destination-based vs generalized forwarding
  - software defined networking (SDN)
- network devices (e.g. router)
  - "match-plus-action" pattern (e.g. router matching a packet's destination IP address and forwarding it along the right path)

### Control vs data plane

- control plane
  - coordinate end-to-end routing, based on routing protocols
  - compute forwarding tables using routing algorithms to determine optimal routing paths
  - implemented in softare
  - network-wide process
- data plane
  - pre-router packet forwarding from (physical) input links to output links
  - using forwarding tables provided by control plane
  - implemented in hardware
  - local to each router

### Router

- network-layer device using network-layer information to forward packets, compare with link-layer switches
- a device that converts one physical layer into another, e.g. home Ethernet to internet service provider (ISP) fibre cable
- send traffic from one IP subset to another
- default gateway for sending traffic to hosts outside LAN, e.g. when your host wants to reach hosts on the internet, it sends traffic to the router’s IP

#### Components

- Physical input port
- Switching fabric
- Physical output port
- routing processor (control-plane functions, e.g. router client for communicating with central control-plane server, or computing per-router forwarding tables)
- implemented in hardware (operating on nanoseconds scale), e.g. assuming 100 Gbps throughput, the router only has 5.12 nanoseconds to process a 64-bytes IP datagram before the next one arrives
- physical input/output ports are not to be confused with process-related port described as part of the transport layer

#### Input port processing (destination-based forwarding)

- selecting packet from input queue
- physical and link-layer functions (de-encapsulation)
- look up output port in forwarding table based on destination IP address, where the forwarding table is computed locally in the router using the router processor, or received from a remote central controller
  - prefix matching of destination IP address (longest-prefix matching rule)
  - look up performed in hardware, e.g. Ternary [Content Addressable Memory](https://en.wikipedia.org/wiki/Content-addressable_memory) (TCAM)

#### Switching

- connecting input and output ports
- forward packets from input port to output port
- switching methods (via memory, bus, interconnected network)

#### Output port processing

- selecting packets from output queue for transmission (scheduling)
- physical and link-layer functions (encapsulation)

#### Queuing

- queuing occurs at input and output ports
- packet loss will occur as queues exhaust router memory
- input queuing means fabric switching not fast enough (head-of-line blocking)
- output queuing means transmission rate not fast enough
- queue management protocols
  - drop arriving packets if queue is full ("drop tail")
  - active queue management algorithms (e.g. Random Early Detection (RED), or [Explicit Congestion Notification](https://en.wikipedia.org/wiki/Explicit_Congestion_Notification) marking packet headers for TCP congestion control)
- buffer sizing problem to find optimal buffer size (e.g. RFC 3439)
  - larger buffer means less packet loss but longer delays
- selecting packets from queue (scheduling)
  - "first in, first out" (FIFO)
  - priority queuing: categorizing packets according to priority depending on purpose identified by source and destination IP address and port, keeping separate FIFO queues for each category; mechanism to give certain companies priority access (jeopardizing net neutrality)
  - weighted-fair queuing (WFQ) based on priority classes (round robin)

### Internet Protocol (IP)

- unreliable, "best-effort" protocol
  - potential packet loss (no delivery guarantee)
  - no guaranteed in-order delivery
  - potential packet error (corruption)
  - no bandwith guarantee
  - no guaranteed (maximum) end-to-end delay for packet delivery
- every network host has at least one IP address

#### Monitoring and diagnostics

- `ipconfig getifaddr en0` to see your IP address for the `en0` network interface

### IPv4

- IP address format
  - 32-bit address
  - dotted-decimal notation, consisting of 4 dot-separated groups of a single byte (i.e. 3 decimals ranging from 0 - 255), e.g. `203.0.113.84`, omitting leading zeros
  - allowing a total of 2^32 distinct addresses from `0.0.0.0` to `255.255.255.255` (represented as all ones in binary)

#### Datagram

- version, e.g. 4 or 6
- header length (to handle variable number of options)
- type of service (TOS), e.g. real-time application traffic (for prioritization)
- datagram length (headers and payload)
- identifier, flags, fragmentation offset (IPv6 no longer allows for fragmentation)
- time-to-live (TTL), decreased by 1 each time the datagram is processed by a router to avoid ever-living packets due to routing loops
- protocol, e.g. 6 (TCP) or 17 (UDP), connecting network layer with transport layer (similar to how a port number connects the transport layer with the application layer)
- header checksum, used to detect errors, routers drop erroneous datagrams using error detection algorithms (RFC 1071), repeated error detection at both transport and network layer
- source and destination IP address, destination IP address often determined by DNS lookup
- options (removed in IPv6 for performance reasons)
- payload, e.g. transport-layer UDP/TCP segment

total of 20 bytes IPv4 headers + 20 bytes TCP headers

### Addresing

- to connect a host to a network, it needs a valid IP address and a subnet mask
- technically, an IP address is associated with a network interface rather than a host (or router) containing that interface, where a network interface is the boundary between the host and the physical link
- each interface on every device (e.g. host, router) in the global internet must have an IP address that is globally unique
- to communicate beyond the LAN, a host needs a default gateway
- hosts can only communicate directly with hosts on the same IP subnet, otherwise they need to go through a router, e.g. if host A is on `192.168.1.x` and host B is on `192.168.2.x`, their subnet masks `255.255.255.0` mean they’re in different subnets, so their traffic must be go through a router
- to communicate with hosts on a different subnet, hosts must go through a router, even if they are on the same Ethernet
- last IP address in a subnet is reserved for broadcasting (i.e. `255.255.255.255`), a message sent to the broadcast address is delivered to all hosts on the same subnet
- every host has a logical loopback interface with IP address `127.0.0.1` (`localhost`), e.g. used for testing network software locally
- classful addressing
  - `a.b.c.d/x` (32-bit) where `x` can be 8 (class A), 16 (class B) or 24 (class C) but inefficient allocation for smaller organisations
    indicates the number of bits in the network prefix, with the remaining bits indicating the device inside the organisation
  - subnet mask addressing, a subnet mask `255.255.255.0` (24-bits) means the first three numbers identify the network (network prefix), and the last number identifies the device inside that network (e.g. `192.168.1.42` is host `42` on network `192.168.1.0`)
- Classless Interdomain Routing (CIDR) generalizes subnet addressing
  - `a.b.c.d/x` (32-bit) where `x` indicates the number of bits in the network prefix, with the remaining bits indicating the device inside the organisation
  - organisations are typically assigned block of continuous IP addresses, i.e. a common network prefix
  - routers outside of organisation only consider leading `x` bits of address (network prefix) during routing, reducing the size of the routing tables since a single entry for an entire organisation will be sufficient

### IP address assignment

- Internet Cooperation for Assigned Names and Numbers (ICANN) responsible for allocating blocks of IP addresses and managing DNS root servers
- assigned block of IP addresses configured into router

### Dynamic Host Configuration Protocol (DHCP)

- client-server protocol
- automatically assigns temporary IP addresses to devices on a network, or same address for returning devices
- mechanism to renew lease
- cannot maintain IP address when connecting to a new subnet, e.g. cannot maintain a TCP connection in mobile applications

protocol flow for assigning an IP address to a new host:

1. a new host send a UDP broadcast discovery message to `255.255.255.255:67` (port `67` is reserved for DHCP)
2. server(s) respond with UDP broadcast offer message, containing proposed address, lease time and ID of the discovery message
3. client sends request message choosing from received offer(s)
4. server responds with acknowledgement

### Private IP addresses

- 3 subnets reserved for private networks, cannot be used on the public internet:
  - `10.0.0.0/8`
  - `172.16.0.0/12`
  - `192.168.0.0/16`

### Network Address Translation (NAT) and Server Name Indication (SNI)

- publicly available IPv4 addresses are exhausted and IPv6 has not been fully adapted
- NAT allows multiple devices on a private network to share a single public IP address on the internet, and to hide internal network topologies
- private addresses in LAN allocated by DHCP server in router
- single public WAN (wide-arean network) IP address allocated by Internet Service Provider DHCP server to gateway router
- the NAT device (e.g. a router) rewrites the source IP address and port of outgoing packets to its own public IP and keeps track of the mapping between LAN-side and WAN-side source IP address and port, so responses can be sent back to the correct device, e.g. at home your laptop (`192.168.0.2`) and phone (`192.168.0.3`) both connect to the internet through your router which uses NAT to translate their private IPs to its public IP (e.g. `203.0.113.5`), so websites only see requests coming from the router’s public address.
- 16-bit port number means ca 60K simultaneous entries in NAT table for a single WAN-side IP address
- NAT transversal
- SNI lets a client tell the server which host it is trying to reach during the TLS handshake, allowing multiple TLS-secured domains to share an IP address

### Proxies and firewalls

- proxy accepts requests for internet resources on behalf of a client
- firewalls usually involve some combination of proxy and NAT

### IPv6

- not enough available public addresses under IPv4
- IP address format
  - 128-bit address, consisting of 8 colon-separated groups of 4 hexadecimal characters, omitting leading zeros (e.g. `2001:0db8:85a3:0000:0000:8a2e:0370:7334` or shortened to `2001:db8:85a3::8a2e:370:7334`)
- uses neighbor discovery (ND) instead of ARP
- ND is a set of protocols used in IPv6 to discover other devices on the same network, determine their link-layer addresses, find routers, and automatically configure addresses
- `::1` (`localhost`) for logical loopback interface (equivalent to `127.0.0.1` in IPv4)
- anycast address
- flow labelling (e.g. for prioritizing realtime streaming)
- unlike IPv4, IPv6 does not allow for fragmentation and reassembly at intermediate routers ("Packet too big" ICMP error message)
- checksum error checking removed since it was redundant with transport-layer checking (e.g. UDP, TCP)
- transition from IPv4 to IPv6 via tunneling, sending IPv6 datagram in payload of IPv4 datagram (RFC 4213)

#### Datagram

fields:

- version (4 bit)
- traffic class (8 bit)
- flow label (20 bit)
- payload length (16 bit)
- next header (like protocol in IPv4)
- hop limit (decremented by 1 by each router that forward the datagram)
- source and destination IPv6 address
- payload

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

- thin wrapper around Internet Protocol (IP)
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
- also see [QUIC] protocol based on UDP
- when a host receives an unexpected packet, i.e. when no receiver or server is running on the destination port, the host replies with a special packet (RST flat for TCP, ICMP datagram for UDP)

[QUIC]: https://en.wikipedia.org/wiki/QUIC

#### Segment structure

- 5 fields: 4 headers with 2 bytes each (8 bytes in total) + payload
  - source port (for sending unicast replies)
  - destination port (multiplexing)
  - length (in bytes, headers and payload)
  - checksum (for end-to-end transmission error checking for corruption during transmission by noise or while being stored/queued in router)
  - payload (application-layer data)
- maximum segment size (MSS) to fit into a single Ethernet frame: 1480 (payload) + 20 (headers) = 1500 bytes

[IP address spoofing]: https://en.wikipedia.org/wiki/IP_address_spoofing
[multicast]: https://en.wikipedia.org/wiki/Multicast

### Reliable data transfer

Essential components include:

- error detection (e.g. checksum)
- receiver feedback to sender (e.g. acknowledgement message (ACK) for received packets)
- re-transmission of lost packets (go-back-N or selective repeat)

which require the following features:

- packet sequence numbers
- timers (e.g. timeouts for ACK reception before re-transmission)
- pipelining (sending multiple packets) (compare with inefficient stop-and-wait technique, waiting for ACK before sending next packet)
- maximum assumed lifetime of packet in transit before re-using sequence number to avoid duplicate sequence numbers

### TCP

- connection-oriented: a logical connection is established between a sender and receiver for transmitting data
  - logical connection maintained by state in endpoints (stateful)
  - simultaneous two-way connection (duplex)
  - single sender, single receiver (point-to-point)
- TCP packet is fully identified by its 4-tuple of source and destination IP address and port
- reliable ("every packet is tracked and assembled"):
  - receiver acknowledges every packet it receives and checks packet integrity using checksum
  - sender re-sends packets that are not acknowledged
  - packet ordering is guaranteed at reception using packet numbering (the packet sequence may be scrambled during transmission is restored at reception)
- network congestion control, matching sender and receiver speed to preempt router queue overflow and packet drops/re-transmission
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

#### Segment structure

- fields include headers (usually 40 bytes) and payload, extending fields used in UDP
  - source port (2 bytes)
  - destination port (2 bytes)
  - checksum (2 bytes)
  - sequence numbers (4 bytes, max 2^32 unique sequence numbers, reliability/re-transmission)
  - receive window (2 bytes, flow/congestion control)
  - header length (4 bytes, in bytes)
  - acknowledgement number (4 bytes, reliability)
  - options field (usually empty)
  - flat field (e.g. ACK, SYN)
- maximum segment size (MSS) to fit into a single Ethernet frame: 1460 (payload) + 40 (headers) = 1500 bytes

### Network congestion control

Costs of congested networks

- large queuing delays in routers
- re-transmission for dropped packets due to router queue overflow
- unnecessary re-transmissions due to timeouts for acknowledgement messages (ACK)
- wasted transmission capacity in previous links/router when a packet is dropped at a later stage

Control strategies

- end-to-end congestion control (e.g. TCP using timeouts as congestion indicators and optimization algorithms for adjusting transmission speed)
- network-assisted congestion control, with routers provide feedback regarding congestion state, even before packet loss occurs
  - direct feedback to sender
  - mark packets in router, which are sent on to the receiver, which then informs the sender

### Ports

> If the subnet mask is like the street name or zip code and the IP address like the house number, then the port is like a room number.

- logical address to identify a (receiving or sending) process on a host, and to enable multiple, simultaneous connections on the same host (multiplexing)
- 16-bit number, ranging from 0 to 65535, total of 65536 ports
- reserved port number ranges (see Internet Assigned Number Authority ([IANA]))
  - well-known ports (0 - 1023), e.g. 21 FTP, 22 SSH, 80 HTTP, 443 HTTPS (privileged, require root access)
  - other services (1024 - 49151)
  - dynamically assigned (ephemeral) ports for user applications/connections (49152 - 65535)
- every connection (or packet) goes from a source address (both IP and port) to a destination address
- source and destination address uniquely identify connections
- connects transport layer with application layer

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

### Quick UDP Internet Connections (QUIC)-HTTP/2

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

- `ss` - modern version of `netstat` for displaying socket statistics
- `ip`
- `ethtool`

## Resources

- [Beej's Guide to Network Programming] (intro level)
- [Computer Networking: A Top-Down Approach] by James Kurose and Keith Ross (standard textbook)
- Networking for System Administrators by Michael Lucas (intro level)
- TCP/IP Illustrated: The Protocols, Volume 1 (classic text), or The Illustrated Network: How TCP/IP Works in a Modern Network (modern adaptation)
- CS 144: Introduction to Computer Networking ([current course](https://cs144.github.io/), [website](https://online.stanford.edu/courses/cs144-introduction-computer-networking))

For more recommendations, see this [HackerNews thread](https://news.ycombinator.com/item?id=38918418).
