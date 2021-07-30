from config import imageurl, fflogslink


class FFReport():
    def __init__(self, charList, healCombinedDamage, tankCombinedDamage,
                 healPercent, tankPercent, fightName, encounterID, duration,
                 code, fightID):
        self.char_list = charList
        self.heal_combinedDamage = healCombinedDamage
        self.heal_percentile = healPercent
        self.tank_combinedDamage = tankCombinedDamage
        self.tank_percentile = tankPercent
        self.fight_name = fightName
        self.fight_icon = imageurl+str(encounterID)+"-icon.jpg"
        self.duration = duration
        self.code = code
        self.fight_id = fightID
        self.link = fflogslink+str(code)+"#fight="+str(fightID)+"&type=summary"

    def __str__(self):
        printString = ''
        for x in self.charList:
            printString += str(x)

        printString += "\nHeal Damage:" + str(self.healPercentile) + ':' 
        +str(self.healCombinedDamage) + '\n' + "Tank Damage:" 
        +str(self.tankPercentile) + ":" + str(self.tankCombinedDamage)
        return printString
