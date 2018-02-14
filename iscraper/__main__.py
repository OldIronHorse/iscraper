import argparse
from .get_iplayer import download_history

#iscraper.py [--simulate] title output-dir

parser = argparse.ArgumentParser()
parser.add_argument('title', help='programme title to download')
parser.add_argument('output-dir', help='directory to download to')
parser.add_argument('-s', '--simulate', action='store_true',
                    help='find programmes but do not download')
parser.parse_args()
history = download_history()
print(history)
  
