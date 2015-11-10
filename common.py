import logging
logging.getLogger('scapy.runtime').setLevel(logging.ERROR)

from scapy.all import Net
from sys import argv

try:
    dst = Net(argv[1])
except IndexError:
    dst = Net('www.example.com')

title = "Tracing route to {}".format(dst.choice())

if dst.repr != dst.choice():
        title += " ({})".format(dst.repr)

