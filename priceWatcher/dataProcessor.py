from sql import alcsession, Price, RoundType, Source, NoResultFound


def processData(dataDict):
    """This function takes data in a standard format and logs it via the SQLAlchemy library.

    This function takes a single dictionary containing the following keys:
    	'nameOfAmmo': the name of the ammo in string format
        'costOfAmmo': the cost of the ammo in float format
        'quantityOfAmmo': the quantity of this item for sale in int format
        'roundCount': the quantity of ammo in this item for sale in int format
        'costPerRound': the cost per round in float format
        'source': the domain where this item is or sale in string format
        'date': the date and time when the data was gathered datetime.datetime object format
    """


    #First we veify the the source is in the DB. If so we get the source_id.
    #If not we add it then get the source id and store it as localSource_id
    try:
        sorceObjec = alcsession.query(Source).filter(Source.source == dataDict['source']).one()
        localSource_id = sorceObjec.source_id
    except NoResultFound as e:
        newSourceObj = Source()
        newSourceObj.source = dataDict['source']
        alcsession.add(newSourceObj)
        alcsession.flush()
        localSource_id = newSourceObj.source_id


    #Next up we make sure the roundType exists. same as the source.
    try:
        typeObjec = alcsession.query(RoundType).filter(RoundType.roundName == dataDict['nameOfAmmo']).one()
        localRoundType_id = typeObjec.roundType_id
    except NoResultFound as e:
        newTypeObj = RoundType()
        newTypeObj.roundName = dataDict['nameOfAmmo']
        alcsession.add(newTypeObj)
        alcsession.flush()
        localRoundType_id = newTypeObj.roundType_id

    #Next up we add the price info to the DB.
    priceLogEvent = Price()
    priceLogEvent.availabilityCount = dataDict['quantityOfAmmo']
    priceLogEvent.wholeCost = dataDict['costOfAmmo']
    priceLogEvent.roundCost = dataDict['costPerRound']
    priceLogEvent.roundCount = dataDict['roundCount']
    priceLogEvent.dateTime = dataDict['date']
    priceLogEvent._roundType_id = localRoundType_id
    priceLogEvent._source_id = localSource_id

    alcsession.add(priceLogEvent)
    alcsession.commit()
