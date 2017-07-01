import sqlite3
import json
import codecs

cnct = sqlite3.connect('akEnergyDb.sqlite')
cur = cnct.cursor()

#Pull all data from the DB
cur.execute('SELECT * FROM Community')

# Write the JSON file for the data retrieved
fileHandle = codecs.open('where.js', 'w', "utf-8")
fileHandle.write("myData = [\n")

count = 0
for row in cur :
    try:
        #TODO work on encoding for Utqiagvik
        where = str(row[1].replace('\n',''))
    except:
        print 'Could not include: ', row[1].replace('\n','')
        continue

    lat = row[3]
    lng = row[4]
    # pop is in row 5 in actual DB
    population = row[5]
    rateResidential = row[6]
    ratePCE = row[7]


    try :
        #print where, lat, lng

        count = count + 1
        if count > 1 : fileHandle.write(",\n")
        output = "["+str(lat)+","+str(lng)+", '"+where+"', " +str(population)+ ", " +str(rateResidential)+", " +str(ratePCE)+"]"
        fileHandle.write(output)
    except:
        continue

fileHandle.write("\n];\n")
cur.close()
fileHandle.close()
print count, "records written to where.js"
print "Open where.html to view the data in a browser"

