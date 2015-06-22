#!/usr/bin/env python
# Make polygon mask for rasdaman using GDAL
# By Jelmer Oosthoek (info@gispla.net)

import os,sys
from osgeo import gdal
from osgeo.gdalconst import *
from osgeo import ogr
import string
import random
import cgi
import string
sys.stderr = sys.stdout

def id_generator(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

path = '<PATH TO STORE MASKS>'
fs = cgi.FieldStorage()
print "Content-type: text/plain\n\n"

STOP = 0
# Check if fields are values
try:
    xres = float(fs['res'].value)
    yres = -xres
    xmin = float(fs['xmin'].value)
    xmax = float(fs['xmax'].value)
    if xmax <= xmin:
        STOP = 1
    ymin = float(fs['ymin'].value)
    ymax = float(fs['ymax'].value)
    if ymax <= ymin:
        STOP = 1
    ncols = int(abs(float(fs['ncols'].value)))
    nrows = int(abs(float(fs['nrows'].value)))
except:
    STOP = 1

if STOP == 1:
    print 0
    sys.exit(0)
    
# Check WKT string
try:
    wktstring = fs['wkt'].value
    wkttype = wktstring.split(" ")[0]
    # ALSO TEST WITH POLYLINE
    if wkttype == "POLYGON" or wkttype == "MULTIPOLYGON":
        geomtype = ogr.wkbPolygon
        test = ogr.CreateGeometryFromWkt(wktstring)
        if test == None:
            STOP = 1
        else:
            del test
    else:
        STOP = 1
except:
    STOP = 1

if STOP == 1:
    print 1
    sys.exit(0)

# Create 'Memory' data source with WKT as feature
try:
    drv = ogr.GetDriverByName('Memory')
    wktds = drv.CreateDataSource('out')
    wktlyr = wktds.CreateLayer('', None, geomtype)
    defn = wktlyr.GetLayerDefn()
    feature = ogr.Feature(defn)
    geom = ogr.CreateGeometryFromWkt(wktstring)
    feature.SetGeometry(geom)
    wktlyr.CreateFeature(feature)
except:
    print 2
    sys.exit(0)

# Create mask TIFF from 'Memory' data source
if STOP == 0:
    randomname = id_generator()
    geotransform=(xmin,xres,0,ymax,0,yres)
    driver = gdal.GetDriverByName('GTiff')
    dst_ds = driver.Create(path + randomname + '.tif', ncols, nrows, 1, gdal.GDT_Byte)
    dst_rb = dst_ds.GetRasterBand(1)
    dst_rb.Fill(0)
    dst_rb.SetNoDataValue(0)
    dst_ds.SetGeoTransform(geotransform)
    maskvalue = 1
    err = gdal.RasterizeLayer(dst_ds, [maskvalue], wktlyr)
    dst_ds.FlushCache()
    dst_ds = None
else:
    print 3
    sys.exit(0)

# Add mask TIFF as in-situ to rasdaman
os.system("rasimport -coll %s -t GreyImage:GreySet -referencing -f %s -conn <PATH TO>rasconnect" % (randomname, path + randomname + '.tif'))

# Return the mask collection name so it can be used in a WCPS query
print randomname
