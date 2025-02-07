
import cupy as cp
from Program import config

camdistanceoffset = 3
totaloffset = cp.array([0, 0, 0], dtype=cp.float32)

class triangle:
    def __init__(self, pointIndexes: list, char: int, txtC: int, highC: int):
        self.pointIndexes = pointIndexes  # Use list of indices
        self.char = char
        self.txtColour = txtC
        self.highlightColour = highC

class mesh:
    def __init__(self):
        self.Points = cp.array([])  # Initialize Points as an empty CuPy array
        self.Triangles = []
        # Arrays to store attributes for rendering
        self.triangle_indices = cp.array([], dtype=cp.int32)
        self.triangle_chars = cp.array([], dtype=cp.int32)
        self.triangle_txt_colours = cp.array([], dtype=cp.int32)
        self.triangle_highlight_colours = cp.array([], dtype=cp.int32)

    def initCube(self, subdivisions: int = 1):
        # Cube initialization code (unchanged)
        pass

    def rotate(self, axis, delta=22.5):
        # Rotation code (unchanged)
        pass

    def translate(self, dx, dy, dz):
        # Translation code (unchanged)
        pass

    def scale(self, isEnlarge: bool):
        # Scaling code (unchanged)
        pass

    def importedMesh(self, points, triangles):
        self.Points = cp.array(points, dtype=cp.float32)
        self.Triangles = triangles
        # Convert triangles to attributes
        self.triangle_indices = cp.array([tri.pointIndexes for tri in triangles], dtype=cp.int32)
        self.triangle_chars = cp.array([tri.char for tri in triangles], dtype=cp.int32)
        self.triangle_txt_colours = cp.array([tri.txtColour for tri in triangles], dtype=cp.int32)
        self.triangle_highlight_colours = cp.array([tri.highlightColour for tri in triangles], dtype=cp.int32)

def importMesh(points, triangles):
    global mainMesh
    mainMesh = mesh()
    mainMesh.importedMesh(points, triangles)

def getMesh():
    return mainMesh

def translateMesh(dx, dy, dz):
    mainMesh.translate(dx, dy, dz)

def rotateMesh(ax: int):
    mainMesh.rotate(ax)

def scaleMesh(isEnlarge):
    mainMesh.scale(isEnlarge)

vertexIndexBeingMoved = None
def startMovingVertex(pixelClicked: tuple, respectiveTriangles, rayDirections):
    global mainMesh
    global vertexIndexBeingMoved
    lowestDistance = 9999
    if respectiveTriangles[pixelClicked[0]][pixelClicked[1]] == 0:
        return False
    for pointIndex in respectiveTriangles[pixelClicked[0]][pixelClicked[1]].pointIndexes:
        thisPoint = mainMesh.Points[pointIndex][:]  # Use CuPy array
        d = rayDirections[pixelClicked[0]][pixelClicked[1]][:]
        perpendicularDistance = cp.linalg.norm(cp.cross(thisPoint, d) / cp.linalg.norm(d))
        if perpendicularDistance < lowestDistance and perpendicularDistance < config.vertexDistanceToCursorMax:
            lowestDistance = perpendicularDistance
            vertexIndexBeingMoved = pointIndex
    if lowestDistance == 9999:
        return False
    return True

planeNorm = cp.array([0, 0, -1], dtype=cp.float32)
def stopMovingVertex(pixelReleased: tuple, rayDirections):
    global mainMesh
    global vertexIndexBeingMoved
    global planeNorm
    rayOfRelease = rayDirections[pixelReleased[0]][pixelReleased[1]]
    planeCoord = mainMesh.Points[vertexIndexBeingMoved][:]  # Use CuPy array
    dot = cp.dot(planeNorm, rayOfRelease)
    fac = cp.dot(planeNorm, planeCoord) / dot
    intersection = rayOfRelease * fac
    mainMesh.Points[vertexIndexBeingMoved][:] = intersection

