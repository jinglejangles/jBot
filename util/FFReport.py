from config import imageurl, fflogslink


class FFReport():
    def __init__(self, charList, healCombinedDamage, tankCombinedDamage,
                 healPercent, tankPercent, fightName, encounterID, duration,
                 code, fightID):
        self.charList = charList
        self.healCombinedDamage = healCombinedDamage
        self.healPercentile = healPercent
        self.tankCombinedDamage = tankCombinedDamage
        self.tankPercentile = tankPercent
        self.fightName = fightName
        self.fightIcon = imageurl+str(encounterID)+"-icon.jpg"
        self.duration = duration
        self.code = code
        self.fightID = fightID
        self.link = fflogslink+str(code)+"#fight="+str(fightID)+"&type=summary"

    def __str__(self):
        printString = ''
        for x in self.charList:
            printString += str(x)

        printString += "\nHeal Damage:" + str(self.healPercentile) + ':' +
        str(self.healCombinedDamage) + '\n' + "Tank Damage:" +
        str(self.tankPercentile) + ":" + str(self.tankCombinedDamage)
        return printString
