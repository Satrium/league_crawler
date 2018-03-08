import threading

class Manager():
    def __init__(self):
        self.match_lock = threading.Lock()
        self.summoner_lock = threading.Lock()
        self.matches = set()
        self.summoners = set()

    def get_match(self):
        with self.match_lock:
            if self.has_match():
                return self.matches.pop()
            else:
                return None

    def get_summoner(self):
        with self.summoner_lock:
            if self.has_summoner():
                return self.summoners.pop()
            else:
                return None

    def add_summoner(self, summoner):
        self.summoners.add(summoner);

    def add_match(self, match):
        self.matches.add(match)

    def has_summoner(self):
        return len(self.summoners) > 0

    def has_match(self):
        return len(self.matches) > 0

    @property
    def summoner_len(self):
        return len(self.summoners)

    @property
    def matches_len(self):
        return len(self.matches)