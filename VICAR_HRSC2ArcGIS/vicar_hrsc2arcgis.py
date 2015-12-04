# Download: ftp://pdsimage2.wr.usgs.gov/pub/pigpen/Perl/vicar2world.pl
# Change line 191 into: $skipbytes = $lblsz;

import os, sys
from glob import glob
import arcpy

filenames = []
for filename in glob("*.??"):
    if ".dt4." in filename or ".nd4." in filename:
        filenames.append(filename)
        
for filename in filenames:
        
    ## Rename to .bil and make .hdr
    bilfile = filename.replace(".", "_")[:-3] + ".bil"
    command = "ren " + filename + " " + bilfile
    print command
    os.system(command)
    command = "perl vicar2world.pl -c " + bilfile
    print command
    os.system(command)
    
    ## Make .prj
    f = open(bilfile, "r")
    data = f.read(5000)
    data = data.split(" ")
    for item in data:
        if "CENTER_LONGITUDE" in item:
            clon = item.strip().split("=")[1]
    proj = '''PROJCS["Mars_Sinusoidal",GEOGCS["Mars",DATUM["D_Mars",SPHEROID["Mars",3396000.0,0.0]],PRIMEM["Greenwich",0.0],UNIT["Decimal_Degree",0.0174532925199433]],PROJECTION["Sinusoidal"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",%s],UNIT["Meter",1.0]]''' % (clon)
    f.close()
    projfile = bilfile.replace("bil", "prj")
    print "Writing:", projfile
    o = open(projfile, "w")
    o.write(proj)
    o.close()
    
    ## Make .tif or .jp2
    if "dt4" in bilfile:
        ext = "tif"
        command = 'gdal_translate -of GTiff -a_srs "ESRI::%s" -of %s %s %s' % (projfile, format, bilfile, bilfile.replace("bil", "tif"))
        print command
        os.system(command)        
    if "nd4" in bilfile:
        ext = "jp2"
        command = 'gdalwarp -of GTiff -s_srs "ESRI::%s" -t_srs "ESRI::Noachis_Stereographic_Sphere.prj" %s %s' % (projfile, bilfile, bilfile.replace(".bil", "_stereo.tif"))
        print command
        os.system(command)
        command = 'gdal_translate -of JP2OpenJPEG %s %s' % (bilfile.replace(".bil", "_stereo.tif"), bilfile.replace(".bil", "_stereo.jp2"))
        print command
        os.system(command)
        os.unlink(bilfile.replace(".bil", "_stereo.tif"))
    arcpy.CalculateStatistics_management(bilfile.replace(".bil", "_stereo." + ext))
    arcpy.BuildPyramids_management(bilfile.replace(".bil", "_stereo." + ext))
    arcpy.MakeRasterLayer_management(bilfile.replace(".bil", "_stereo." + ext), bilfile.replace(".bil", "_stereo"))
    arcpy.SaveToLayerFile_management(bilfile.replace(".bil", "_stereo"), bilfile.replace(".bil", "_stereo.lyr"), "ABSOLUTE")
    arcpy.ApplySymbologyFromLayer_management(bilfile.replace(".bil", "_stereo.lyr"), ext + ".lyr")
