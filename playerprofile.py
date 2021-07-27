from config import jobList


class FFPlayerFight():
    def __init__(self, fight, rank, kills, fastest, spec, amount):
        self.fight = fight
        self.rank = int(rank)
        self.kills = kills
        self.fastest = fastest
        self.spec = spec
        self.amount = int(amount)
        self.shorthand = jobList.get(self.spec, None)
