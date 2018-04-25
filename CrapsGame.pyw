from Dice import Die
import sys
import crapsResources_rc
from time import sleep
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import QMainWindow, QApplication

class CrapsGame(QMainWindow) :
    """A game of Craps"""
    def __init__(self, parent= None):
        super().__init__(parent)
        uic.loadUi("craps.ui",self)
        self.winCount = 0
        self.lossCount = 0
        self.currentBet = 0
        self.startingBank = 1000
        self.currentBank = self.startingBank
        self.results="Welcome to Craps"
        self.die1 = Die(6)
        self.die2 = Die(6)
        self.firstThrow=0
        self.secondRoll=False
        self.payOut=1
        self.rollButton.clicked.connect(self.rollButtonClickedHandler)
        self.betSpinBox.valueChanged.connect(self.spinBoxChangedHandler)


    def __str__(self):
        return ""

    def setPayOut(self,num):
        self.payOut=num

    def getPayOut(self):
        return self.payOut

    def setFirstThrow(self,num):
        self.firstThrow=num

    def setResults(self,newResult):
        self.results=newResult

    def setWinCount(self, num):
        self.winCount = num

    def getWinCount(self):
        return self.winCount

    def setLossCount(self, num):
        self.lossCount = num

    def getLossCount(self):
        return self.lossCount

    def setCurrentBet(self, num):
        self.currentBet = num

    def getCurrentBet(self):
        return self.currentBet

    def setCurrentBank(self, num):
        self.currentBank = num

    def getCurrentBank(self):
        return self.currentBank

    def updateUI(self):
        self.winsCountLabel.setText(str(self.winCount))
        self.lossesCountLabel.setText(str(self.lossCount))
        self.resultsLabel.setText(str(self.results))
        self.bankAmountLabel.setText(str(self.getCurrentBank()))
        self.die1View.setPixmap(QtGui.QPixmap(":/" + str(self.die1.getValue())))
        self.die2View.setPixmap(QtGui.QPixmap(":/" + str(self.die2.getValue())))


    @pyqtSlot()
    def rollButtonClickedHandler(self):
        if self.currentBet is 0:
            self.setResults("Please Place A Bet")
            self.rollButton.clicked.disconnect(self.rollButtonClickedHandler)
        else:
            self.die1.roll()
            self.die2.roll()
            if self.secondRoll==True:
                if self.firstThrow==self.die1.getValue() + self.die2.getValue():
                    print("You Win!")
                    self.setResults("You Win!")
                    self.setWinCount(self.getWinCount() + 1)
                    self.currentBank = self.getCurrentBank() + (self.getCurrentBet()*self.getPayOut())
                    self.secondRoll=False
                    self.betSpinBox.valueChanged.connect(self.spinBoxChangedHandler)
                    self.setPayOut(1)

                else:
                    print("You Lose!")
                    self.setResults("You Lose!")
                    self.setLossCount(self.getLossCount() + 1)
                    self.currentBank = self.getCurrentBank() - (self.getCurrentBet()*self.getPayOut())
                    if self.currentBank is 0:
                        self.setResults("You Are Out Of Money. Please Come Again Later.")
                        self.rollButton.clicked.disconnect(self.rollButtonClickedHandler)
                        self.updateUI()
                    elif self.currentBank < 0:
                        self.setResults("You Are Now Being Hunted")
                        self.rollButton.clicked.disconnect(self.rollButtonClickedHandler)
                        self.updateUI()
                    else:
                        self.secondRoll = False
                        self.betSpinBox.valueChanged.connect(self.spinBoxChangedHandler)
                        self.setPayOut(1)

            elif self.die1.getValue() + self.die2.getValue() is 7 or self.die1.getValue() + self.die2.getValue() is 11:
                print("You Win!")
                self.setResults("You Win!")
                self.setWinCount(self.getWinCount() + 1)
                self.currentBank = self.getCurrentBank() + (self.getCurrentBet()*self.getPayOut())
            elif self.die1.getValue() + self.die2.getValue() is 2 or self.die1.getValue() + self.die2.getValue() is 3 or self.die1.getValue() + self.die2.getValue() is 12:
                print("You Lose!")
                self.setResults("You Lose!")
                self.setLossCount(self.getLossCount() + 1)
                self.currentBank = self.getCurrentBank() - (self.getCurrentBet()*self.getPayOut())
            else:
                self.betSpinBox.valueChanged.disconnect(self.spinBoxChangedHandler)
                self.secondRoll = True
                self.setResults("Please Roll Again")
                self.setFirstThrow(self.die1.getValue() + self.die2.getValue())
                if self.firstThrow is 4 or self.firstThrow is 10:
                    self.setPayOut(2)
                elif self.firstThrow is 5 or self.firstThrow is 9:
                    self.setPayOut(1.5)
                elif self.firstThrow is 6 or self.firstThrow is 8:
                    self.setPayOut(1.2)

        self.updateUI()
    @pyqtSlot()
    def spinBoxChangedHandler(self):
        if self.betSpinBox.value() > self.getCurrentBank():
            self.setResults("You Do Not Have That Much Money")
            self.rollButton.clicked.disconnect(self.rollButtonClickedHandler)
            self.updateUI()
        else:
            self.setCurrentBet(self.betSpinBox.value())
            self.rollButton.clicked.connect(self.rollButtonClickedHandler)
            self.setResults("You May Roll Now")
            self.updateUI()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    crapsApp= CrapsGame()
    crapsApp.updateUI( )
    crapsApp.show( )
    sys.exit(app.exec_())

