"""
SHARAD 2 KMZ python script
Jelmer Oosthoek
jhpoosthoek@gispla.net
"""

# imports available in python
from math import cos,acos,radians,degrees,sin,asin,pi
import os
import sys
import urllib
import zipfile
import tempfile

# other imports
from PIL import Image # http://www.pythonware.com/products/pil/
import numpy as NX # http://www.scipy.org/Download
from GreatCircle import GreatCircle # https://pyroms.googlecode.com/svn-history/r39/trunk/pyroms/greatcircle.py

def lllength(lat1,lon1,lat2,lon2,radius_sphere):
    """
    Code to find the length on a sphere between two lat/lon pairs.
    
    Code originally from: http://jsp.vs19.net/lr/sphere-distance.php
    """
    
    p1 = cos(radians(lon1-lon2))
    p2 = cos(radians(lat1-lat2))
    p3 = cos(radians(lat1+lat2))
    return acos(((p1*(p2+p3))+(p2-p3))/2) * radius_sphere

def calcheading(lat1,lon1,lat2,lon2,radius_sphere):
    """
    Find the heading between two lat/lon pairs.
    
    Code originally from http://www.ac6v.com/greatcircle.htm
    
    A = YOUR latitude in degrees.
    B = latitude of the other location in degrees.
    L = YOUR longitude minus that of the other location. (Algebraic difference.)
    D = Distance along path in degrees of arc.
    C = True bearing from north if the value for sin(L) is positive.  If
    sin(L) is negative, true bearing is 360 - C.
    """
    
    A = radians(lat1)
    B = radians(lat2)
    L = radians(lon1) - radians(lon2)
    D = acos((sin(A) * sin(B)) + (cos(A) * cos(B) * cos(L)))
    C = acos((sin(B) - (sin(A) * cos(D))) / (cos(A) * sin(D)))
    
    if sin(L) < 0:
        C = (pi * 2) - C
    
    return 180 - degrees(C)

def writekml(kmlfile,name,lon,lat,heading,scale):
    """
    Write a KML file. The template was originally created using Google Sketchup.
    """
    
    content = "".join(("<?xml version='1.0' encoding='UTF-8'?>\n",
    "<kml xmlns='http://earth.google.com/kml/2.1' hint='target=mars'>\n",
    "<Folder>\n",
    "    <name>SHARAD</name>\n",
    "    <description><![CDATA[Created by Jelmer Oosthoek]]></description>\n",
    "    <DocumentSource></DocumentSource>\n",
    "<visibility>1</visibility>\n",
    "  <Placemark>\n",
    "    <name>" + name + "</name>\n",
    "    <description><![CDATA[]]></description>\n",
    "    <Style id='default'>\n",
    "    </Style>\n",
    "    <Model>\n",
    "        <altitudeMode>relativeToGround</altitudeMode>\n",
    "        <Location>\n",
    "            <longitude>" + str(lon) + "</longitude>\n",
    "            <latitude>" + str(lat) + "</latitude>\n",
    "            <altitude>0.000000000000</altitude>\n",
    "        </Location>\n",
    "        <Orientation>\n",
    "            <heading>" + str(heading) + "</heading>\n",
    "            <tilt>0</tilt>\n",
    "            <roll>0</roll>\n",
    "        </Orientation>\n",
    "        <Scale>\n",
    "            <x>" + str(scale) + "</x>\n",
    "            <y>" + str(scale) + "</y>\n",
    "            <z>" + str(scale) + "</z>\n",
    "        </Scale>\n",
    "        <Link>\n",
    "            <href>models/profile.dae</href>\n",
    "        </Link>\n",
    "    </Model>\n",
    "  </Placemark></Folder>\n",
    "</kml>"))
    writeFile(content,kmlfile)

