# This is a reconstruction of the prisoners dilemma. 
# It randomly generates a number of games after a maximum is given.
# User then choses a strategy for each player. 

import subprocess
import os
import pandas as pd
import quantumrandom
import lib.logic.player as pl
import lib.logic.runState as rs  
import lib.logic.prompts as pmt


def main():
    clearScreen()
    printIntroduction()
    n = setIterationNumber()
    e = configureEntropy()

    currRS = rs.runState(e, n)
    p1 = pl.player(1, n, getStrategy("Player " + str(1)))
    p2 = pl.player(2, n, getStrategy("Player " + str(2)))

    for i in range(0, currRS.gameLength):
        p1.makeChoice(currRS.p1_moves, currRS.p2_moves, i, currRS.entropy)
        p2.makeChoice(currRS.p2_moves, currRS.p1_moves, i, currRS.entropy)
        currRS.updateGame(p1, p2)

    print(str(p1) + " served " + str(p1.years) + " years but had they perfect knowledge, they would have only served " + str(p1.minYears) + " years. ")
    print(str(p2) + " served " + str(p1.years) + " years but had they perfect knowledge, they would have only served " + str(p2.minYears) + " years. ")

    placeStats(p1,p2, currRS.gameLength)


def configureEntropy():
    text = pmt.getEntropyText()
    for x in text:
        print(x)
    choice = validateInput()
    return choice


def placeStats(p1, p2, n):
    #so I want to be able to easily see which strats are best, so it's a bit hacky
    subprocess.run(["cp", "stats/strat.txt", "ipd_stats.tmp"])
    df = pd.read_csv("ipd_stats.tmp", index_col="strat")
    
    df.loc[p1.strat, "num_games"] += n
    df.loc[p1.strat, "num_years"] += p1.years
    df.loc[p1.strat, "min_years"] += p1.minYears
    df.loc[p1.strat, "num_entropy"] += p1.entropyInvoked
    df.loc[p2.strat, "num_games"] += n
    df.loc[p2.strat, "num_years"] += p2.years
    df.loc[p2.strat, "min_years"] += p2.minYears
    df.loc[p2.strat, "num_entropy"] += p2.entropyInvoked
    
    text = str(df).split("\n")
    print(text)

    df.to_csv("stats/strat.txt")

    subprocess.run(["rm", "ipd_stats.tmp"])


def printIntroduction():
    text = pmt.getInstructions()
    for x in text:
        print(x)


def setIterationNumber():
    text = pmt.getMaxGamesText()
    for x in text:
        print(x)
    
    n_max = validateInput()
    n = int(quantumrandom.randint(1, n_max))
    print("\nLooks like you're playing " + str(n) + " games.\n")
    return n 

    
def getStrategy(player):
    print("What strategy would you like " + player + " to use?")
    print("1.) Random")
    print("2.) Tit for tat")
    print("3.) Pavlov")
    print("(or enter \"q\" to quit)")
    choice = validateInput()

    return choice


def clearScreen():
    _ = subprocess.call("clear" if os.name == "posix" else "cls")


def validateInput():
    buff = input()
    if buff == "q":
        exit(0)

    return int(buff)


def quit():
    print("Bye bae")
    exit()
