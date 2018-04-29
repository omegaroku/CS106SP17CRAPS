from Dice import Die
import sys
import crapsResources_rc
from time import sleep
from PyQt5.QtCore import pyqtSlot, QSettings, Qt, QCoreApplication
from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog

class CrapsGame(QMainWindow) :
    """A game of Craps"""
    def __init__(self, parent= None):
        super().__init__(parent)
        self.appSettings = QSettings('CrapsNp', 'CrapsGame')
        uic.loadUi("craps.ui",self)
        self.startingBank = 1000
        self.currentBank = self.startingBank
        self.maximumBet = self.currentBank
        self.minmumBet = 1
        self.winCount = 0
        self.lossCount = 0
        self.currentBet = 0
        self.results="Welcome to Craps"
        self.die1 = Die(6)
        self.die2 = Die(6)
        self.firstThrow=0
        self.secondRoll=False
        self.payOut=1
        self.rollButton.clicked.connect(self.rollButtonClickedHandler)
        self.betSpinBox.valueChanged.connect(self.spinBoxChangedHandler)
        self.preferencesPushButton.clicked.connect(self.preferencesOpenHandler)
        self.restoreSettings()


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
        self.currentBet=num

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

    def restoreSettings(self):
        self.appSettings = QSettings('CrapsNp', 'CrapsGame')
        if self.appSettings.contains('logFile'):
            self.logFilename = self.appSettings.value('logFile', type=str)
        else:
            self.logFilename = 'crapsLog.txt'
            self.appSettings.setValue('logFile', self.logFilename)

        if self.appSettings.contains('pickleFileName'):
            self.pickleFileName = self.appSettings.value('pickleFileName', type= str)
        else:
            self.pickleFileName = ".crapsSavedObjects.pl"
            self.appSettings.setValue('pickleFileName', self.pickleFileName)
        self.startingBank = self.appSettings.value('startingBank')
        self.currentBank = self.startingBank
        self.maximumBet=self.appSettings.value('maximumBet')
        self.minmumBet=self.appSettings.value('minimumBet')
        self.updateUI()

    @pyqtSlot()
    def preferencesOpenHandler(self):
        preferenceWindow.show()

    def rollButtonClickedHandler(self):
        if self.currentBet is 0:
            self.setResults("Please Place A Bet")
            self.rollButton.setEnabled(False)
        else:
            self.die1.roll()
            self.die2.roll()
            if self.secondRoll==True:
                if self.firstThrow == self.die1.getValue() + self.die2.getValue():
                    print("You Win!")
                    self.setResults("You Win!")
                    self.setWinCount(self.getWinCount() + 1)
                    self.currentBank = self.getCurrentBank() + (self.getCurrentBet()*self.getPayOut())
                    self.secondRoll=False
                    self.betSpinBox.valueChanged.connect(self.spinBoxChangedHandler)
                    self.setPayOut(1)
                    self.firstThrow=0
                else:
                    print("You Lose!")
                    self.setResults("You Lose!")
                    self.setLossCount(self.getLossCount() + 1)
                    self.currentBank = self.getCurrentBank() - (self.getCurrentBet()*self.getPayOut())
                    if self.currentBank is 0:
                        self.setResults("You Are Out Of Money. Please Come Again Later.")
                        self.rollButton.setEnabled(False)
                        self.updateUI()
                    elif self.currentBank < 0:
                        self.setResults("You Are Now Being Hunted")
                        self.rollButton.setEnabled(False)
                        self.updateUI()
                    else:
                        self.secondRoll = False
                        self.betSpinBox.valueChanged.connect(self.spinBoxChangedHandler)
                        self.setPayOut(1)
                    self.firstThrow=0

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
            self.rollButton.setEnabled(False)
            self.updateUI()
        elif self.betSpinBox.value() > self.maximumBet:
            self.setResults("Please bet less than "+str(self.maximumBet))
            self.rollButton.setEnabled(False)
            self.updateUI()
        elif self.betSpinBox.value() < self.minmumBet:
            self.setResults("Please bet more than "+str(self.minmumBet))
            self.rollButton.setEnabled(False)
            self.updateUI()
        else:
            self.setCurrentBet(self.betSpinBox.value())
            self.rollButton.setEnabled(True)
            self.setResults("You May Roll Now")
            self.updateUI()

class PreferencesDialog(QDialog):
        def __init__(self, parent = CrapsGame):
            super(PreferencesDialog, self).__init__()
            uic.loadUi('Preferences.ui',self)
            self.appSettings = QSettings('CrapsNp', 'CrapsGame')
            if self.appSettings.contains('startingBank'):
                self.startingBank = self.appSettings.value('startingBank', type=int)
            else:
                self.startingBank = 1000
                self.appSettings.setValue('startingBank', self.startingBank)
            if self.appSettings.contains('minimumBet'):
                self.minimumBet = self.appSettings.value('minimumBet', type=int)
            else:
                self.minimumBet = 1
                self.appSettings.setValue('minimumBet', self.minimumBet)
            if self.appSettings.contains('maximumBet'):
                self.maximumBet = self.appSettings.value('maximumBet', type=int)
            else:
                self.maximumBet = self.startingBank
                self.appSettings.setValue('maximumBet', self.maximumBet)

            self.startingBankValue.editingFinished.connect(self.startingBankValueChanged)
            self.maximumBetValue.editingFinished.connect(self.maximumBetValueChanged)
            self.minimumBetValue.editingFinished.connect(self.minimumBetValueChanged)
            self.pushButton.rejected.connect(self.cancelClickedHandler)
            self.pushButton.accepted.connect(self.okayClickedHandler)

        @pyqtSlot()
        def startingBankValueChanged(self):
            self.startingBank=int(self.startingBankValue.text())

        @pyqtSlot()
        def maximumBetValueChanged(self):
            self.maximumBet = int(self.maximumBetValue.text())

        @pyqtSlot()
        def minimumBetValueChanged(self):
            self.minimumBet = int(self.minimumBetValue.text())


        @pyqtSlot()
        def cancelClickedHandler(self):
            self.close()

        @pyqtSlot()
        def okayClickedHandler(self):
            self.appSettings.setValue('startingBank', self.startingBank)
            self.appSettings.setValue('minimumBet', self.minimumBet)
            self.appSettings.setValue('maximumBet', self.maximumBet)
            crapsApp.restoreSettings()
            self.close()


if __name__ == "__main__":
    appSettings=QSettings('CrapsNp','CrapsGame')
    app = QApplication(sys.argv)
    crapsApp= CrapsGame()
    crapsApp.updateUI( )
    crapsApp.show( )
    preferenceWindow = PreferencesDialog()
    sys.exit(app.exec_())
