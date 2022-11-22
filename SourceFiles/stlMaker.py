from madcad import *

def generateSTL(coordinates, fileNumber):
    part = read('SourceFiles/world.stl')

    maxCylinderHeight = 100
    minCylinderHeight = 30

    #Map satellite radialLengths to cylinder heights if there are more than one selected satellite
    if len(coordinates.keys()) >= 2:
        maxRad = 0
        minRad = 99999
        for name, data in coordinates.items():
            maxRad = max(maxRad, data[2])
            minRad = min(minRad, data[2])

    for data in coordinates.values():
        lon = data[0]
        lat = data[1]
        rad = data[2]

        if len(coordinates.keys()) >= 2:
            height = (rad - minRad) / (maxRad - minRad) * (maxCylinderHeight - minCylinderHeight) + minCylinderHeight
        else:
            height = 50

        print(height)

        if lon > 180:
            lon = -180+lon-180

        x = 179 * (180 + lon) / 360
        y = 74 * (90 + lat) / 180

        part.mergeclose()# merge points at the same location

        ahull = vec3(x, y, 0)
        bhull = vec3(x, y, height)

        hull = cylinder(ahull,bhull, 1, True)

        # your desired operations (example)
        #transformed = pierce(part, hull)
        part = union(part, hull)

    write(part, f'SatellitePositions{fileNumber}.stl')

if __name__ == '__main__':
    generateSTL(None)