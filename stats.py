from traceroute import trace

from sys import argv
from curses import initscr, endwin

from numpy import mean, std

# log es una lista con los historiales de cada hop
# Cada historial es una lista de diccionarios
# Devuelve una lista de estadisticas de cada hop
# Cada estadistica es un diccionario {rtt_m, rtt_sd, d_rtt_m, d_rtt_sd}
def statistics(log):
	stats = [ {'rtt_m': mean([y['rtt'] for y in x]), 'rtt_sd': std([y['rtt'] for y in x]), 'd_rtt_m': mean([y['d_rtt'] for y in x if 'd_rtt' in y]), 'd_rtt_sd': std([y['d_rtt'] for y in x if 'd_rtt' in y]) } for x in log if len(x)>0 ] # plz don't kill me
	return stats

SCR_START_POS = 2

scr = initscr()
scr.addstr(0, 0, "LE MONITOR."); scr.refresh()
MAX_HOPS = 30

log = [[] for i in range(MAX_HOPS)]

try:
	while True:
		scr.clear()
		scr.addstr(0, 0, "LE MONITOR.")
		scr.addstr(SCR_START_POS, 0, "TTL \t RTT mean \t RTT stdev \t D_RTT mean \t D_RTT stdev")
		if len(argv) > 1:
			output = trace(argv[1])
		else:
			output = trace()


		for i, hop in enumerate(output):
			if hop:
				log[i].append(hop)
				if i == 0:
					log[i][-1]['d_rtt'] = hop['rtt']
				elif output[i-1]:
					log[i][-1]['d_rtt'] = max(0, hop['rtt'] - output[i-1]['rtt'])
				
		stats = statistics(log)
		for i, stat in enumerate(stats):
			row = i + SCR_START_POS + 1
			ttl = i + 1
			scr.addstr(row, 0, str(ttl) + '\t' + "%.8f" %(stat['rtt_m']) + '\t' + "%.8f" %(stat['rtt_sd']) + '\t' + "%.8f" %(stat['d_rtt_m']) + '\t' + "%.8f" %(stat['d_rtt_sd']) )
		scr.refresh()
except KeyboardInterrupt:
	endwin()
	for i, stat in enumerate(stats):
		print str(i+1) + '\t' + "%.8f" %(stat['rtt_m']) + '\t' + "%.8f" %(stat['rtt_sd']) + '\t' + "%.8f" %(stat['d_rtt_m']) + '\t' + "%.8f" %(stat['d_rtt_sd'])
