from random import randint

class Die(object):
    def __init__(self, numberOfSides, startValue=1, incrementValue=1):
        self.value=None
        self.numberOfSides=numberOfSides
        self.startingValue=startValue
        self.incrementValue=incrementValue
    def getValue(self):
        return self.value
    def setValue(self,number):
        self.value=number
    def setNumberOfSides(self,numOfSides):
        self.numberOfSides=numOfSides
    def getNumberOfSides(self):
        return self.numberOfSides
    def setIncrementValue(self,newValue):
        self.incrementValue=newValue
    def getIncrementValue(self):
        return self.incrementValue
    def setStartingValue(self,newStart):
        self.startingValue=newStart
    def getStartingValue(self):
        return self.startingValue
    def __str__(self):
        return str(self.getValue())
    def roll(self):
            self.setValue((randint(0,self.numberOfSides-1)*self.incrementValue+self.startingValue))
