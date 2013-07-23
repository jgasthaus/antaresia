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

def getCommitInfo():
  import os, subprocess
  """Get latest commit info for the current directory"""
  GIT_CMD = "git rev-parse HEAD"
  BZR_COMMAND = "bzr version-info"
  try:
    git_result = subprocess.check_call(GIT_CMD, stderr=None, shell=True)
    return git_result
  except:
    pass
  #git_result = os.popen(GIT_CMD).read()
  bzr_result = os.popen(BZR_COMMAND).read()
  if bzr_result[:10] != "bzr: ERROR":
    return bzr_result
