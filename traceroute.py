from scapy.all import sr, IP, ICMP

TIMEOUT = 5
MAX_HOPS = 30

example_ip = '181.15.96.29'

def trace(dst = example_ip):
	hops = []
	for ttl in range(1, MAX_HOPS):
		ans, unans = sr(IP(dst = dst, ttl = ttl) / ICMP(), timeout = TIMEOUT, verbose = False)
		if ans:
			snt, rcv = ans[0]
			hops.append({'ip' : rcv.src, 'rtt' : rcv.time - snt.sent_time})
			if rcv.src == dst:
				break
		else:
			hops.append(None)
	return hops