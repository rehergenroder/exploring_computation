import subprocess
import curses
import pandas as pd

import lib.logic.runState as rs
import lib.logic.player as pl
import lib.logic.prompts as pmt

def main():
    curses.wrapper(mainLoop)


def print_menu(stdscr, selected_row_idx, menu):
    h, w = stdscr.getmaxyx()

    for idx, row in enumerate(menu):
        x = w // 2 - len(row) // 2
        y = h //2 - len(menu) // 2 + idx

        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(2))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(2))
        else:
            stdscr.addstr(y, x, row)

    stdscr.refresh()


def printIntroScr(stdscr):
    curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    stdscr.attron(curses.color_pair(1))
    h,w = stdscr.getmaxyx()

    intro = ["Welcome to an iterated prisoners' dilemma!"]
    printCenteredText(stdscr, intro)

    stdscr.attroff(curses.color_pair(1))
    add_any_key(stdscr)


def add_any_key(stdscr):
    h,w = stdscr.getmaxyx()

    any_key = "press any key to continue"
    stdscr.addstr(h - 1, w - len(any_key) - 1, any_key)
    stdscr.refresh()
    stdscr.getch()
    

def quitProgram():
    exit()


def printCenteredText(stdscr, text):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    
    for idx, elem in enumerate(text):
        x = w // 2 - len(elem) // 2
        y = h // 2 - len(text) // 2 + idx
        stdscr.addstr(y, x, elem)

    stdscr.refresh()


def printInstructions(stdscr):
    instructions = pmt.getInstructions() 
    printCenteredText(stdscr, instructions)
    add_any_key(stdscr)


def echoIntInput(stdscr, x, y, min_in, max_in):
    curses.echo()
    curses.curs_set(1)
    stdscr.refresh()

    in_raw = stdscr.getstr(y, x)

    curses.curs_set(0)
    curses.noecho()

    if in_raw.isdigit() and int(in_raw) > min_in and int(in_raw) <= max_in:
        in_passed = int(in_raw)
        return True, in_passed
    else:
        return False, None
  

def setEntropy(stdscr):
    h,w = stdscr.getmaxyx()
    inputValid = False

    while(not inputValid):
        text = pmt.getEntropyText()   
        printCenteredText(stdscr, text)

        in_x = w // 2 - 1
        in_y = h // 2 + len(text) 

        inputValid, e = echoIntInput(stdscr, in_x, in_y, 0, 100)

    return e


def setMaxGames(stdscr):
    h,w = stdscr.getmaxyx()
    inputValid = False

    while(not inputValid):
        text = pmt.getMaxGamesText()
        printCenteredText(stdscr, text)

        in_x = w // 2 - 1
        in_y = h //2 + len(text)

        inputValid, n = echoIntInput(stdscr, in_x, in_y, 0, 256)

    return n


def pickStrategy(stdscr, player):
    h, w = stdscr.getmaxyx()
    
    curr_row_idx = 0
    strategies = ["Random", "Tit for Tat", "Tit for Two Tat", "Pavlov", "GRIM", "Tribal Equilibrium", "Exit Program"]
    text = "Please pick a strategy for player " + str(player) + ":"

    while(1):
        stdscr.clear()
        y = h // 2 - len(strategies) - 3
        x = w // 2 - len(text) // 2
        stdscr.addstr(y, x, text)
        print_menu(stdscr, curr_row_idx, strategies)
        key = stdscr.getch()
        stdscr.clear()

        if key == curses.KEY_UP:
            if curr_row_idx == 0:
                curr_row_idx = len(strategies) - 1
            else:
                curr_row_idx -= 1
        elif key == curses.KEY_DOWN:
            if curr_row_idx == len(strategies) - 1:
                curr_row_idx = 0
            else:
                curr_row_idx += 1
        elif key == curses.KEY_ENTER or key in [10,13]:
            stdscr.clear()
            if curr_row_idx == 6:
                quitProgram()
            else:
                return strategies[curr_row_idx]


