# Planetary
All my planetary science related tools

# CRISM_WCPS_ScatterPlot
![ScatterPlot](https://raw.githubusercontent.com/jhpoosthoek/Planetary/master/CRISM_WCPS_ScatterPlot/scatter.png)

Example how to access CRISM data on PlanetServer (www.planetserver.eu). The values for three bands are extracted and shown in a matplotlib scatter plot

# BufferedCraterCounting
Buffered Crater Counting, following the technique by Fasset and Head (2008). It creates an SSC file for CraterStats. It needs ArcGIS 10+ to run.

After:
Fassett, C.I., Head, J.W., 2008. The timing of martian valley network activity: Constraints from buffered crater counting. Icarus 195, 61-89.

# DTM Minus Scale
![MOLA Example](https://raw.githubusercontent.com/jhpoosthoek/Planetary/master/DTMMinusScale/MOLAExample.jpg)
DTMMinusScale generates a smoothed interpolated version of a DTM and subtracts this from the DTM. The cellfactor is the smoothing factor. The above example is the MOLA data after a 256x smaller scale version was subtracted. The result clearly shows the morphology of the Hellas basin. This would normally not be visible when looking at the standard MOLA data in ArcGIS. It needs ArcGIS 10+ to run.
