from common import load

def calc_hop_means(d_rtts):
	if len(d_rtts) > 0:
		return sum(x['rtt'] for x in d_rtts) / len (d_rtts)
		# return reduce(lambda x,y: x['rtt'] + y['rtt'], d_rtts) / len(d_rtts) # promedio
	return -1

def calc_route_means(log):
	return map(calc_hop_means, log)

route_means = calc_route_means(load())

for index, mean in enumerate(route_means):
	if mean > -1:
		print index+1, mean
