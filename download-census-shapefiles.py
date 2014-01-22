''' 
Download selected census shapefiles, unzip them in directories named by state abbreviation

fips.csv looks like this:
statename,code,twoletter                                                                                                                                                              
Alabama,1,AL    
Alaska,2,AK
Arizona,4,AZ
Arkansas,5,AR
'''
 

import urllib
import csv
import sys
import os

fips_csv = csv.DictReader(open('fips-.csv', 'rU'), dialect='excel')

for row in fips_csv:
    stateabbrev = row['twoletter']
#    statename = row['statename'].upper().replace(' ','_')
    statecode = row['code'].zfill(2)
    filename_congress =  'tl_rd13_' + statecode + '_cd113.zip'
    filename_upper =  'tl_rd13_' + statecode + '_sldu.zip'
    filename_lower =  'tl_rd13_' + statecode + '_sldl.zip'
    url_congress = 'http://www2.census.gov/geo/tiger/TIGERrd13_st/' + statecode + '/' + filename_congress
    url_upper = 'http://www2.census.gov/geo/tiger/TIGERrd13_st/' + statecode + '/' + filename_upper
    url_lower = 'http://www2.census.gov/geo/tiger/TIGERrd13_st/' + statecode + '/' + filename_lower
      
    if not os.path.exists(stateabbrev):
        os.makedirs(stateabbrev)
    print 'getting ' + url_congress + ' ('+stateabbrev+')'
    try:
        urllib.urlretrieve(url_congress, stateabbrev + '/' +filename_congress)
        urllib.urlretrieve(url_upper, stateabbrev + '/' +filename_upper)
        urllib.urlretrieve(url_lower, stateabbrev + '/' +filename_lower)

        os.chdir('/home/action/maps/'+stateabbrev)
        os.system('unzip ' + filename_congress)
        os.system('unzip ' + filename_upper)
        os.system('unzip ' + filename_lower)
        os.chdir('/home/action/maps/')
        # os.system('rm ' + filename_congress)
    except:
        print "Unexpected error:", sys.exc_info()[0]
        sys.exc_clear()
