#!/usr/bin/env python

import os
# We move to the local directory so we can read the relevent files
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

from sql import alcsession
import yaml
from bulkammocom import getBulkAmmoComData
from dataProcessor import processData

"""
This is the main file that should be called by cron.
"""

#Import out settings
with open('settings.yaml', 'r') as f:
    doc = yaml.load(f)
    sites = doc['sites']
    urls = doc['urls']

# We loop over all sites in the site list
for site in sites:

    #We loop over urls under site.
    for url in urls[site]:

        #We get the data and log it for bulkammo
        if site == 'bulkammo.com':
            data = getBulkAmmoComData(site,url)
            processData(data)
