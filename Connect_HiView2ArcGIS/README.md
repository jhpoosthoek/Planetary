# Connect HiView to ArcGIS
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

In a similar way HiView could be connected to QGIS and Google Earth. Please let me know if you would find that handy.
