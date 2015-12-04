ArcGIS Python Console Snippets
===========

CTX footprints, read labels to make a 'wget' download list file
```python
import pythonaddins
SelectedLayer = pythonaddins.GetSelectedTOCLayerOrDataFrame()
for row in arcpy.SearchCursor(SelectedLayer):
    print row.LabelURL
```

Used to create my crater map.
```python
import pythonaddins
SelectedLayer = pythonaddins.GetSelectedTOCLayerOrDataFrame()
desc = arcpy.Describe(SelectedLayer)
if not desc.FIDSet  == '':
    with arcpy.da.UpdateCursor(SelectedLayer, ["DESTROYED"]) as cursor:
        for row in cursor:
            row[0] = 1
            cursor.updateRow(row)
    arcpy.SelectLayerByAttribute_management(SelectedLayer, "CLEAR_SELECTION")
    arcpy.RefreshActiveView()
```

Used to download CTX browse images provided by ASU
```python
import pythonaddins
SelectedLayer = pythonaddins.GetSelectedTOCLayerOrDataFrame()
for row in arcpy.SearchCursor(SelectedLayer):
    LabelURL = row.LabelURL.strip()
    BrowseURL = "http://global-data.mars.asu.edu/map/ctx_new/%s/prj_browse/%s.jpg" % (LabelURL[73:82],LabelURL[88:-4])
    print BrowseURL
```
