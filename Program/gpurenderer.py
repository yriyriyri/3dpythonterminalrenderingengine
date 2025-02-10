

import cupy as cp
import math
from Program import config

epsilon = cp.finfo(float).eps

def doRender(myMesh):
    global render
    respectiveTriangles = cp.zeros((config.resolution['y'], config.resolution['x']), dtype=cp.int32)
    respectiveColours = cp.zeros((config.resolution['y'], config.resolution['x'], 2), dtype=cp.int32)
    respectiveVertices = cp.full_like(render, 9)

    rayDirections_cp = cp.asarray(rayDirections)

    for i in range(render.shape[0]):
        for j in range(render.shape[1]):
            d = rayDirections_cp[i, j, :]
            closestT = 10000
            closestTriangle = None
            for triangleInScene in myMesh.Triangles:
                a = cp.array(myMesh.Points[triangleInScene.pointIndexes[0]])
                b = cp.array(myMesh.Points[triangleInScene.pointIndexes[1]])
                c = cp.array(myMesh.Points[triangleInScene.pointIndexes[2]])
                e1 = b - a
                e2 = c - a
                raycrosse2 = cp.cross(d, e2)
                det = cp.dot(e1, raycrosse2)
                if abs(det) < epsilon:
                    continue
                invdet = 1 / det
                s = -a
                u = cp.dot(s, raycrosse2) * invdet
                if u < 0 or u > 1:
                    continue
                scrosse1 = cp.cross(s, e1)
                v = invdet * cp.dot(d, scrosse1)
                if v < 0 or v + u > 1:
                    continue
                t = invdet * cp.dot(e2, scrosse1)
                if t > epsilon and t < closestT:
                    closestT = t
                    closestTriangle = triangleInScene
            if closestTriangle is None:
                render[i, j] = config.backgroundASCII
            else:
                render[i, j] = closestTriangle.char
                respectiveTriangles[i, j] = closestTriangle
                txt_color = closestTriangle.txtColour
                high_color = closestTriangle.highlightColour
                respectiveColours[i, j, 0] = txt_color
                respectiveColours[i, j, 1] = high_color

    return render, respectiveTriangles, respectiveVertices, respectiveColours

render = None
camPos = cp.array([0, 0, 0])
rayDirections = None
camProjectionWidth = 2

# INITIALISATION
def initialise(dimensions: dict):
    global render
    camProjectionHeight = config.resolution['y'] / config.resolution['x'] * camProjectionWidth
    camProjectionOriginDistance = camProjectionHeight / math.tan(math.radians(config.fov / 2))
    render = cp.empty((dimensions['y'], dimensions['x']), dtype=cp.ubyte)
    global rayDirections
    rayDirections = cp.empty((dimensions['y'], dimensions['x'], 3), dtype=cp.float32)  # Use float32 for lower precision
    for i in range(dimensions['y']):
        for j in range(dimensions['x']):
            xRawPos = (((i + 0.5) / dimensions['x']) - 0.5) * camProjectionWidth
            yRawPos = (((j + 0.5) / dimensions['y']) - 0.5) * camProjectionHeight * -1
            rawDirVector = cp.array([xRawPos, yRawPos, camProjectionOriginDistance])
            length = cp.linalg.norm(rawDirVector)
            dirVector = rawDirVector / length
            rayDirections[i, j, :] = dirVector
