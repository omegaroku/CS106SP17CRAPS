from Dice import Die
class CrapsGame(object):
    def __init__(self):
        self.winCount = 0
        self.lossCount = 0
        self.currentBet = 0
        self.startingBank= 1000
        self.currentBank= self.startingBank

    def __str__(self):
        return "Bank: %i, Wins: %i, Losses: %i" % (self.currentBank, self.winCount, self.lossCount)
    def setWinCount(self,num):
        self.winCount=num
    def getWinCount(self):
        return self.winCount
    def setLossCount(self,num):
        self.lossCount=num
    def getLossCount(self):
        return self.lossCount
    def setCurrentBet(self,num):
        self.currentBet=num
    def getCurrentBet(self):
        return self.currentBet
    def setCurrentBank(self,num):
        self.currentBank=num
    def getCurrentBank(self):
        return self.currentBank
    def throw(self):
        """

        :rtype: object
        """
        Dice1 = Die(6)
        Dice2 = Die(6)
        Dice1.roll()
        Dice2.roll()
        firstThrow = Dice1.getValue() + Dice2.getValue()

        if firstThrow is 7 or firstThrow is 11:
            print("You Win!")
            self.setWinCount(self.getWinCount()+1)
            self.currentBank=self.getCurrentBank()+self.getCurrentBet()
        elif firstThrow is 2 or firstThrow is 3 or firstThrow is 12:
            print("You Lose!")
            self.setLossCount(self.getLossCount()+1)
            self.currentBank=self.getCurrentBank()-self.getCurrentBet()
        else:
            Dice1.roll()
            Dice2.roll()
            if Dice1.getValue()+Dice2.getValue() is firstThrow:
                print("You Win!")
                self.setWinCount(self.getWinCount() + 1)
                self.currentBank = self.getCurrentBank() + self.getCurrentBet()
            else:
                print("You Lose!")
                self.setLossCount(self.getLossCount() + 1)
                self.currentBank = self.getCurrentBank() - self.getCurrentBet()
        pass
