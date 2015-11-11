from traceroute import trace
from numpy import mean, std
from scipy.stats.mstats import normaltest
from math import isnan
import matplotlib.pyplot as plt

header = ['ip', 'rtt_m', 'rtt_sd', 'd_rtt_m', 'd_rtt_sd', 'n']

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
	stats = [ {
		'n': len(x),
		'ip': most_common( [h['ip'] for h in x] ),
		'rtt_m': mean([y['rtt'] for y in x]),
		'rtt_sd': std([y['rtt'] for y in x]),
		'd_rtt_m': mean([y['d_rtt'] for y in x if 'd_rtt' in y]),
		'd_rtt_sd': std([y['d_rtt'] for y in x if 'd_rtt' in y])
		} if x else None for x in log ] # plz don't kill me
	return stats

def hist(log):
	plt.hist(log, 100)
	plt.show()

def dump(log):
	f = open('{}.trace'.format(dst.repr), 'w')
	for i, hops in enumerate(log):
		for hop in hops:
			f.write('\t'.join(str(x) for x in [i+1, hop['ip'], hop['rtt']]) + '\n')

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
				if i == 0:
					log[i][-1]['d_rtt'] = hop['rtt']
				elif hops[i-1]:
					log[i][-1]['d_rtt'] = hop['rtt'] - hops[i-1]['rtt']

		stats = statistics(log)

		return [[s[key] for key in header] if s else ['*'] for s in stats], log

	log = monitor(header, update_stats, [])

	dump(log)

	samples = [x['d_rtt'] for hop in log for x in hop if x and 'd_rtt' in x]
	hist(samples)
	nt = normaltest(samples)
	print("normaltest con p-value {}".format(nt[1]))
