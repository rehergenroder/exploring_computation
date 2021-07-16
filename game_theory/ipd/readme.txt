Iterated Prisoners' Dilemma

This program is an attempt at exploring strategies in an IPD.
    It currently has the ability to import and export culminative stats about various strategies

Run with "python3 ipd.py" or "python3 ipd.py --tui" for ncurses display

Necessary modules:
    -quantumrandom 
    -curses 
    -pandas

Current strategies:
    -quantumrandom
    -tit for tat
    -tit for two tat
    -pavlov
    -GRIM

Future Updates:
    -gui
    -more strats
    -statistical analysis slash visualizations
    -refactor "basic" to "batch"
        --having a way to pit one strat against all others would be good

Updates:
    7/16/21
        --basic stats on tui working
        --more work on ncurses tui
        --logic cleanup
        --refactoring directories
    7/15/21
        --Refactored IPD.py such that it displays help. 
        --Created "--tui" argument which invokes ncurses
            --(Note: ncurses tui isn't fully functional yet.)
