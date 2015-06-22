# By Jelmer Oosthoek (info@gispla.net)

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import os, sys
import urllib
import urllib2

# input bands
bands = [100,200,300]

# WCPS
wcpsurl = 'http://planetserver.jacobs-university.de:8080/rasdaman/ows'
scatterdata = []
for band in bands:
    values = {'query' : 'for data in ( frt0001968f_07_if165l_trr3_1_01 ) return encode(data.' + str(band) + ', "csv" )'}
    data = urllib.urlencode(values)
    req = urllib2.Request(wcpsurl, data)
    response = urllib2.urlopen(req)
    data = response.read()
    scatterdata.append(data[1:-1].replace("},{",",").split(","))

# Plot 3D
scatterx = []
scattery = []
scatterz = []
for i in range(len(scatterdata[0])):
    if scatterdata[0][i] != '65535' and scatterdata[1][i] != '65535' and scatterdata[2][i] != '65535':
        scatterx.append(float(scatterdata[0][i]))
        scattery.append(float(scatterdata[1][i]))
        scatterz.append(float(scatterdata[2][i]))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(scatterx, scattery, scatterz)

ax.set_xlabel("band" + str([0]))
ax.set_ylabel("band" + str([1]))
ax.set_zlabel("band" + str([2]))

plt.show()