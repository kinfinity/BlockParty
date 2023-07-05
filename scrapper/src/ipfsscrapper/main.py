""" Scrap IPFS Metadata and update references in RDS Postgres

Usage:
  ipfsscrapper --help
  ipfsscrapper --configuration FILE

Options:
  -h --help                             Show this screen.
  -c FILE, --configuration FILE  configuration json file
"""
import asyncio
import concurrent.futures
import csv
import logging
import math
import sys
import time
from pathlib import PurePath
from typing import List

from docopt import docopt

from ipfsscrapper.adaptors.metadata_postgresadaptor import IPFSMetadataPostgresAdaptor
from ipfsscrapper.connections.postgresConnection import PostgressConnection
from ipfsscrapper.models.ipfsmetada import IPFSMetadata
from ipfsscrapper.scrapper.scrapper import Scrapper
from ipfsscrapper.utils.config import Config


def scrap2rds(object_list: list, _configuration: Config, postgressConnection):
  # connect to postgres
  ipfsmetadata_postgrescon: IPFSMetadataPostgresAdaptor = IPFSMetadataPostgresAdaptor(connection=postgressConnection)

  try:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Pinata IPFS gateway URL
        BaseURL = _configuration.ipfs_url
        # query ipfs 
        metadata = Scrapper(BaseURL)
        results_cid = executor.map(metadata.fetch_metadata, object_list[0])
        logging.info("CID: "+str(object_list[0]))
        # create & flush objects to RDS
        metadata_list = []
        for res_cid in results_cid:
          print(res_cid)
          metadata_list.append(IPFSMetadata(name=res_cid["name"], image=res_cid["image"], description=res_cid["description"], cid=str(object_list[0][0])))
        
        results_rds = executor.map(ipfsmetadata_postgrescon.write_metadata, metadata_list)
        for res_rds in results_rds:
          logging.info(res_rds)

  except Exception as e:
        logging.error(f"Error: {e}")
        sys.exit(1)

async def recursive_(object_list: list, _configuration: Config, postgressConnection):
  iter_fit = _configuration.batch_number
  logging.info("Iter: "+str(iter_fit))
  if  len(object_list)<= iter_fit:
    # launch scrapping process
    scrap2rds(object_list,_configuration, postgressConnection)
  else:
    await recursive_(object_list[0:math.floor(len(object_list)/2-1)], _configuration, postgressConnection)
    await recursive_(object_list[math.floor(len(object_list)/2):len(object_list)-1], _configuration, postgressConnection)

def run(argv=None):
    if argv is None:
      argv = sys.argv[1:]
    arguments = docopt(__doc__, argv=argv)

    # setup logging 
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logging.info(arguments)

    # Load config
    configuration = Config(PurePath(arguments["--configuration"]))

    #  db connection 
    _postgressConnection = PostgressConnection(configuration=configuration).engine

    # Build list from ipfs_cids file
    ipfs_cids_list = []
    with open(configuration.ipfs_cids, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            ipfs_cids_list.append(row)

    for cid in ipfs_cids_list:
       logging.info(cid[0])

    # recursion on list to maximize metadata scrapping process
    # use multithread Adaptors to scrape and write metadata
    start = time.perf_counter()
    asyncio.get_event_loop().run_until_complete(recursive_(ipfs_cids_list, configuration, _postgressConnection))
    finish = time.perf_counter()
    logging.info(f"It took {finish-start} second(s) to finish.")

if __name__ == '__main__':
    run()
