# Buffered Crater Counting
# By Jelmer Oosthoek (info@gispla.net)
#
# After: Fassett, C.I., Head, J.W., 2008. The timing of martian valley network activity: Constraints from buffered crater counting. Icarus 195, 61-89.
#
# Made possible thanks to:
# http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#//0017000000tt000000
# http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#//000v00000001000000
# http://blogs.esri.com/esri/arcgis/2010/02/23/how-do-i-use-arcpy-geometry-objects-in-scripting/
# http://support.esri.com/cn/knowledgebase/techarticles/detail/41027
# http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#//001700000072000000
# https://gis.stackexchange.com/questions/52936/arcpy-points-in-polygon-check

from shapefile import shapefile
import os, sys
import json
import time
from math import *
import arcpy
arcpy.env.overwriteOutput = True
arcpy.env.workspace = os.getcwd()

text = '''
Buffered Crater Counting
Jelmer Oosthoek
Usage:
BufferedCraterCounting.py <crater points.shp> <diameter column> <name column> <min diameter> <linear polygon.shp>
'''
 
if len(sys.argv) == 1:
    print text
    sys.exit()

# variables
try:
    cratershapefile = sys.argv[1]
    diameter_column = sys.argv[2]
    name_column = sys.argv[3]
    min_diameter = int(sys.argv[4])
    linearshapefile = sys.argv[5]
except:
    print text
    sys.exit()
if name_column == "FID":
    print "Please use a different name field"
    sys.exit()
    
if min_diameter > 0:
    lt = "_lt" + str(min_diameter)
else:
    lt = ""

# Define CRS filenames
cratercrs = cratershapefile.replace(".shp",".prj")
linearcrs = linearshapefile.replace(".shp",".prj")
if not os.path.exists(cratercrs):
    print "Crater point shapefile doesn't have a CRS!"
    sys.exit()
if not os.path.exists(linearcrs):
    print "Linear feature polygon shapefile doesn't have a CRS!"
    sys.exit()

# Make the input CSV files for TableToEllipse:
cratercsvfile = cratershapefile[:-4] + lt + ".csv"
crater3dcsvfile = cratershapefile[:-4] + lt + "_3d.csv"
craterinput = shapefile("read", cratershapefile)
cratercsv = file(cratercsvfile, "w")
crater3dcsv = file(crater3dcsvfile, "w")
cratercsv.write("X,Y,MAJOR,MINOR,UNIT,NAME\n")
crater3dcsv.write("X,Y,MAJOR,MINOR,UNIT,NAME\n")
featurelist = craterinput.feats2list()
for features in featurelist:
    feature = features[0]
    table = features[1]
    try:
        diameter = float(table[diameter_column])
        name = str(table[name_column])
        if len(name) > 1:
            name = name[:1].upper() + name[1:].lower()
        if name == "None":name = ""
        x = feature[0][0]
        y = feature[0][1]
        out = str(x) + "," + str(y) + "," + str(diameter) + "," + str(diameter) + ",KILOMETERS," + str(name) + "\n"
        out3d = str(x) + "," + str(y) + "," + str(3*diameter) + "," + str(3*diameter) + ",KILOMETERS," + str(name) + "\n"
        if diameter >= min_diameter:
            cratercsv.write(out)
            crater3dcsv.write(out3d)
    except:
        print "wrong feature: " + str(feature[0])
cratercsv.close()
crater3dcsv.close()
craterinput.finish()

# Execute TableToEllipse:
craterellipsefile = cratershapefile[:-4] + lt + "_ellipse.shp"
crater3dellipsefile = cratershapefile[:-4] + lt + "_ellipse_3d.shp"
spatialRef = arcpy.SpatialReference(cratercrs)
arcpy.TableToEllipse_management(cratercsvfile, craterellipsefile, "X", "Y", "MAJOR", "MINOR", "KILOMETERS", "", "", "NAME", spatialRef)
arcpy.TableToEllipse_management(crater3dcsvfile, crater3dellipsefile, "X", "Y", "MAJOR", "MINOR", "KILOMETERS", "", "", "NAME", spatialRef)
os.unlink(cratercsvfile)
os.unlink(crater3dcsvfile)

# Convert to linear shapefile CRS:
craterellipsefile = cratershapefile[:-4] + lt + "_ellipse.shp"
crater3dellipsefile = cratershapefile[:-4] + lt + "_ellipse_3d.shp"
arcpy.env.outputCoordinateSystem = linearcrs
arcpy.CopyFeatures_management(craterellipsefile, craterellipsefile[:-4] + "_prj.shp")
arcpy.CopyFeatures_management(crater3dellipsefile, crater3dellipsefile[:-4] + "_prj.shp")
arcpy.Delete_management(craterellipsefile)
arcpy.Delete_management(crater3dellipsefile)
craterellipsefile = craterellipsefile[:-4] + "_prj.shp"
crater3dellipsefile = crater3dellipsefile[:-4] + "_prj.shp"

### Check, I think we can skip Part 1 as Part 2 does the same

## Part 1: Only keep if the crater rim + ejecta (a circle of 2 times the diameter) intersects the linear feature polygon
arcpy.MakeFeatureLayer_management(crater3dellipsefile, 'crater3d') 
arcpy.MakeFeatureLayer_management(linearshapefile, 'linear')
arcpy.SelectLayerByLocation_management('crater3d', 'intersect', 'linear')
names = []
rows = arcpy.SearchCursor('crater3d')
for row in rows:
    name = row.NAME
    if not name in names:
        names.append(name)

