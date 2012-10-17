#!/bin/env python
import json
from os.path import abspath
import os
from uuid import uuid4
import cPickle
import fcntl # for locking

class FileCollection:
  """Implements a poor man's schema-free database with an interface similar to
  that of PyMongo. Supports only a tiny subset of the PyMongo interface and is
  intended as a no-setup replacement when performance is not important 
  and no advanced features are required.
  """

  def __init__(self, dataDir='.data'):
    self.dataDir = abspath(dataDir)
    try:
      os.makedirs(self.dataDir)
    except:
      pass
    #self.lockFile = open(self.dataDir + os.sep + 'lock', 'w')


  def insert(self, doc):
    if "_id" in doc:
      id = doc['_id']
    else:
      id = self.__getNewID(doc)
    doc['_id'] = id
    self.__writeToFile(id, doc)
    return id


  def find(self, query={}, includeBinary=True):
    ids = self.__listDocIDs()
    if '_id' in query and query['_id'] in ids:
      yield self.__readFromFile(query['_id'], includeBinary)
    else:
      for id in ids:
        if self.__isMatch(id, query):
          yield self.__readFromFile(id, includeBinary)


  def find_one(self, query={}):
    try:
      return self.find(query).next()
    except:
      return None

  def find_sorted(self, query={}, sortBy=[], includeBinary=True):
    docs = [[d[k] for k in sortBy if k in d] + [d] 
            for d in self.find(query, includeBinary)]
    docs.sort()
    return [d[-1] for d in docs]
    


  def update(self, spec, doc, upsert=False):
    d = self.find_one(spec)
    if d != None:
      doc['_id'] = d['_id']
      self.__writeToFile(d['_id'], doc)
    elif upsert:
      self.insert(doc)


  def save(self, to_save):
    if '_id' in to_save:
      self.__writeToFile(to_save['_id'], to_save)
      return to_save['_id']
    else:
      return self.insert(to_save)
    

  def __lock(self):
    pass
    #fcntl.lockf(self.lockFile, fcntl.LOCK_EX)

  def __unlock(self):
    pass
    #fcntl.lockf(self.lockFile, fcntl.LOCK_UN)

  def __getNewID(self, doc):
    return unicode(uuid4())

  def __canJSON(self, var):
    if (type(var) in (str, unicode, int, long, float, bool)
       or var == None
       or (type(var) == list and all(map(self.__canJSON, var)))
       or (type(var) == tuple and all(map(self.__canJSON, var)))):
      return True
    else:
      return False


  def __splitParts(self, doc):
    jsonPart = dict((unicode(k),doc[k]) for k in doc 
                    if self.__canJSON(doc[k])
                       or k == '_dumped_keys')
    binaryPart = dict((unicode(k),doc[k]) for k in doc 
                      if unicode(k) not in jsonPart)
    return (jsonPart, binaryPart)


  def __writeToFile(self, id, doc):
      jsonPart, binaryPart = self.__splitParts(doc)
      jsonPart['_dumped_keys'] = list(binaryPart.keys())
      json_fn = self.dataDir + os.sep + id + '.json'
      binary_fn = self.dataDir + os.sep + id + '.pickle'
      self.__lock()
      json.dump(jsonPart, open(json_fn, 'w'))
      if len(binaryPart) != 0:
        cPickle.dump(binaryPart, open(binary_fn, 'wb'),
            cPickle.HIGHEST_PROTOCOL)
      self.__unlock()


  def __readFromFile(self, id, includeBinary = True):
      json_fn = self.dataDir + os.sep + id + '.json'
      binary_fn = self.dataDir + os.sep + id + '.pickle'
      self.__lock()
      jsonPart = json.load(open(json_fn, 'r'))
      doc = jsonPart
      if includeBinary and len(doc['_dumped_keys']) != 0:
        binaryPart = cPickle.load(open(binary_fn, 'rb'))
        doc.update(binaryPart)
      self.__unlock()
      return doc


  def __listDocIDs(self):
    dirpath, dirnames, filenames = os.walk(self.dataDir).next()
    ids = list(set([fn.split('.')[0] for fn in filenames if fn != 'lock']))
    return ids


  def __isMatch(self, id, query):
    json_fn = self.dataDir + os.sep + id + '.json'
    self.__lock()
    jsonPart = json.load(open(json_fn, 'r'))
    self.__unlock()
    for k in query:
      if unicode(k) not in jsonPart or jsonPart[unicode(k)] != query[k]:
        return False
    return True


def main():
  import sys
  numArgs = len(sys.argv)
  columns = None
  if numArgs > 2:
    fc = FileCollection(sys.argv[1])
    query = sys.argv[2]
  elif numArgs == 2:
    fc = FileCollection(".")
    query = sys.argv[1]
  else:
    fc = FileCollection(".")
    query = "{}"
  if numArgs > 3:
      columns = [str(k) for k in eval(sys.argv[3])]
  if columns:
    print '\t'.join(columns)
    sortBy = columns
  else:
    sortBy = []
  for d in fc.find_sorted(eval(query), sortBy, False):
    out = []
    if columns:
      for c in columns:
        if c in d:
          out.append(str(d[c]))
        else:
          out.append('N/A')
      print '\t'.join(out)
    else:
      for k in sorted(d.keys()):
        print "%s: %s" % (str(k), str(d[k]))
      print


if __name__ == '__main__':
  main()
