#!/usr/bin/env python3

import argparse
import sys
import numpy as np
import h5py


parser = argparse.ArgumentParser(description='Read, explore, and  process an HDF5 file.')

# Positional argument: filename
parser.add_argument('filename', help='Name of the HDF5 file to be processed.')

# Optional argument: verbose
parser.add_argument('-e', '--explore', action='store_true', help='Explore contents in detail.')

# Optional argument: dataset
parser.add_argument('-d', '--dataset', metavar='DATASET', help='Specify the dataset to print.')

# Optional argument: dataset
parser.add_argument('-o', '--output', action='store_true', help='Whether to store DATASET in a file.')

args = parser.parse_args()
filin =  h5py.File(args.filename, "r")
def listkeys(obj):
    keylist = list(filin.keys())
    print("Keys:", keylist)
def explore_hdf5(obj, path='/'):
    if isinstance(obj, h5py.Group):
        for key, val in obj.items():
            explore_hdf5(val, path + key + '/')
    elif isinstance(obj, h5py.Dataset):
        print(f'Dataset: {path} | Shape: {obj.shape} | Data Type: {obj.dtype}')
def get_dataset(name, group):
    if isinstance(group, h5py.Group):
        for key, val in group.items():
            get_dataset(key, val)
    elif isinstance(group, h5py.Dataset):
        data = group[()]
        print(f"{name} is {data.dtype}")
        print(data)
        if args.output:
            fout.write(f"{name}\n")
            if data.ndim in (1,2):
                np.savetxt(fout, data, delimiter="  ")
                fout.write("\n")
            else:
                fout.write(f"{data}\n")
if not args.explore:
    listkeys(filin)
else:
    explore_hdf5(filin)
if args.output:
    fout = open(args.dataset, 'w')
else:
    fout =''
if args.dataset:
    group = filin[args.dataset]
    get_dataset(args.dataset, group)
if fout:
    fout.close()
