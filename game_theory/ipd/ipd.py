# IPD.py differentiates between interaction type:
#   --basic
#   --ncurses tui

import argparse
import subprocess


# Makes sure necessary modules are installed, if not-- installs them.
try:
    import quantumrandom
except ModuleNotFoundError:
    print("Quantumrandom not installed. Installing via pip now.")
    install = subprocess.run(["pip", "install", "quantumrandom"])
    if install.returncode == 1:
        failedInstall("quantumrandom")
try:
    import pandas
except ModuleNotFoundError:
    print("Pandas not installed. Installing via pip now.")
    install = subprocess.run(["pip", "install", "quantumrandom"])
    if install.returncode == 1:
        failedInstall("Pandas")


def failedInstall(mod_name):
    print("For some reason I cannot connect to the package manager to install " + mod_name + ".")
    print("Terminating application.")
    print("Bye bae!")
    exit(1)


# Differentiate between different interaction modes
def main(args):
    if args.tui:
        import lib.ipd_curses as nc
        nc.main()
    else:
        import lib.ipd_basic as ib
        ib.main()

# Help screen
def makeParser():
    parser = argparse.ArgumentParser(
        description="""An iterated prisoners' dilemma with variable strategies and statistical persistence.""",
        epilog="""maintained by th3_5m0k1ng_m1rr0r""")
    parser.add_argument("--tui", action="store_true", help="ncurses based tui")
    return parser

if __name__ == "__main__":
    parser = makeParser()
    args = parser.parse_args()
    main(args)
