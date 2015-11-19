# SHARAD 2 KMZ
Prerequisites:
```python
from PIL import Image # http://www.pythonware.com/products/pil/
import numpy as NX # http://www.scipy.org/Download
from GreatCircle import GreatCircle # https://pyroms.googlecode.com/svn-history/r39/trunk/pyroms/greatcircle.py
```

Usage:
 - Open in a GIS: http://ode.rsl.wustl.edu/mars/datafile/derived_products/coverageshapefiles/mars/mro/sharad/usrdr/mars_mro_sharad_usrdr_c0l.zip
 - Select a footprint line and copy the LabelURL text
 - In the terminal/command prompt do, for example:
```
python sharad2kmz.py http://pds-geosciences.wustl.edu/mro/mro-m-sharad-5-radargram-v1/mrosh_2001/data/rgram/s_0183xx/s_01833102_rgram.lbl
```
 - This will generate a KMZ which you can open in Google Earth:

![SHARADinGE](https://raw.githubusercontent.com/jhpoosthoek/Planetary/master/SHARAD2KMZ/SHARADinGE.jpg)
