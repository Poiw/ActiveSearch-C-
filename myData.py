import sys
from PIL import Image
import numpy as np

image_rows = 480
image_cols = 640
camera_tx = 320
camera_ty = 240
camera_f = 585

def calcoord(c, r, depth, pose):
    z = depth / 1000
    x = (c - camera_tx) * z / camera_f
    y = (r - camera_ty) * z / camera_f

    v = np.array([x, y, z, 1])
    coord = np.dot(pose, v)
    return coord[0:3]

def main():
    if len(sys.argv) < 3:
        print(' parameter error')
        exit(0)
    
    dataListname = str(sys.argv).split()[1][1:-2]
    dataBundlename = str(sys.argv).split()[2][1:-2]

    fileList = []
    with open(dataListname) as f:
        buf = f.readlines()
        for line in buf:
            fileList.append(line[0:-11])

    print(fileList)

    depth_suffix = '.depth.png'
    pose_suffix = '.pose.txt'

    with open(dataBundlename) as f:
        buf = f.readlines()

    cameraNum = int(buf[1].split()[0])
    pointNum = int(buf[1].split()[1])

    print('{} {}'.format(cameraNum, pointNum))

    output = []
    output.append(buf[0])
    output.append(buf[1])

    for i in range(cameraNum):
        output.append('585 0 0\n')
        pose = np.loadtxt(fileList[i] + pose_suffix)
        output.append('{} {} {}\n'.format(pose[0, 0], pose[0, 1], pose[0, 2]))
        output.append('{} {} {}\n'.format(pose[1, 0], pose[1, 1], pose[1, 2]))
        output.append('{} {} {}\n'.format(pose[2, 0], pose[2, 1], pose[2, 2]))
        output.append('{} {} {}\n'.format(pose[0, 3], pose[1, 3], pose[2, 3]))

    index = 5 * cameraNum + 2
    for i in range(502, 502 + pointNum):

        cameras = buf[index+2].split()[1:]
        num = int(buf[index+2].split()[0])
        print(num)
        print(buf[index], end='')

        xx = []
        yy = []
        zz = []

        for j in range(0, 4*num, 4):
            x = float(cameras[j+2])
            y = float(cameras[j+3])

            x = 320 + x
            y = 240 + y

            idx = int(cameras[j])

            pose = np.loadtxt(fileList[idx] + pose_suffix)
            depth = np.array(Image.open(fileList[idx] + depth_suffix))

            coord = calcoord(x, y, depth[int(y)][int(x)], pose)

            print(coord)

            xx.append(coord[0])
            yy.append(coord[1])
            zz.append(coord[2])

        print('')

        # output.append('{} {} {}\n'.format(np.median(xx), np.median(yy), np.median(zz)))
        output.append('{} {} {}\n'.format(xx[0], yy[0], zz[0]))
        output.append(buf[index+1])
        output.append(buf[index+2])

        index += 3
    

    with open(dataBundlename+'.motify', 'w') as f:
        for line in output:
            f.write(line)

if __name__ == '__main__':
    main()
