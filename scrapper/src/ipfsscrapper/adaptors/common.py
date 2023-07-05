from __future__ import annotations

import string
from abc import ABC, abstractmethod
from pathlib import PurePath

from ..models.ipfsmetada import IPFSMetadata


class IPFSMetadataResult:
    def __init__(self) -> None:
        pass
    
    def metadata(self, _name: string, _image: string, _description: string ):
        self.metadata :IPFSMetadata =  IPFSMetadata(name= _name, image= _image , description= _description )

class IPFSMetadataAdaptor(ABC):
    # @abstractmethod
    # def read_metadata(self) -> IPFSMetadataResult:
    #     pass
    @abstractmethod
    def write_metadata(self, avatar):
        pass
