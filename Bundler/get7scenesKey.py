import os
import numpy as np 
import sys



def main():
    if len(sys.argv) < 2:
        print(' parameter error')
        exit(0)
    
    dataDir = str(sys.argv).split()[1][1:-2]
    print(dataDir)

    trainDir = os.path.join(dataDir, 'ours')

    os.system('../RunBundler.sh ' + trainDir)
    with open('list.txt') as f:
        buf = f.readlines()
    with open(os.path.join(dataDir, 'trainList.txt'), 'w') as f:
        for line in buf:
            if line[0] == '\n':
                continue

            f.write(line)

    testsplit = []
    with open(os.path.join(dataDir, 'TestSplit.txt')) as f:
        buf = f.readlines()
        for line in buf:
            testsplit.append('seq-{0:02d}'.format(int(line[8:])))

    testList = []
    for seqname in testsplit:
        testDir = os.path.join(dataDir, seqname)
        os.system('../RunBundler.sh ' + testDir)
        with open('list.txt') as f:
            buf = f.readlines()

        for line in buf:
            if line[0] == '\n':
                continue
            testList.append(line)

    with open(os.path.join(dataDir, 'testList.txt'), 'w') as f:
        for line in testList:
            f.write(line)


        

if __name__ == '__main__':
    main()
    print('done.')
