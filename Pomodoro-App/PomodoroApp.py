import argparse

import GUIGuts
import TerminalGuts
import ConstValues


# NOTE: make a array of colors so each run of the timer will have a
#       different color
# TODO: Add config file to set a default colors and time


def getCommandLineArgs():
    parser = argparse.ArgumentParser(description='Setup your Pomodoro Timer')
    parser.add_argument(
        '-nw',
        action="store_true",
        help='This flag will make the script run with out the GUI'
        ' so it will run in the terminal'
    )
    parser.add_argument(
        'Focus timer length', 
        metavar='F_Time',
        type=int,
        nargs='?',
        help='The number of minutes you want to focus for. Default: ' +
                str(ConstValues.WORK_MINUTES)+' minutes'
    )
    parser.add_argument(
        'Break timer length',
        metavar='B_Time',
        type=int,
        nargs='?',
        help='The number of minutes you want to break for. Default: ' +
                str(ConstValues.BREAK_MINUTES)+' minutes'
    )
    # parser.add_argument(
    #   'Long break timer length',
    #   metavar='L_Time',
    #   type=int,
    #   nargs='?',
    #   help='The number of minutes you want to take a long break for'
    # )
    parser.add_argument(
        'Window Width',
        metavar='w',
        type=int,
        nargs='?',
        help='Width. Default:'+str(ConstValues.WINDOW_WIDTH)
    )
    parser.add_argument(
        'Window Height',
        metavar='h',
        type=int,
        nargs='?',
        help='Height. Default:'+str(ConstValues.WINDOW_HEIGHT)
    )
    return vars(parser.parse_args())


def main():
    args = getCommandLineArgs()

    # this flag indicates if the user wants to use a GUI or not
    if args['nw']:
        TerminalGuts.Application(
            workMin=args['Focus timer length'],
            breakMin=args['Break timer length'],
            #  longBreakMin=args['Long break timer length']
        ).run()
    else:
        GUIGuts.Application(
            windowWidth=args['Window Width'],
            windowHeight=args['Window Height'],
            workMin=args['Focus timer length'],
            breakMin=args['Break timer length'],
            #  longBreakMin=args['Long break timer length']
        ).mainloop()
    return 0


if __name__ == "__main__":
    main()
