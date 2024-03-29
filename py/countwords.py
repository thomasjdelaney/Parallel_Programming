import os, sys, glob, time
if float(sys.version[:3])<3.0:
    execfile(os.path.join(os.environ['HOME'], '.pystartup'))
import re
import datetime as dt
from functools import reduce
from multiprocessing import Pool, cpu_count

proj_dir = os.path.join(os.environ['PROJ'], 'Practice', 'Parallel_Programming')
shake_dir = os.path.join(proj_dir, 'shakespeare')

shake_files = glob.glob(os.path.join(shake_dir, '*'))

def count_words(filename):
    """
    Count the number of times every word in the file `filename` is contained in this file.
    Args:       filename (str): the filename to count the words multiprocessing
    Returns:    dict: a mapping of word to count
    """
    all_words = {}
    with open(filename) as f:
        for line in f:
            words = line.split()
            for word in words:
                #lowercase the word and remove all
                #characters that are not [a-z] or hyphen
                word = word.lower()
                match = re.search(r"([a-z\-]+)", word)
                if match:
                    word = match.groups()[0]
                    if word in all_words:
                        all_words[word] += 1
                    else:
                        all_words[word] = 1
    return all_words

def reduce_dicts(dict1, dict2):
    """
    Combine (reduce) the passed two dictionaries to return
    a dictionary that contains the keys of both, where the
    values are equal to the sum of values for each key
    """
    # explicitly copy the dictionary, as otherwise we risk modifying 'dict1'
    combined = {}
    for key in dict1:
        combined[key] = dict1[key]
    for key in dict2:
        if key in combined:
            combined[key] += dict2[key]
        else:
            combined[key] = dict2[key]
    return combined

def print_dict(final_dict):
    for k in sorted(final_dict.keys()):
        if final_dict[k] > 2000:
            print(dt.datetime.now().isoformat() + ' INFO: ' + k + ': ' + str(final_dict[k]))
    return None

if __name__ == "__main__":
    start_time = dt.datetime.now()
    num_workers = int(sys.argv[1]) if 1 < len(sys.argv) else cpu_count()
    chunk_size = max(1, int(len(shake_files)/int(sys.argv[2]))) if 2 < len(sys.argv) else int(len(shake_files)/2)
    with Pool(num_workers) as pool:
        word_dict_future = pool.map_async(count_words, shake_files, chunksize = chunk_size)
        while not word_dict_future.ready():
            print(dt.datetime.now().isoformat() + ' INFO: ' + 'Counting words...')
            time.sleep(0.5)
        print(dt.datetime.now().isoformat() + ' INFO: ' + 'Counting finished.') 
    final_dict = reduce(reduce_dicts, word_dict_future.get())
    print_dict(final_dict)
    end_time = dt.datetime.now()
    print(dt.datetime.now().isoformat() + ' INFO: ' + 'Time taken:' + str(end_time - start_time))
