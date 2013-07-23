import numpy as np

class MemBlock:
  """A wrapper around a flat numpy array that allows several
  arrays of different shapes to be stored with offsets in 
  one underlying array.
  
  Useful for storing model parameters for optimization.
  """
  def __init__(self, shapes, mem = None, dtype = np.float64):
    """Initialize MemBlock.

      @shapes A dictionary mapping names (strings) to shape tuples
      @mem A numpy array to use as storage (a new array will be allocated 
           if not provided).
    """

    self.dtype = dtype
    self.total_size = 0
    self.shapes = shapes
    for k,v in shapes:
      self.total_size += np.prod(v)
    self.alloc(mem)

  def alloc(self, mem = None):
    """Allocate or assign a new underlying memory block to this 
    object. The mappings will be updated to point to this new memory area.
    """
    if mem != None:
      if mem.size == self.total_size and mem.dtype == self.dtype:
        self.mem = mem
      else:
        raise ValueError("Provided memory block has wrong size/type!")
    else:
      self.mem = np.zeros(self.total_size, dtype = self.dtype)
    self._makeViews()

  def _makeViews(self):
    offset = 0
    for k,v in self.shapes:
      size = np.prod(v)
      a = self.mem[offset:offset + size]
      a.shape = v
      self.__dict__[k] = a
      offset += size


  def __repr__(self):
      return "< MemBlock instance @ %s, underlying mem @ %s, shapes: %s >" % (hex(id(self)), hex(id(self.mem)), str(self.shapes))



def vectorFromDict(d, N):
  """Given a dictionary mapping keys 0...N-1 to floats, 
  produce a vector v such that v[i] = d[i] if i in d and 
  0.0 otherwise."""
  v = np.zeros(N)
  for (k,val) in d.iteritems():
    v[k] = val
  return v


def coinflip(alpha):
  return (np.random.rand()<alpha)*1
    

def xlogy(x,y):
    """Compute x log(y) in such a way that 0 log(0) = 0"""
    if x == 0.0:
        return 0.0
    else:
        return x * np.log(y)


def sample_multinomial(unnormalized_probs, N = 1):
  cumprobs = np.cumsum(unnormalized_probs)
  u = np.random.rand(N)*cumprobs[-1]
  return np.sum(cumprobs[:, np.newaxis] < u[np.newaxis, :], 0)


def softmax(a, axis=0):
  a -= np.max(a, axis)
  np.exp(a,a)
  a /= np.sum(a,axis)


def blockavg(a, block_size = 1000):
  idx = range(0, len(a), block_size)
  res = np.add.reduceat(a, idx) / float(block_size)
  res[-1] = res[-1] * block_size / (len(a)-idx[-1])
  return res

def inverseCDF(cdf,values):
    return cdf.searchsorted(values)

def counts_to_index(counts):
    """Transform an array of counts to the corresponding array of indices, 
    i.e. [2,3,1] -> [0,0,1,1,1,2]
    """
    idx = np.empty(np.sum(counts),dtype=np.int32)
    k = 0
    for i in range(len(counts)):
        for j in range(counts[i]):
            idx[k] = i
            k += 1
    return idx

# Multinomial distribution
def rmultinomial(p, N):
    if N==0:
        return zeros(len(p),dtype=int32)
    else:
        return np.random.multinomial(N, p)

def residual_resampling(weights):
    """Residual resampling. The counts in each bin are floor(w*N) + N' where
    N' is sampled from a multinomial with the residual weights."""
    N = weights.shape[0]
    counts = np.floor(weights*N)
    R = int(np.sum(counts))
    new_weights = (weights*N - counts)/(N-R)
    counts += rmultinomial(new_weights,N-R)
    return counts_to_index(np.array(counts,dtype=np.int32))

def stratified_resampling(weights):
    N = weights.shape[0]
    # obtain u_i drawn from U(i/N,(i+1)/N)
    us = 1./N*np.arange(N) + 1./N*np.random.rand(N) 
    return inverseCDF(np.cumsum(weights),us)
