# Select and download JMars CTX JP2 using ArcGIS

1. Save attached jmarsctx.py to the location where you want to download the CTX JP2.
2. Make sure you have wget in your windows path (download from: http://gnuwin32.sourceforge.net/packages/wget.htm)
3. Add the ODE footprints for CTX to ArcGIS: http://ode.rsl.wustl.edu/mars/datafile/derived_products/coverageshapefiles/mars/mro/ctx/edr/mars_mro_ctx_edr_c0a.zip
4. Select the footprints you want with the 'select features' button in ArcGIS.
5. Select the footprint shapefile in the ArcGIS TOC.
6. In the python console add:
```python
import pythonaddins
SelectedLayer = pythonaddins.GetSelectedTOCLayerOrDataFrame()
for row in arcpy.SearchCursor(SelectedLayer):
    print row.LabelURL.strip()
```
7. Copy the results to a text file like 'download.txt'.
8. In the command line (which is set to run the python which came with ArcGIS) type:
```
python jmarsctx.py download.txt
```
9. You can also use it to single download a CTX, for example:
```
python jmarsctx.py http://pds-imaging.jpl.nasa.gov/data/mro/mars_reconnaissance_orbiter/ctx/mrox_1594/data/G22_026719_1952_XN_15N028W.IMG
```
