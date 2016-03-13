import os,sys
import arcpy

def betweenstring(string,a,b):
    list = []
    stringsplit = string.split(a)
    if stringsplit != []:
        for item in stringsplit[1:]:
            nr = item.find(b)
            if nr != -1:
                list.append(item.split(b)[0])
    return list

arcpy.env.workspace = os.getcwd()

if len(sys.argv) == 1:
    sys.exit()

input = sys.argv[1]
if "http://" in input:
    list = [input]
else:
    list = open(input).readlines()

for line in list:
    LabelURL = line.strip()
    JP2URL = "http://global-data.mars.asu.edu/map/ctx/%s/prj_full/%s.jp2" % (LabelURL[73:82],LabelURL[88:-4])
    HDR1URL = "http://global-data.mars.asu.edu/map/ctx/%s/stage/%s.scyl.isis.hdr" % (LabelURL[73:82],LabelURL[88:-4])
    HDR2URL = "http://global-data.mars.asu.edu/map/ctx/%s/stage/%s.ps.isis.hdr" % (LabelURL[73:82],LabelURL[88:-4])
    
    if os.path.exists(os.path.basename(JP2URL)):
        print JP2URL + " already exists!"
    else:
        os.system("wget -c " + JP2URL)
        os.system("wget -c " + HDR1URL)
        os.system("wget -c " + HDR2URL)

        STOP = 0
        if os.path.exists(os.path.basename(HDR1URL)):
            f = open(os.path.basename(HDR1URL))
            sp = 0
        elif os.path.exists(os.path.basename(HDR2URL)):
            f = open(os.path.basename(HDR2URL))
            sp = 1
        else:
            STOP = 1

        if STOP == 1:
            print os.path.basename(JP2URL) + " is not part of JMARS (yet)!"
            f = open("jmarsctx.log","a")
            f.write(LabelURL + "\n")
            f.close()
        else:
            data = f.readlines()
            data = "".join(data)
            f.close()

            header = betweenstring(data,"Group = Mapping","End_Group")[0]
            res = betweenstring(header,"PixelResolution    = "," <meters/pixel>")[0]
            ulx = betweenstring(header,"UpperLeftCornerX   = "," <meters>")[0]
            uly = betweenstring(header,"UpperLeftCornerY   = "," <meters>")[0]

            jp2 = open(os.path.basename(JP2URL)[:-4] + ".j2w","w")
            jp2.write("%s\n0\n0\n-%s\n%s\n%s\n" %(res,res,ulx,uly))
            jp2.close()

            proj = 'PROJCS["Mars Equicylindrical clon=180",GEOGCS["GCS_Mars_2000_Ellipse",DATUM["D_Mars_2000_Ellipse",SPHEROID["Mars_2000_Ellipse_IAU_IAG",3396190.0,169.8944472236118]],PRIMEM["Reference_Meridian",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Equidistant_Cylindrical"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",180.0],PARAMETER["Standard_Parallel_1",0.0],UNIT["Meter",1.0]]'

            if sp == 1:
                clon = betweenstring(header,"CenterLongitude    = ","\n")[0]
                clat = betweenstring(header,"CenterLatitude     = ","\n")[0]
                if clat == "90.0":
                    pole = "NP"
                    projtype = "Stereographic_North_Pole"
                else:
                    pole = "SP"
                    projtype = "Stereographic_South_Pole"
                proj = 'PROJCS["Mars %s Stereographic Sphere",GEOGCS["GCS_Mars_2000_Sphere_Polar",DATUM["D_Mars_2000_Sphere_Polar",SPHEROID["Mars_2000_Sphere_Polar",3396190.0,0.0]],PRIMEM["Reference_Meridian",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["%s"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",%s],PARAMETER["Standard_Parallel_1",%s],UNIT["Meter",1.0]]' % (pole,projtype,clon,clat)

            arcpy.DefineProjection_management(os.path.basename(JP2URL), proj)
            arcpy.SetRasterProperties_management(os.path.basename(JP2URL),nodata="1 0")
            arcpy.CalculateStatistics_management(os.path.basename(JP2URL))
            # arcpy.BuildPyramids_management(os.path.basename(JP2URL))