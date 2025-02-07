import curses
import time
import sys

#terminal error check


def check_terminal_size(window):
    min_height = 10  # min height required
    min_width = 10  # min width required
    max_y, max_x = window.getmaxyx()
    
    if max_y < min_height or max_x < min_width:
        window.clear()
        window.addstr(3, 0, f"Error: Terminal size is too small. Minimum size required: {min_width}x{min_height}")
        window.addstr(4, 0, f"Please resize your terminal window and restart the program.")
        time.sleep(5)
        window.refresh()
        window.getch()
        sys.exit(1)  


#initialise colours 


def initcolors():
    curses.start_color()
    text_colors = [curses.COLOR_BLACK,curses.COLOR_YELLOW,curses.COLOR_RED,curses.COLOR_GREEN,curses.COLOR_BLUE,curses.COLOR_CYAN,curses.COLOR_MAGENTA,curses.COLOR_WHITE]

    for i, color in enumerate(text_colors, start=1):
        curses.init_pair(i, color, curses.COLOR_BLACK)
        for x, color2 in enumerate(text_colors, start=1):
            curses.init_pair((i * 10) + x, color2, color)


#initialise curses

def initmousein():
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
    curses.curs_set(0)