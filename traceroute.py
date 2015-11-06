import logging
logging.getLogger('scapy.runtime').setLevel(logging.ERROR)

from scapy.all import sr, IP, ICMP
from random import random

TIMEOUT = 5
MAX_HOPS = 30

example_ip = '181.15.96.29'

def trace(dst = example_ip):
	id = int(random() * 0xFFFF)
	pkts = [IP(dst = dst, ttl = i) / ICMP(id = id, seq = i) for i in range(1, MAX_HOPS)]

	ans, unans = sr(pkts, timeout = TIMEOUT, verbose = False, chainCC = True)

	hops = [None] * MAX_HOPS
	final = MAX_HOPS

	for snt, rcv in ans:
		hops[snt.ttl - 1] = {'ip' : rcv.src, 'rtt' : rcv.time - snt.sent_time}

		if rcv.type == 0:
			final = min(final, snt.ttl)

	del hops[final:]

	return hops

if __name__ == "__main__":
	from common import dst, write_trace

	hops = trace(dst)

	for i, hop in enumerate(hops):
		ttl = i + 1

		if not hop:
			print(str(ttl) + '\t' + '*')
		else:
			print(str(ttl) + '\t' + str(hop['ip']) + '\t' + str(hop['rtt']))
