import curses
from Program import renderer
from Program import objmanagement as scene

# from Program import gpurenderer
# from Program import gpuobjmanagement as scene

from Program import config
from Program import encodedecode
from Program import files as fileHandling
from Program import frontendinitialisation
from Program import startuprocedures
from Program import runningstates
from Program import closingprocedures
from Program import mousestateactions
from Program import keyboardstateactions

def main(window):
    frontendinitialisation.check_terminal_size(window)
    frontendinitialisation.initcolors()
    frontendinitialisation.initmousein()
    state = 1 #1 for normal, 2 for paint state, 3 for texture, -1 for quit
    selected_pair = 8
    texture = "#"
    max_y, max_x = window.getmaxyx()
    config.resolution['x'] = max_x - runningstates.borderWidthX
    config.resolution['y'] = max_x - runningstates.borderWidthY
    config.resolution['x'] = 66
    config.resolution['y'] = 66
    renderer.initialise(config.resolution)

    if startuprocedures.openingscreen(window, max_x, max_y):  # startup procedures
        return
    
    doRender = True
    dragging = False
    drag_start_x, drag_start_y = -1, -1
    
    while True: #input loop running states

        if doRender:
            runningstates.loading(window, max_x, max_y)
            render_data = renderer.doRender(scene.getMesh())
            doRender = False

        window.clear()
        runningstates.printscreen(window, render_data[0], render_data[3])
        paint_bucket_box, change_texture_box, save_quit_box, plus_box, minus_box = runningstates.printui(window, max_x, max_y, selected_pair, texture, state)
        window.refresh()  
        key = window.getch()

        if key == curses.KEY_MOUSE and state != -1:
            _, x, y, _, button = curses.getmouse()
            selected_pair = runningstates.checkcolorchange(paint_bucket_box, x, y, selected_pair)

            if mousestateactions.mousestatechecks(state, button, render_data, selected_pair, texture, x, y):
                doRender = True
            
            state = runningstates.checkstatechange(paint_bucket_box, change_texture_box, save_quit_box, x, y)
            buttonstate = runningstates.checkbuttonchange(plus_box, minus_box, x, y)
            if buttonstate == True:
                doRender = True
        
        if state == -1:
            break

        if keyboardstateactions.keyboardstateaction(state, key):
            doRender = True 
        
        if state == 3:
            if 32 <= key <= 126:
                texture = chr(key)
                state = 1

        if key == 27:
            break

    # closing procedures

    if key != ord('q'):
        scene.translateMesh(0, 0, -3)
        result = closingprocedures.savequitscreen(window, max_x, max_y) 
        initialFile = fileHandling.readfile(startuprocedures.fileSelected)
        mesh = scene.getMesh()
        savingFile = encodedecode.encode(mesh.Points, mesh.Triangles, initialFile)
        if result == 1:
            fileHandling.writeToSavedFile(savingFile, startuprocedures.fileSelected)
            closingprocedures.endscreen(window, max_x, max_y, "Saved to 'ShapeStorage'")
        elif result == 2:
            filename = closingprocedures.filenameentry(window, max_x, max_y)
            fileHandling.writeToNewFile(savingFile, filename + f".obj")
            closingprocedures.endscreen(window, max_x, max_y, "Saved as " + str(filename) + " to 'ShapeStorage'")

def supermain(main):
    curses.wrapper(main)