from shapefile import shapefile
import sys

sfname = "mars_mro_sharad_usrdr_c0l.shp"

insf = shapefile("read", sfname)
outfieldslist = []
for line in insf.fieldslist:
    outfieldslist.append(line)
outfieldslist.append(['BROWSEURL',4,254,0])

outsf = shapefile("write", sfname[:-4] + "_browse.shp", insf.type, outfieldslist, insf.projection)
featurelist = insf.feats2list()

for features in featurelist:
    feature = features[0]
    table = features[1]
    labelurl = table['LabelURL']
    url = labelurl.replace("rgram.lbl","thm.jpg")
    url = url.replace("data/rgram","browse/thm")
    table['BROWSEURL'] = url
    outsf.createfeatfromlist(feature, table)
outsf.finish()
insf.finish()
