
import sys
import optparse
import socket
import select
import errno
import pytun
import dns.message
import dns.name
import dns.query
import dns.resolver
import base64 as coder
import time
import queue
local_addr = '10.9.0.1'
dst_addr = '10.9.0.2'
local_mask = '255.255.255.0'
# remote_dns_addr = '120.78.166.34'
remote_dns_addr = '52.82.46.4'
remote_dns_port = 53
mtu = 160
query_root_name = 'group-24.cs305.fun'
label_len = 63

'''
Working Flow(client):
1. build local tun
2. send query to dns server timely to keep data transmit 

'''
class client_tun:
    def __init__(self):
        self._tun = pytun.TunTapDevice(
            name='mytun', flags=pytun.IFF_TUN | pytun.IFF_NO_PI)
        self._tun.addr = local_addr
        self._tun.dstaddr = dst_addr
        self._tun.netmask = local_mask
        self._tun.mtu = mtu
        self._tun.persist(True)
        self._tun.up()
        self.speed = 0.5
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def run(self):
        mtu = self._tun.mtu
        r = [self._tun, self._socket]
        w = []
        x = []
        data_to_tun = b''
        data_to_socket = b''
        last_blank = time.time()
        while True:
            # print(1)
#           read write excute, wait for available
            r, w, x = select.select(r, w, x)
            if self._tun in r:
                data_to_socket = self._tun.read(mtu)
            if self._socket in r:
#                 decode the ip packet, write it into kernel
                data_to_tun, target_addr = self._socket.recvfrom(65532)
                dns_response = dns.message.from_wire(data_to_tun)
                if dns_response.answer:
                    txt_record = dns_response.answer[0]
                    data_to_tun = coder.b64decode(str(txt_record.items[0]))
                else:
                    data_to_tun = b''

            if self._tun in w:
                self._tun.write(data_to_tun)
                data_to_tun = b''
            if self._socket in w:
#                 encoding local ip packet into qname 
                encoded_data_to_socket = coder.b64encode(data_to_socket)
                split_labels = [str(encoded_data_to_socket[i:i + label_len], encoding='ascii')
                                for i in range(0, len(encoded_data_to_socket), label_len)]
                split_labels.append(query_root_name)
                target_domain = '.'.join(split_labels)
                name = dns.name.from_text(target_domain)
                query = dns.message.make_query(name, 'TXT')
                self._socket.sendto(
                    query.to_wire(), (remote_dns_addr, remote_dns_port))
                data_to_socket = b''

            r = []
            w = []
            if data_to_tun:
                w.append(self._tun)
            else:
                r.append(self._socket)
            if not data_to_socket:
                r.append(self._tun)
            now = time.time()
            print(now - last_blank)
#             prevent the client send packet too fast
            if now - last_blank > self.speed or data_to_socket:
                print(data_to_socket)
                w.append(self._socket)
                last_blank = now


if __name__ == '__main__':
    server = client_tun()

    server.run()
