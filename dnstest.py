import dns.message
import dns.edns
import socket
import asyncio
import pytun

ping = b'\x00\x00\x08\x00E\x00\x00T|J@\x00@\x01\xaaL\n\x08\x00\x01\n\x08\x00\x02\x08\x00\xa0E\x00\x03\x00\x04\x83\x94\xfb]\x00\x00\x00\x00\x0c\xee\r\x00\x00\x00\x00\x00\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./01234567'

if __name__ == '__main__':
    # try:
    tun = pytun.TunTapDevice('mytun',flags=pytun.IFF_TUN)
    tun.addr = '10.9.0.1'
    tun.netmask = '255.255.255.0'
    tun.mtu = 1500
    tun.up()

    
    while True:
        
        # option.to_wire(tun)
       print(tun.read(1500))
    # #         pass
    # # except Exception as e:
    # #     tun.down()
    # #     tun.close()
    # #     raise e
    
    # # with open('t.txt','wb') as f:
    # #     bbb = option.to_wire(f)
    # #     print(bytes(bbb))
    # option = dns.edns.GenericOption(1, ping)
    # dns_msg = {
    #     'qname': 'group-24.cs305.fun',
    #     'rdtype': 'NS',
    #     'rdclass': 1,
    #     'use_edns': False,
    #     'want_dnssec': False,
    #     'ednsflags': 5,
    #     'payload': 4096,
    #     'request_payload': 4096,
    #     'options': [option]
    # }

    # message = dns.message.make_query(qname=dns_msg['qname'],
    #                                  rdtype=dns_msg['rdtype'],
    #                                  rdclass=dns_msg['rdclass'],
    #                                  use_edns=dns_msg['use_edns'],)
    #                                 #  options=[option])
    # a = message.to_wire()
    # # print(len(a))
    # # print(message)
    # message.use_edns(edns=0, ednsflags=1, payload=4096, options=[option,option])
    # # b = message.to_wire()
    # # print(len(b))
    # print(message)
    # # print('-----------------------')
    # # x = dns.message.from_wire(b)
    # # op = x.options[0]
    # # print(op.to_text())