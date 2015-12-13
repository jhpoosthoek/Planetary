Connect HiView to GIS software
===========

This method allows you to find HiRISE images of your liking on a map in a GIS (ArcGIS or QGIS) and open the full resolution HiRISE JP2 image in HiView using JPIP

# HiView and HiRISE footprints
 - Install HiView: http://www.uahirise.org/hiview/
 - Download the latest HiRISE footprints shapefile from the Mars Orbital Data Explorer:http://ode.rsl.wustl.edu/mars/datafile/derived_products/coverageshapefiles/mars/mro/hirise/rdrv11/mars_mro_hirise_rdrv11_c0a.zip

# Connect HiView to ArcGIS
 - Add the HiRISE footprints shapefile to ArcMap.
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

# Connect HiView to QGIS
 - Add the HiRISE footprints shapefile to QGIS
 - Go to Layer Properties of the HiRISE footprints shapefile and go to the Actions tab.
 - Make a new Generic Action, name it HiView and set the following in the Action field:
```
"C:/Program Files/HiView/HiView.exe" -Image [% "Ext2URL" %]
```
![QGIS_Action](https://raw.githubusercontent.com/jhpoosthoek/Planetary/master/Connect_HiView2GIS/QGIS_Action.jpg)
 - Click on 'Add to action list' and close the Layer Properties window.
 - Now click on the Run Feature Action button and select HiView.
![QGIS_RunFeatureActionButton](https://raw.githubusercontent.com/jhpoosthoek/Planetary/master/Connect_HiView2GIS/QGIS_RunFeatureActionButton.jpg)
 - If you now click on a HiRISE footprint HiView will load showing the full resolution image.
 
# Final note
 - The color HiRISE footprint might be behind the larger greyscale footprint. It is best to make the polygon style semitransparent or only show the border.