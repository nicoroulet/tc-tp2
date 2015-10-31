import logging

logging.getLogger('scapy.runtime').setLevel(logging.ERROR)

from sys import argv
from scapy.all import sr, IP, ICMP
from curses import *
from time import sleep
from threading import Thread

TIMEOUT = 5
SCR_START_POS = 2

scr = initscr()
scr.addstr(0, 0, "LE MONITOR."); scr.refresh()

def traceroute(dst ,max = 30):
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

# def dots_msg(y, x, str = "ya va"):
# 	scr.addstr(y, x, str)
# 	dots_x_pos = x + len(str)
# 	while True:
# 		for i in range(0,3):
# 			sleep(1)
# 			scr.addstr(y, dots_x_pos + i, '.'); scr.refresh()

# def monitor():

# def interactive():

while True:
	output = traceroute(argv[1])
	for i, hop in enumerate(output):
		ttl = i + 1
		row = i + SCR_START_POS
		if not hop:
			scr.addstr(row, 0, str(ttl) + '\t' + '*')
		else:
			scr.addstr(row, 0, str(ttl) + '\t' + str(hop['ip']) + '\t' + str(hop['rtt']))
		scr.refresh()
		
endwin()