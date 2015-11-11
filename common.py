import logging
logging.getLogger('scapy.runtime').setLevel(logging.ERROR)

from scapy.all import Net
from sys import argv

if argv[0] != 'test.py':
	try:
		dst = Net(argv[1])
	except IndexError:
		dst = Net('www.example.com')

	title = "Tracing route to {}".format(dst.choice())
	if dst.repr != dst.choice():
		title += " ({})".format(dst.repr)

log_file = '{}.log'.format(argv[1])

def load():
	f = open(log_file, 'r')
	log = []
	for line in f:
		row = line.strip().split('\t')
		i = int(row[0])
		log.extend([[] for _ in range(1 + i - len(log))])
		log[i].append({'ip' : row[1], 'rtt' : float(row[2])})
	return log

def dump(log):
	f = open(log_file, 'w')
	for i, hops in enumerate(log):
		for hop in hops:
			f.write('\t'.join(str(x) for x in [i+1, hop['ip'], hop['rtt']]) + '\n')
