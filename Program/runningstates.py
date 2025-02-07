import curses
from Program import guirenderers
from Program import objmanagement as scene
from Program import config


borderWidthX = 9
borderWidthY = 7
def printscreen(window, render_chars, render_colours):
    for i in range(config.resolution['y']):
        for j in range(config.resolution['x']):

            if  type(render_colours[i][j]) == tuple:
                textCol = render_colours[i][j][0]
                highlightCol = render_colours[i][j][1]
                window.attron(curses.color_pair(highlightCol * 10 + textCol))
            window.addstr(borderWidthY + i - 1, borderWidthX + j - 1, chr(render_chars[i][j]))
            if type(render_colours[i][j]) == tuple:
                window.attroff(curses.color_pair(highlightCol * 10 + textCol))

def loading(window, max_x, max_y):
    window.attron(curses.color_pair(8))
    guirenderers.drawbox(window, "Loading...", 64, max_x - 30 - 1, 30, 5, max_x, max_y)
    window.attroff(curses.color_pair(8))

def printui(window, max_x, max_y, selected_pair, texture, state):
    box_width = 20
    plusminus_box_width = 3
    box_height = 3
    box_y = 1
    box_x_1 = 1  # (paint bucket)
    box_x_2 = box_x_1 + box_width + 2  # (change texture)
    box_x_3 = max_x - box_width - 1  # (save and quit) top right
    box_x_plus = box_x_2 + box_width + 4
    box_x_minus = box_x_plus + plusminus_box_width + 1
    
    if state == 2:
        pcolor = 3
    else:
        pcolor = 8
    
    if state == 3:
        tcolor = 3
    else:
        tcolor = 8
        

    window.attron(curses.color_pair(pcolor))  
    guirenderers.drawbox(window, "Paint Bucket     ", box_y, box_x_1, box_width, box_height, max_x, max_y)
    window.addstr(box_y + 1, box_x_1 + 14, "####", curses.color_pair(selected_pair))
    window.attroff(curses.color_pair(pcolor))

    window.attron(curses.color_pair(tcolor)) 
    guirenderers.drawbox(window, "Change Texture     ", box_y, box_x_2, box_width + 2, box_height, max_x, max_y)
    window.addstr(box_y + 1, box_x_2 + 16, texture * 4 , curses.color_pair(8))
    window.attroff(curses.color_pair(tcolor))

    window.attron(curses.color_pair(2))  
    guirenderers.drawbox(window, "Save and Quit", box_y, box_x_3, box_width, box_height, max_x, max_y)
    window.attroff(curses.color_pair(2))

    window.attron(curses.color_pair(8))  
    guirenderers.drawbox(window, "+", box_y, box_x_plus, plusminus_box_width, box_height, max_x, max_y)
    window.attroff(curses.color_pair(8))

    window.attron(curses.color_pair(8))  
    guirenderers.drawbox(window, "-", box_y, box_x_minus, plusminus_box_width, box_height, max_x, max_y)
    window.attroff(curses.color_pair(8))

    color_box_y = box_y + box_height + 2
    color_box_x = box_x_1

    #  color squares
    for i in range(8):
        window.attron(curses.color_pair(i + 1))  
        for x in range(2):  # height in lines
            window.addstr(color_box_y + x, color_box_x, "#" * 5)  # width in characters
        window.attroff(curses.color_pair(i + 1))
        color_box_y += box_height + 1 

    for i in range(8):
        highlight_pair = (i + 1) * 10 + (i + 1)  # height in lines
        window.attron(curses.color_pair(highlight_pair))  
        for x in range(2): 
            window.addstr(color_box_y + x, color_box_x, "#" * 5)  # width in characters
        window.attroff(curses.color_pair(highlight_pair))
        color_box_y += box_height + 1  #step down 1 line

    return (box_y, box_x_1, box_width, box_height), (box_y, box_x_2, box_width, box_height), (box_y, box_x_3, box_width, box_height), (box_y, box_x_plus, plusminus_box_width, box_height), (box_y, box_x_minus, plusminus_box_width, box_height)

def checkstatechange(paint_bucket_box, change_texture_box, save_quit_box, x, y):

    if (paint_bucket_box[1] <= x <= paint_bucket_box[1] + paint_bucket_box[2] and
        paint_bucket_box[0] <= y <= paint_bucket_box[0] + paint_bucket_box[3]):
        print ("Paint Bucket has been pressed")
        return 2


    elif (change_texture_box[1] <= x <= change_texture_box[1] + change_texture_box[2] and
            change_texture_box[0] <= y <= change_texture_box[0] + change_texture_box[3]):
        print ("Change Texture has been pressed")
        return 3

    elif (save_quit_box[1] <= x <= save_quit_box[1] + save_quit_box[2] and
            save_quit_box[0] <= y <= save_quit_box[0] + save_quit_box[3]):
        print ("Save and Quit has been pressed")
        return -1
    
    else:
        return 1
    
def checkbuttonchange(plus_box, minus_box, x, y):

    if (plus_box[1] <= x < plus_box[1] + plus_box[2]):  # '<' instead of '<=' to prevent overlap
        if plus_box[0] <= y <= plus_box[0] + plus_box[3]:
            print("Plus has been pressed")
            scene.scaleMesh(True)
            return True 

    if (minus_box[1] <= x < minus_box[1] + minus_box[2]):  # '<' instead of '<='
        if minus_box[0] <= y <= minus_box[0] + minus_box[3]:
            print("Minus has been pressed")
            scene.scaleMesh(False)
            return True
    
    return False 

            
            

def checkcolorchange(paint_bucket_box, x, y, selected_pair):

    color_box_y = paint_bucket_box[0] + paint_bucket_box[3] + 2
    color_box_x = paint_bucket_box[1]  
    box_found = False 

    for i in range(8):
        if (color_box_y <= y <= color_box_y + 3 and
            color_box_x <= x <= color_box_x + 8) and not box_found:
            selected_pair = (((selected_pair // 10) * 10) + i + 1)
            print("Text Color {i + 1} has been pressed")
            box_found = True
        color_box_y += 4

    for i in range(8):
        if (color_box_y <= y <= color_box_y + 3 and
            color_box_x <= x <= color_box_x + 8) and not box_found:
            selected_pair = (((i + 1) * 10) + selected_pair % 10)
            print("Highlight Color {i + 1} has been pressed")
            box_found = True
        color_box_y += 4
    
    return selected_pair

