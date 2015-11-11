# coding=utf-8

from common import load
from stats import statistics
from numpy import mean, std
from scipy.stats import t
from math import sqrt
from scipy.stats.mstats import normaltest

def grubbs(samples_rtt):
	N = len(samples_rtt)
	G = (max(samples_rtt) - mean(samples_rtt)) / std(samples_rtt)
	a = 0.01
	crit_val = t.isf(a / N, N - 2)
	crit_reg = (crit_val ** 2 / (N - 2 + crit_val ** 2)) * (N - 1) / sqrt(N)
	return G, a, crit_reg

def test(log):
	stats = statistics(log)

	# for i, stat in enumerate(stats):
	#	if stat:
	#		print "%d \t %.8f \t %.8f \t %s \t %d " %(i+1, stat['rtt_m'], stat['rtt_std'], str(stat['d_rtt_m']) if 'd_rtt_m' in stat else "*" , stat['n'])

	samples = [ s for s in stats if s and 'd_rtt_m' in s and s['d_rtt_m'] != '*' and s['d_rtt_m'] > 0 ]

	samples_rtt = [ s['d_rtt_m'] for s in samples ]

	print "== Test de normalidad ==\n"
	print "p-value = {}\n".format(normaltest(samples_rtt)[1])

	for k in range(len(samples)):
		print "MAX: {}".format(max(samples_rtt))
		G, a, G_crit = grubbs(samples_rtt)

		hop_to = max((s for s in samples if s['d_rtt_m'] in samples_rtt),
				key = lambda s: s['d_rtt_m'])['ip']
		for i in range(len(stats) - 1):
			if stats[i+1] and 'ip' in stats[i+1] and stats[i+1]['ip'] == hop_to:
				hop_from = stats[i]['ip']

		print """
== Test de outliers de Grubbs #{} ==

     G = {}
     a = {}
G_crit = {}

Hop: {} -> {}
""".format(k, G, a, G_crit, hop_from, hop_to)

		if G > G_crit:
			samples_rtt.remove(max(samples_rtt))
		else:
			break

if __name__ == "__main__":
	log = load()
	test(log)

# vim: noet ts=4
