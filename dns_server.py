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
import dns.rrset
from queue import Queue
from queue import LifoQueue
local_addr = '10.9.0.2'
local_mask = '255.255.255.0'
mtu = 160
server_port = 53
'''
Working Flow(server):
the same as client.
DIFF: packet ip into dns response and send it back
'''


class server_tun:
    def __init__(self):
        '''
        IFF_NO_PI: no flag in discrete packet
        '''
        self._tun = pytun.TunTapDevice(
            name='mytun', flags=pytun.IFF_TUN | pytun.IFF_NO_PI)

        self._tun.addr = local_addr
        self._tun.netmask = local_mask
        self._tun.mtu = mtu
        self._tun.persist(True)
        self._tun.up()
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.bind(('', 53))
        self.data_queue = LifoQueue(65532)
        self.ip_queue = Queue(65532)

    def _recv_from_socket(self):
        # use stack to store the recieved dns packet
        data, addr = self._socket.recvfrom(65523)
        query_msg = dns.message.from_wire(data)
        name = str(query_msg.question[0].name)
        name = name[:-20]
        ip_data = ''.join(name.split('.'))
        data_to_tun = coder.b64decode(ip_data)

        self.data_queue.put((query_msg, addr))

        return data_to_tun

    def run(self):

        mtu = self._tun.mtu
        r = [self._tun, self._socket]
        w = []
        x = []
        data_to_tun = ''
        data_to_socket = ''
        target_addr = ()
        query_msg = None

        while True:
            # print(1)
            r, w, x = select.select(r, w, x)
            if self._tun in r:
                data_to_socket = self._tun.read(mtu)
                print(data_to_socket)
            if self._socket in r:
                data_to_tun = self._recv_from_socket()
                # print(data_to_tun)
            if self._tun in w:
                self._tun.write(data_to_tun)
                data_to_tun = ''
            if self._socket in w and not self.data_queue.empty():
                # get the newest recieved dns packet, prevent dns time out
                # encode ip data into TXT field
                query_msg, target_addr = self.data_queue.get()
                response = dns.message.make_response(
                    query_msg, recursion_available=True)
                response.answer.append(dns.rrset.from_text(
                    query_msg.question[0].name, 30000, 1, 'TXT', str(coder.b64encode(data_to_socket), encoding='ascii')))
                self._socket.sendto(response.to_wire(), target_addr)
                data_to_socket = b''
            r = []
            w = []
            if data_to_tun:
                w.append(self._tun)
            else:
                r.append(self._socket)

            if data_to_socket:
                w.append(self._socket)
            else:
                r.append(self._tun)


if __name__ == '__main__':
    server = server_tun()
    server.run()
