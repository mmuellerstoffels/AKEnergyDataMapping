import urllib
import sqlite3
import energySpiderHelpers
import re
from urlparse import urljoin
from urlparse import urlparse
from BeautifulSoup import *

# Setup database
cnct = sqlite3.connect('akEnergyDb.sqlite')
cur = cnct.cursor()

cur.executescript('''
    DROP TABLE IF EXISTS Community;
    DROP TABLE IF EXISTS Units;
    
    CREATE TABLE Community (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        name TEXT UNIQUE,
        identifier INTEGER,
        latitude REAL,
        longitude REAL,
        population INTEGER,
        rateResidential REAL,
        ratePCE REAL
    );
    
    CREATE TABLE Units (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        rateResidentialUnits TEXT
    );
''')

# Retrieve overview data from the Alaska Energy Data Gateway
urlMain = 'https://akenergygateway.alaska.edu/'
mainGate = urllib.urlopen(urlMain).read()

mainData = BeautifulSoup(mainGate)

communityList = mainData('option')



for community in communityList:
    if community.get('value',None) == '':continue
    identifier = int(community.get('value', None))
    name = community.text

    #cur.execute('''INSERT OR IGNORE INTO Community (name, identifier)
    #    VALUES ( ? , ? ) ''', (name,identifier ) )
    #cur.execute('''SELECT id FROM Community WHERE name = ?''', (name,))

    siteUrl = urlMain + '/community-data-summary/' + str(identifier)
    siteHtml = urllib.urlopen(siteUrl).read()
    siteData = BeautifulSoup(siteHtml)

    siteTables = siteData('tr')

    for tab in siteTables:
        children = tab.findChildren()
        for child in children:
            if child.text == 'Latitude, Longitude':
                latlon = energySpiderHelpers.handleCoordinates(child.findNextSibling().text)
                #lat = re.findall('([0-9\.]+)\,', latlon, 0)
                #lon = re.findall('\, ([\-0-9\.]+)', latlon, 0)
            elif child.text.split(' ', 1)[0] == 'Population' and child.text != 'Population by Age and Sex':
                try:
                    population = int(child.findNextSibling().text)
                except:
                    population = -9999
            elif child.text == 'Residential Rate':
                rateResidential = float(energySpiderHelpers.handleRate(child.findNextSibling().text)[0])
                print rateResidential
            elif child.text == 'PCE Rate':
                ratePCE = float(energySpiderHelpers.handleRate(child.findNextSibling().text)[0])
    cur.execute('''INSERT OR IGNORE INTO Community 
                    (name, identifier, latitude, longitude, population, rateResidential, ratePCE)
                    VALUES ( ? , ? , ? , ? , ? , ? , ? ) ''',
                    (name, identifier, latlon[0], latlon[1], population, rateResidential, ratePCE))
    cur.execute('''SELECT id FROM Community WHERE name = ?''', (name,))
    print name, latlon[0], latlon[1], population



    cnct.commit()

