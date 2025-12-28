---
title: Network engineering
date: 2025-07-24T23:07:58+02:00
draft: false
---
## Intro

I recently had to think more about network engineering.
Here are my notes from reading [Beej's Guide to Network Programming] and [Computer Networking: A Top-Down Approach].

[Beej's Guide to Network Programming]: https://beej.us/guide/bgnet/
[Computer Networking: A Top-Down Approach]: https://gaia.cs.umass.edu/kurose_ross/

## Overview

Five-layer version of [Open System Interconnection] (OSI) model:

| Layer | Name        | Protocol Data Unit | Function                                                                                                                             | Diagnostic Tools                          |
| ----- | ----------- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------- |
| 5     | Application | Data               | Protocols for data exchange, resource sharing and remote file access (e.g. HTTP, SMTP, LDAP, DNS)                                    | Loggers, debuggers                        |
| 4     | Transport   | Segment            | Logical communication between processes on network hosts, including segmentation, reliability and multiplexing (e.g. TCP, UDP, ICMP) | `netstat`, `nc` (netcat), `tcpdump`       |
| 3     | Network     | Packet, Datagram   | Logical communication between network hosts, including addressing, routing and traffic control (e.g. IPv4, IPv6, ICMP)               | `ifconfig`, `route`, `ping`, `traceroute` |
| 2     | Data link   | Frame              | Transmission of data between network hosts connected by a physical layer (e.g. Ethernet, WiFi)                                       | `arp`, `ndp`, `tcpdump`                   |
| 1     | Physical    | Bit, Symbol        | Transmission of raw streams over a physical medium (e.g. copper/fibre wires, WiFi/radio waves)                                       | Hardware status lights, `ifconfig`        |

Level 5 is sometimes broken down further (7-layer model), but for a high-level understanding, the differences are not critical; they all concern the application.

Intuitively, the layers works like a postal system.
When sending a message, each layer passes its message (payload) down to the next layer, which wraps it in its own envelope, adding its own layer-specific information (headers) (see [encapsulation]).
At reception, the reverse happens.
Starting from the physical layer, each layer unwraps the message using the information in the headers and passes it up to the next layer (de-encapsulation).
Each layer only acts on its layer-specific headers, leaving the rest untouched.
In practice, encapsulation and de-encapsulation is more complex: a message may be split up into multiple segments, which in turn are split up into multiple datagrams.

The network edge consists of end systems (hosts) like computers and servers where applications run, while the network core is the mesh of routers and switches that interconnects them.
Most complexity is designed to be in the network-edge devices (end systems), including the application and transport layer (see [End-to-end Principle]).
Network-core devices, including everything from the network layer and below, are designed to be simple.

Upper layers are constrained by services provided by lower layers (e.g. physical limitations like bandwith or transmission delay), but can build services on top to remedy lower-level limitations (e.g. TCP provides reliable data transfer on the transport layer on top of the unreliable network layer IPv4 protocol).

Much of modern network engineering is defined by specific conventions adhered to by millions of networks around the world, rather than physical laws or an overarching, central design.
Conventions are primarily defined by the [Internet Engineering Task Force] (IETF) in [Request for Comments] (RFCs).

[Open System Interconnection]: https://en.wikipedia.org/wiki/OSI_model
[protocol stack]: https://en.wikipedia.org/wiki/Protocol_stack
[encapsulation]: https://en.wikipedia.org/wiki/Encapsulation_(networking)
[End-to-end Principle]: https://en.wikipedia.org/wiki/End-to-end_principle
[Internet Engineering Task Force]: https://www.ietf.org/
[Request for Comments]: https://en.wikipedia.org/wiki/Request_for_Comments

## Physical layer

While upper layers deal with logic, software and data, the physical layer is concerned with the transmission of raw bit streams over a physical medium.
It bridges the gap between the digital and physical world (electricity, light, radio waves).

### Transmission media

- Wired (guided):
  - Twisted Pair: Copper wires twisted to reduce interference (typically up to 10 Gbps)
  - Coaxial Cable: Copper core with shielding (e.g. cable TV, older Ethernet) (typically up to 10 Gbps)
  - Fiber Optics: Glass/plastic strands transmitting light; high bandwidth, low attenuation, immune to electromagnetic interference (typically up to 100 Gbps)
- Wireless (unguided):
  - Radio waves: WiFi (WiFi 6E: typically 1-2 Gbps), Bluetooth (up to 3 Mbps), Cellular (4G: up to 100 Mbps, 5G: typically 100-500 Mbps)
  - Microwaves: Line-of-sight communication
  - Infrared: Short-range

Real-world wireless transmission speed is typically lower due to interference, distance and shared bandwidth.
Wired connections offer more consistent speeds and lower latency.

### Signal encoding

- Converts digital bits into physical signals for transmission
- Encoding methods:
  - Voltage levels: Different voltage levels represent 0s and 1s (e.g. Ethernet over copper)
  - Light pulses: Presence/absence or intensity of light (e.g. fiber optics)
  - Radio frequency modulation: Amplitude, frequency or phase modulation (e.g. WiFi)

### Transmission modes

- Simplex: One-way communication (e.g. radio station -> radio)
- Half-duplex: Two-way, but one at a time (e.g. walkie-talkie, WiFi)
- Full-duplex: Two-way simultaneously (e.g. telephone, modern Ethernet)

### Devices

- Repeater: Regenerates signal to extend range
- Hub: Multi-port repeater; broadcasts data to all ports (obsolete, replaced by switches) (physical layer)
- Modem: Modulates/Demodulates signals (Digital <-> Analog)
- Network Interface Card (NIC): Hardware that connects a device to a network (e.g. Ethernet cards or WiFi adapters); operates at both physical and link layers
  - Each interface has a unique MAC address (link-layer identifier)
  - Can be physical (e.g. an Ethernet card) or virtual (e.g. an interface for VMs)

## Link layer (data link layer)

The link layer is responsible for node-to-node transfer of data across a physical link (hop-to-hop).
It ensures data moves correctly from one device to the next one in the chain.

### Key Responsibilities

- Framing: it encapsulates network-layer packets with a header (containing source/destination MAC addresses and type/length) and trailer (CRC), defining frame boundaries.
- Media Access Control (MAC): it acts as the "moderator" determining who is allowed to transmit on the cable or wireless frequency at any given moment to prevent collisions.
- Error detection: it checks the integrity of the received frame (using a CRC/Checksum) to ensure bits weren't corrupted by electrical noise.

The link layer is hop-to-hop rather than end-to-end.
It gets the data to the next device in the network, not the final destination (e.g. connecting single laptop to the nearby Ethernet switch).

Link-layer functionality is primarily implemented in hardware on the network interface card (NIC) (fast bit sending/receiving), with software managing setup, addressing assembly and communication with the network layer (encapsulation/de-encapsulation).

The link layer defines two main connection types:

- Broadcast (shared media connecting multiple hosts)
- Point-to-Point (a dedicated connection between two specific devices, like a laptop to a switch)

The link layer is also often divided into two sub-layers:

- Logical Link Control (LLC) layer: communication with the Network Layer (multiplexing)
- Media Access Control (MAC) layer: addressing and channel access control

### Devices

- Bridge: Connects two network segments (link layer)
- Switch: Connects multiple devices within a local network, forwarding data only to the device intended to receive it (link layer)

### Services

Services provided by link layer:

- Framing (encapsulation/de-encapsulation) based on link-layer protocols
- Link access (MAC protocol) to coordinate frame transmission
- Reliable data transfer depending on protocol (e.g. Ethernet provides unreliable data transfer while [PPP] can provide reliable data transfer)
- Error detection and correction due to signal attenuation or electromagnetic noise (corruption of transmitted bits)

[PPP]: https://en.wikipedia.org/wiki/Point-to-Point_Protocol

### Error detection and correction

- Error detection and correction bits (EDC)
- Challenge is to detect errors in received data D', relative to originally sent data D and EDC, given that we only have received D' and EDC', both of which may be corrupted due to in-transit bit flips
- No perfect solution, but goal is to minimize probability of undetected errors for acceptable overhead
- Forward error correction (FEC) at receiver side avoiding re-transmission and related delays
- Parity checks
  - Extra parity bit to denote whether number of 1s in payload is even or odd
  - But weak against multiple errors (cancelling each other out)
  - two-dimensional row and column parity to detect and correct errors, can correct single but not multiple errors
- Checksum methods
  - Internet checksum (RFC 1071)
  - Used in IP/TCP/UDP
  - Simple and fast compared to cyclical redundancy checks (CRC)
- Cyclical redundancy checks (CRC)
  - Polynomial codes

### Multiple access links and protocols

- Point-to-point link (single sender and receiver), e.g. HDLC or PPP protocol
- Broadcast link (multiple senders and receivers), e.g. Ethernet/LAN
- Multiple access problem
  - Coordinate transmission of frames to not send frame at the same time (to avoid frame colliding and becoming inextricably tangled together)
- Desirable properties of solutions
  - If one node transmits data, the node has full throughput rate R bps
  - If M nodes transmit data simultaneously, each node has roughly throughput rate R/M bps
- 3 categories of multiple access protocols
  - Channel partitioning
  - Random access
  - Taking turns

#### Channel partitioning protocols

- Time-division multiplexing (TDM)
- Frequency-division multiplexing (FDM)
- Code division multiple access (CDMA)

#### Random access protocols

- Carrier sense multiple access (CSMA) with collision detection (CSMA/CD), e.g. Ethernet
  - Listen for active transmission and wait for free transmission slot
  - Stop transmission if collision detected and wait for some duration before re-trying transmission
  - Random wait duration or determined by some algorithm (e.g. binary exponential backoff algorithm)

#### Taking turns protocols

- Polling protocol
- Master node coordinating turns (e.g. round robin)
- Token-passing protocol
- e.g. DOCSIS

### Link layer addressing

- Each host or router interface (network adapter) has a globally unique link-layer address in addition to its IP address
- Link-layer switches do not have link-layer address associated with their interface, they are invisible to the devices connected to it; they read the MAC address of the frame and forward it to the correct interface
- MAC address
  - 6 bytes, 2^48 possible MAC addresses
  - Hexadecimal notation, with each byte a pair of hexadecimal numbers
  - Managed by IEEE and allocated to network adapter manufacturers
  - Address fixed for adapter, no matter where the adapter is moved
  - Flat address structure unlike hierarchical IP address (network prefix vs host)
- Sending adapter inserts its MAC address into link-layer frame before transmission
- Receiving adapter may receive frames not addressed to its own MAC address, which will be discarded without passing it up to the network-layer and interrupting the host
- Last address in 6-bytes space is broadcast MAC address consisting of 48 consecutive 1s, i.e. `FF-FF-FF-FF-FF-FF`
- Link-layer addressing works independently of network-layer addressing
  - Support for arbitrary network-layer protocol, not just IP (e.g. [IPX] or [DECnet])
  - Operating without having to pass up frames to network layer and interrupt hosts

[IPX]: https://en.wikipedia.org/wiki/IPX
[DECnet]: https://en.wikipedia.org/wiki/DECnet

### Local area network (LAN)

- [LAN] is essentially a network of trusted hosts in a limited area, privately managed (e.g. a home or office); compare with wide-area network ([WAN]), a network of untrusted hosts in a large area, publicly managed (e.g. the Internet)
- Devices on the same LAN can communicate with each other directly without going through a router
- Devices can send messages to all other devices on the LAN (broadcast domain)

[LAN]: https://en.wikipedia.org/wiki/Local_area_network
[WAN]: https://en.wikipedia.org/wiki/Wide_area_network

#### Switched LAN

- Modern LANs use switches instead of hubs to improve performance (e.g. selective forwarding of frames, fewer collisions)
- Switches learn MAC addresses by observing source addresses of incoming frames and building a forwarding table
- Link-layer devices forwarding frames based on link-layer information (e.g. MAC address)
- Link-layer switches operate on link-layer frames, rather than network-layer address and routing algorithms (e.g. OSPF)

#### Ethernet

- Link-layer protocol commonly used in LANs
- Broadcast protocol: any frame transmitted can go to any other host in the LAN (broadcast domain)
- Every network interface has a unique identifier called the media access control (MAC) address
- Provides connectionless transmission service for network layer
- Unreliable data transfer as frames failing cyclical redundancy checks (CRC) are dropped silently without acknowledgements or re-transmission mechanisms (for more on reliable data transfer, see transport layer section)
- Ethernet frame, 6 fields
  - Data: IP datagram, between 46 - 1500 bytes
  - Destination MAC address (6 bytes)
  - Source MAC address (6 bytes)
  - Type, e.g. IP protocol, ARP (like protocol field in IP datagram, used for de-encapsulation) (2 bytes)
  - Cyclic redundancy check (CRC) (4 bytes)
  - Preamble (8 bytes), 7 bytes of alternating 1s and 0s for synchronization, followed by a 1-byte Start Frame Delimiter (SFD)
- Data smaller than 46 bytes is padded and "unstuffed" or decoded based on IP datagram length field
- Maximum transmission unit (MTU) refers to the maximum payload size, typically 1500 bytes for Ethernet; the total frame size including 14-byte Ethernet header and 4-byte CRC is 1518 bytes (or 1522 bytes with VLAN tag)
- If a frame exceeds the MTU, it may be fragmented into multiple frames or dropped, depending on the protocol and device configuration, fragmentation increases the overhead
- Different Ethernet flavours (e.g. 10BASE-T)

#### Virtual LAN (VLAN)

- A VLAN is a logical sub-group within a LAN that groups together devices as if they were on the same physical network
- All hosts on the same VLAN can see each other
- Virtual LANs allow to separate LANs into multiple segments
- Adds extra tag to Ethernet frames indicating the VLAN they belong to
- Separate IP configuration
- Set up by network engineers on switches
- Useful for isolating network traffic for security (e.g. separating guest WiFi from internal company network)

#### Address Resolution Protocol (ARP)

- Maps LAN network-layer IP addresses to link-layer MAC addresses (interface between link layer and network layer)
- Similar to DNS mapping global application-layer host name to network-layer IP addresses
- Used when a device wants to communicate with another device on the same LAN and only knows its IP address
- Works only for devices in the same IP subnet (ARP uses broadcast, which doesn't cross subnet boundaries)
- Each host or router has an ARP table mapping IP address to MAC address including time-to-live (TTL)
- Message protocol to update tables if table has no entry for IP address
  - Query packet with source and destination IP and MAC address sent to all hosts and routers on the same subnet via broadcast MAC address
  - Response packets if query a host's or router's MAC address matches with desired mapping

## Network layer: data plane

- Logical communication between network hosts
- Network management
  - Control vs data plane
  - Destination-based vs generalized forwarding
  - Software defined networking (SDN)
- Network devices (e.g. router)
  - "Match-plus-action" pattern (e.g. router matching a packet's destination IP address and forwarding it along the right path)

### Control vs data plane

Control plane

- Coordinate end-to-end routing, based on routing protocols
- Compute forwarding tables using routing algorithms to determine optimal routing paths
- Implemented in software
- Network-wide process

Data plane

- Pre-router packet forwarding from (physical) input links to output links
- Using forwarding tables provided by control plane
- Implemented in hardware
- Local to each router

### Router

- Network-layer device using network-layer information to forward packets, compare with link-layer switches
- Determines the path for data packets to travel across different networks based on IP address, creating a broadcast domain boundary
- Send traffic from one IP subset to another
- Default gateway for sending traffic to hosts outside LAN, e.g. when your host wants to reach hosts on the internet, it sends traffic to the router’s IP

#### Components

A router has the following components:

- Physical input port
- Switching fabric
- Physical output port
- Routing processor (control-plane functions, e.g. router client for communicating with central control-plane server, or computing per-router forwarding tables)
- Implemented in hardware (operating on nanoseconds scale), e.g. assuming 100 Gbps throughput, the router only has 5.12 nanoseconds to process a 64-bytes IP datagram before the next one arrives
- Physical input/output ports are not to be confused with process-related port described as part of the transport layer

#### Input port processing (destination-based forwarding)

- Selecting packet from input queue
- Physical and link-layer functions (de-encapsulation)
- Look up output port in forwarding table based on destination IP address, where the forwarding table is computed locally in the router using the router processor, or received from a remote central controller
  - Prefix matching of destination IP address (longest-prefix matching rule, i.e. most specific route that matches)
  - Look up performed in hardware, e.g. Ternary [Content Addressable Memory](https://en.wikipedia.org/wiki/Content-addressable_memory) (TCAM), which allows searching for data in a single clock cycle (hardware parallelism)

#### Switching

- Connecting input and output ports
- Forward packets from input port to output port
- Switching methods (via memory, bus, inter-connected network)

#### Output port processing

- Selecting packets from output queue for transmission (scheduling)
- Physical and link-layer functions (encapsulation)

#### Queuing

- Queuing occurs at input and output ports
- Packet loss will occur as queues exhaust router memory
- Input queuing means fabric switching not fast enough (head-of-line blocking), i.e. a packet at the front of the queue waits for a specific output port, blocking packets behind it that want to go to free output ports
- Output queuing means transmission rate not fast enough
- Queue management protocols
  - Drop arriving packets if queue is full ("drop tail")
  - Active queue management algorithms (e.g. Random Early Detection (RED), or [Explicit Congestion Notification](https://en.wikipedia.org/wiki/Explicit_Congestion_Notification) marking packet headers for TCP congestion control)
- Buffer sizing problem to find optimal buffer size (e.g. RFC 3439)
  - Larger buffer means less packet loss but longer delays
- Selecting packets from queue (scheduling)
  - First in, first out (FIFO)
  - Priority queuing: categorizing packets according to priority depending on purpose identified by source and destination IP address and port, keeping separate FIFO queues for each category; mechanism to give certain companies priority access (jeopardizing [net neutrality])
  - Weighted-fair queuing (WFQ) based on priority classes (round robin)

[net neutrality]: https://en.wikipedia.org/wiki/Net_neutrality

### Internet Protocol (IP)

- Unreliable, "best-effort" protocol
  - Potential packet loss (no delivery guarantee)
  - No guaranteed in-order delivery
  - Potential packet error (corruption)
  - No bandwith guarantee
  - No guaranteed (maximum) end-to-end delay for packet delivery
- Every network host has at least one IP address

#### Monitoring and diagnostics

- `ipconfig getifaddr en0` to see your IP address for the `en0` network interface

### IPv4

- IP address format
  - 32-bit address
  - Dotted-decimal notation, consisting of 4 dot-separated groups of a single byte (i.e. 3 decimals ranging from 0 - 255), e.g. `203.0.113.84`, omitting leading zeros
  - Allowing a total of 2^32 distinct addresses from `0.0.0.0` to `255.255.255.255` (represented as all ones in binary)

#### Datagram

- Version, e.g. 4 or 6
- Header length (to handle variable number of options)
- Type of service (TOS), e.g. real-time application traffic (for prioritization)
- Datagram length (headers and payload)
- Identifier, flags, fragmentation offset (IPv6 no longer allows for fragmentation)
- Time-to-live (TTL), decreased by 1 each time the datagram is processed by a router to avoid ever-living packets due to routing loops
- Protocol, e.g. 6 (TCP) or 17 (UDP), connecting network layer with transport layer (similar to how a port number connects the transport layer with the application layer)
- Header checksum, used to detect errors, routers drop erroneous datagrams using error detection algorithms (RFC 1071), repeated error detection at both transport and network layer
- Source and destination IP address, destination IP address often determined by DNS lookup
- Options (removed in IPv6 for performance reasons)
- Payload, e.g. transport-layer UDP/TCP segment

Total of 20 bytes IPv4 headers + 20 bytes TCP headers

#### Fragmentation and Reassembly

- If a datagram is larger than the MTU (Maximum Transmission Unit), the router fragments it; the MTU depends on the link layer protocol (e.g. Ethernet has an MTU of 1500 bytes).
- Reassembly happens strictly at the destination host, not at intermediate routers (in IPv4).
- Fragmentation is often used as an attack vector (fragment overlap attacks), which is why IPv6 removed it from routers.

### Addressing

- To connect a host to a network, it needs a valid IP address and a subnet mask
- Technically, an IP address is associated with a network interface rather than a host (or router) containing that interface, where a network interface is the boundary between the host and the physical link
- Each interface on every device (e.g. host, router) in the global internet must have an IP address that is globally unique
- To communicate beyond the LAN, a host needs a default gateway
- Hosts can only communicate directly with hosts on the same IP subnet, otherwise they need to go through a router, e.g. if host A is on `192.168.1.x` and host B is on `192.168.2.x`, their subnet masks `255.255.255.0` mean they’re in different subnets, so their traffic must be go through a router
- To communicate with hosts on a different subnet, hosts must go through a router, even if they are on the same Ethernet
- Last IP address in a subnet is reserved for broadcasting (i.e. `255.255.255.255`), a message sent to the broadcast address is delivered to all hosts on the same subnet
- Every host has a logical loopback interface with IP address `127.0.0.1` (`localhost`), e.g. used for testing network software locally
- Classful addressing
  - `a.b.c.d/x` (32-bit) where `x` can be 8 (class A), 16 (class B) or 24 (class C) but inefficient allocation for smaller organisations
    indicates the number of bits in the network prefix, with the remaining bits indicating the device inside the organisation
  - Subnet mask addressing, a subnet mask `255.255.255.0` (24-bits) means the first three numbers identify the network (network prefix), and the last number identifies the device inside that network (e.g. `192.168.1.42` is host `42` on network `192.168.1.0`)
- Classless Interdomain Routing (CIDR) generalizes subnet addressing
  - `a.b.c.d/x` (32-bit) where `x` indicates the number of bits in the network prefix, with the remaining bits indicating the device inside the organisation (CIDR notation)
  - Organisations are typically assigned block of continuous IP addresses, i.e. a common network prefix
  - Routers outside of organisation only consider leading `x` bits of address (network prefix) during routing, reducing the size of the routing tables since a single entry for an entire organisation will be sufficient

### IP address assignment

- Internet Cooperation for Assigned Names and Numbers (ICANN) responsible for allocating blocks of IP addresses and managing DNS root servers
- Assigned block of IP addresses configured into router

### Dynamic Host Configuration Protocol (DHCP)

- Client-server protocol
- Automatically assigns temporary IP addresses to devices on a network, or same address for returning devices
- Mechanism to renew lease
- Cannot maintain IP address when connecting to a new subnet, e.g. cannot maintain a TCP connection in mobile applications

Protocol flow for assigning an IP address to a new host:

1. A new host send a UDP broadcast discovery message to `255.255.255.255:67` (server listens on port `67`, client listens on port `68`)
2. Server(s) respond with UDP broadcast offer message, containing proposed address, lease time and ID of the discovery message
3. Client sends request message choosing from received offer(s)
4. Server responds with acknowledgement

### Private IP addresses

- 3 subnets reserved for private networks, cannot be used on the public internet:
  - `10.0.0.0/8`
  - `172.16.0.0/12`
  - `192.168.0.0/16`

### Network Address Translation (NAT)

- Publicly available IPv4 addresses are exhausted and IPv6 has not been fully adapted
- NAT allows multiple devices on a private network to share a single public IP address on the internet, thereby hiding internal network topologies
- Private addresses in LAN allocated by DHCP server in router
- Single public WAN (wide-arean network) IP address allocated by Internet Service Provider DHCP server to gateway router
- The NAT device (e.g. a router) rewrites the source IP address and port of outgoing packets to its own public IP and keeps track of the mapping between LAN-side and WAN-side source IP address and port, so responses can be sent back to the correct device, e.g. at home your laptop (`192.168.0.2`) and phone (`192.168.0.3`) both connect to the internet through your router which uses NAT to translate their private IPs to its public IP (e.g. `203.0.113.5`), so websites only see requests coming from the router’s public address.
- 16-bit port number means up to ca. 60K simultaneous entries in NAT table for a single WAN-side IP address
- NAT traversal

### Proxies and firewalls

- Proxy accepts requests for internet resources on behalf of a client
- Firewalls usually involve some combination of proxy and NAT

### IPv6

- Not enough available public addresses under IPv4
- IP address format
  - 128-bit address, consisting of 8 colon-separated groups of 4 hexadecimal characters, omitting leading zeros (e.g. `2001:0db8:85a3:0000:0000:8a2e:0370:7334` or shortened to `2001:db8:85a3::8a2e:370:7334`)
- Uses neighbor discovery (ND) instead of ARP
- ND is a set of protocols used in IPv6 to discover other devices on the same network, determine their link-layer addresses, find routers, and automatically configure addresses
- `::1` (`localhost`) for logical loopback interface (equivalent to `127.0.0.1` in IPv4)
- Anycast address
- Flow labelling (e.g. for prioritizing realtime streaming)
- Unlike IPv4, IPv6 does not allow for fragmentation and reassembly at intermediate routers ("Packet too big" ICMP error message)
- Checksum error checking removed since it was redundant with transport-layer checking (e.g. UDP, TCP)
- Transition from IPv4 to IPv6 via tunneling, sending IPv6 datagram in payload of IPv4 datagram (RFC 4213)

#### Datagram

Fields:

- Version (4 bit)
- Traffic class (8 bit), differentiated into Differentiated Services (DiffServ) bits and ECN bits
- Flow label (20 bit)
- Payload length (16 bit)
- next header (like protocol in IPv4)
- hop limit (decremented by 1 by each router that forward the datagram)
- Source and destination IPv6 address
- Payload

### Internet control message protocol (ICMP)

- Based on IP (like TCP/UDP), ICMP messages are carried in IP datagram payload
- Fields
  - Type
  - Code
- E.g. ping send (type: 8, code: 0), ping reply (type: 0, code: 0)
- Used for routing, network control, probing of availability and status, and error reporting, e.g. `ping` or `traceroute` (e.g. "port unreachable", "host unreachable")
- Not used for transmitting application data

### Generalized forwarding and software defined networking (SDN)

- Traditionally, data and control plane functionality has been implemented monolithically in a router, but SDN introduces distinction between data and control plane (separate remote control service)
- Packet switches (rather than routers) making forwarding decision based on network-layer and link-layer packet headers
- Remote controller updates match-plus-action tables (e.g. OpenFlow protocol)

#### OpenFlow protocol

- Packet forwarding based on matching via flow table
  - Set of transport, network and link layer header field values for which an incoming packet will be matched
  - Set of counters that are updated as packets are matched to entries
  - Set of actions taken when a packet matches an entry
    - Drop packet
    - Forward packet to a (physical) output port
    - Copy packet and send to multiple output ports (broadcast/multicast)
    - Rewrite selected packet header fields
- Packet not matching any entry will be dropped, or sent to remote controller for further processing
- Use cases
  - Simple forwarding
  - Load balancing
  - Firewall

### Middle boxes

- A middle box is any intermediate device performing functions apart from standard functions of an IP router on the data path between source and desitination host
- NAT translation
- Security
  - Deep packet inspection (DPI)
  - Intrusion Detection System (IDS)
  - Firewall filtering based on packet headers
- Network performance enhancements
  - Packet compression
  - Caching
  - Load balancing
- Network function virtualization (NFV)
- Operate on data from all layers, e.g. NAT rewrites network-layer IP address and transport-layer port number, in-network firewalls blocks traffic using application, transport and network layer headers

## Network layer: control plane

Centralized vs per-router control

- Per-router control (router communication with other routers to compute forwarding table, e.g. OSPF, BGP)
- Logically centralized control for network-wide logic for packet routing (e.g. update flow table) and network-layer service configuration and management

### Routing algorithms

- Goal is to determine sequence of routers from sender to receiver that minimizes costs (e.g. physical length, link speed, monetary costs)
- Mathematically expressed as cost optimization problem using graph with nodes representing routers and edges routers having varying costs
- Algorithm properties
  - Centralized: using complete, global information about the network graph, its connectivity and costs (e.g. link-state algorithm)
  - Decentralized: using incomplete, local information about neighbor nodes, each node iteratively estimates least-cost routes and shares its informations with neighbors (e.g. distance-vector algorithm)
  - Static: routes change very slowly over time, often result of human intervention (e.g. manually configuring static routes)
  - dynamic: recomputed periodically or upon network graph change
  - load-sensitive: cost vary dynamically based on congestion

#### Link-state broadcast algorithms (centralized)

- Each node broadcasts link state packets to all other notes containing the identities and costs associated with each of its attached links/edges
- All nodes end up with identical and complete information about all other nodes and their associated costs (within the same area)
- Dijkstra's Shortest Path First (SPF) algorithm, computing least-cost route for each destination in network

#### Distance-vector algorithms (decentralized)

- Each node receives information from neighboring nodes, computes routes and re-distributes new information with neighbors (distributed)
- Algorithm run until no more information is exchanged between nodes (iterative)
- Does not require all nodes to operate in lock step (asynchronous)
- Bellman-Ford equation
- RIP (Routing Information Protocol), EIGRP (Enhanced Interior Gateway Routing Protocol), ISO IDRP, Novell IPX

### Autonomous systems (AS) and intra-AS routing protocol

- An AS is a group of routers under the same administrative control, with administrative autonomy from other ASs
- All routers in AS run the same routing protocol and have information about each other
- Breaks internet into smaller scales to manage overhead of communicating, computing and storing routing information
- Handles destinations within the same AS, with entries in forwarding table determined by intra-AS routing protocol

#### Open-Shortest Path First (OSPF) protocol

- Widely used in Internet (also see IS-IS protocol)
- Publicly available protocol (open) (RFC 2328)
- Link-state protocol, based on Dijkstra's least-cost algorithm
- Link/edge weights can be set to 1 (equivalent to minimum-hop routing) or reflect link capacity
- Messages carried over IP
- Secure (e.g. MD5 authentication to prevent malicious updates of routing tables)
- Supports splitting traffic between multiple same-cost paths
- Integrated unicast and multicast routing (Multicast OSPF)

### Inter-AS routing (among Internet Service Providers)

> Glues together thousands of Internet Service Providers in the Internet

#### Border Gateway Protocol (BGP)

- Obtains prefix reachability information from neighboring ASs
- Determines best route(s) to a specific prefix (BGP router selection algorithm)
  - Hot-potato-routing
- Handles destination outside of AS
- As important for the Internet as IP itself
- Decentralized
- Path vector protocol (based on distance-vector concepts but evolved to include `AS_PATH` attribute to prevent routing loops)
- External gateway routers (eBGP connections)
  - Connected to other ASs
  - Exchange information over TCP (port 179) with other external routers, sending messages to advertise their AS (prefix), including `AS_PATH` information containing the path taken by the message and `NEXT_HOP`
  - Propagate incoming messages to internal routers
- Internal routers (iBGP connections)
  - Propagate information inside AS

### IP Anycast

- Replicate same content on different servers in different geographical locations
- Have each user access content from the closest server

Example:

- 13 IP addresses for DNS root servers but multiple servers corresponding to each address, with DNS assigning same IP address to many of its servers
- Uses BGP to advertise this address from each server
- BGP router treats multiple adverts as providing different paths to the same location when in fact they are adverts for different paths to different locations
- BGP selects least-cost route as defined in BGP route selection algorithm, i.e. usually the closest server in terms of BGP hops/network topology (which usually correlates with geography but not always)

### Software-Defined Networking (SDN)

- Simple but fast switches (routers) executing match-plus-action (data plane)
- Servers and software determine and manage switches and their forwarding/flow tables
- Decouples network functionality from hardware, previously bundled together monolithically and embedded in switches/routers by vendor
- Enables vendor agnosticism using generic, off-the-shelf hardware ("white box switching") and automation via APIs, e.g. Python/Ansible rather than manual CLI
- Rich, open ecosystem of hardware, software and network control applications

#### Components

- SDN controller (logically centralized but physically distributed and scalable) maintains network-wide state information through APIs
- SDN network control applications using controller API to specify and control SDN-enabled data-plane network devices (e.g. executing routing algorithms)

#### Controller

- Operates as communication layer between controller and SND-enabled devices ("southboud interface"), e.g. OpenFlow
- Network-wide state management
- Interface to network control applications ("northbound interface")
  - Read/write network state and flow tables in state-management layer so that they can act upon in response to events sent by devices
- Examples: ONOS, OpenDaylight

#### OpenFlow API

The OpenFlow API provides message protocols based on TCP based (port 6653).

Controller -> switch (Southbound interface):

- Set/query switch configuration parameters
- Modify-state: modify switch flow table entries
- Read-state: get statistics and counters from switch flow table entries
- Send-packet: send packet out of a specific port at the controlled switch

Switch -> controller (Northbound interface):

- Port-status: inform (physical) port status change
- Packet-in: send packet not matching any flow table entry to controller for further processing
- Flow-removed: confirm that flow table entry has been removed (e.g. due to timeout or as the result of a modify-state message)

### Network management

- Manage network servers for configuring, monitoring, controlling network devices
- Manged devices (e.g. host, router, switch) with operational state (Management Information Base)
- Data
  - Configuration
  - Operational (e.g. list of neighbors)
  - Device statistics
- Network management agent (client) running in managed devices
- Network management protocol (e.g. application-layer Simple Network Management Protocol (SNMP v3), NETCONF/YANG)

## Transport layer

- Logical communication between processes (on different network hosts)
- Breaks down large chunks of application-layer data into smaller units called segments for network transmission (segmentation)
- Extend host-to-host communication (network layer) to process-to-process communication (multiplexing)

### Principles for choosing transport layer protocols

- Reliability (reliable data transfer)
- Throughput guarantees: bandwith-sensitive vs adaptive applications
- Timing guarantees (latency, transmission delay)
- Security

### TCP/IP protocol stack

A single chunk of data, called a segment, is wrapped in a IPv4 or IPv6 packet for transmission which add source and destination IP address, which in turn is wrapped in a data link frame (i.e. "envelopes in envelopes")

The stack encompasses common protocols including:

- Internet control message protocol (ICMP)
- User Datagram Protocol (UDP)
- Transmission Control Protocol (TCP), with security via Transport Layer Security ([TLS])

[TLS]: https://en.wikipedia.org/wiki/Transport_Layer_Security

### UDP

- Thin wrapper around Internet Protocol (IP)
- Connectionless: no connection is established for transmitting packets
- UDP packet is fully identified by its 2-tuple of destination IP address and port
- Each packet is considered a discrete entity and has no relationship to other packets
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
- When a host receives an unexpected packet, i.e. when no receiver or server is running on the destination port, the host replies with a special packet (RST flag for TCP, ICMP datagram for UDP)

[QUIC]: https://en.wikipedia.org/wiki/QUIC

#### Segment structure

- 5 fields: 4 headers with 2 bytes each (8 bytes in total) + payload
  - Source port (for sending unicast replies)
  - Destination port (multiplexing)
  - Length (in bytes, headers and payload)
  - checksum (for end-to-end transmission error checking for corruption during transmission by noise or while being stored/queued in router)
  - payload (application-layer data)
- maximum segment size (MSS) to fit into a single Ethernet frame: 1472 (payload) + 8 (UDP headers) + 20 (IP headers) = 1500 bytes

[IP address spoofing]: https://en.wikipedia.org/wiki/IP_address_spoofing
[multicast]: https://en.wikipedia.org/wiki/Multicast

### Reliable data transfer

To achieve reliable data transfer, essential aspects include:

- Error detection (e.g. checksum)
- Receiver feedback to sender (e.g. acknowledgement message (ACK) for received packets)
- Re-transmission of lost packets (go-back-N or selective repeat)

These aspects require the following features:

- Packet sequence numbers
- Timers (e.g. timeouts for ACK reception before re-transmission)
- Pipelining (sending multiple packets) (compare with inefficient stop-and-wait technique, waiting for ACK before sending next packet)
- Maximum segment lifetime (MSL) of a segment in transit to prevent the re-use of sequence numbers within a segment's assumed network lifetime, thereby avoiding ambiguity from old, duplicate segments.

### TCP

- Connection-oriented: a logical connection is established between a sender and receiver for transmitting data
  - Logical connection maintained by state in endpoints (stateful)
  - Simultaneous two-way connection (duplex)
  - Single sender, single receiver (point-to-point)
- TCP packet is fully identified by its 4-tuple of source and destination IP address and port
- Reliable ("every packet is tracked and assembled"):
  - Receiver acknowledges every packet it receives and checks packet integrity using checksum
  - Sender re-sends packets that are not acknowledged
  - Packet ordering is guaranteed at reception using packet numbering (the packet sequence may be scrambled during transmission is restored at reception using sequence numbers)
- Network congestion control, dynamically matching sender and receiver speed to preempt router queue overflow and packet drops/re-transmission
- Flow control, matching sender and receiver speed to prevent a faster sender from overwhelming a slow receiver by limiting the amount of unacknowledged data the sender can transmit (see [Network congestion control])
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
  - other data messaging and streaming protocols (e.g. [ZeroMQ])
- security via [TLS]

[ZeroMQ]: https://zeromq.org/

#### Segment structure

- Fields include headers (usually 20 bytes, maximum 40 bytes including all options) and payload, extending the fields used in UDP
  - Source port (2 bytes)
  - Destination port (2 bytes)
  - Checksum (2 bytes)
  - Sequence numbers (4 bytes, max 2^32 unique sequence numbers, reliability/re-transmission)
  - Receive window (2 bytes, flow control)
  - Data offset (4 bits, header lengths in bytes)
  - Acknowledgement number (4 bytes, reliability)
  - Options field (usually empty)
  - Flags (e.g. ACK, SYN)
- Maximum segment size (MSS) for payload to fit into a single Ethernet frame: 1460 (payload) + 20 (TCP headers) + 20 (IPv4 headers) = 1500 bytes

### Network congestion control

Costs of congested networks

- Large queuing delays in routers
- Re-transmission for dropped packets due to router queue overflow
- Unnecessary re-transmissions due to timeouts for acknowledgement messages (ACK)
- Wasted transmission capacity in previous links/router when a packet is dropped at a later stage

Control strategies

- End-to-end congestion control, e.g. TCP using timeouts as congestion indicators and optimization algorithms for adjusting transmission speed (e.g. Reno, Cubic, BBR)
- Network-assisted congestion control, with routers provide feedback regarding congestion state, even before packet loss occurs
  - Direct feedback to sender
  - Mark packets in router, which are sent on to the receiver, which then informs the sender

### Ports

> If the subnet mask is like the stream name and the IP address like the house number, then the port is like a room number.

- Logical address to identify a (receiving or sending) process on a host, and to enable multiple, simultaneous connections on the same host (multiplexing)
- 16-bit number, ranging from 0 to 65535, total of 65536 ports
- Reserved port number ranges (see Internet Assigned Number Authority ([IANA]))
  - Well-known ports (0 - 1023), e.g. 21 FTP, 22 SSH, 80 HTTP, 443 HTTPS (privileged, require root access)
  - Other services (1024 - 49151)
  - Dynamically assigned (ephemeral) ports for user applications/connections (49152 - 65535)
- Every connection (or packet) goes from a source address (IP and port) to a destination address
- Source and destination address together uniquely identify connections
- Connects transport layer with application layer

Monitoring and diagnostics:

- `netstat -n -a` (disable DNS lookup, filter active ports)
- `lsof -n -i` (disable DNS lookup, filter network ports)

[IANA]: https://en.wikipedia.org/wiki/Internet_Assigned_Numbers_Authority

### Quick UDP Internet Connections (QUIC) (HTTP/3)

- Transport layer network protocol designed by Google
- Built on top of UDP rather than TCP
- Reduces latency compared to TCP by reducing round-trip times (RTT) during connection setup (0-RTT handshakes)
- Solves the head-of-line blocking problem present in TCP/HTTP2; in TCP, if one packet is lost, all subsequent packets are delayed until the lost packet is retransmitted, even if they belong to different streams; QUIC allows independent streams, so a lost packet only affects the stream it belongs to
- Used as the underlying transport for HTTP/3
- Includes built-in encryption (TLS 1.3) by default

## Application layer

### High-level network application design

There are two main types of network applications, client/server and peer-to-peer (P2P).
Many applications combine elements of both types.

#### Client/server

- Client: host process initiating the communication
- Server: host process waiting to begin communication with a client

Server is

- Always on
- Fixed IP known to the client(s)
- No client-to-client communication

For example, HTTP web servers.

#### Peer-to-peer (P2P)

- Intermittently connected hosts
- No central server with fixed IP, peers discover and connect to each other
- Direct client-to-client communication

For example, [BitTorrent], Skype (VoIP), brokerless messaging systems (e.g. [ZeroMQ]), message broadcasting.

[BitTorrent]: https://en.wikipedia.org/wiki/BitTorrent

### Sockets

- Software interface between application and transport layer
- Virtual, low-level programming abstraction representing an instance of a communication endpoint defined by a domain (e.g. `AF_INET` for IPv4), IP address, port number, and transport protocol (e.g. `SOCK_DGRAM` for UDP)
- Defined by the [socket API] (e.g. `socket()`, `connect()`, `listen()`, `accept()`, `send()`, `receive()`)
- Used to implement higher-level protocols (e.g. TCP or UDP)
- Exposed in higher-level languages, e.g. see [Python socket guide]
- A process can open multiple sockets
- A socket can accept multiple connections (as long as they are unique in terms of source and destination IP address and port number)
- Sockets are non-competing consumers of broadcast messages, when creating multiple socket instances on the same host and port number, each socket will receive a copy of the broadcast message sent to that port
- Besides network sockets, there are other sockets for inter-process communication called Unix Domain sockets (`AF_UNIX` or `AF_LOCAL`) which bypass the network stack

[Python socket guide]: https://docs.python.org/3.13/howto/sockets.html
[socket API]: https://en.wikipedia.org/wiki/Berkeley_sockets

#### Bind (server) and connect (client)

- A server binds to a particular port to specify where it will listen for incoming client connections (`bind()`), making its service available for clients under a specific address; after binding, it will listen for incoming connection requests (`listen()`)
- A client connects to a server using the server's IP address and bound port (`connect()`)

### Domain name system (DNS)

- maps human-readable domain names (e.g. `www.google.com`) to an IP address
- Hierarchical structure: Root servers -> Top-Level Domain (TLD) servers (.com, .org) -> Authoritative name servers (google.com)
- Query resolution:
  - Recursive: resolver asks server to do the work and return the final answer
  - Iterative: server returns the address of the next server to ask
- Caching: responses are cached at various levels (browser, OS, ISP) to improve performance (TTL determines cache duration); changes can take up to 48 hours to propagate across the internet
- Usually uses UDP on port 53
- Local `/etc/hosts` file overrides DNS lookups
- Types of records:
  - `A`: maps a domain name to an IPv4 address
  - `AAAA`: maps a domain name to an IPv6 address
  - `CNAME`: maps a domain name to an alias domain name (canonical name)
  - `PTR`: maps an IP address to a domain name (reverse lookup)
  - `MX`: specifies mail servers for the domain
  - `NS`: specifies authoritative name servers for the domain
  - `TXT`: holds text information (often used for verification, SPF, DKIM)

Monitoring and diagnostics:

- `host <name>` to perform a simple lookup
- `dig +trace <name>` to trace the full resolution path
- `nslookup <name>`, older tool, similar to host

### Hypertext Transfer Protocol (HTTP)

- HTTP is the foundation of data communication for the internet and the dominant protocol for modern web and APIs
- based on TCP (HTTP/1.1, HTTP/2) or UDP (HTTP/3)
- stateless: no persistent information about clients, but use of cookies to identify returning clients
- persistent (default in HTTP/1.1) or non-persistent connections
- Request methods:
  - `GET`: retrieve data
  - `POST`: submit data to be processed
  - `PUT`: update a resource
  - `DELETE`: delete a resource
- Status codes:
  - `2xx`: Success (e.g., 200 OK)
  - `3xx`: Redirection (e.g., 301 Moved Permanently)
  - `4xx`: Client Error (e.g., 404 Not Found)
  - `5xx`: Server Error (e.g., 500 Internal Server Error)
- Versions:
  - HTTP/1.1: text-based, sequential requests (head-of-line blocking)
  - HTTP/2: binary, multiplexing (multiple requests over one connection), header compression
  - HTTP/3: based on QUIC (UDP), faster connection setup, no TCP head-of-line blocking

### Dynamic Adaptive Streaming over HTTP (MPEG-DASH)

- adaptive streaming over HTTP
- video is broken into small chunks (e.g., 2-10 seconds) encoded at different bitrates/resolutions
- client requests chunks sequentially using standard HTTP GET requests
- client dynamically selects the best quality chunk based on current network conditions (bandwidth)
- uses a manifest file (MPD - Media Presentation Description) to describe available streams and chunks
- Allows smooth playback with minimal buffering even with fluctuating network speeds
- Used by streaming services like Netflix, Amazon Prime Video, YouTube

### Content Delivery Network (CDN)

- Network of geographically distributed servers
- Delivers content to users based on their geographic location
- Caches static content (e.g. images, videos) at "edge" servers close to the user
- Reduces latency and server load
- Improves availability and reliability
- Provides security features like DDoS protection
- Popular providers: Cloudflare, Akamai, Amazon CloudFront, Fastly

### Messaging systems

Network messaging systems can be categorized by architecture (centralized vs. decentralized) and data model (transient queues vs. persistent logs).

- Brokerless (P2P): direct producer-to-consumer communication for speed and low latency (e.g. [ZeroMQ])
- Brokered: central broker manages message routing, retries and distribution (smart broker/dumb consumer) (e.g. RabbitMQ, MQTT)
- Log-based: high-volume data pipelines with append-only, persistent log storage (dumb broker/smart consumer) (e.g. Apache Kafka)
- Cloud-native serverless queues: managed services via HTTP APIs with no infrastructure management (e.g. AWS SQS, Azure Service Bus)

Why use messaging systems instead of direct HTTP calls?

- Asynchronous "fire and forget" processing; producer continues immediately while consumer processes when ready, avoiding failures when services are busy or down
- Queue buffers traffic spikes, allowing consumers to process at constant sustainable rate instead of being overwhelmed
- Horizontal scaling with multiple workers sharing workload without load balancer

### Clock synchronization

Distributed systems often involve processing  timestamp from different clocks, and being able to treat them as if they come from a single, unified time source.

The most common protocol for synchronizing clocks is [NTP](https://en.wikipedia.org/wiki/Network_Time_Protocol). 

Also check out this [blog post](https://arpitbhayani.me/blogs/clock-sync-nightmare/).

## Security

- 3 factors of authentification
  - Something you know (e.g. a password)
  - Something you have (e.g. a hardware security key like YubiKey)
  - Something you are (e.g. fingerprint or face recognition)
- 3 pillars of information security
  - Confidentiality (not disclosed to unauthorized entities), including endpoint authentication and authorization 
  - Integrity (not modified by unauthorized entities)
  - Availability (information is available when needed)
- Ways to compromise a network system
  - Put malware into a host
  - Disrupt servers and network infrastructure (denial of service, or distributed denial of service attacks)
  - Sniff packets (gain access to private information)
  - IP spoofing (identifying as another person or program by falsifying network data)

### [Let's Encrypt](https://letsencrypt.org/)

- A free, automated and open certificate authority (CA) run by the nonprofit Internet Security Research Group (ISRG) to replace costly, manual CAs and enable widespread HTTPS adoption
- Provides free TLS/SSL certificates to enable HTTPS on websites
- Issues short-lived certificates (90 days) that encourage automation and regular renewal
- ACME Protocol for automated certificate issuance and management
- Domain validation challenges; to prove you control a domain, Let's Encrypt requires completing one of these challenges:
  - HTTP-01: Let's Encrypt provides a token that must be served at a specific HTTP URL on your domain which Let's Encrypt queries to verify the token (`http://<YOUR_DOMAIN>/.well-known/acme-challenge/<TOKEN>`)
  - DNS-01: Let's Encrypt provides a token that must be placed in a DNS TXT record which Let's Encrypt verifies via a DNS query
- Certificate lifecycle; after domain validation, Let's Encrypt issues a certificate; ACME client automatically installs the certificate on your web server

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
- https://www.ducktyped.org/p/why-is-it-called-a-cloud-if-its-not (blog post series on AWS networking and virtual private cloud)

For more recommendations, see this [HackerNews thread](https://news.ycombinator.com/item?id=38918418).
