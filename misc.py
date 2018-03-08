# Setup logging
import logging
from cassiopeia import Summoner

logger = logging.getLogger("CRAWLER")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
#logger.addHandler(ch)
logger.info("Starting league crawler")

# I want to store a summoner in a set and because we will always have the summonerId
# when storing into a set, I will atach a custom hash function to summoner

def summoner_hash(self):
    return hash(self.id)

Summoner.__hash__ = summoner_hash

def get_sqlstore(cass):
    settings = cass.configuration._settings
    for source in settings.pipeline._sources:
        for s in source:
            if s.__class__.__name__ == "SQLStore":
                return s