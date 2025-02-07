import curses
from Program import config
from Program import renderer
from Program import objmanagement as scene

def mousestatechecks(state,button, render_data, selected_pair, texture, x, y,):
    
    global dragging 
    global drag_start_x, drag_start_y

    if state == 1:
        if button & curses.BUTTON1_PRESSED:
            dragging = True
            drag_start_x, drag_start_y = x-9, y-7


        elif button & curses.BUTTON1_RELEASED:
            if dragging:
                dragging = False                
                renderX = x - 9
                renderY = y - 7
                if renderX >= 0 and renderY >= 0 and renderX < config.resolution['x'] and renderY < config.resolution['y']:
                    if scene.startMovingVertex((drag_start_y, drag_start_x), render_data[1], renderer.rayDirections):
                        scene.stopMovingVertex((renderY, renderX), renderer.rayDirections)
                        return True

                
    if state == 2:
        if button & curses.BUTTON1_CLICKED:
            
            state = 1
            renderX = x - 9
            renderY = y - 7
            if renderX >= 0 and renderY >= 0 and renderX < config.resolution['x'] and renderY < config.resolution['y'] and type(render_data[1][renderY][renderX]) == scene.triangle:
                render_data[1][renderY][renderX].highlightColour = selected_pair // 10
                render_data[1][renderY][renderX].txtColour = selected_pair % 10
                return True


    if state == 3:
        if button & curses.BUTTON1_CLICKED:

            state = 1
            renderX = x - 9
            renderY = y - 7
            if renderX >= 0 and renderY >= 0 and renderX < config.resolution['x'] and renderY < config.resolution['y'] and type(render_data[1][renderY][renderX]) == scene.triangle:
                render_data[1][renderY][renderX].char = ord(texture)
                return True