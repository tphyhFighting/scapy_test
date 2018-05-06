#### scapy 环境
[scapy](https://github.com/secdev/scapy)
```bash
cd dns_demo
docker run --rm -it -v `pwd`:/tmp  openswitch/ubuntuscapy sh
```

![image](https://raw.githubusercontent.com/tphyhFighting/static/master/img/scapy_docker_run.jpg)



####scapy
```python
dns_server = '8.8.8.8'
dns_dport = 53
client_server = "192.168.43.213"
```
#####发一个dns的请求
```python
>>> dns_baidu=IP(dst="8.8.8.8")/UDP()/DNS(qd=DNSQR(qname="www.baidu.com"))
>>> dns_baidu.show()
###[ IP ]###
  version= 4
  ihl= None
  tos= 0x0
  len= None
  id= 1
  flags=
  frag= 0
  ttl= 64
  proto= udp
  chksum= None
  src= 172.17.0.4
  dst= 8.8.8.8
  \options\
###[ UDP ]###
     sport= domain
     dport= domain
     len= None
     chksum= None
###[ DNS ]###
        id= 0
        qr= 0
        opcode= QUERY
        aa= 0
        tc= 0
        rd= 0
        ra= 0
        z= 0
        ad= 0
        cd= 0
        rcode= ok
        qdcount= 1
        ancount= 0
        nscount= 0
        arcount= 0
        \qd\
         |###[ DNS Question Record ]###
         |  qname= 'www.baidu.com'
         |  qtype= A
         |  qclass= IN
        an= None
        ns= None
        ar= None





sr1(IP(dst="8.8.8.8")/UDP()/DNS(qd=DNSQR(qname="www.baidu.com")))
>>> q=sr1(IP(dst="8.8.8.8")/UDP()/DNS(qd=DNSQR(qname="www.baidu.com")))
Begin emission:
.Finished to send 1 packets.
*
Received 2 packets, got 1 answers, remaining 0 packets
>>> q.show()
###[ IP ]###
  version= 4L
  ihl= 5L
  tos= 0x0
  len= 118
  id= 49282
  flags=
  frag= 0L
  ttl= 37
  proto= udp
  chksum= 0x18d0
  src= 8.8.8.8
  dst= 172.17.0.4
  \options\
###[ UDP ]###
     sport= domain
     dport= domain
     len= 98
     chksum= 0x5540
###[ DNS ]###
        id= 0
        qr= 1L
        opcode= QUERY
        aa= 0L
        tc= 0L
        rd= 0L
        ra= 1L
        z= 0L
        ad= 0L
        cd= 0L
        rcode= ok
        qdcount= 1
        ancount= 3
        nscount= 0
        arcount= 0
        \qd\
         |###[ DNS Question Record ]###
         |  qname= 'www.baidu.com.'
         |  qtype= A
         |  qclass= IN
        \an\
         |###[ DNS Resource Record ]###
         |  rrname= 'www.baidu.com.'
         |  type= CNAME
         |  rclass= IN
         |  ttl= 547
         |  rdlen= 18
         |  rdata= 'www.a.shifen.com.'
         |###[ DNS Resource Record ]###
         |  rrname= 'www.a.shifen.com.'
         |  type= A
         |  rclass= IN
         |  ttl= 95
         |  rdlen= 4
         |  rdata= '220.181.112.244'
         |###[ DNS Resource Record ]###
         |  rrname= 'www.a.shifen.com.'
         |  type= A
         |  rclass= IN
         |  ttl= 95
         |  rdlen= 4
         |  rdata= '220.181.111.188'
        ns= None
        ar= None
```



######测试rdlen=70000
```python
>>> ip = IP(dst=dns_server,src=client_server)
>>> udp = UDP(sport=RandShort(),dport=dns_dport)
>>> dns_query = DNS(id = 1, qr = 0,opcode = 0,tc = 0,rd = 1,qdcount=1,ancount = 0,nscount=0,arcount=1)
>>> query_type = 1
>>> dns_query.qd = DNSQR(qname = "www.baidu.com",qtype=query_type,qclass = 1)
>>> dns_query.ar = DNSRR(rrname="www.baidu.com",type=1,rclass = 1,ttl = 64,rdlen= 700000,rdata="hello")
>>>
>>>
>>> query = ip/udp/dns_query
>>>
>>> query.show()
###[ IP ]###
  version= 4
  ihl= None
  tos= 0x0
  len= None
  id= 1
  flags=
  frag= 0
  ttl= 64
  proto= udp
  chksum= None
  src= 172.20.10.6
  dst= 8.8.8.8
  \options\
###[ UDP ]###
     sport= <RandShort>
     dport= domain
     len= None
     chksum= None
###[ DNS ]###
        id= 1
        qr= 0
        opcode= QUERY
        aa= 0
        tc= 0
        rd= 1
        ra= 0
        z= 0
        ad= 0
        cd= 0
        rcode= ok
        qdcount= 1
        ancount= 0
        nscount= 0
        arcount= 1
        \qd\
         |###[ DNS Question Record ]###
         |  qname= 'www.baidu.com'
         |  qtype= A
         |  qclass= IN
        an= None
        ns= None
        \ar\
         |###[ DNS Resource Record ]###
         |  rrname= 'www.baidu.com'
         |  type= A
         |  rclass= IN
         |  ttl= 64
         |  rdlen= 700000
         |  rdata= 'hello'
>>>
>>>




>>> send(query)
Traceback (most recent call last):
  File "<console>", line 1, in <module>
  File "/usr/local/lib/python2.7/dist-packages/scapy/sendrecv.py", line 251, in send
    __gen_send(conf.L3socket(*args, **kargs), x, inter=inter, loop=loop, count=count,verbose=verbose, realtime=realtime)
  File "/usr/local/lib/python2.7/dist-packages/scapy/sendrecv.py", line 234, in __gen_send
    s.send(p)
  File "/usr/local/lib/python2.7/dist-packages/scapy/arch/linux.py", line 395, in send
    sx = str(ll(x))
  File "/usr/local/lib/python2.7/dist-packages/scapy/packet.py", line 268, in __str__
    return self.build()
  File "/usr/local/lib/python2.7/dist-packages/scapy/packet.py", line 330, in build
    p = self.do_build()
  File "/usr/local/lib/python2.7/dist-packages/scapy/packet.py", line 322, in do_build
    pay = self.do_build_payload()
  File "/usr/local/lib/python2.7/dist-packages/scapy/packet.py", line 314, in do_build_payload
    return self.payload.do_build()
  File "/usr/local/lib/python2.7/dist-packages/scapy/packet.py", line 322, in do_build
    pay = self.do_build_payload()
  File "/usr/local/lib/python2.7/dist-packages/scapy/packet.py", line 314, in do_build_payload
    return self.payload.do_build()
  File "/usr/local/lib/python2.7/dist-packages/scapy/packet.py", line 322, in do_build
    pay = self.do_build_payload()
  File "/usr/local/lib/python2.7/dist-packages/scapy/packet.py", line 314, in do_build_payload
    return self.payload.do_build()
  File "/usr/local/lib/python2.7/dist-packages/scapy/packet.py", line 319, in do_build
    pkt = self.self_build()
  File "/usr/local/lib/python2.7/dist-packages/scapy/packet.py", line 310, in self_build
    p = f.addfield(self, p, val)
  File "/usr/local/lib/python2.7/dist-packages/scapy/fields.py", line 347, in addfield
    return s+self.i2m(pkt, val)
  File "/usr/local/lib/python2.7/dist-packages/scapy/layers/dns.py", line 118, in i2m
    return str(x)
  File "/usr/local/lib/python2.7/dist-packages/scapy/packet.py", line 268, in __str__
    return self.build()
  File "/usr/local/lib/python2.7/dist-packages/scapy/packet.py", line 330, in build
    p = self.do_build()
  File "/usr/local/lib/python2.7/dist-packages/scapy/packet.py", line 319, in do_build
    pkt = self.self_build()
  File "/usr/local/lib/python2.7/dist-packages/scapy/packet.py", line 310, in self_build
    p = f.addfield(self, p, val)
  File "/usr/local/lib/python2.7/dist-packages/scapy/fields.py", line 70, in addfield
    return s+struct.pack(self.fmt, self.i2m(pkt,val))
error: 'H' format requires 0 <= number <= 65535
>>>
```


#####测试域名错误
```python
>>> ip = ip = IP(dst="8.8.8.8",src="192.168.43.213")
>>> udp = UDP(sport=RandShort(),dport=53)
>>> dns_query = DNS(id = 1, qr = 0,opcode = 0,tc = 0,rd = 1,qdcount=1,ancount = 0,nscount=0,arcount=0)
>>> dns_query.qd = DNSQR(qname = "wx.qx.com",qtype=1,qclass = 1)
>>> query = ip/udp/dns_query
>>> query.show()
###[ IP ]###
  version= 4
  ihl= None
  tos= 0x0
  len= None
  id= 1
  flags=
  frag= 0
  ttl= 64
  proto= udp
  chksum= None
  src= 192.168.43.213
  dst= 8.8.8.8
  \options\
###[ UDP ]###
     sport= <RandShort>
     dport= domain
     len= None
     chksum= None
###[ DNS ]###
        id= 1
        qr= 0
        opcode= QUERY
        aa= 0
        tc= 0
        rd= 1
        ra= 0
        z= 0
        ad= 0
        cd= 0
        rcode= ok
        qdcount= 1
        ancount= 0
        nscount= 0
        arcount= 0
        \qd\
         |###[ DNS Question Record ]###
         |  qname= 'wx.qx.com'
         |  qtype= A
         |  qclass= IN
        an= None
        ns= None
        ar= None
>>> send(query)
.
Sent 1 packets.
>>> sr1(query)
Begin emission:
Finished to send 1 packets.
...........

```
#####测试rdlen=12
>>> dns_server = '8.8.8.8'
>>> dns_dport = 53
>>> client_server = "192.168.43.213"
>>> ip = IP(dst=dns_server,src=client_server)
>>> udp = UDP(sport=RandShort(),dport=dns_dport)
>>> dns_query = DNS(id = 1, qr = 0,opcode = 0,tc = 0,rd = 1,qdcount=1,ancount = 0,nscount=0,arcount=1)
>>> query_type = 1
>>> dns_query.qd = DNSQR(qname = "www.baidu.com",qtype=query_type,qclass = 1)
>>> dns_query.ar = DNSRR(rrname="www.baidu.com",type=1,rclass = 1,ttl = 64,rdlen= 12)
>>> query=ip/udp/dns_query
>>> send(query)
.
Sent 1 packets.
>>>
>>> query.show()
###[ IP ]###
  version= 4
  ihl= None
  tos= 0x0
  len= None
  id= 1
  flags=
  frag= 0
  ttl= 64
  proto= udp
  chksum= None
  src= 192.168.43.213
  dst= 8.8.8.8
  \options\
###[ UDP ]###
     sport= <RandShort>
     dport= domain
     len= None
     chksum= None
###[ DNS ]###
        id= 1
        qr= 0
        opcode= QUERY
        aa= 0
        tc= 0
        rd= 1
        ra= 0
        z= 0
        ad= 0
        cd= 0
        rcode= ok
        qdcount= 1
        ancount= 0
        nscount= 0
        arcount= 1
        \qd\
         |###[ DNS Question Record ]###
         |  qname= 'www.baidu.com'
         |  qtype= A
         |  qclass= IN
        an= None
        ns= None
        \ar\
         |###[ DNS Resource Record ]###
         |  rrname= 'www.baidu.com'
         |  type= A
         |  rclass= IN
         |  ttl= 64
         |  rdlen= 12
  
2. hhh
3. hhh
