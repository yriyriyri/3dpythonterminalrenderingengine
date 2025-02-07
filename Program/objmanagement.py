import numpy
from Program import config
import random

camdistanceoffset = 3

totaloffset = numpy.array([0, 0, 0])
##centre is (0, 0, camdistoffset)
class triangle:
    def __init__(self, pointIndexes : list, char : int, txtC : int, highC : int):#sort out private variables later
        self.pointIndexes = pointIndexes # of type  array
        self.char = char
        self.txtColour = txtC ##1-49
        self.highlightColour = highC
        #PROB A GOOD IDEA    TO PRECOMPUTE NORMS HERE
class mesh:

    #Declare Points : 2d array 3 floats horizontally, however many vertically
    #declare traingles : 1d array of triangle objects
    #declare pointstotrianglemap : 1d array of 1d array of integers
    #declare pointDistances : 1d array 
    def __init__(self):
        pass

    def initCube(self, subdivisions : int = 1):
        #subdivisions is number of edges -1 in each way. NOT NUMBER OF TIMES CUT IN HALF
        numVertices = 6 * subdivisions * subdivisions + 2
        numTriangles = 3 * 4^subdivisions
        oneDimensionSliced = numpy.linspace(-1, 1, subdivisions+1)

        xPositionOfPoints = oneDimensionSliced.copy()
        for x in range(subdivisions): #filling out floor
            xPositionOfPoints = numpy.concatenate((xPositionOfPoints, oneDimensionSliced))
        for y in range(subdivisions-1): #filling out walls. looping for each vertical layer
            xPositionOfPoints = numpy.concatenate((xPositionOfPoints, oneDimensionSliced))
            for i in range(subdivisions-1): #for each vertical layer, we fill out the inner edges
                xPositionOfPoints = numpy.append(xPositionOfPoints, -1)
                xPositionOfPoints = numpy.append(xPositionOfPoints, 1)
            xPositionOfPoints = numpy.concatenate((xPositionOfPoints, oneDimensionSliced))
        for x in range(subdivisions+1): #filling out roof
            xPositionOfPoints = numpy.concatenate((xPositionOfPoints, oneDimensionSliced))

        zPositionOfPoints = numpy.array([])
        for x in range(subdivisions+1):#doing floor
            thisRow = numpy.full(subdivisions+1, oneDimensionSliced[x])
            zPositionOfPoints = numpy.concatenate((zPositionOfPoints, thisRow))
        for y in range(subdivisions-1):
            thisRow = numpy.full(subdivisions+1, -1)
            zPositionOfPoints = numpy.concatenate((zPositionOfPoints, thisRow))
            for z in range(subdivisions -1):
                thisRow = numpy.full(2, oneDimensionSliced[z+1])
                zPositionOfPoints = numpy.concatenate((zPositionOfPoints, thisRow))
            thisRow = numpy.full(subdivisions+1, 1)
        for x in range(subdivisions+1):
            thisRow = numpy.full(subdivisions+1, oneDimensionSliced[x])
            zPositionOfPoints = numpy.concatenate((zPositionOfPoints, thisRow))
        

        yPositionOfPoints = numpy.full((subdivisions +1)* (subdivisions +1), -1)
        for i in range(subdivisions-1):
            yPositionOfPoints = numpy.concatenate((yPositionOfPoints, numpy.full(subdivisions * 4, oneDimensionSliced[i+1])))
        yPositionOfPoints = numpy.concatenate( yPositionOfPoints, numpy.full((subdivisions +1)* (subdivisions +1), 1))

        for x in range(len(xPositionOfPoints)):
            print(xPositionOfPoints[x], yPositionOfPoints[x], zPositionOfPoints[x])

        #do linspace for each ubdivisons+ 1 then once morer then only -1 and 1 for inner of subdivisons then again for each layer and then do initial again
    

        #number of layers = subdivisions +1 

        
       #points need to be stored in numpy array so matrix transformations applu

    def rotate(self, axis, delta=22.5):
        delta = numpy.deg2rad(delta)
        if axis < 0:
            delta *= -1
        axis = abs(axis)
        match axis: ## +x = 1; -x = -1; +y = 2; -y = -2; +z = 3; -z = -3
            case 1:
                rtMatrix = numpy.array([[1, 0, 0], [0, numpy.cos(delta), numpy.sin(delta)], [0, -numpy.sin(delta), numpy.cos(delta)]])
            case 2:
                rtMatrix = numpy.array([[numpy.cos(delta), 0, -numpy.sin(delta)], [0, 1, 0], [numpy.sin(delta), 0, numpy.cos(delta)]])
            case 3:
                rtMatrix = numpy.array([[numpy.cos(delta), numpy.sin(delta), 0], [-numpy.sin(delta), numpy.cos(delta), 0], [0, 0, 1]])
        self.Points = numpy.subtract(self.Points, totaloffset)
        self.Points = numpy.matmul(self.Points, rtMatrix)
        self.Points = numpy.add(self.Points, totaloffset)

    def translate(self, dx, dy, dz):
        delta = numpy.array([dx, dy, dz])
        global totaloffset
        totaloffset = totaloffset + delta

        self.Points = numpy.add(self.Points, delta)
    
    def scale(self, isEnlarge : bool):
        self.Points = numpy.subtract(self.Points, totaloffset)
        if isEnlarge:
            self.Points = self.Points * config.scaleChange
        else:
            self.Points = self.Points / config.scaleChange
        self.Points = numpy.add(self.Points, totaloffset)
        


    def importedMesh(self, points, triangles):
        self.Points = points
        self.Triangles = triangles

