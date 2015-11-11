from traceroute import trace
from numpy import mean, std
from scipy.stats.mstats import normaltest
from math import isnan
import matplotlib.pyplot as plt

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
		if x:
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
	# stats = [ {
	# 	'n': len(x),
	# 	'ip': most_common( [h['ip'] for h in x] ),
	# 	'rtt_m': mean([y['rtt'] for y in x]),
	# 	'rtt_sd': std([y['rtt'] for y in x]),
	# 	'd_rtt_m': mean([y['d_rtt'] for y in x if 'd_rtt' in y]),
	# 	'd_rtt_sd': std([y['d_rtt'] for y in x if 'd_rtt' in y])
	# 	} if x else None for x in log ] # plz don't kill me
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
					log[i][-1]['d_rtt'] = max(0, hop['rtt'] - hops[i-1]['rtt'])

		stats = statistics(log)

		return [[s[key] for key in header] if s else ['*'] for s in stats], log

	log = monitor(header, update_stats, [])

	dump(log)
	
	stats = statistics(log)
	
 	for i, stat in enumerate(stats):
		if stat:
			print "%d \t %.8f \t %.8f \t %s \t %d " %(i+1, stat['rtt_m'], stat['rtt_std'], str(stat['d_rtt_m']) if 'd_rtt_m' in stat else "*" , stat['n'])
			
	samples = [ stat['d_rtt_m'] for stat in stats if stat and 'd_rtt_m' in stat ]
	# samples = [x['d_rtt'] for hop in log for x in hop if x and 'd_rtt' in x]
	hist([x['d_rtt'] for hop in log for x in hop if x and 'd_rtt' in x])
	nt = normaltest([ x['d_rtt_m'] for x in stats if x ])
	# nt = normaltest([x['d_rtt'] for hop in log for x in hop if x and 'd_rtt' in x])
	
	
	# samples = [x['d_rtt'] for hop in log for x in hop if x and 'd_rtt' in x]
	# samples = [mean([x['d_rtt'] for x in hop if x and 'd_rtt' in x ]) for hop in log if len([ y for y in hop if ('d_rtt' in y)])>0 ]
	# samples = [ (x-mean(samples) / std(samples)) for x in samples ]
	print("normaltest con p-value {}".format(nt[1]))
