from sqlalchemy import Column, Integer, Float, DateTime, String, MetaData,Table, create_engine, ForeignKey, join
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound
import yaml

#Import out settings
with open('settings.yaml', 'r') as f:
    doc = yaml.load(f)
    sqlConf = doc['sqlConfiguration']



# =======================================================================
# =================== Database Descriptors & MetaData ===================
# =======================================================================
metadata = MetaData()
Base = declarative_base()

price = Table('prices', metadata,
    Column('price_id', Integer, primary_key = True),
    Column('availabilityCount', Integer, nullable = False),
    Column('wholeCost', Float, nullable = False),
    Column('roundCost', Float, nullable = False),
    Column('roundCount', Integer, nullable = False),
    Column('dateTime', DateTime, nullable = False),
    Column('_roundType_id', Integer, ForeignKey("roundTypes.roundType_id")),
    Column('_source_id', Integer, ForeignKey("sources.source_id"))
)

roundType = Table('roundTypes', metadata,
    Column('roundType_id', Integer, primary_key = True),
    Column('roundName', String(200), unique=True)
)

source = Table('sources', metadata,
    Column('source_id', Integer, primary_key = True),
    Column('source', String(200), unique=True)
)



# =======================================================================
# ====================== Relevant DataBase Objects ======================
# =======================================================================
class Source(Base):
    __tablename__ = 'sources'
    source_id = Column(Integer, primary_key=True)
    source = Column(String(200), unique=True)
    def __repr__(self):
        return "<Source (id='%s', name='%s')>" % (self.source_id, self.source)

class RoundType(Base):
    __tablename__ = 'roundTypes'
    roundType_id = Column(Integer, primary_key=True)
    roundName = Column(String(200), unique=True)
    def __repr__(self):
        return "<Roundtype (id='%s', name='%s')>" % (self.roundType_id, self.roundName)

class Price(Base):
    __tablename__ = 'prices'
    price_id = Column(Integer, primary_key=True)
    availabilityCount = Column(Integer, nullable = False)
    wholeCost = Column(Float, nullable = False)
    roundCost = Column(Float, nullable = False)
    roundCount = Column(Integer, nullable = False)
    dateTime = Column(DateTime, nullable = False)
    _roundType_id = Column(Integer, ForeignKey("roundTypes.roundType_id"))
    roundType = relationship("RoundType")
    _source_id = Column(Integer, ForeignKey("sources.source_id"))
    source = relationship("Source")
    def __repr__(self):
        return "<PriceInfo (price='%s', id='%s')>" % (self.wholeCost, self.price_id)


# =======================================================================
# ====================== SQLAlchemy Engine Details ======================
# =======================================================================

#We create an engine
engine = create_engine('mysql+pymysql://%s:%s@%s/%s'% (sqlConf['username'],sqlConf['password'],sqlConf['dbLocation'],sqlConf['dbName']))

#This causes all missing tables to be created, Comment to prevent this.
metadata.create_all(engine)

# You can import alcsession and use to to access the relevant database.
Session = sessionmaker()
Session.configure(bind=engine)
alcsession = Session()
