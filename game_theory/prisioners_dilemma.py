# This is a reconstruction of the prisoners dilemma. 
# It randomly generates a number of games after a maximum is given.
# User then choses a strategy for each player. 

import subprocess
import os
import sys
try:
    import quantumrandom
except ImportError:
    print("Quantunrandom not installed. Installing now.")
    _ = subprocess.run(["pip", "install", "quantumrandom"])
    import quantumrandom


def main():
    clearScreen()
    printIntroduction()
    n = setIterationNumber()

    p1 = Player(1, n)
    p2 = Player(2, n)

    for i in range(0, n):
        p1.takeTurn()
        p2.takeTurn()        
        calculateGame(p1, p2, i+1)

    print(str(p1) + " served " + str(p1.totalTime) + " years but had they perfect knowledge, they would have only served " + str(p1.minTotalTime) + " years. ")
    print(str(p2) + " served " + str(p1.totalTime) + " years but had they perfect knowledge, they would have only served " + str(p2.minTotalTime) + " years. ")

class Player:
    def __init__(self, playerNumber, n):
        self.playerNumber = playerNumber
        self.strat = getStrategy("Player " + str(playerNumber))
        self.randomArr = quantumrandom.get_data(array_length = n)
        self.numGamesPlayed = 0
        self.lastChoicePlayed = -1
        self.opponentLastChoicePlayed = -1
        self.currentChoice = -1
        self.totalTime = 0
        self.minTotalTime = 0    

    def __str__(self):
        return "Player " + str(self.playerNumber) + " "

    def playGame(self, opponentChoice, time):
        self.numGamesPlayed += 1
        self.lastChoicePlayed = self.currentChoice
        self.totalTime += time
        self.opponentLastChoicePlayed = opponentChoice
        if time == 2:
            self.minTotalTime += time
        elif time == 3:
            self.minTotalTime += 2

    def takeTurn(self):
        if self.strat == 1: # Random
            self.currentChoice = self.randomArr[self.numGamesPlayed] % 2
        elif self.strat == 2: # tit_for_tat
            if self.opponentLastChoicePlayed == -1:
                self.currentChoice = 0
            elif self.opponentLastChoicePlayed == 1:
                self.currentChoice = 1
            else:
                self.currentChoice = 0
        elif self.strat == 3: # pavlov
            if self.opponentLastChoicePlayed == -1:
                self.currentChoice = 0;
            elif self.opponentLastChoicePlayed != self.lastChoicePlayed:
                self.currentChoice = (self.lastChoicePlayed + 1) % 2
                

def calculateGame(p1, p2, n):
# 2x2 matrix
#    print("Game #" + str(n) + "(" + str(p1.currentChoice) + ", " + str(p2.currentChoice) + ")")
    if(p1.currentChoice == 0 and p2.currentChoice == 0):
        p1.playGame(0, 1)
        p2.playGame(0, 1)
    if(p1.currentChoice == 0 and p2.currentChoice == 1):
        p1.playGame(1, 3)
        p2.playGame(0, 0)
    if(p1.currentChoice == 1 and p2.currentChoice == 0):
        p1.playGame(0, 0)
        p2.playGame(1, 3)
    if(p1.currentChoice == 1 and p2.currentChoice == 1):
        p1.playGame(1, 2)
        p2.playGame(1, 2)


def printIntroduction():
    print("Welcome to the prisoner's dilemma!\n")
    print("You have been arrested for a crime, as has your partner. You are currently being interrogated, as is your partner.") 
    print("If both you and your partner implicate the other-- you each recieve 2 years in prison.")
    print("If neither implicate the other-- you each recieve 1 year in prison.")
    print("If you implicate your partner, and they do not implicate you-- they recieve three years (and vice-versa.)\n")

def setIterationNumber():
    print("Maximum number of games you want to play?")
    n_max = validateInput()
    n = int(quantumrandom.randint(1, n_max))
    print("\nLooks like you're playing " + str(n) + " games.\n")
    return n 
    
def getStrategy(player):
    print("What strategy would you like " + player + " to use?")
    print("1.) Random")
    print("2.) Tit for tat")
    print("3). Pavlov")
    print("(or enter \"q\" to quit)")
    choice = validateInput()

    if(choice == "q"):
        quit()

    return choice

def clearScreen():
    _ = subprocess.call("clear" if os.name == "posix" else "cls")

def validateInput():
    return int(input())

def quit():
    print("Bye bae")
    exit()

if __name__ == "__main__":
    main()
