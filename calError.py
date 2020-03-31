import sys
from PIL import Image
import numpy as np
import os
import cv2
import math

def main():
    if len(sys.argv) < 3:
        print(' parameter error')
        exit(0)
    
    dataListname = str(sys.argv).split()[1][1:-2]
    poseDir = str(sys.argv).split()[2][1:-2]

    fileList = []
    with open(dataListname) as f:
        buf = f.readlines()
        for line in buf:
            fileList.append(line[0:-11])

    pose_suffix = '.pose.txt'

    terr, rerr = [], []
    mdet = []

    for frameid, filename in enumerate(fileList):
        pose = np.loadtxt(filename + pose_suffix)
        std_rot = pose[0:3,0:3]
        std_trans = pose[0:3, 3]

        pred_rot = np.zeros((3, 3))
        pred_trans = np.zeros(3)

        with open(os.path.join(poseDir,'pose_{}.txt'.format(frameid))) as f:
            buf = f.readlines()
            for i in range(3):
                line = buf[i].split()
                pred_rot[i][0], pred_rot[i][1], pred_rot[i][2] = float(line[1][:-1]), float(line[2][:-1]), float(line[3])
            pred_trans[0], pred_trans[1], pred_trans[2] = float(buf[3].split()[0]), float(buf[3].split()[1]), float(buf[3].split()[2])

        pred = np.zeros((4,4))
        for i in range(3):
            for j in range(3):
                pred[i,j] = pred_rot[i,j]
        pred[0:3,0:3] = pred_rot
        pred[0,3], pred[1,3], pred[2,3] = pred_trans[0], pred_trans[1], pred_trans[2]
        pred[3,3] = 1

        # pred = -pred
        # pred[3,3] = 1
        # pred = np.linalg.inv(pred)

        pred[0, 1] = -pred[0, 1]
        pred[0, 2] = -pred[0, 2]
        pred[1, 1] = -pred[1, 1]
        pred[2, 2] = -pred[2, 2]

        mdet.append(np.linalg.det(pred))

        pred_trans = pred[0:3, 3]
        pred_rot = pred[0:3,0:3]

        rvec = cv2.Rodrigues(np.linalg.inv(pred_rot) @ std_rot)

        tmp_err = np.linalg.norm(rvec[0]) / math.pi * 180
        rerr.append(min(tmp_err, 180-tmp_err))
        terr.append(np.linalg.norm(pred_trans - std_trans))

        print(pred)

    with open('result.txt', 'w') as f:
        for i in range(len(terr)):
            te = terr[i]
            re = rerr[i]
            f.write('{} {} {} {}\n'.format(i, te, re, mdet[i]))
        f.write('median {} {}\n'.format(np.median(terr), np.median(rerr)))



        
        
        

if __name__ == '__main__':
    main()
    print('done.')
