from sqlalchemy import Column, Integer, Float, String, MetaData,Table, create_engine, ForeignKey, join
from settings import sqlConf
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound

metadata = MetaData()
Base = declarative_base()

user = Table('prices', metadata,
    Column('price_id', Integer, primary_key = True),
    Column('availabilityCount', Integer, nullable = False),
    Column('wholeCost', Float, nullable = False),
    Column('roundCount', Float, nullable = False),
    Column('_roundType_id', Integer, ForeignKey("roundTypes.roundType_id"))
)

userTypes = Table('roundTypes', metadata,
    Column('roundType_id', Integer, primary_key = True),
    Column('roundName', String(200), unique=True)
)

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
    roundCount = Column(Float, nullable = False)
    _roundType_id = Column(Integer, ForeignKey("roundTypes.roundType_id"))
    roundType = relationship("RoundType")
    def __repr__(self):
        return "<PriceInfo (price='%s', id='%s')>" % (self.wholeCost, self.price_id)

engine = create_engine('mysql+pymysql://%s:%s@%s/%s'% (sqlConf['username'],sqlConf['password'],sqlConf['dbLocation'],sqlConf['dbName']))

metadata.create_all(engine)

Session = sessionmaker()
Session.configure(bind=engine)
alcsession = Session()

#qUser = alcsession.query(User).filter(User.email == 'ff').one()
#print(qUser.email,qUser.accountType.accountTypeStr)
