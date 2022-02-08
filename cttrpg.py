from curses import wrapper
from CursesApp import CursesApp
import os, shutil

# Check for data folder
if not 'data' in os.listdir() :
    os.mkdir('data')
    shutil.copytree('DefaultConfiguration', 'data/SampleDeck')
if os.listdir('data') == [] :
    shutil.copytree('DefaultConfiguration', 'data/SampleDeck')



def main(stdscr):
    # Clear screen
    stdscr.clear()

    app = CursesApp(stdscr)


wrapper(main)
