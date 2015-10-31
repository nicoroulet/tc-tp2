from scapy.all import sr, IP, ICMP

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