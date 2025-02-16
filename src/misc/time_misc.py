import datetime

def IsDataOlderOneHour(lastPriceTimeStampUnix):
    if (not str(lastPriceTimeStampUnix).replace('.','').isnumeric()):  lastPriceTimeStampUnix = 0
    try:
        lastPriceTimeStamp = datetime.datetime.utcfromtimestamp(lastPriceTimeStampUnix)
    except:
        lastPriceTimeStamp = datetime.datetime.utcfromtimestamp(0)


    return( lastPriceTimeStamp < datetime.datetime.now()-datetime.timedelta(hours=1))

def IsDataOlderTenMinutes(lastPriceTimeStampUnix):
    if (not str(lastPriceTimeStampUnix).replace('.','').isnumeric()):  lastPriceTimeStampUnix = 0
    try:
        lastPriceTimeStamp = datetime.datetime.utcfromtimestamp(lastPriceTimeStampUnix)
    except:
        lastPriceTimeStamp = datetime.datetime.utcfromtimestamp(0)


    return( lastPriceTimeStamp < datetime.datetime.now()-datetime.timedelta(minutes=10))



def toUnixTimestamp(t):
    return((t - datetime.datetime(1970, 1, 1)).total_seconds() )