def daewrite(daefile, filename, width, height):
    """
    Write a COLLADA DAE file. The template was originally created using Google Sketchup.
    """
    
    content = "".join(("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n",
    "<COLLADA xmlns=\"http://www.collada.org/2005/11/COLLADASchema\" version=\"1.4.1\">\n",
    "   <asset>\n",
    "      <contributor>\n",
    "         <authoring_tool>Python</authoring_tool>\n",
    "      </contributor>\n",
    "      <created></created>\n",
    "      <modified></modified>\n",
    "      <unit name=\"meter\" meter=\"1\"/>\n",
    "      <up_axis>Z_UP</up_axis>\n",
    "   </asset>\n",
    "   <library_images>\n",
    "      <image id=\"material0-image\" name=\"material0-image\">\n",
    "         <init_from>../images/" + filename + ".jpg</init_from>\n",
    "      </image>\n",
    "   </library_images>\n",
    "   <library_materials>\n",
    "      <material id=\"material0ID\" name=\"material0\">\n",
    "         <instance_effect url=\"#material0-effect\"/>\n",
    "      </material>\n",
    "   </library_materials>\n",
    "   <library_effects>\n",
    "      <effect id=\"material0-effect\" name=\"material0-effect\">\n",
    "         <profile_COMMON>\n",
    "            <newparam sid=\"material0-image-surface\">\n",
    "               <surface type=\"2D\">\n",
    "                  <init_from>material0-image</init_from>\n",
    "               </surface>\n",
    "            </newparam>\n",
    "            <newparam sid=\"material0-image-sampler\">\n",
    "               <sampler2D>\n",
    "                  <source>material0-image-surface</source>\n",
    "               </sampler2D>\n",
    "            </newparam>\n",
    "            <technique sid=\"COMMON\">\n",
    "               <phong>\n",
    "                  <emission>\n",
    "                     <color>0.000000 0.000000 0.000000 1</color>\n",
    "                  </emission>\n",
    "                  <ambient>\n",
    "                     <color>0.000000 0.000000 0.000000 1</color>\n",
    "                  </ambient>\n",
    "                  <diffuse>\n",
    "                     <texture texture=\"material0-image-sampler\" texcoord=\"UVSET0\"/>\n",
    "                  </diffuse>\n",
    "                  <specular>\n",
    "                     <color>0.330000 0.330000 0.330000 1</color>\n",
    "                  </specular>\n",
    "                  <shininess>\n",
    "                     <float>20.000000</float>\n",
    "                  </shininess>\n",
    "                  <reflectivity>\n",
    "                     <float>0.100000</float>\n",
    "                  </reflectivity>\n",
    "                  <transparent>\n",
    "                     <color>1 1 1 1</color>\n",
    "                  </transparent>\n",
    "                  <transparency>\n",
    "                     <float>0.000000</float>\n",
    "                  </transparency>\n",
    "               </phong>\n",
    "            </technique>\n",
    "         </profile_COMMON>\n",
    "      </effect>\n",
    "   </library_effects>\n",
    "   <library_geometries>\n",
    "      <geometry id=\"mesh1-geometry\" name=\"mesh1-geometry\">\n",
    "         <mesh>\n",
    "            <source id=\"mesh1-geometry-position\">\n",
    "               <float_array id=\"mesh1-geometry-position-array\" count=\"12\">0.000000 -" + str(height / 2) + " 0.000000 0.000000 -" + str(height / 2) + " " + str(width) + " 0.000000 " + str(height / 2) + " 0.000000 0.000000 " + str(height / 2) + " " + str(width) + " </float_array>\n",
    "               <technique_common>\n",
    "                  <accessor source=\"#mesh1-geometry-position-array\" count=\"4\" stride=\"3\">\n",
    "                     <param name=\"X\" type=\"float\"/>\n",
    "                     <param name=\"Y\" type=\"float\"/>\n",
    "                     <param name=\"Z\" type=\"float\"/>\n",
    "                  </accessor>\n",
    "               </technique_common>\n",
    "            </source>\n",
    "            <source id=\"mesh1-geometry-normal\">\n",
    "               <float_array id=\"mesh1-geometry-normal-array\" count=\"6\">-1.000000 0.000000 0.000000 1.000000 0.000000 0.000000 </float_array>\n",
    "               <technique_common>\n",
    "                  <accessor source=\"#mesh1-geometry-normal-array\" count=\"2\" stride=\"3\">\n",
    "                     <param name=\"X\" type=\"float\"/>\n",
    "                     <param name=\"Y\" type=\"float\"/>\n",
    "                     <param name=\"Z\" type=\"float\"/>\n",
    "                  </accessor>\n",
    "               </technique_common>\n",
    "            </source>\n",
    "            <source id=\"mesh1-geometry-uv\">\n",
    "               <float_array id=\"mesh1-geometry-uv-array\" count=\"8\">-1 0.000000 -1 1 0.000000 0.000000 0.000000 1 </float_array>\n",
    "               <technique_common>\n",
    "                  <accessor source=\"#mesh1-geometry-uv-array\" count=\"4\" stride=\"2\">\n",
    "                     <param name=\"S\" type=\"float\"/>\n",
    "                     <param name=\"T\" type=\"float\"/>\n",
    "                  </accessor>\n",
    "               </technique_common>\n",
    "            </source>\n",
    "            <vertices id=\"mesh1-geometry-vertex\">\n",
    "               <input semantic=\"POSITION\" source=\"#mesh1-geometry-position\"/>\n",
    "            </vertices>\n",
    "            <triangles material=\"material0\" count=\"4\">\n",
    "               <input semantic=\"VERTEX\" source=\"#mesh1-geometry-vertex\" offset=\"0\"/>\n",
    "               <input semantic=\"NORMAL\" source=\"#mesh1-geometry-normal\" offset=\"1\"/>\n",
    "               <input semantic=\"TEXCOORD\" source=\"#mesh1-geometry-uv\" offset=\"2\" set=\"0\"/>\n",
    "               <p>0 0 0 1 0 1 2 0 2 2 1 2 1 1 1 0 1 0 3 0 3 2 0 2 1 0 1 1 1 1 2 1 2 3 1 3 </p>\n",
    "            </triangles>\n",
    "         </mesh>\n",
    "      </geometry>\n",
    "   </library_geometries>\n",
    "   <library_cameras>\n",
    "      <camera id=\"Camera-camera\" name=\"Camera-camera\">\n",
    "         <optics>\n",
    "            <technique_common>\n",
    "               <perspective>\n",
    "                  <xfov>46.666667</xfov>\n",
    "                  <yfov>35.000000</yfov>\n",
    "                  <znear>1.000000</znear>\n",
    "                  <zfar>1000.000000</zfar>\n",
    "               </perspective>\n",
    "            </technique_common>\n",
    "         </optics>\n",
    "      </camera>\n",
    "   </library_cameras>\n",
    "   <library_visual_scenes>\n",
    "      <visual_scene id=\"SketchUpScene\" name=\"SketchUpScene\">\n",
    "         <node id=\"Model\" name=\"Model\">\n",
    "            <node id=\"mesh1\" name=\"mesh1\">\n",
    "               <instance_geometry url=\"#mesh1-geometry\">\n",
    "                  <bind_material>\n",
    "                     <technique_common>\n",
    "                        <instance_material symbol=\"material0\" target=\"#material0ID\">\n",
    "                           <bind_vertex_input semantic=\"UVSET0\" input_semantic=\"TEXCOORD\" input_set=\"0\"/>\n",
    "                        </instance_material>\n",
    "                     </technique_common>\n",
    "                  </bind_material>\n",
    "               </instance_geometry>\n",
    "            </node>\n",
    "         </node>\n",
    "         <node id=\"Camera\" name=\"Camera\">\n",
    "            <matrix>\n",
    "               0.903474 0.059047 -0.424557 -2151.311302\n",
    "               -0.428643 0.124457 -0.894861 -6797.912539\n",
    "               0.000000 0.990467 0.137753 680.201057\n",
    "               0.000000 0.000000 0.000000 1.000000\n",
    "            </matrix>\n",
    "            <instance_camera url=\"#Camera-camera\"/>\n",
    "         </node>\n",
    "      </visual_scene>\n",
    "   </library_visual_scenes>\n",
    "   <scene>\n",
    "      <instance_visual_scene url=\"#SketchUpScene\"/>\n",
    "   </scene>\n",
    "</COLLADA>"))
    writeFile(content, daefile)

