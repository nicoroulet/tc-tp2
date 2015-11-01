import logging
logging.getLogger('scapy.runtime').setLevel(logging.ERROR)

from traceroute import trace

from sys import argv
from scapy.all import sr, IP, ICMP
from curses import *
from time import sleep
from threading import Thread

SCR_MSG_ROW = 2
SCR_DATA_START_ROW = SCR_MSG_ROW + 1
tracing_message = 'Tracing'

scr = initscr()
curs_set(0)
scr.addstr(0, 0, "LE MONITOR.")
scr.addstr(1, 0, "Route trace to IP " + argv[1])
scr.refresh()

def print_tracing_message(y, x):
	scr.addstr(y, x, tracing_message)
	dots_x_pos = x + len(tracing_message)
	while True:
		sleep(1)
		scr.addstr(y, dots_x_pos, ' '*3)
		scr.refresh()
		for i in range(0,3):
			sleep(1)
			scr.addstr(y, dots_x_pos + i, '.'); scr.refresh()

def monitor():
	total_monitor_its = 0
	while True:
		if len(argv) > 1:
			output = trace(argv[1])
		else:
			output = trace()
		total_monitor_its += 1

		total_monitor_its_msg = '[total iterations: ' + str(total_monitor_its) + ']'
		scr.addstr(SCR_MSG_ROW, len(tracing_message + '...')+1, total_monitor_its_msg)

		for i, hop in enumerate(output):
			ttl = i + 1
			row = i + SCR_DATA_START_ROW
			if not hop:
				scr.addstr(row, 0, str(ttl) + '\t' + '*')
			else:
				scr.addstr(row, 0, str(ttl) + '\t' + str(hop['ip']) + '\t' + str(hop['rtt']))
			scr.refresh()

monitor_thread = Thread(target = monitor)
msg_thread = Thread(target = print_tracing_message, args = (SCR_MSG_ROW, 0))

monitor_thread.start()
msg_thread.start()

raw(); cbreak()
c = scr.getch()
if c == 'q':
	monitor_thread.stop()
	msg_thread.stop()
	nocbreak()
	endwin()
