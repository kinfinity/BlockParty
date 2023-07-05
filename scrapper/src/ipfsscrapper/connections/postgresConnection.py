import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base

from ipfsscrapper.utils.config import Config


Base = declarative_base()

class  PostgressConnection():
    def __init__(self, configuration: Config):
        self.engine = None
        self.username = configuration.db_username
        self.password = configuration.db_password
        self.host = configuration.db_host
        self.port = configuration.db_port
        self.database = configuration.database
        self.connect()
        
    def connect(self):
        try:
            
            DB_CONN_STRING = URL.create(
                "postgresql+psycopg2",
                username=self.username,
                password=self.password,
                host=self.host,
                database=self.database,
            )
            # DB_CONN_STRING = os.getenv('DB_CONN_STRING', 'postgres://'+self.username+":"+self.password+"@"+self.host+"/"+self.database)
            self.engine = create_engine(DB_CONN_STRING)
            Base.metadata.create_all(self.engine)

        except (Exception, psycopg2.Error) as error:
            print("Failed to connect to database ->", error)
