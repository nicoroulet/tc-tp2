from traceroute import trace

from sys import argv
from curses import *
from time import sleep
from threading import Thread

SCR_START_POS = 2

scr = initscr()
scr.addstr(0, 0, "LE MONITOR."); scr.refresh()

while True:
	
	if len(argv) > 1:
		output = trace(argv[1])
	else:
		output = trace()
	
	scr.clear()
	scr.addstr(0, 0, "LE MONITOR.")
	
	for i, hop in enumerate(output):
		ttl = i + 1
		row = i + SCR_START_POS
		if not hop:
			scr.addstr(row, 0, str(ttl) + '\t' + '*')
		else:
			scr.addstr(row, 0, str(ttl) + '\t' + str(hop['ip']) + '\t' + str(hop['rtt']))
	scr.refresh()
	
endwin()