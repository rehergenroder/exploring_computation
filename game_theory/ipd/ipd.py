# IPD.py differentiates between interaction type:
#   --basic
#   --ncurses tui

import argparse

def main(args):
    if args.tui:
        import lib.ipd_curses as nc
        nc.main()
    else:
        import lib.ipd_basic as ib
        ib.main()


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
