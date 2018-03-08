from misc import logger, get_sqlstore

logger.debug("Loading config")
from config import config, generate_cassio_conf
from manager import Manager
from crawler import Crawler
from database import SQLParticipantAdditional
import cassiopeia as cass

cass.apply_settings(generate_cassio_conf())
cass.set_default_region(config["region"])
if "api-key" in config:
    cass.set_riot_api_key(config["api-key"])


manager = Manager()
sqlstore = get_sqlstore(cass)
from cassiopeia.core import League, ChallengerLeague, MasterLeague, Summoner
from cassiopeia.data import Queue

if config["seed"]["type"] == "LEAGUE":    
    # Load this league and use it as seeding
    league = None
    if config["seed"]["id"] == "CHALLENGER":
        logger.info("Using challenger league as seed")
        league = ChallengerLeague(queue=Queue.ranked_solo_fives)
    elif config["seed"]["id"] == "MASTER":
        logger.info("Using master league as seed")
        league = MasterLeague(queue=Queue.ranked_solo_fives)
    else:
        logger.info("Using league with id=" + config["seed"]["id"] + " as seed")
        league = League(id=config["seed"]["id"])
    for entry in league.entries:
        summoner = entry.summoner
        manager.add_summoner(summoner)
    logger.info("Loaded " + str(manager.summoner_len) + " summoners")

for i in range(config["threads"]):
    crawler = Crawler(manager, sqlstore)
    crawler.start()

