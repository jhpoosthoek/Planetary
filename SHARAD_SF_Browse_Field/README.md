# SHARAD browse images in ArcGIS
This script adds a BROWSEURL field in the PDS ODE SHARAD RDR footprint shapefile:
 - http://ode.rsl.wustl.edu/mars/datafile/derived_products/coverageshapefiles/mars/mro/sharad/rdr/mars_mro_sharad_rdr_c0l.zip
 - OR:
 - http://ode.rsl.wustl.edu/mars/datafile/derived_products/coverageshapefiles/mars/mro/sharad/usrdr/mars_mro_sharad_usrdr_c0l.zip
 
When you open this shapefile in ArcGIS you can set the BROWSEURL field to open as a URL hyperlink:
![BROWSEURLhyperlink](https://raw.githubusercontent.com/jhpoosthoek/Planetary/master/SHARAD_SF_Browse_Field/BROWSEURLhyperlink.jpg)

This allows you to click on a line in ArcGIS by using the Hyperlink button (lightning icon). The script needs GDAL/OGR and https://github.com/jhpoosthoek/Python-shapefile-class/ to run.