## Part 2: For each crater make a linear feature buffer of 1.5xD and check if the crater center lies inside this buffer
# Get the centroid points of the in Part 1 kept craters
cursor = arcpy.da.SearchCursor('crater3d', "SHAPE@XY")
centroid_coords = []
for feature in cursor:
    centroid_coords.append(feature[0])

# Only keep the Part 1 craters in the 1D crater polyline shapefile
cursor = arcpy.UpdateCursor(craterellipsefile)
for feature in cursor:
    name = feature.NAME
    if not name in names:
        cursor.deleteRow(feature)

# Get area of linear feature
lineargeometry = arcpy.CopyFeatures_management(linearshapefile, arcpy.Geometry())
lineararea = lineargeometry[0].area / 10000000 # in km^2
linearpoints = json.loads(lineargeometry[0].JSON)["rings"][0]

# Get the point coordinates of the linear feature polygon
#shp = shapefile("write", "check.shp","polygon")
spatialRef = arcpy.SpatialReference(cratercrs)
desc = arcpy.Describe(linearshapefile)
shapefieldname = desc.ShapeFieldName
rows = arcpy.SearchCursor(linearshapefile, "", spatialRef)
for row in rows:
    feat = row.getValue(shapefieldname)
    polygoncoords = json.loads(feat.JSON)["rings"][0]
    #shp.createfeatfromlist(polygoncoords)
#shp.finish()

# Go through each remaining crater in the 1D crater polyline shapefile:
i = 0
cursor = arcpy.UpdateCursor(craterellipsefile)
freqdict = {}
fractionlist = []
for feature in cursor:
    # Get the diameter
    diam = feature.MAJOR
    buffer = 1.5 * diam
    # Calculate the buffer:
    arcpy.Buffer_analysis(linearshapefile, linearshapefile[:-4] + "_" + str(i) + ".shp", str(buffer) + " Kilometers", "FULL", "ROUND", "ALL")
    # Get the centroid point coordinate of the crater:
    point = arcpy.Point(centroid_coords[i][0], centroid_coords[i][1])
    # Get the linear feature 1.5D buffer geometry object:
    linearfeaturebuffer = arcpy.CopyFeatures_management(linearshapefile[:-4] + "_" + str(i) + ".shp", arcpy.Geometry())
    linearbufferarea = linearfeaturebuffer[0].area / 10000000 # in km^2
    # 
    if not linearfeaturebuffer[0].contains(point):
        cursor.deleteRow(feature)
    else:
        freqdict[diam] = [linearbufferarea, feature.X, feature.Y, feature.NAME]
        fractionlist.append([diam, lineararea/linearbufferarea, feature.X, feature.Y])
    arcpy.Delete_management(linearshapefile[:-4] + "_" + str(i) + ".shp")
    i += 1
 
# Calculate cumulative crater frequency
csvfile = cratershapefile[:-4] + ".csv"
csv = open(csvfile, "w")
csv.write("X,Y,NAME,DIAM,FREQ\n")
diams = freqdict.keys()
diams.sort(reverse=True)
start = 1
for diam in diams:
    if start == 1:
        freq = 1 / freqdict[diam][0]
        start = 0
    else:
        freq = (1 + (freq * freqdict[diam][0])) / freqdict[diam][0]
    out = "%s,%s,%s,%s,%s\n" % (freqdict[diam][1], freqdict[diam][2], freqdict[diam][3], diam, float(freq))
    csv.write(out)
csv.close()

# Finish up:
arcpy.SelectLayerByAttribute_management('crater3d', 'CLEAR_SELECTION')
arcpy.Delete_management(crater3dellipsefile)

# Convert crater shapefile CRS back to original
arcpy.env.outputCoordinateSystem = cratercrs
arcpy.CopyFeatures_management(craterellipsefile, craterellipsefile[:-8] + ".shp")
arcpy.Delete_management(craterellipsefile)

# Create SSC file for CraterStats2:
curdate = "%s.%s.%s" % (time.gmtime()[2], time.gmtime()[1], time.gmtime()[0])

polygonstring = ""
i = 1
for coord in polygoncoords:
    polygonstring = polygonstring + '%s   1   ext %s   %s\n' % (i, coord[0], coord[1])
    i += 1
polygonstring = polygonstring[:-1]

fractionstring = ""
for item in fractionlist:
    fractionstring = fractionstring + '%s   %s   %s   %s\n' % (item[0], item[1], item[2], item[3])
fractionstring = fractionstring[:-1]

string = '''
# Spatial crater count
#
# Date of measurement = %s
#
# Ellipsoid axes:
a_axis_radius = 3396.19 <km>
b_axis_radius = 3396.19 <km>
c_axis_radius = 3396.19 <km>
#
# area_shapes:
unit_boundary = {vertex,sub_area,tag,lon,lat
#
#Area_name1 = %s
#Area_size1 = %s <km^2>
#
%s
}
#
Total_area = %s <km^2>
#
# crater_diameters:
crater = {diam,fraction,lon,lat
%s
}
''' % (curdate, cratershapefile[:-4], lineararea, polygonstring, lineararea, fractionstring)

sccfile = cratershapefile[:-4] + ".scc"
scc = open(sccfile, "w")
scc.write(string)
scc.close()
