# CS305IP-Over-DNS

This project is a trail just use DNS packet transmitting data between client and server.

## Main Principle

It use the authority DNS name server, local DNS will forward the query to corrosponding name server with subdomain. So client can encode data into QNAME to send data percisely. And the local DNS will recurisively query the authority DNS, so the data can be encoded in TXT fields in RR as well.  

- read ip packet from tun and pack it as dns packet  
  
- write ip packet decode form dns response into tun

## Features

- Use timer to control whether send packet to the server, improve efficient

- Base64 encode provide a bad security, however, a ssh tunnel can solve it.

## Server Usage

The choice of proxy or NAT is yours.

Run the dns_server.py script in privileged mode

`sudo python3 dns_server.py`
  
## Client Usage

Run the dns_client.py script in privileged mode

`sudo python3 dns_client.py`

### SOCKS proxy using SSH

> Suppose the IP address of client's TUN is 10.9.0.1 and the server's TUN IP is 10.9.0.2

1. `ssh -i xxx.pem -D 10.9.0.1:8080 ubuntu@10.9.0.2 -N -f`

   - `-D` Represents local port forwarding. When listening to a connection on this port, the data in this connection will be forwarded to the server through a secure tunnel. Currently it supports SOCKS4 and SOCKS5 protocols.

   - `-N` Indicates that the remote command is not executed. Useful for port forwarding only

   - `-f` Request ssh to work in background mode. This option implies the "-n" option, so standard input will become / dev / null

    This command will establish a connection with the server through the tunnel, and open the SOCKS proxy service on the local port 8080 in background.

2. Set the SOCKS5 proxy for **current terminal**

   ``` bash
   # set socks proxy
   $ export http_proxy = socks5://10.9.0.1:8080
   $ export https_proxy = socks5://10.9.0.1:8080
   # or
   $ export ALL_PROXY = socks5://10.9.0.1:8080
   ```

    Cancel proxy settings

   ```bash
    $ unset http_proxy
    $ unset https_proxy
    $ unset ALL_RPOXY
   ```

   Now the programs run in the terminal will use the proxy automatically

## Testing

![test1](README.assets/1b3e2e971b955cbb77471df4527b36bb.png)

![test2](README.assets/479ff4b200009bfa252c36971f0aa17b.png)
