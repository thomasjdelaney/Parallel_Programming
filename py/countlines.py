import os, sys, glob
import datetime as dt
from functools import reduce
from multiprocessing import Pool

proj_dir = os.path.join(os.environ['PROJ'], 'Practice', 'Parallel_Programming')
shake_dir = os.path.join(proj_dir, 'shakespeare')

shake_files = glob.glob(os.path.join(shake_dir, '*'))

def countLinesInFile(file_name):
    with open(file_name) as f:
        for i, l in enumerate(f):
            pass
    print(dt.datetime.now().isoformat() + ' INFO: ' + os.path.basename(file_name) + ': ' + str(i+1) + ' lines.')
    return i+1

if __name__ == "__main__":
    with Pool() as pool:
        counts = pool.map(countLinesInFile, shake_files)
    l = list(counts)

    total_lines = reduce(lambda x,y: x+y, l)
    print(dt.datetime.now().isoformat() + ' INFO: ' + 'Total lines: ' + str(total_lines))
