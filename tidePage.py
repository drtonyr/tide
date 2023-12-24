#!/usr/bin/python3

# example usage code

import os
import argparse
from datetime import datetime
from dateutil import tz

import tide

parser = argparse.ArgumentParser()
parser.add_argument('--year', type=int, default=2023)
parser.add_argument('--config', type=str, default='config.txt')
arg = parser.parse_args()

UK  = tz.gettz('UK/London')
UTC = tz.gettz('UTC')
initTime = int(datetime(arg.year,   1, 1, 0, 0, 0, tzinfo=UK).timestamp())
quitTime = int(datetime(arg.year+1, 1, 1, 0, 0, 0, tzinfo=UK).timestamp())
dayFormat = '%A %-d %B'

path = str(arg.year) + '/'
os.makedirs(path, exist_ok=True)

uncomment=True
index = []
for site in tide.tideSites(arg.config, uncomment=uncomment):
  nospace = site.replace(' ', '-')
  index.append('[%s](%s)' % (site, nospace))
  with open(path + nospace + '.md', 'w') as f:
    model = tide.Tide(arg.config, site, uncomment=uncomment)

    print('#', site, arg.year, file=f)
    print('Free tide predictions for', site + '.\n', file=f)
    if model.error > 0:
      print('Times are displayed in BST where appropriate.\n', file=f)
      print('Expect high tide times to be correct to about ±%d minutes (one standard deviation).' % model.error, file=f)
      print('If you need better consult the [BBC site](https://www.bbc.co.uk/weather/coast-and-sea/tide-tables).\n', file=f)
      tz = UK
    else:
      print('These tide times work worldwide.  Just scroll through these pages until you find one that matches your current tides.\n', file=f)
      print('Note that no adjustment for any daylight savings time is made.  If you need to do this then switch to the file that is an hour earlier/later when your clocks change.\n', file=f)
      tz = UTC
      

    lastHigh = model.high(initTime)
    if lastHigh > initTime:
      lastHigh = model.high(lastHigh - model.basePeriod)

    tides = []
    while lastHigh < quitTime:
      nextHigh = model.high(lastHigh + model.basePeriod)

      low = model.low(None, lastHigh=lastHigh, nextHigh=nextHigh)
      if low > initTime and low < quitTime:
        tides.append(('Low', low))

      if nextHigh < quitTime:
        tides.append(('High', nextHigh))

      lastHigh = nextHigh

    sort = {}
    for hl, ts in tides:
      dt  = datetime.fromtimestamp(ts, tz=tz)
      day = dt.strftime(dayFormat)
      item = hl + dt.strftime(" %H:%M")
      if day in sort:
        sort[day].append(item)
      else:
        sort[day] = [ item ]

    ntide = max(len(sort[day]) for day in sort)
        
    print('| date |' + '   |' * ntide, file=f)
    print('|:-----|' + '---|' * ntide, file=f)

    for day in sort:
      line = [ day ] + [''] * ntide
      line[1:len(sort[day])] = sort[day]
      print('| ' + ' | '.join(line), file=f)

with open(path + 'index.md', 'w') as f:
  print('# tides in', arg.year, file=f)
  print('Chose your location below and times will be adjusted for daylight savings.\n', file=f)
  print('For other locations, chose the `custom XXhXXm` that best matches your current tides.\n', file=f)
  
  print(', '.join(index), file=f)
