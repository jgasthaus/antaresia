def filterKeys(d, allowedKeys):
  return dict((k,d[k]) for k in d if k in allowedKeys)


def invertMap(map):
  return dict((v,k) for k, v in map.iteritems())


def getterWithDefault(D, defaultKey, defaultValue = None):
  if defaultKey not in D and not defaultValue:
    raise KeyError(str(defaultKey) + " not in D and no defaultValue provided!")
  if defaultKey in D and not defaultValue:
    defaultValue = D[defaultKey]
  def mapper(x):
   if x in D:
     return D[x]
   else:
     return defaultValue
  return mapper

  # return lambda x: (   ((x in D) and D[x])
  #                   or defaultValue 
  #                   or (defaultKey in D and D[defaultKey]) 
  #                   or None )
