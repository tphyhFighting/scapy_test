import sys
import getopt
import socket
import fcntl
import struct
import random
from scapy.all import *


def get_ip(ifname):
    return '17.0.0.1'
    local_ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(local_ip.fileno(), 0x8915, struct.pack('256s', bytes(ifname[:15], 'utf-8')))[20:24])


def make_domain_name():
    seed = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXY#!@$%^&*()_+=-'
    sa = []
    for i in range(100):
        sa.append(random.choice(seed))
    host = ''.join(sa)
    TLDstring = RandString(RandNum(2, 3))
    tld = TLDstring.lower()
    SLDstring = RandString(RandNum(3, 6))
    sld = SLDstring.lower()
    name = host+"."+sld.decode()+"."+tld.decode()
    return name


def make_random(start, end, res=[]):
    for i in range(100):
        num=random.randint(start, end)
        print("start,end:",start,end)
        if num >65535:
            print("haha out")
        res.append(num)
    return res

def make_dns_query(qr_ele=0,
                   opcode_ele=0,
                   tc_ele=0,
                   rd_ele=0,
                   qd_ele=1,
                   an_ele=0,
                   ns_ele=0,
                   ar_ele=0,
                   qclass_ele=1,
                   ar_type_ele=41,
                   ar_ttl_ele=60,
                   ar_rclass_ele=512,
                   ar_rdlen_ele=0,
                   ip=None,
                   udp=None
                  ):
    dns_query = DNS(id=0, qr=qr_ele, opcode=opcode_ele, tc=tc_ele, rd=rd_ele, qdcount=qd_ele, ancount=an_ele,
                    nscount=ns_ele, arcount=ar_ele)
    qtype_list = list(range(0, 255))
    query_type = random.sample(qtype_list, 1)
    domain_name=make_domain_name()
    dns_query.qd = DNSQR(qname=domain_name, qtype=query_type, qclass=qclass_ele)
    dns_query.ar = DNSRR(type=ar_type_ele, ttl=ar_ttl_ele, rclass=ar_rclass_ele, rdlen=ar_rdlen_ele)
    query = ip / udp / dns_query
    return query
def main():
    #client_server=get_ip('knil')
    client_server = '17.0.0.1'
    dns_server = '192.168.43.213'
    dns_dport = 53
    qr_list = range(0, 2)
    opcode_list = [0, 1, 2, 15]
    tc_list = range(0, 2)
    rd_list = range(0, 2)
    qdcount_list = [0, 1, 65535]+make_random(0,65535)
    ancount_list = [0, 1, 65535]
    nscount_list = [0, 1, 65535]
    arcount_list = [0, 1, 65535]
    qclass_list = [1, 2, 3, 4, 255]
    ar_type_list = [0, 1, 30000, 65535]
    ar_ttl_list = [0, 1, 0xFFFFFFFF]
    ar_rclass_list = [0, 1500, 4096, 65535]
    ar_rdlen_list = [0, 31900, 65535]

    ip = IP(dst=dns_server, src=client_server)
    udp = UDP(sport=RandShort(), dport=dns_dport)

    for qr_ele in qr_list:
        query=make_dns_query(qr=qr_ele)
        send(query)
    for opcode_ele in opcode_list:
        query=make_dns_query(opcode=opcode_ele)
        send(query)
    for tc_ele in tc_list:
        query=make_dns_query(tc=tc_ele)
        send(query)
    for rd_ele in rd_list:
        query=make_dns_query(rd=rd_ele)
        send(query)
    for qd_ele in qdcount_list:
        query=make_dns_query(qd=qd_ele)
        send(query)
    for an_ele in ancount_list:
        query=make_dns_query(an=an_ele)
        send(query)
    for ns_ele in nscount_list:
        query=make_dns_query(ns=ns_ele)
        send(query)
    for ar_ele in arcount_list:
        query=make_dns_query(ar=ar_ele)
        send(query)
    for qclass_ele in qclass_list:
        query=make_dns_query(qclass=qclass_ele)
        send(query)
    for ar_type_ele in ar_type_list:
        query=make_dns_query(type=ar_type_ele)
        send(query)
    for ar_ttl_ele in ar_ttl_list:
        query=make_dns_query(ttl=ar_ttl_ele)
        send(query)
    for ar_rclass_ele in ar_rclass_list:
        query=make_dns_query(rclass=ar_rclass_ele)
        send(query)
    for ar_rdlen_ele in ar_rdlen_list:
        query=make_dns_query(rdlen=ar_rdlen_ele)
        send(query)

if  __name__ == '__main__':
    make_random(0,65535)