def writeFile(content, fileName):
    """
    Made by Roderik Koenders
    Writes a file with name.extension and content.
    """
    with open(fileName, 'w') as f:
        for line in content.splitlines():
            f.write("%s\n" % line)

"""
MAIN code
"""

# variables
lblurl = sys.argv[1]
tempdir = tempfile.mkdtemp()
jpgurl = lblurl.replace("rgram.lbl","thm.jpg")
jpgurl = jpgurl.replace("data/rgram","browse/thm")
lblurl = jpgurl.replace(".jpg", ".lbl")
name = os.path.basename(jpgurl)[:-4]
radius_sphere = 3396190
outputdir = os.getcwd()

# download and open the label and read lat/lon:
h = urllib.urlretrieve(lblurl, tempdir + "/" + name + ".lbl")
print "Downloading " + name + ".lbl and extracting coordinates"
input = open(tempdir + "/" + name + ".lbl","r")
for line in input:
    line = line.strip()
    if line[:34] == "MRO:START_SUB_SPACECRAFT_LONGITUDE":
        outcoord = line[37:].split(" ")[0]
        lon1 = float(outcoord)
    if line[:33] == "MRO:START_SUB_SPACECRAFT_LATITUDE":
        outcoord = line[37:].split(" ")[0]
        lat1 = float(outcoord)
    if line[:33] == "MRO:STOP_SUB_SPACECRAFT_LONGITUDE":
        outcoord = line[37:].split(" ")[0]
        lon2 = float(outcoord)
    if line[:32] == "MRO:STOP_SUB_SPACECRAFT_LATITUDE":
        outcoord = line[37:].split(" ")[0]
        lat2 = float(outcoord)
