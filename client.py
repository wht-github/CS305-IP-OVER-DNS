import pytun
import socket
import time
import select
import errno
import sys
import asyncio
class TunnelServerClient(object):
    '''
    tun definition:
        taddr: tun address
        tdstaddr: tun destination address
        tmask: tun netmask
        tmtu: tun mtu
        raddr: remote address
        rport: remote port
    '''
    def __init__(self, taddr, tdstaddr, tmask, tmtu, raddr, rport):
        self._tun = pytun.TunTapDevice('mytun',flags=pytun.IFF_TUN)
        self._tun.addr = taddr
        self._tun.dstaddr = tdstaddr
        self._tun.netmask = tmask
        self._tun.mtu = tmtu
        self._tun.up()
        
        self._raddr = raddr
        self._rport = rport
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def run(self):
        mtu = self._tun.mtu
        r = [self._tun, self._sock]; w = []; x = []
        to_tun = ''
        to_sock = ''
        self._sock.connect((self._raddr, self._rport))
        print('begin')
        while True:
           

            try:
                r, w, x = select.select(r, w, x)
                if self._tun in r:
                    to_sock = self._tun.read(mtu)
                if self._sock in r:
                    to_tun, addr = self._sock.recvfrom(65535)
                    # if addr[0] != self._raddr or addr[1] != self._rport:
                        # to_tun = '' # drop packet
                if self._tun in w:
                    self._tun.write(to_tun)
                    to_tun = ''
                if self._sock in w:
                    self._sock.sendto(to_sock, (self._raddr, self._rport))
                    to_sock = ''
                r = []; w = []
                if to_tun:
                    w.append(self._tun)
                else:
                    r.append(self._sock)
                if to_sock:
                    w.append(self._sock)
                else:
                    r.append(self._tun)
            except Exception as e:
                raise e
if __name__ == '__main__':
    mytun = TunnelServerClient('10.8.0.1','10.8.0.2','255.255.255.0',1500,'52.82.46.4',999)
    mytun.run()
