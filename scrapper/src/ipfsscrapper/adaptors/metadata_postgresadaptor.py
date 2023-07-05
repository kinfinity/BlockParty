import logging
from pathlib import PurePath
from typing import Any

from sqlalchemy import insert, lambda_stmt, select
from sqlalchemy.orm import Session

from ipfsscrapper.connections import postgresConnection

from ..models.ipfsmetada import IPFSMetadata
from .common import IPFSMetadataAdaptor

class IPFSMetadataPostgresAdaptor(IPFSMetadataAdaptor):
    def __init__(self, connection: postgresConnection):
        self.session = Session(connection)

    def write_metadata(self, _data: IPFSMetadata) -> Any:
        logging.info(_data)
        return Query().insert_statement(self.session, _data)

# Execute Queries 
class Query():
    #  Insert metadata
    def insert_statement(self, session: Session, data: IPFSMetadata):
        # stmt = lambda_stmt(lambda: insert(IPFSMetadata).values(name=data.name))
        session.add(data)
        return  session.commit()
