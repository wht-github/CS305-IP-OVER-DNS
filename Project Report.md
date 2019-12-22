# DNS Project Report

Group Member: 11711201 王皓天   11710809 李艺聪  11710807 贺贵岩

## Background

### 1.  TUN interface & TUN tunnel

According to the Linux kernel:

> *TUN/TAP provides packet reception and transmission for user space programs. It can be seen as a simple Point-to-Point or Ethernet device, which, instead of receiving packets from physical media, receives them from user space program and instead of sending packets via physical media writes them to the user space program.*

That means TUN (tunnel) simulates a network layer device which operates in layer 3 carrying IP packets and TAP(network tap) simulates a link layer device which operates in layer 2 carrying Ethernet frames.

As a TUN interface is a virtual IP Point-to-Point interface, the user space program can only read/write IP packets form/to A TUN interface.

### 2. DNS

The Domain Name System(DNS) works as a distributed database that maps domain names and IP addresses to each other.

Due to the hierarchical stucture of DNS, the DNS resolver has different query methods, such as recursive and iterative. In a recursive query, the DNS resolver queries a single DNS server, which in turn can query other DNS servers on behalf of the requester. While in a iterative query, the DNS server will answer the client with other DNS server address that can resolve the query instead of the query result. Each DNS server directs the client to the next server in the chain until the current server can fully resolve the request.

### 3. Proxy & NAT

#### 3.1. Proxy

Proxy is a special network service that allows one network terminial(such as a client) to make indirect connections with anthoer network terminal(such as a server) through this service. Thus the proxy server runs on behalf of the client when requesting services, which may obscure the true source of the request to the resource server.

There are many different implenmentations of proxy, for example web proxy, SOCKS proxy and transparent proxy. While SOCKS proxies works at a lower level than HTTP proxies, as SOCKS uses a handshake protocol to notify the proxy software that its client is attempting to make a connection to SOCKS, and then operates as transparently as possible, while regular proxies may interpret and rewrite header

#### 3.2 NAT

Network Address Translation(NAT in short) is a technology that rewrites the source IP address or the destination IP address when an IP packet passes through a router or firewall which is widely use in a private network with multiple hosts but only one public IP address to access the Internet.

One common method of NAT is port mapping, which maps a port of the IP address of a host on the external network to a machine on the internal network and provides corresponding services. When the user accesses this port of the IP, the server automatically maps the request to the corresponding internal internal machine.

NAT can be use to redirect HTTP connections to the Internet to a specified HTTP proxy server to cache data and filter requests.

There are different type of NAT:

1. Full cone NAT(one-to-one)

2. Address-Restricted cone NAT

3. Port-Restricted cone NAT

4. Symmetric NAT

## Implementation

### 1. The network topology

### 2. Design of solution

### 3. Important Code

## Testing

## Contribution

## Conclusion
