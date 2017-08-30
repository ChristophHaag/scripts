#!/usr/bin/env python3

import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook

dates = []
with open("/var/log/pacman.log", "r") as log:
    lastdate = ""
    for line in log:
        if not "starting full system upgrade" in line: continue
        datestring = line[1:11]
        date = datetime.datetime.strptime(datestring, "%Y-%m-%d")
        if date != lastdate:
            dates.append((date, 1))
        else:
            dates[-1] = (dates[-1][0], dates[-1][1] + 1)
        lastdate = date

x = [mdates.date2num(date) for (date, value) in dates]
y = [value for (date, value) in dates]
fig = plt.figure()
graph = fig.add_subplot(111)
graph.bar(x,y)
graph.set_xticks(x)
graph.set_xticklabels(
        [date.strftime("%Y-%m-%d") for (date, value) in dates]
        )
plt.show()

