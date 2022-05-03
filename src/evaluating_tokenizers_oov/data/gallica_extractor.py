# coding: utf-8

"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
``[options.entry_points]`` section in ``setup.cfg``::

    console_scripts =
         fibonacci = evaluating_tokenizers_oov.skeleton:run

Then run ``pip install .`` (or ``pip install -e .`` for editable mode)
which will install the command ``fibonacci`` inside your current environment.

Besides console scripts, the header (i.e. until ``_logger``...) of this file can
also be used as template for Python modules.

Note:
    This skeleton file can be safely removed if not needed!

References:
    - https://setuptools.pypa.io/en/latest/userguide/entry_point.html
    - https://pip.pypa.io/en/stable/reference/pip_install
"""

import logging
import sys

from evaluating_tokenizers_oov import __version__

__author__ = "ALEXANDRA BENAMAR"
__copyright__ = "ALEXANDRA BENAMAR"
__license__ = "MIT"

_logger = logging.getLogger(__name__)


from fdh_gallica import Periodical

from tqdm import tqdm
import pandas as pd

from bs4 import BeautifulSoup
import urllib

PRESSE_MEDICALE = [("journal_microbiologie", "http://gallica.bnf.fr/ark:/12148/cb34348753q/date", 1887, 1900)]
                   #("annales_immuno", "http://gallica.bnf.fr/ark:/12148/cb34374507n/date", 1973, 1984)]

#--------------------------------------
# UTILS

def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


#--------------------------------------
# ---- Python API ----
# The functions defined in this section can be imported by users in their
# Python scripts/interactive interpreter, e.g. via
# `from evaluating_tokenizers_oov.gallica_extractor import openurl`,
# when using this Python module as a library.

def parse_date(document):
    return pd.to_datetime(document.oai()['results']['notice']['record']['metadata']['oai_dc:dc']['dc:date'])

def openurl(url, textfile):
    auth = urllib.request.HTTPBasicAuthHandler()
    opener = urllib.request.build_opener(auth, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    page=urllib.request.urlopen(url)
    reader = page.read()
    soup = BeautifulSoup(reader, "html.parser")
    pressbottom=str(soup.get_text())
    with open(textfile, 'w', encoding="utf-8") as myFile:
        myFile.write(pressbottom)


def run():
    """Main function for running Gallica extraction"""
    
    setup_logging(1)

    _logger.debug("Starting extraction...")

    for periodical_name, key, start, end in PRESSE_MEDICALE:
        periodical = Periodical(key)

        issues = []
        for year in tqdm(range(start, end+1)):
            issues.extend(periodical.issues_per_year(year))
        
        for i in issues:
            document = i.oai()
            date = str(parse_date(i)).split()[0]
            identitifer = str(document["results"]['notice']['record']['header']['identifier']).split("gallica/")[1]
            url = "https://gallica.bnf.fr/" + identitifer + ".texteBrut"
            # title = str(document["results"]['notice']['record']["metadata"]["oai_dc:dc"]['dc:title']).replace(" ", "_").replace("'", "").lower()
            output_file = "data/" + periodical_name + "_" + date + ".txt"
            openurl(url, output_file)
    
    _logger.info(f"Done.")

#--------------------------------------

if __name__=="__main__":
    run()
