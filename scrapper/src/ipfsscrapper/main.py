""" Scrap IPFS Metadata and update references in RDS Postgres

Usage:
  ipfsscrapper --help

Options:
  -h --help                             Show this screen
"""
import logging
import sys
import csv
from pathlib import PurePath

from docopt import docopt
from ipfsscrapper.connections.postgresConnection import PostgressConnection
from ipfsscrapper.utils.config import Config


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


    #  

if __name__ == '__main__':
    run()
