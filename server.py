import pytun
import socket
import time
import select
import errno
import sys
# ping  = b'\x00\x00\x08\x00E\x00\x00TT\xcc@\x00@\x01\xd1\xc7\n\x08\x00\x01\n\x08\x00\x05\x08\x00\x1ei\x002\x00\x05\xde\x82\xf9]\x00\x00\x00\x00<\xac\x06\x00\x00\x00\x00\x00\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./01234567'
class TunnelServerClient(object):

    def __init__(self, taddr, tdstaddr, tmask, tmtu, laddr, lport):
        self._tun = pytun.TunTapDevice(name='mytun',flags=pytun.IFF_TUN)
        self._tun.addr = taddr
        self._tun.dstaddr = tdstaddr
        self._tun.netmask = tmask
        self._tun.mtu = tmtu
        self._tun.up()
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.bind((laddr, lport))
        # self._sock.connect((raddr, rport))
        # self._raddr = raddr
        # self._rport = rport

    def run(self):
        self._sock.listen()
        conn, addr = self._sock.accept()
        mtu = self._tun.mtu
        r = [self._tun, self._sock]; w = []; x = []
        to_tun = ''
        to_sock = ''
        while True:
            try:
                r, w, x = select.select(r, w, x)
                if self._tun in r:
                    to_sock = self._tun.read(mtu)
                if self._sock in r:
                    to_tun, addr = conn.recv(65535)
                    # if addr[0] != self._raddr or addr[1] != self._rport:
                        # to_tun = '' # drop packet
                if self._tun in w:
                    self._tun.write(to_tun)
                    to_tun = ''
                if self._sock in w:
                    # self._sock.sendto(to_sock, (self._raddr, self._rport))
                    conn.send(to_sock)
                    to_sock = ''
                r = []; w = []
                if to_tun:
                    w.append(self._tun)
                else:
                    r.append(conn)
                if to_sock:
                    w.append(conn)
                else:
                    r.append(self._tun)
            except (select.error, socket.error, pytun.Error) as e:
                if e[0] == errno.EINTR:
                    continue
                print >> sys.stderr, str(e)
                break
if __name__ == '__main__':
    mytun = TunnelServerClient('10.8.0.2','10.8.0.1','255.255.255.0',1500,'52.82.46.4',999)
    mytun.run()
    # try:
    #     tun = TunTapDevice(name='mytun', flags=IFF_TUN)
    #     print(tun.name)
    #     tun.addr = '10.8.0.1'
    #     tun.dstaddr = '10.8.0.2'
    #     tun.netmask = '255.255.255.0'
    #     tun.mtu = 1500
    #     print(tun.addr)
    #     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #     sock.bind()
    #     tun.up()
    #     # tun.fileno()
    #     tun.persist(True)
    #     while(True):
    #         buf = tun.read(tun.mtu)
    #         print(buf)
    #         # tun.write(ping)
    #         # time.sleep(10)
    #         # tun.write(b'test')
    # # except KeyboardInterrupt:
    # #     tun.down()
    # #     tun.close()
    # except Exception as e:
    #     raise e
