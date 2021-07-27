from config import jobList


class FFPlayer():
    def __init__(self, name, job, dps, percentile, playerID):
        self.name = name
        self.job = job
        self.dps = dps
        self.percentile = percentile
        self.shorthand = jobList.get(self.job, None)
        self.playerID = playerID

    def __str__(self):
        return str(self.percentile) + ":" + self.job + ":" + self.name + ":" +
        str(self.dps) + "\n"

    def __eq__(self, other):
        return self.dps == other.dps

    def __lt__(self, other):
        return self.dps < other.dps

    def __gt__(self, other):
        return self.dps > other.dps
