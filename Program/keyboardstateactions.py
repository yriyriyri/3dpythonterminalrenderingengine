from Program import objmanagement as scene

def keyboardstateaction(state, key ):
    
    if state == 1:
        if key == ord('a'):
            scene.rotateMesh(1)
            return True
        if key == ord('d'):
            scene.rotateMesh(-1)
            return True
        if key == ord('w'):
            scene.rotateMesh(2)
            return True
        if key == ord('s'):
            scene.rotateMesh(-2)
            return True
        if key == ord('e'):
            scene.rotateMesh(3)
            return True
        if key == ord('q'):
            scene.rotateMesh(-3)
            return True


