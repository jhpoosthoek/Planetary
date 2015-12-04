VICAR HRSC2ArcGIS
===========

Prerequisites: ArcGIS (arcpy) and GDAL (gdal_translate and gdalwarp)

It converts a VICAR labelled HRSC image: DT4 into a TIF, ND4 into a JP2.

It reprojects the data from Sinusoidal to another CRS, in this case stereographic.

It calculates statistics and builds pyramids

It applies layer symbology to the data.

The final result is a .lyr file for each dataset which could open in ArcGIS
