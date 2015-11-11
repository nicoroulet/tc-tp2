from common import load
from stats import statistics
from numpy import mean, std
from scipy.stats import t
from math import sqrt
from scipy.stats.mstats import normaltest

def test(log):
	stats = statistics(log)

	# for i, stat in enumerate(stats):
	#	if stat:
	#		print "%d \t %.8f \t %.8f \t %s \t %d " %(i+1, stat['rtt_m'], stat['rtt_std'], str(stat['d_rtt_m']) if 'd_rtt_m' in stat else "*" , stat['n'])

	samples = [ stat['d_rtt_m'] for stat in stats if stat and 'd_rtt_m' in stat and stat['d_rtt_m'] != '*' and stat['d_rtt_m'] > 0 ]

	print "== Test de normalidad ==\n"
	print "p-value = {}".format(normaltest(samples)[1])

	N = len(samples)
	G = (max(samples) - mean(samples)) / std(samples)
	a = 0.5
	crit_val = t.isf(a / N, N - 2)
	crit_reg = (crit_val ** 2 / (N - 2 + crit_val ** 2)) * (N - 1) / sqrt(N)

	print """
== Test de outliers de Grubbs ==

H0: there are no outliers in the data
Ha: the maximum value is an outlier

G = {}
a = {}

Rechazar H0 si G > {}\
""".format(G, a, crit_val, crit_reg)

if __name__ == "__main__":
	log = load()
	test(log)

# vim: noet ts=4
