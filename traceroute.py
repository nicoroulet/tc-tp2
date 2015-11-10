import logging
logging.getLogger('scapy.runtime').setLevel(logging.ERROR)

from scapy.all import sr, IP, ICMP, Net
from random import random

TIMEOUT = 5
MAX_HOPS = 30

def trace(dst):
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
	from monitor import monitor 
	from common import dst

	def trace_display(_):
		hops = trace(dst)

		return [hop and hop.values() or ['*'] for hop in hops], None

	monitor(None, trace_display, None)
