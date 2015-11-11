from pylab import *

t = []
s=[]

read_file = [x.strip().split() for x in open('RTT EEUU').readlines()]

s = [ [int(x[0]), float(x[2])] for x in read_file if len(x) > 2]

t=[x[0] for x in s]
s=[x[1] for x in s]

plot(t, s, label="RTT del paquete hacia California")

legend()
xlabel('Time To Live')
ylim(0.001,1)
xlim([1, 19])
xticks(np.arange(1, 19, 1))
ylabel('Round Trip Time')
title('Universidad de California, Santa Cruz')
grid(True)
show()
