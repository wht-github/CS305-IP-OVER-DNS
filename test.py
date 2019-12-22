import socket
import dns.resolver
import dns.message
import dns.renderer
import dns.rrset
import dns.name
import random
if __name__ == '__main__':
    print(random.uniform(0,1))
    print(random.uniform(0,1))
    a = '123456'
    print(a[0:4])
    print(a[4:8])
    # a = dns.message.make_query('dafd','TXT')
    # # a.answer.
    # b = dns.message.make_response(a,True)
    # nn = dns.name.from_text('fafdd')
    # b.answer.append(dns.rrset.from_text(nn,3000,1,'TXT','4'))
    # print(b.to_wire())
    # print(x)
    # print(len(x))
    # print(type(x))
    # b.to_wire()
    # # print(b.set_opcode(0))
    # print(a.is_response(b))
    # print(a)
    # print('-----------------')
    # print(b)
    # a = b'\x00\x00\x08\x00E\x00\x00T!\x80\x00\x00@\x01E\x17\n\x08\x00\x02\n\x08\x00\x01\x00\x00\xda\x05\x00\x13\x01\xa7\xaa\xdf\xfc]\x00\x00\x00\x00\xb4/\n\x00\x00\x00\x00\x00\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./01234567'
    # print(a)
    # print(str(a[0:-15]))
    # dns.rrset.RRset.to_wire()