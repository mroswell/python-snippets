import urllib
import csv
import sys
import os
import exceptions
import re

makedirs = lambda x: os.path.exists(x) or os.makedirs(x)

TIGER_SHAPE_TYPES = {
    'congress': 'cd113',
    'upper': 'sldu',
    'lower': 'sldl',
}
TIGER_DISTRICTS_URL_BASE = 'http://www2.census.gov/geo/tiger/TIGERrd13_st'
OGR2OGR = '/Library/Frameworks/GDAL.framework/Versions/Current/Programs/ogr2ogr'
OGRINFO = '/Library/Frameworks/GDAL.framework/Versions/Current/Programs/ogrinfo'

mkOGR_NAD84_2_webm_cmd = lambda src, dst: (OGR2OGR + ' -f "ESRI Shapefile" '+dst +' '+ src + ' -s_srs "EPSG:4269" -t_srs "EPSG:3857" -overwrite' )
DOWNLOAD_DIR = os.path.expanduser('~/Desktop/ogr2ogr-tests/downloads'); makedirs(DOWNLOAD_DIR)
WEBM_DIR = os.path.expanduser('~/Desktop/ogr2ogr-tests/overlays'); makedirs(WEBM_DIR)
TMP_DIR = os.path.expanduser('~/Desktop/ogr2ogr-tests/tmp'); makedirs(TMP_DIR)

# The full fips.csv file is here (below the python script)
# http://vvanhee.wordpress.com/2012/01/25/download-all-u-s-census-block-shapefiles/
fips_csv = csv.DictReader(open('overlays.csv', 'rU'), dialect='excel')

for row in fips_csv:
    stateabbrev = row['twoletter']
#    statename = row['statename'].upper().replace(' ','_')
    statefips = row['code'].zfill(2)


    statedownloads = os.path.join(DOWNLOAD_DIR, stateabbrev)
    makedirs(statedownloads)
    os.chdir(statedownloads)
    webmaps = os.path.join(WEBM_DIR, stateabbrev)
    makedirs(webmaps)

    for stype in TIGER_SHAPE_TYPES.itervalues():
        filename = 'tl_rd13_%(statefips)s_%(stype)s' % {'statefips': statefips, 'stype': stype, }
        fullfilename = (os.path.join(DOWNLOAD_DIR, stateabbrev, filename))
        webmapname = (os.path.join(webmaps, filename))

        print(fullfilename+".shp")
        url = '%(base)s/%(statefips)s/%(filename)s.zip' % { 'base': TIGER_DISTRICTS_URL_BASE, 'statefips': statefips, 'filename': filename, }
        print(url)
        print 'getting %(url)s (%(stateabbrev)s)' % {'url': url, 'stateabbrev': stateabbrev, }

        try:
            urllib.urlretrieve(url, filename + ".zip")
            os.system('unzip ' + filename + ".zip")
            os.system(OGR2OGR + ' -f "ESRI Shapefile" '+webmapname +'.shp '+ filename + '.shp -s_srs "EPSG:4269" -t_srs "EPSG:3857" -overwrite' )

#        except:
#            print "Unexpected error:", sys.exc_info()[0]
#            sys.exc_clear()
#        except (NameError,),e:
#            print re.findall("name '(\w+)' is not defined",str(e))[0]
        except exceptions.NameError, e:
            print e

