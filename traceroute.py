import logging

logging.getLogger('scapy.runtime').setLevel(logging.ERROR)

from sys import argv
from scapy.all import sr, IP, ICMP

TIMEOUT = 5

def traceroute(dst, max = 30):
	hops = []
	for ttl in range(1, max):
		ans, unans = sr(IP(dst = dst, ttl = ttl) / ICMP(), timeout = TIMEOUT, verbose = False)
		if ans:
			snt, rcv = ans[0]
			hops.append({'ip' : rcv.src, 'rtt' : rcv.time - snt.sent_time})
			if rcv.src == dst:
				break
		else:
			hops.append(None)
	return hops

for i, hop in enumerate(traceroute(argv[1])):
	ttl = i + 1
	if not hop:
		print ttl, '\t', '*'
	else:
		print ttl, '\t', hop['ip'], '\t', hop['rtt']