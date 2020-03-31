import sys
from PIL import Image
import numpy as np

image_rows = 480
image_cols = 640
camera_tx = 320
camera_ty = 240
camera_f = 585
voxelSize = 0.05

def calcoord(c, r, depth, pose):
    z = depth / 1000
    x = (c - camera_tx) * z / camera_f
    y = (r - camera_ty) * z / camera_f

    v = np.array([x, y, z, 1])
    coord = np.dot(pose, v)
    return coord[0:3]

def getIndex(coord):
    x, y, z = coord[0], coord[1], coord[2]
    return (int(x // voxelSize), int(y // voxelSize), int(z // voxelSize))

def main():
    if len(sys.argv) < 2:
        print(' parameter error')
        exit(0)
    
    dataListname = str(sys.argv).split()[1][1:-2]

    fileList = []
    with open(dataListname) as f:
        buf = f.readlines()
        for line in buf:
            fileList.append(line[0:-11])

    depth_suffix = '.depth.png'
    pose_suffix = '.pose.txt'
    key_suffix = '.color.key'
    color_suffix = '.color.png'

    spaceMap = dict()
    for frameid, filename in enumerate(fileList):
        color_img = np.array(Image.open(filename + color_suffix))
        depth_img = np.array(Image.open(filename + depth_suffix))
        pose = np.loadtxt(filename + pose_suffix)
        
        with open(filename + key_suffix) as f:
            buf = f.readlines()
            num = int(buf[0].split()[0])
            usedIndex = []
            for idx in range(num):
                r, c = float(buf[idx*8+1].split()[0]), float(buf[idx*8+1].split()[1])
                coord = calcoord(c, r, depth_img[int(r), int(c)], pose)
                coordIndex = getIndex(coord)
                if coordIndex in usedIndex:
                    continue
                usedIndex.append(coordIndex)
                # print('{} {}'.format(c, r))
                # print(coord)
                # print(coordIndex)
                if coordIndex in spaceMap:
                    spaceMap[coordIndex].append((frameid, idx, c - 320, r - 240, color_img[int(r), int(c)], coord))
                else:
                    spaceMap[coordIndex] = [(frameid, idx, c - 320, r - 240, color_img[int(r), int(c)], coord)]

    spacePoints = []
    for idx in spaceMap:
        tmp = spaceMap[idx]
        # print(tmp)
        if len(tmp) > 1:
            points = []  
            coordx = []
            coordy = []
            coordz = []
            colorr = []
            colorg = [] 
            colorb = []
            for point in tmp:
                points.append((point[0], point[1], point[2], point[3]))
                coordx.append(point[5][0])
                coordy.append(point[5][1])
                coordz.append(point[5][2])
                colorr.append(point[4][0])
                colorg.append(point[4][1])
                colorb.append(point[4][2])

            spacePoints.append(( (np.median(coordx), np.median(coordy), np.median(coordz)), (np.median(colorr), np.median(colorg), np.median(colorb)), points))

    print('start write')
    with open('./Bundler/info/bundle.ours', 'w') as f:
        f.write('# Bundle file v0.3\n')
        f.write('{} {}\n'.format(len(fileList), len(spacePoints)))
        for i in range(len(fileList)):
            f.write('585 0 0\n')
            pose = np.loadtxt(fileList[i] + pose_suffix)
            pose = np.linalg.inv(pose)
            f.write('{} {} {}\n'.format(pose[0, 0], pose[0, 1], pose[0, 2]))
            f.write('{} {} {}\n'.format(pose[1, 0], pose[1, 1], pose[1, 2]))
            f.write('{} {} {}\n'.format(-pose[2, 0], -pose[2, 1], -pose[2, 2]))
            f.write('{} {} {}\n'.format(pose[0, 3], pose[1, 3], -pose[2, 3]))
        for point in spacePoints:
            f.write('{} {} {}\n'.format(point[0][0], point[0][1], point[0][2]))
            f.write('{} {} {}\n'.format(int(point[1][0]), int(point[1][1]), int(point[1][2])))
            cameraNum = len(point[2])
            print(cameraNum)
            f.write('{} '.format(cameraNum))
            for p in point[2]:
                f.write('{} {} {} {} '.format(p[0], p[1], p[2], p[3]))
            f.write('\n')
        

if __name__ == '__main__':
    main()
    print('done.')
