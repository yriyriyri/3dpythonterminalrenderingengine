import curses
from Program import guirenderers
import time


def savequitscreen(window, max_x, max_y):
    curses.mousemask(curses.ALL_MOUSE_EVENTS) 

    title_exit_width = 45
    box_x_title = (curses.COLS - title_exit_width) // 2

    option_boxes = []

    while True:
        window.clear()

        y_increment = 5

        window.attron(curses.color_pair(2))
        guirenderers.drawbox(window, "SAVE AND QUIT?", y_increment, box_x_title, title_exit_width, 5, max_x, max_y)
        window.attroff(curses.color_pair(2))
        y_increment += 6

        window.attron(curses.color_pair(3))
        guirenderers.drawbox(window, "1. Save", y_increment, (curses.COLS - 12) // 2, 12, 3, max_x, max_y)
        window.attroff(curses.color_pair(3))
        option_boxes.append((y_increment, (curses.COLS - 12) // 2, 3, 12, 1))
        y_increment += 4

        window.attron(curses.color_pair(4))
        guirenderers.drawbox(window, "2. Save As", y_increment, (curses.COLS - 15) // 2, 15, 3, max_x, max_y)
        window.attroff(curses.color_pair(4))
        option_boxes.append((y_increment, (curses.COLS - 15) // 2, 3, 15, 2))
        y_increment += 4

        window.attron(curses.color_pair(5))
        guirenderers.drawbox(window, "q. Quit Without Saving", y_increment, (curses.COLS - 27) // 2, 27, 3, max_x, max_y)
        window.attroff(curses.color_pair(5))
        option_boxes.append((y_increment, (curses.COLS - 27) // 2, 3, 27, 'q'))
        y_increment += 4

        window.refresh()

        key = window.getch()

        if key == ord('q'):
            return -1

        if key == ord('1'):
            return 1
        if key == ord('2'):
            return 2

        if key == curses.KEY_MOUSE:
            _, mouse_x, mouse_y, _, _ = curses.getmouse()

            for (y, x, height, width, option) in option_boxes:
                if y <= mouse_y < y + height and x <= mouse_x < x + width:
                    if option == 'q':
                        return -1 
                    else:
                        return option  # 1 save 2 save as


def filenameentry(window, max_x, max_y):
    title_width = 45
    box_x_title = (curses.COLS - title_width) // 2

    input_str = ""
    max_input_length = 50 

    while True:
        window.clear()

        y_increment = 5
        
        window.attron(curses.color_pair(2))
        guirenderers.drawbox(window, "SAVE AS?", y_increment, box_x_title, title_width, 5, max_x, max_y)
        window.attroff(curses.color_pair(2))
        y_increment += 6

        guirenderers.drawbox(window, "Enter Filename: " + input_str, y_increment, ((curses.COLS - (len(input_str)+ 21)) // 2), (len(input_str)+ 21), 3, max_x, max_y)

        window.refresh()
        key = window.getch()
       
        #enter returns 
        if key == ord('\n'):
            if input_str:  
                return input_str

        elif key in (curses.KEY_BACKSPACE, 127, 8):
            input_str = input_str[:-1]
        
        # capture keys
        elif 32 <= key <= 126 and len(input_str) < max_input_length:
            input_str += chr(key)

def endscreen(window, max_x, max_y, text):
    window.clear()
    window.attroff(curses.color_pair(8))
    guirenderers.drawbox(window, text, max_y // 2, ((curses.COLS - (len(text) + 5)) // 2), len(text) + 5, 3, max_x, max_y)
    window.attroff(curses.color_pair(8))
    time.sleep(5)