import curses

def drawbox(window, text, y, x, width, height, max_x, max_y):

    if y < 0 or x < 0 or y + height >= max_y or x + width > max_x:
        return  # skip drawing if out of bounds
    
    horizontalBorder = "─"
    verticalBorder = "│"
    cornerTl = "┌"
    cornerTr = "┐"
    cornerBl = "└"
    cornerBr = "┘" 
    #  top border
    window.addstr(y, x, cornerTl + horizontalBorder * (width - 2) + cornerTr)  
    # side borders
    for i in range(1, height - 1):  # leave space for the top and bottom borders
        window.addstr(y + i, x, verticalBorder)
        window.addstr(y + i, x + width - 1, verticalBorder)
    
    # bottom border
    window.addstr(y + height - 1, x, cornerBl + horizontalBorder * (width - 2) + cornerBr)
    
    # denter the text between the top and bottom borders
    text_x = x + (width - len(text)) // 2
    text_y = y + (height - 1) // 2
    window.addstr(text_y, text_x, text)
    
    window.refresh()