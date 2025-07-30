#!/usr/bin/env python3
#
# Python module to create MD5 files that contains the
#   MD5 hash of all the files in a subdirectory for digital deliveries.
# v 0.3.0
# 
# 10 Jun 2025
#
# Digitization Program Office,
# Office of the Chief Information Officer,
# Smithsonian Institution
# https://dpo.si.edu
#

# Import modules
import os
import glob
import itertools
import pandas as pd

# from pathlib import Path
from time import localtime
from time import strftime
from pathlib import Path
from multiprocessing import Pool

# Parallel
import multiprocessing
from p_tqdm import p_map


def md5sum(filename):
    """
    Get MD5 hash from a file.
    """
    # https://stackoverflow.com/a/7829658
    import hashlib
    from functools import partial
    # Open file and calculate md5 hash
    with open("{}".format(filename), mode='rb') as f:
        d = hashlib.md5()
        for buf in iter(partial(f.read, 128), b''):
            d.update(buf)
    # Return filename and md5 hash
    return filename, d.hexdigest()


def md5_file(folder=None, fileformat="m f", no_workers=multiprocessing.cpu_count(), forced=False):
    # If there is already a md5 file, ignore unless forced is True
    if len(glob.glob("{}/*.md5".format(folder))) > 0 and forced is False:
        print("\n   md5 file exists, skipping...")
        return
    # Scan the folder
    list_folder = os.scandir(folder)
    files = []
    for entry in list_folder:
        # Only get files, ignore folders
        if entry.is_file():
            files.append("{}/{}".format(folder, entry.name))
    if len(files) == 0:
        print("\n There are no files in {}".format(folder))
        return
    else:
        print("\n Running on {} using {} workers".format(folder, no_workers))
        # Calculate md5 hashes in parallel using a progress bar
        results = p_map(md5sum, files, **{"num_cpus": int(no_workers)})
        with open("{}/{}_{}.md5".format(folder, os.path.basename(folder), strftime("%Y%m%d%H%M%S", localtime())),
                  'w') as fp:
            for res in results:
                # Save according to the format selected
                if fileformat == "m f":
                    fp.write("{} {}\n".format(res[1], os.path.basename(res[0])))
                elif fileformat == "f m":
                    fp.write("{} {}\n".format(os.path.basename(res[0]), res[1]))
                elif fileformat == "m,f":
                    fp.write("{},{}\n".format(res[1], os.path.basename(res[0])))
                elif fileformat == "f,m":
                    fp.write("{},{}\n".format(os.path.basename(res[0]), res[1]))
        return


def check_md5sum(md5_file, file):
    import hashlib
    from pathlib import Path
    # https://stackoverflow.com/a/7829658
    filename = Path(file).name
    md5_hash = hashlib.md5()
    with open(file, "rb") as f:
        # Read and update hash in chunks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            md5_hash.update(byte_block)
    file_md5 = md5_hash.hexdigest()
    md5_from_file = md5_file[md5_file.file == filename]['md5'].to_string(index=False).strip()
    if file_md5 == md5_from_file:
        return (filename, file_md5, md5_from_file, 0)
    elif md5_from_file == 'Series([], )':
        return (filename, file_md5, md5_from_file, 1)
    else:
        return (filename, file_md5, md5_from_file, 1)


def check_md5_file(md5_file=None, files=None, csv=False, no_workers=1):
    """
    Compare hashes between files and what the md5 file says
    """
    try:
        no_workers = int(no_workers)
    except ValueError:
        print("Invalid value for no_workers")
        return 9, 9
    no_cores = os.cpu_count()
    if no_workers > no_cores:
        no_workers = no_cores
    if md5_file == None:
        print("Missing md5_file")
        return 9, 9
    md5_file = pd.read_csv(md5_file, sep=" ", names=('md5', 'file'))
    if files == None:
        print("Missing list of files")
        return 9, 9
    files=glob.glob(files)
    inputs = zip(itertools.repeat(md5_file), files)
    if csv:
        if os.path.isfile("results.csv"):
            try:
                os.remove("results.csv")
            except:
                return 1, "Error removing results.csv file"
    with Pool(no_workers) as pool:
        checked_files = pd.DataFrame(pool.starmap(check_md5sum, inputs), columns=("filename", "file_md5", "md5_from_file", "error"))
        pool.close()
        pool.join()
    if csv:
        checked_files.to_csv("results.csv", header = 1, index = False, mode = "w")
    if checked_files['error'].sum() > 0:
        return 1, "Hash of {} files don't match the contents of the MD5 file".format(str(checked_files['error'].sum()))
    else:
        return 0, 0
