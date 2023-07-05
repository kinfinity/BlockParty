from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from pathlib import PurePath
from ipfsscrapper.connections.postgresConnection import PostgressConnection
from ipfsscrapper.utils.config import Config

engine= PostgressConnection(Config(PurePath("config.json"))).engine
Base = declarative_base()

class IPFSMetadata(Base):
    __tablename__ = 'metadata'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    image = Column(String)
    description = Column(String)
    cid = Column(String, unique=True)

    # 
    def __repr__(self):
        return "<User(name='%s', image='%s', description='%s')>" % (
            self.name,
            self.image,
            self.description,
        )
    
Base.metadata.create_all(engine)