def printRS(stdscr, currRS, p1, p2):
    text = ["Well, it looks like you're playing " + str(currRS.gameLength) + " games.",
            "Player " + str(p1.id) + " has chosen a strategy of " + p1.strat + ".",
            "Player " + str(p2.id) + " has chosen a strategy of " + p2.strat + "."]

    printCenteredText(stdscr, text)
    add_any_key(stdscr)  

def runGames(currRS, p1, p2):
    for x in range(0, currRS.gameLength):
        p1.makeChoice(currRS.p1_moves, currRS.p2_moves, x, currRS.entropy)
        p2.makeChoice(currRS.p2_moves, currRS.p1_moves, x, currRS.entropy)
        currRS.updateGame(p1, p2)

def printFinish(stdscr, currRS, p1, p2):
    text = currRS.getMoves(p1, p2)

    printCenteredText(stdscr, text)
    add_any_key(stdscr)


def updateStats(p1, p2, n):
    subprocess.run(["cp", "stats/strat_tui.txt", "ipd_stats.tmp"])
    df = pd.read_csv("ipd_stats.tmp", index_col="strat")

    df.loc[p1.strat, "num_games"] += n
    df.loc[p1.strat, "num_years"] += p1.years
    df.loc[p1.strat, "min_years"] += p1.minYears
    df.loc[p1.strat, "efficiency"] = df.loc[p1.strat, "min_years"] / df.loc[p1.strat, "num_years"]
    df.loc[p1.strat, "num_entropy"] += p1.entropyInvoked
    df.loc[p2.strat, "num_games"] += n
    df.loc[p2.strat, "num_years"] += p2.years
    df.loc[p2.strat, "min_years"] += p2.minYears
    df.loc[p2.strat, "num_entropy"] += p2.entropyInvoked
    df.loc[p2.strat, "efficiency"] = df.loc[p2.strat, "min_years"] / df.loc[p2.strat, "num_years"]


    df.to_csv("stats/strat_tui.txt")
    subprocess.run(["rm", "ipd_stats.tmp"])


def playIPD(stdscr):
    printInstructions(stdscr)
    e = setEntropy(stdscr)
    n = setMaxGames(stdscr)
    
    currRS = rs.runState(e, n)
    p1 = pl.player(1, n, pickStrategy(stdscr, 1))
    p2 = pl.player(2, n, pickStrategy(stdscr, 2))
 
    printRS(stdscr, currRS, p1, p2)    

    runGames(currRS, p1, p2) 
    updateStats(p1, p2, currRS.gameLength)
    
    printFinish(stdscr, currRS, p1, p2)

def printStats(stdscr):
    stdscr.clear()
    h,w = stdscr.getmaxyx()

    subprocess.run(["cp", "stats/strat_tui.txt", "ipd_stats.tmp"])
    df = pd.read_csv("ipd_stats.tmp", index_col="strat")

    text = str(df).split("\n")
    printCenteredText(stdscr, text)

    df.to_csv("stats/strat_tui.txt")
    subprocess.run(["rm", "ipd_stats.tmp"])
    add_any_key(stdscr)


def mainLoop(stdscr):
    curses.curs_set(0)
    h, w = stdscr.getmaxyx()

    printIntroScr(stdscr)
    
    curr_row_idx = 0 
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    main_menu = ["Play IPD", "View Stats", "Quit"]

    while 1:
        stdscr.clear()
        print_menu(stdscr, curr_row_idx, main_menu)
        key = stdscr.getch()
        stdscr.clear()

        if key == curses.KEY_UP:
            if curr_row_idx == 0:
                curr_row_idx = len(main_menu) - 1
            else:
                curr_row_idx -= 1
        elif key == curses.KEY_DOWN:
            if curr_row_idx == len(main_menu) -1:
                curr_row_idx = 0
            else:
                curr_row_idx += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if curr_row_idx == 0:
                playIPD(stdscr)
            elif curr_row_idx == 1:
#                printCenteredText(stdscr, ["Stats is still under construction.", "=("])
#                add_any_key(stdscr)            
                printStats(stdscr)
            elif curr_row_idx == 2:
                quitProgram()
