from traceroute import trace
from numpy import mean, std
from math import isnan
import matplotlib.pyplot as plt
from common import dump

header = ['ip', 'rtt_m', 'rtt_std', 'd_rtt_m', 'n']

def most_common(l) :
	d = dict()
	for i in l:
		if i in d:
			d[i] += 1
		else:
			d[i] = 1
		max = 0
		res = 0
	for i in d:
		if d[i] > max:
			res = i
			max = d[i]
	return res

# log es una lista con los historiales de cada hop
# Cada historial es una lista de diccionarios
# Devuelve una lista de estadisticas de cada hop
# Cada estadistica es un diccionario {rtt_m, rtt_sd, d_rtt_m, d_rtt_sd}
def statistics(log):
	stats = []
	for i, x in enumerate(log):
		if len(x) > 0:
			ip = most_common([ h['ip'] for h in x ])
			rtts = [ y['rtt'] for y in x if y['ip'] == ip ]
			rtt_m = mean(rtts)
			rtt_std = std(rtts)
			stats.append({ 'ip': ip, 'rtt_m': rtt_m, 'rtt_std': rtt_std, 'd_rtt_m': '*', 'n': len(rtts)})
			if i == 0:
				stats[0]['d_rtt_m'] = rtt_m
			elif stats[i-1]:
				stats[i]['d_rtt_m'] = rtt_m - stats[i-1]['rtt_m']
		else:
			stats.append(None)

	return stats

def hist(log):
	plt.hist(log, 20)
	plt.show()

if __name__ == "__main__":
	from monitor import monitor 
	from common import dst

	def update_stats(log):
		hops = trace(dst)

		for i, hop in enumerate(hops):
			if i >= len(log):
				log.append([])
			if hop:
				log[i].append(hop)
		stats = statistics(log)

		return [[s[key] for key in header] if s else ['*'] for s in stats], log

	log = monitor(header, update_stats, [])

	dump(log)

	# hist(samples)
