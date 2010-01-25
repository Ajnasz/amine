#!/usr/bin/python

from amine import Amine
import sys

try:
  x = int(sys.argv[1])
except:
  x = 8

try:
  y = int(sys.argv[2])
except:
  y = 8

try:
  mines = int(sys.argv[3])
except:
  mines = 10

miner = Amine(x, y, mines)
miner.start()
