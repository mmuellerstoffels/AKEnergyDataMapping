import re

# helper functions
def handleCoordinates(inputString):
    lat = re.findall('([0-9\.]+)\,', inputString, 0)
    lon = re.findall('\, ([\-0-9\.]+)', inputString, 0)
    return (lat[0],lon[0])

# $0.63 per kWh, Dec 2013
def handleRate(inputString):
    rate = re.findall('\$([0-9\.]+) ', inputString, 0)
    return rate