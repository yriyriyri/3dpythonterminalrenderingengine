import numpy ##can remove for final export
import math
from Program import config

epsilon = numpy.finfo(float).eps

def doRender(myMesh):
    global render
    respectiveTriangles = [[0 for i in range(config.resolution['x'])] for j in range(config.resolution['y'])]
    respectiveColours = [[0 for i in range(config.resolution['x'])] for j in range(config.resolution['y'])]
    respectiveVertices = numpy.full_like(render, 9)
    for i in range(render.shape[0]):
        for j in range(render.shape[1]): ##for each pixel in screen# goes for each x for each y . looping vertically down then across
            d = rayDirections[i][j][:]
            closestT = 10000
            closestTriangle = None
            for triangleInScene in myMesh.Triangles:
                a = myMesh.Points[triangleInScene.pointIndexes[0]][:]
                b = myMesh.Points[triangleInScene.pointIndexes[1]][:]
                c = myMesh.Points[triangleInScene.pointIndexes[2]][:]
                e1 = b -a
                e2 = c - a
                raycrosse2 = numpy.cross(d, e2)
                det = numpy.dot(e1, raycrosse2)
                if abs(det) < epsilon:
                    continue
                invdet = 1 / det
                s = -a
                u = numpy.dot(s, raycrosse2) * invdet
                if u < 0 or u > 1:
                    continue
                scrosse1 = numpy.cross(s, e1)
                v = invdet * numpy.dot(d, scrosse1)
                if v<0 or v+u>1:
                    continue
                t = invdet * numpy.dot(e2, scrosse1)
                if t>epsilon and t<closestT:
                    closestT = t
                    closestTriangle = triangleInScene
            if closestTriangle == None:

                render[i][j] = config.backgroundASCII
                
            else:
                render[i][j] = closestTriangle.char
                respectiveTriangles[i][j] = closestTriangle
                respectiveColours[i][j] = (closestTriangle.txtColour, closestTriangle.highlightColour)


    return (render, respectiveTriangles, respectiveVertices, respectiveColours)


render = None
camPos = [0, 0, 0] ##camera direction is 0, 0, 1
rayDirections = None
camProjectionWidth = 2#so going from -1 to +1

#INITIALISATION
def initialise(dimensions : dict):
    global render 
    camProjectionHeight = config.resolution['y']/config.resolution['x'] * camProjectionWidth
    camProjectionOriginDistance = camProjectionHeight/math.tan(math.radians(config.fov/2))
    render = numpy.empty((dimensions['y'], dimensions['x']), dtype=numpy.ubyte)
    global rayDirections
    rayDirections = numpy.empty((dimensions['y'], dimensions['x'], 3)) #preloading all rays is maybe too hard on memory. maybe change precision here
    for i in range(dimensions['y']):
        for j in range(dimensions['x']):
            xRawPos = ( ((i + 0.5) / dimensions['x'] ) - 0.5) * camProjectionWidth
            yRawPos = ( ((j + 0.5) / dimensions['y'] ) - 0.5) * camProjectionHeight * -1
            rawDirVector = numpy.array([xRawPos, yRawPos, camProjectionOriginDistance])
            length = numpy.linalg.norm(rawDirVector)
            dirVector = rawDirVector/length #now normalised
            rayDirections[i, j, :] = dirVector






        

    