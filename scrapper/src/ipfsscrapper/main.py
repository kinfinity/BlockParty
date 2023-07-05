""" Scrap IPFS Metadata and update references in RDS Postgres

Usage:
  ipfsscrapper --help

Options:
  -h --help                             Show this screen
"""
import logging
import sys

from docopt import docopt


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



if __name__ == '__main__':
    run()