import os
import math
import time
import array

def tideSites(config, uncomment=False):
  allSite = [ line.split(',', 1)[0] for line in open(config, 'r') ] 
  if uncomment:
    return [ line.lstrip('#') for line in allSite ]
  else:
    return [ line for line in allSite if not line.startswith('#') ]
  
class Tide():
  def __init__(self, config, site, uncomment=False):
    self.config = config
    init = (2025, 1, 1, 0, 0, 0, 0, 0)
    if 'tzname' in dir(time):
      # running python or on host, likely 1735689600 from 1Jan1970
      self.t0 = int(time.mktime(init + (0,)))
    else:
      # running micropython on board, likely 789004800 from 1Jan2000
      self.t0 = time.mktime(init)
    self.basePeriod100 = 4471416 # 100 times M2 so that we can represent as an int
    self.basePeriod = int(round(self.basePeriod100 / 100)) # M2 in seconds
    self.halfPeriod = int(round(self.basePeriod100 / 200))
    self.period = array.array('I', [
      1275721,  # 2551442.9/2, # half synodic month 
      2380713,  # 2380713.2,   # anomalistic month
      2748551,  # 2748551.4,   # lunar evection
      1180292,  # 2360584.7/2, # half tropical month
      637861,   # 2551442.9/4, # quarter synodic month
      613005,   # unknown   7 days 5 hours 42 minutes
      871276 ]) # unknown  10 days 2 hours 1 minute
    for line in open(config, 'r'):
      if uncomment:
        line = line.lstrip('#')
      if line.split(',', 1)[0] == site:
        word = line.split(',')
        self.offset = int(word[1])
        self.lowf   = float(word[2]) / 100
        self.s = array.array('f', [ float(s) for s in word[3:-1:2] ])
        self.c = array.array('f', [ float(s) for s in word[4:-1:2] ])
        self.error = int(word[-1])
        break
    else:
      raise Exception("site: %s not found in config: %s" % (site, config))
      
  def high(self, t):
    time0 = t - self.t0 - self.offset + self.halfPeriod
    base = time0 - (time0 % self.basePeriod100) % self.basePeriod + self.offset
    offset = 0
    for i in range(len(self.period)):
      omega = (base % self.period[i]) * (2.0 * math.pi / self.period[i])
      offset += self.s[i] * math.sin(omega) + self.c[i] * math.cos(omega)
    return self.t0 + base + int(offset)
    
  def low(self, t, lastHigh=None, nextHigh=None):
    if lastHigh == None:
      lastHigh = self.high(t - self.halfPeriod) 
    if nextHigh == None:
      nextHigh = self.high(t + self.halfPeriod) 
    return lastHigh + self.lowf * (nextHigh - lastHigh)
    
  def event(self, t):
    lastHigh = self.high(t)
    if lastHigh > t:
      nextHigh = lastHigh
      lastHigh = self.high(nextHigh - self.basePeriod)
    else:
      nextHigh = self.high(lastHigh + self.basePeriod)
    low = self.low(None, lastHigh=lastHigh, nextHigh=nextHigh)

    return min([(lastHigh, 'High'), (low, 'Low'), (nextHigh, 'High')], key=lambda x: abs(x[0] - t))