def importMesh(points, triangles):
    global mainMesh
    mainMesh = mesh()
    mainMesh.importedMesh(points, triangles)

def getMesh():
    #if mainMesh == None:
    #    return False
    return mainMesh

def translateMesh(dx, dy, dz):
    mainMesh.translate(dx, dy, dz)

def rotateMesh(ax : int):
    mainMesh.rotate(ax)

def scaleMesh(isEnlarge):
    mainMesh.scale(isEnlarge)

vertexIndexBeingMoved = None
def startMovingVertex(pixelClicked : tuple, respectiveTriangles, rayDirections):
    global mainMesh
    global vertexIndexBeingMoved
    lowestDistance = 9999
    if respectiveTriangles[pixelClicked[0]][pixelClicked[1]] == 0:
        return False
    for pointIndex in respectiveTriangles[pixelClicked[0]][pixelClicked[1]].pointIndexes:
        thisPoint = mainMesh.Points[pointIndex][:]
        d = rayDirections[pixelClicked[0]][pixelClicked[1]][:]
        perpendicularDistance = numpy.linalg.norm(numpy.cross(thisPoint, d)/numpy.linalg.norm(d))
        if perpendicularDistance < lowestDistance and perpendicularDistance < config.vertexDistanceToCursorMax:
            lowestDistance = perpendicularDistance
            vertexIndexBeingMoved =  pointIndex
    if lowestDistance == 9999:
        return False
    return True

planeNorm = numpy.array([0, 0, -1])
def stopMovingVertex(pixelReleased : tuple, rayDirections):##plane passes thru vertexIndexBeingMoved with norm vertexIndexBeingMoved
    global mainMesh
    global vertexIndexBeingMoved
    global planeNorm
    rayOfRelease = rayDirections[pixelReleased[0]][pixelReleased[1]]
    planeCoord = mainMesh.Points[vertexIndexBeingMoved][:]
    dot = numpy.dot(planeNorm, rayOfRelease)
    fac =  numpy.dot(planeNorm, planeCoord)/ dot
    intersection = rayOfRelease * fac
    mainMesh.Points[vertexIndexBeingMoved][:] = intersection

