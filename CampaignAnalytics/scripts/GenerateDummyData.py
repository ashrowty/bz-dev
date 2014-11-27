import random
import datetime
import uuid

regionsAndCities = { 
            'NE': ['Boston', 'NYC', 'Edison'], 
            'SE' : ['Miami', 'Orlando', 'Atlanta'], 
            'MW' : ['Cincinnati', 'Pittsburgh', 'Chicao'], 
            'NW' : ['San Francisco', 'Oakland', 'Seattle'] 
           }
catsAndItems = {
                'Dairy' : ['Chocolate Milk', 'Cheddar Cheese', 'Yogurt', 'Butter', 'Ice Cream'],
                'Bakery' : ['Bread', 'Dinner Rolls', 'Muffins', 'Croissants', 'Cakes'],
                'Produce' : ['Potatoes', 'Carrots', 'Spinach', 'Eggplant', 'Onions'],
                'Meat' : ['Sausage', 'Bacon', 'Ground Beef', 'Chicken Breast', 'Turkey'],
                'Cleaning Supplies' : ['Mops', 'Brooms', 'Detergents', 'Brushes', 'Sponge']
                }

header = ['activityId', 'yrMonth', 'compId', 'region', 'storeGrp', 'storeId', 'segment', 'custId', 'channel', 
          'campaignId', 'offerId', 'category', 'itemId', 'zoneId', 'posx',
          'posy', 'beaconId', 'lat', 'lng', 'iarTs', 'iarInd']

segments = ['Gold', 'Premier', 'Affluent', 'Bronze', 'Loyal', 'GenY']
channels = ['Email', 'Web', 'App']
storeGroups = ['Inner City', 'Suburban', 'Mall', 'Urban', 'High Growth']
compIds = [1000, 2000, 3000, 4000]
mfgIds = [8000, 8010, 8020, 8030]
activityInd = ['i', 'r', 'a']
custSegMap = {}
offerCampMap = {}

def getActivity():
    idx = random.randint(0, len(activityInd)-1)
    return activityInd[idx]
    
def getCategory():
    idx = random.randint(0, len(catsAndItems)-1)
    return catsAndItems.keys()[idx]

def getItem(cat):
    idx = random.randint(0, len(catsAndItems)-1)
    return catsAndItems[cat][idx]

def getSegment(custId):
    if custSegMap.has_key(custId):
        return custSegMap[custId]
    idx = random.randint(0, len(segments)-1)
    custSegMap[custId] = segments[idx]
    return segments[idx]

def getStoreGroup():
    idx = random.randint(0, len(storeGroups)-1)
    return storeGroups[idx]

def getRegion():
    idx = random.randint(0, len(regionsAndCities)-1)
    return regionsAndCities.keys()[idx]

def getCompId():
    idx = random.randint(0, len(compIds)-1)
    return compIds[idx]

def getMfgId():
    idx = random.randint(0, len(mfgIds)-1)
    return mfgIds[idx]

def getStoreId(compId):
    return random.randint(compId, compId+999)

def getCustomerId():
    return random.randint(5000, 5010)

def getChannel():
    idx = random.randint(0, len(channels)-1)
    return channels[idx]

def getCampaignId(offerId):
    if offerCampMap.has_key(offerId):
        return offerCampMap[offerId]
    campId = random.randint(100, 105)
    offerCampMap[offerId] = campId    
    return campId
    
def getOfferId():
    return random.randint(200, 210)

# generates YYYYMM second activity ts
def generateTs():
    yr = random.randint(2001, 2014)
    mo = random.randint(1,12)
    day = random.randint(1,28)
    hr = random.randint(0,23)
    mn = random.randint(0,59)
    sec = random.randint(0,59)
    ts = '{:%Y-%m-%dT%H:%M:%SZ}'.format(datetime.datetime(yr,mo,day,hr,mn,sec))
    return (str(yr)+'-%02d' % mo, ts)

# Below is the cassandra table/solr docs that this script generates data for
# -- Campaign data for retailer view, for brands, partitionkey would change to
# -- ((yrMonth, cpgId), brandId, insertTs)
# CREATE TABLE activity (
# "activityId" TIMEUUID,
# "yrMonth" VARCHAR,
# "compId" VARCHAR,
# "region" VARCHAR,
# "storeGrp" VARCHAR,
# "storeId" VARCHAR,
# "campId" VARCHAR,
# "offerId" VARCHAR,
# "segment" VARCHAR,    
# "custId" VARCHAR,
# "channel" VARCHAR,
# "mfgId" VARCHAR,    
# "category" VARCHAR,
# "itemId" VARCHAR,
# "zoneId" INT,
# "posx" FLOAT,
# "posy" FLOAT,
# "beaconId" INT,
# "latlng" VARCHAR,
# "iarInd" VARCHAR,
# "activityTs" TIMESTAMP,
# PRIMARY KEY (("yrMonth", "compId"), "storeId", "insertTs")
# );
  
header = ['activityId', 'yrMonth', 'compId', 'region', 'storeGrp', 'storeId',  
          'campId', 'offerId', 'segment', 'custId', 'channel','mfgId', 'category',  
          'itemId', 'zoneId', 'posx', 'posy', 'beaconId', 'latlng', 'activityInd', 'activityTs']

def generateData(outFile, numRecs, hdrFlg):
    counter = 0
    fw = open(outFile, 'w')
    print hdrFlg
    if hdrFlg == 'Y':
        fw.write(','.join(header)+'\n')
    while counter < numRecs:
        print "Writing row "+str(counter)
        flds = []
        flds.append("\""+str(uuid.uuid1())+"\"")
        yrMo, ts = generateTs()
        flds.append("\""+yrMo+"\"")
        compId = getCompId();
        flds.append("\""+str(compId)+"\"")
        region = getRegion()
        flds.append("\""+region+"\"")
        flds.append("\""+getStoreGroup()+"\"")
        flds.append("\""+str(getStoreId(compId))+"\"")
        offerId = getOfferId()        
        campId = getCampaignId(offerId)    
        flds.append("\""+str(campId)+"\"")
        flds.append("\""+str(offerId)+"\"")        
        custId = getCustomerId()
        flds.append("\""+getSegment(custId)+"\"")
        flds.append("\""+str(custId)+"\"")
        flds.append("\""+getChannel()+"\"")
        flds.append("\""+str(getMfgId())+"\"")
        category = getCategory()
        flds.append("\""+category+"\"")
        flds.append("\""+getItem(category)+"\"")
        # zone id
        flds.append(str(random.randint(100,150)))
        # posx
        flds.append(str(random.randint(100,999)/10.0))
        # posy
        flds.append(str(random.randint(100,999)/10.0))
        #beaconid
        flds.append(str(random.randint(1,100)))
        # lat long
#         flds.append(str(random.randint(100,999)/10.0))
#         flds.append(str(random.randint(100,999)/10.0))
        flds.append("\""+str(random.randint(100,999)/10.0)+","+str(random.randint(100,999)/10.0)+"\"")        
        flds.append("\""+getActivity()+"\"")        
        # activity ts
        flds.append("\""+ts+"\"")
        fw.write(','.join(flds)+'\n')
        counter += 1
    fw.close()
    print "Done!"
    
if __name__=="__main__":
    from sys import argv
    if (len(argv) < 4):
        print "usage: GenerateDummyData <outFile> <numRecs> <header(default=Y)=Y|N>"
    else:
        hdrFlg = 'Y' if argv[3] != 'N' else 'N'
        generateData(argv[1],int(argv[2]), hdrFlg)
        