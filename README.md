# Planetary
All my planetary science related tools

# CRISM_WCPS_ScatterPlot
![ScatterPlot](https://raw.githubusercontent.com/jhpoosthoek/Planetary/master/CRISM_WCPS_ScatterPlot/scatter.png)

Example how to access CRISM data on PlanetServer (www.planetserver.eu). The values for three bands are extracted and shown in a matplotlib scatter plot

# BufferedCraterCounting
Buffered Crater Counting, following the technique by Fasset and Head (2008). It creates an SSC file for CraterStats.
It needs ArcGIS 10+, GDAL/OGR and https://github.com/jhpoosthoek/Python-shapefile-class/ to run.

After:
Fassett, C.I., Head, J.W., 2008. The timing of martian valley network activity: Constraints from buffered crater counting. Icarus 195, 61-89.

# DTM Minus Scale
![MOLA Example](https://raw.githubusercontent.com/jhpoosthoek/Planetary/master/DTMMinusScale/MOLAExample.jpg)
DTMMinusScale generates a smoothed interpolated version of a DTM and subtracts this from the DTM. The cellfactor is the smoothing factor. The above example is the MOLA data after a 256x smaller scale version was subtracted. The result clearly shows the morphology of the Hellas basin. This would normally not be visible when looking at the standard MOLA data in ArcGIS. It needs ArcGIS 10+ to run.

# Make Mask Rasdaman
This CGI script was made for www.planetserver.eu to add the possibility to extract WCPS information within a (irregular) polygon. This way a WCPS derived average CRISM spectrum within a certain polygon (geological layer) could be calculated. Please change line 18 and 98 before use.

# (US) SHARAD SF Browse Field
This script adds a BROWSEURL field in the PDS ODE SHARAD RDR footprint shapefile:
 - http://ode.rsl.wustl.edu/mars/datafile/derived_products/coverageshapefiles/mars/mro/sharad/rdr/mars_mro_sharad_rdr_c0l.zip
 - OR:
 - http://ode.rsl.wustl.edu/mars/datafile/derived_products/coverageshapefiles/mars/mro/sharad/usrdr/mars_mro_sharad_usrdr_c0l.zip
 
When you open this shapefile in ArcGIS you can set the BROWSEURL field to open as a URL hyperlink:
![BROWSEURLhyperlink](https://raw.githubusercontent.com/jhpoosthoek/Planetary/master/SHARAD_SF_Browse_Field/BROWSEURLhyperlink.jpg)

This allows you to click on a line in ArcGIS by using the Hyperlink button. The script needs GDAL/OGR and https://github.com/jhpoosthoek/Python-shapefile-class/ to run.

# Connect HiView to ArcGIS 10
This method allows you to connect within ArcGIS 10 to HiView and load an online JPIP streamed HiRISE JP2 image:
 - Install HiView: http://www.uahirise.org/hiview/
 - Download the latest HiRISE footprints shapefile from the Mars Orbital Data Explorer:http://ode.rsl.wustl.edu/mars/datafile/derived_products/coverageshapefiles/mars/mro/hirise/rdrv11/mars_mro_hirise_rdrv11_c0a.zip
 - Add the shapefile to ArcMap.
Go to Layer Properties > Display. Select 'Support Hyperlinks using field'. Select Script and click on Edit. Add the contents of runhiview.vbscript:
```vbscript
Function OpenLink ( [Ext2URL] )
Dim pathHiView
Dim argHiView
Dim objShell
pathHiView = "C:\\Program Files\\HiView\\HiView.exe"
argHiView =  "-Image " & [Ext2URL]
Set objShell = CreateObject("Shell.Application")
objShell.ShellExecute pathHiView, argHiView, "", "open", 1
End Function
```
 - In ArcGIS click on the Hyperlink button (the lightning icon) and select a footprint.
 - HiView opens and the selected HiRISE image is loaded.