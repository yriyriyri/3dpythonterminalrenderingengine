import curses
from Program import guirenderers
from Program import objmanagement as scene
from Program import files as fileHandling
from Program import encodedecode

fileSelected = None

def openingscreen(window, max_x, max_y):
    curses.mousemask(curses.ALL_MOUSE_EVENTS)  # Enable mouse events

    title_exit_width = 45
    box_x_title = (curses.COLS - title_exit_width) // 2
    files = fileHandling.MakeDirectoryAndGetFileList()

    # To store the coordinates and dimensions of file boxes
    file_boxes = []

    while True:
        window.clear()
        y_increment = 5  # starting y for title

        window.attron(curses.color_pair(2))
        guirenderers.drawbox(window, "3D CONSOLE RENDERER", y_increment, box_x_title, title_exit_width, 5, max_x, max_y)
        window.attroff(curses.color_pair(2))
        y_increment += 6  # increment under title (related to box height, box height + 1)

        file_boxes = []  # reset the list of file box coordinates for each start

        # file boxes
        for i, file in enumerate(files):
            color_pair = (i % 4) + 3  # cycle through colors (3, 4, 5, 6)
            box_x_file = (curses.COLS - (len(file) + 5)) // 2  # center
            if y_increment + 2 < curses.LINES and box_x_file + (len(file) + 5) <= curses.COLS:
                window.attron(curses.color_pair(color_pair))
                guirenderers.drawbox(window, f"{i + 1}. {file}", y_increment, box_x_file, (len(file) + 5), 3, max_x, max_y)
                window.attroff(curses.color_pair(color_pair))
                file_boxes.append((y_increment, box_x_file, 3, len(file) + 5, i))
                y_increment += 4
            else:
                break

        window.attron(curses.color_pair(7))
        guirenderers.drawbox(window, "Enter 'q' to exit", y_increment, box_x_title, title_exit_width, 5, max_x, max_y)
        window.attroff(curses.color_pair(7))

        window.refresh()

        key = window.getch()

        if key == ord('q'):
            return True  # exit the program

        if key == curses.KEY_MOUSE:
            _, mouse_x, mouse_y, _, _ = curses.getmouse()
    
            for (y, x, height, width, file_index) in file_boxes:
                if y <= mouse_y < y + height and x <= mouse_x < x + width:
                    # process the selection
                    window.clear()
                    global fileSelected
                    fileSelected = file_index
                    selected_file = files[file_index][0]
                    print(f"Selected file: {selected_file}")
                    plaintext = fileHandling.readfile(file_index)
                    meshData = encodedecode.decode(plaintext)
                    scene.importMesh(meshData[0], meshData[1])
                    scene.translateMesh(0, 0, 3)
                    return False  # proceed to the main program