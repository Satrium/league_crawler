import threading, time, arrow

from datetime import datetime, timedelta

from manager import Manager
from config import config
from database import SQLParticipantAdditional

from cassiopeia.core import MatchHistory
from cassiopeia import Queue, Patch, Division, Tier, ChampionMastery
from cassiopeia_sqlstore import SQLStore

class Crawler(threading.Thread):

    def __init__(self, manager:Manager, sqlstore:SQLStore):
        super().__init__()
        self.manager = manager
        self.sqlstore = sqlstore
        self.running = True 
        self.queues = [Queue(q) for q in config["match-filter"]["queues"]]

    def run(self):
        while(self.running):
            match = self.manager.get_match()
            if match:
                self.load_match(match)
            else:
                summoner = self.manager.get_summoner()
                if summoner:
                    self.load_summoner(summoner)
                else:
                    time.sleep(0.1)

    def load_match(self, match):
        match.load()
        if config["loading"]["timeline"]:
            match.timeline.load()
        if config["loading"]["league"] or config["loading"]["championmastery"]:
            for participant in match.participants:
                division = -1
                tier = -1
                champ_level = -1
                champ_points = -1
                if config["loading"]["league"]:                    
                    rank = participant.summoner.ranks[Queue.ranked_solo_fives]
                    division = Division._order()[rank.division],
                    tier = Tier._order()[rank.tier]
                if config["loading"]["championmastery"]:
                    masteries = participant.summoner.champion_masteries
                    if participant.champion in masteries:
                        mastery = masteries[participant.champion]
                        champ_level = mastery.level
                        champ_points = mastery.points
                    else:
                        champ_level = 0
                        champ_points = 0
                info = SQLParticipantAdditional(
                    platformId=match.platform.value,
                    gameId=match.id,
                    participantId=participant.id,
                    division=division,
                    tier=tier,
                    champ_level=champ_level,
                    champ_points=champ_points
                )
                self.sqlstore._put(info)

    def load_summoner(self, summoner):
        summoner.load()
        start_time = config["match-filter"]["begin-time"]
        now = arrow.utcnow()
        if start_time < 0:
            start_time = now.shift(seconds=start_time)
        else:
            start_time = arrow.get(start_time)
        match_history = MatchHistory(summoner=summoner, queues=self.queues)
        for match in match_history:
            if(match.creation.to("UTC") > start_time):
                self.manager.add_match(match)
            else:
                break