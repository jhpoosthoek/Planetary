# DTMMinusScale: DTM minus a certain scale
# By Jelmer Oosthoek (info@gispla.net)
#
# DTMMinusScale generates a smoothed interpolated version of a DTM and subtracts this from the DTM.
# The cellfactor is the smoothing factor.

import os, sys
try:
    import arcpy
    from arcpy import env
    from arcpy.sa import *
except:
    print "Please use this with the Python installation of ArcGIS 10"
    sys.exit()

text = '''By: Jelmer Oosthoek (info@gispla.net)

Usage: DTMMinusScale.py inputdtm cellfactor

DTMMinusScale generates a smoothed version of a DTM and subtracts this from the DTM.
The cellfactor is the smoothing factor.'''

if len(sys.argv) == 1:
    print text
    sys.exit()
else:
    inRaster = sys.argv[1]
    cellFactor = int(sys.argv[2])

env.workspace = os.getcwd()
arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput = True

# Set local variables
aggrRaster = inRaster[:-4] + "_" + str(cellFactor) + ".img"
aggrPoints = inRaster[:-4] + "_" + str(cellFactor) + ".shp"
smoothRaster = inRaster[:-4] + "_smooth.img"
clipRaster = inRaster[:-4] + "_clipped.img"
outRaster = inRaster[:-4] + "_Minus" + str(cellFactor) + "Scale.img"

# Determine cellSize
CellsizeResult = arcpy.GetRasterProperties_management(inRaster, "CELLSIZEX")
cellSize = CellsizeResult.getOutput(0) 
print "Cellsize of %s: %s" % (inRaster, cellSize)

# Execute Aggregate
print "Creating aggregate with %sx smaller cellsize than %s" % (cellFactor, inRaster)
outAggreg = Aggregate(inRaster, cellFactor, "MEAN", "EXPAND", "DATA")
outAggreg.save(aggrRaster)

# Execute RasterToPoint
print "Convert aggregate raster to point shapefile"
arcpy.RasterToPoint_conversion(aggrRaster, aggrPoints, "VALUE")

# Execute NaturalNeighbor
print "Interpolate point shapefile using Natural neighbor to %s meter cellsize" % (cellSize)
outNatNbr = NaturalNeighbor(aggrPoints, "grid_code", cellSize)
outNatNbr.save(smoothRaster)

#Clip Raster Dataset
print "Clip: " + inRaster
arcpy.Clip_management(inRaster, "#", clipRaster, smoothRaster)

# Map Algebra
print "Map Algebra: Clipped raster minus Natural neighbor interpolation"
divRaster = Raster(clipRaster) - Raster(smoothRaster)
divRaster.save(outRaster)
