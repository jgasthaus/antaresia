import numpy as np
import h5py
from array import array

def readBText(fn):
  f = open(fn, "r")
  a = np.fromfile(f, dtype=np.uint32)
  return a

def writeBText(fn, xx):
  a = array("i")
  a.extend(xx)
  f = open(fn, "w")
  a.write(f)
  f.close()

def readHDF5(fn, dataset = "default"):
  parts = fn.split(":")
  if len(parts) == 1:
    f = h5py.File(fn, "r")
    d = f[dataset][:]
    f.close()
    return d
  else:
    fn = parts[0]
    datasetPath = '/'.join(parts[1:])
    f = h5py.File(fn, "r")
    print f.items()
    d = f[datasetPath][:]
    f.close()
    return d

def writeHDF5(fn, data, name = "default"):
  f = h5py.File(fn, "w")
  d = f.create_dataset(name, data=data)
  f.close()
  return d
