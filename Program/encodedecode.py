from Program import objmanagement as scene
import numpy
import random

chars = ".:-=+*#%@"

def decode(plaintext : str):
    lines = plaintext.splitlines()
    vertices = []
    verticesEmpty = True 
    triangles = []    
    for line in lines:
        line = line.split()
        if len(line)>0 and len(line)<5:
            if line[0] == 'v':
                thisVert = numpy.array([float(line[1]), float(line[2]), float(line[3])])
                if verticesEmpty:
                    vertices = thisVert
                    verticesEmpty = False
                else:
                    vertices = numpy.vstack((vertices, thisVert))
            if line[0] == 'f':
                for wordindex in range(len(line)):
                    word = line[wordindex]
                    thisWord = ""
                    for char in word:
                        if char == '/':
                            break
                        thisWord = thisWord + char
                    line[wordindex] = thisWord
            
                thisTri = scene.triangle([int(line[1]) - 1, int(line[2])-1, int(line[3])-1], ord(chars[random.randint(0, 8)]), random.randint(1, 8), random.randint(1, 8))
                if triangles == []:
                    triangles = [thisTri]
                else:
                    triangles.append(thisTri)
        
        #quads handling (inefficent)
        
        if len(line)>4:
            if line[0] == 'v':
                thisVert = numpy.array([float(line[1]), float(line[2]), float(line[3])])
                thisVert2 = numpy.array([float(line[1]), float(line[3]), float(line[4])])
                if verticesEmpty:
                    vertices = thisVert
                    vertices = numpy.vstack((vertices, thisVert2))
                    verticesEmpty = False
                else:
                    vertices = numpy.vstack((vertices, thisVert))
                    vertices = numpy.vstack((vertices, thisVert2))
            if line[0] == 'f':
                for wordindex in range(len(line)):
                    word = line[wordindex]
                    thisWord = ""
                    for char in word:
                        if char == '/':
                            break
                        thisWord = thisWord + char
                    line[wordindex] = thisWord ##tweaker hold tab lol 
                
                thisTri = scene.triangle([int(line[1]) - 1, int(line[2])-1, int(line[3])-1], ord(chars[random.randint(0, 8)]), random.randint(1, 8), random.randint(1, 8)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   )
                thisTri2 = scene.triangle([int(line[1]) - 1, int(line[3])-1, int(line[4])-1], ord(chars[random.randint(0, 8)]), random.randint(1, 8), random.randint(1, 8))
                
                if triangles == []:
                    triangles = [thisTri]
                    triangles.append(thisTri2)
                else:
                    triangles.append(thisTri)
                    triangles.append(thisTri2)

    return (vertices, triangles)


def encode(vertices, triangles, originalFile: str):
    lines = originalFile.splitlines()
    vertCount = 0
    triCount = 0
    for lineIndex in range(len(lines)):
        lineByWords = lines[lineIndex].split()
        if len(lineByWords) > 0:
            if lineByWords[0] == 'v':  # Handling vertices
                if len(lineByWords) == 5:
                    pass
                else:
                    # Update vertex coordinates
                    lineByWords[1] = str(vertices[vertCount][0])
                    lineByWords[2] = str(vertices[vertCount][1])
                    lineByWords[3] = str(vertices[vertCount][2])
                    lineByWords = lineByWords[0:4]
                    vertCount += 1

            if lineByWords[0] == 'f':  # Handling faces
                # The triangle points are 1-indexed in .obj format
                lineByWords[1] = str(triangles[triCount].pointIndexes[0] + 1)
                lineByWords[2] = str(triangles[triCount].pointIndexes[1] + 1)
                lineByWords[3] = str(triangles[triCount].pointIndexes[2] + 1)
                lineByWords = lineByWords[0:4]
                triCount += 1

        lines[lineIndex] = ' '.join(lineByWords) + '\n'

    plaintext = "".join(lines)
    return plaintext
