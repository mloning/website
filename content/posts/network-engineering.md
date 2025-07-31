---
title: "Network Engineering"
date: 2025-07-24T23:07:58+02:00
last_modified: .Lastmod
draft: true
---

## Layers

[Open System Interconnection] (OSI) layer model:

| Layer            | Protocol Data Unit (PDU) | Function                                                                                                                                            | Diagnostic tools                          |
| ---------------- | ------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------- |
| **Host layers**  |                          |                                                                                                                                                     |                                           |
| 7 Application    | Data                     | High-level protocols such as for resource sharing or remote file access (e.g. HTTP, SMTP, LDAP)                                                     | logging, debugging                        |
| 6 Presentation   | Data                     | Translation of data between a networking service and an application; including character encoding, data compression, and encryption/decryption      | logging, debugging                        |
| 5 Session        | Data                     | Managing communication sessions, i.e., continuous exchange of information in the form of multiple back-and-forth transmissions between two nodes    | logging, debugging                        |
| 4 Transport      | Segment                  | Reliable transmission of data segments between points on a network, including segmentation, acknowledgement, and multiplexing (e.g. TCP, UDP, ICMP) | `netstat`, `netcat`, `tcpdump`            |
| **Media layers** |                          |                                                                                                                                                     |                                           |
| 3 Network        | Packet, Datagram         | Structuring and managing a multi-node network, including addressing, routing, and traffic control                                                   | `ifconfig`, `route`, `ping`, `traceroute` |
| 2 Data link      | Frame                    | Transmission of data frames between two nodes connected by a physical layer (e.g. Ethernet)                                                         | `arp`, `ndp`, `tcpdump`                   |
| 1 Physical       | Bit, Symbol              | Transmission and reception of raw bit streams over a physical medium (e.g. wires, WiFi/radio waves)                                                 | Link status, hardware lights, `ifconfig`  |

For a high-level understanding, the differences between layers 5 - 7 are not very important; they all concern the application.

[Open System Interconnection]: https://en.wikipedia.org/wiki/OSI_model

## Hardware

- TODO switches

## Ethernet

- [Local area network] (LAN) protocol
- broadcast protocol: any frame transmitted can go to any other host in the LAN (broadcast domain)
- every device has unique identifier: media access control (MAC) address
- maximum transmission unit (MTU)
- [Address Resolution Protocol] (ARP): mapping MAC to IP addresses in LAN

[Local area network]: https://en.wikipedia.org/wiki/Local_area_network
[Address Resolution Protocol]: https://en.wikipedia.org/wiki/Address_Resolution_Protocol

## Virtual LAN (VLAN)

- all hosts on LAN can see each other
- virtual LANs allow to separate LANs into multiple segments as if they had separate network interfaces/hardware
- adds extra tag to Ethernet frames indicating the VLAN they belong to
- separate IP configuration
- set up by network engineers on switches

## Tools

### macOS

- `ifconfig`
- `arp`
- `ndp`
- `ipconfig`
- `netstat` - established connections
- `lsof` - processes and files
- `route` - where traffic is being sent
- `tcpdump` - traffic to and from server
- `Wireshark`
- `netcat` - receive and send traffic
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

For more recommendations, see this [Hacker News discussion](https://news.ycombinator.com/item?id=38918418).

Courses:

- CS 144: Introduction to Computer Networking ([current course](https://cs144.github.io/), [website](https://online.stanford.edu/courses/cs144-introduction-computer-networking))

Other resources

- Python guide https://docs.python.org/3.13/howto/sockets.html