input.close()

# find the middle lat/lon using the GreatCircle class:
gc = GreatCircle(radius_sphere,radius_sphere,lon1,lat1,lon2,lat2)
lons,lats = gc.points(3)
midlon = lons[1]
midlat = lats[1]
print "Center Longitude = " + str(midlon)
print "Center Latitude  = " + str(midlat)

# calculate the heading:
##    if lat2 >= lat1:
##        heading = calcheading(midlat,midlon,lat2,lon2,radius_sphere)
##    else:
heading = calcheading(midlat,midlon,lat1,lon1,radius_sphere)
print "Heading = " + str(heading)

# download the browse image using urllib in the images folder:
print "Downloading " + name + ".jpg"
os.mkdir(tempdir + "/images")
site = urllib.urlopen(jpgurl)
meta = site.info()
urlExists = str(meta).find("Content-Length:")
if urlExists < 0:
    sys.exit()
h = urllib.urlretrieve(jpgurl, tempdir + "/images/" + name + ".jpg")

# get the width/height using the Image module
im = Image.open(tempdir + "/images/" + name + ".jpg")
(width, height) = im.size
del im
print "Image width, height = " + str(width) + ", " + str(height)

# use the input lons/lats to get the length on the Mars globe
length = lllength(lat1,lon1,lat2,lon2,radius_sphere)
print "The length on the Mars globe = " + str(length)

# calculate the scale:
scale = length / width
print "The scale = " + str(scale)

# writing profile.dae, doc.kml and textures.txt:
print "Creating the KMZ contents"
writekml(tempdir + "/doc.kml",name,midlon,midlat,heading,scale)
os.mkdir(tempdir + "/models")
daewrite(tempdir + "/models/profile.dae", name, height, width)
text = open(tempdir + "/textures.txt","w")
text.write("<../images/" + name + ".jpg> <../images/" + name + ".jpg>")
text.close()

# create the KMZ using the zipfile module
print "Creating %s.kmz" % (name)
zout = zipfile.ZipFile(outputdir + "/" + name + ".kmz", "w")
zout.write(tempdir + "/doc.kml","doc.kml")
zout.write(tempdir + "/images/" + name + ".jpg","images/" + name + ".jpg")
zout.write(tempdir + "/models/profile.dae","models/profile.dae")
zout.write(tempdir + "/textures.txt","textures.txt")
zout.close()

# delete unnecessary data and remove folders
print "Deleting temporary files"
os.unlink(tempdir + "/" + name + ".lbl")
os.unlink(tempdir + "/doc.kml")
os.unlink(tempdir + "/textures.txt")
os.unlink(tempdir + "/images/" + name + ".jpg")
os.unlink(tempdir + "/models/profile.dae")
os.rmdir(tempdir + "/images")
os.rmdir(tempdir + "/models")
os.rmdir(tempdir)
