from collections import defaultdict
import numpy as np

def getNGramCounts(data, N):
  """Count the occurences of all N+1 grams in the 
  data. Outputs a dictionary mapping histories of length N
  to a histogram dictionary."""
  counts = defaultdict(dict)
  for i in xrange(N,len(data)):
    history = tuple(data[i-N:i])
    obs = data[i]
    if obs in counts[history]:
      counts[history][obs] += 1
    else:
      counts[history][obs] = 1
  return counts


def generateContextSymbolPairs(input, n):
    for i in xrange(n,len(input)):
        yield (input[i-n:i], input[i])


def computeLogLoss(predictor, data, maxContextLength=1000):
  N = len(data)
  probabilities = np.zeros(N)
  for i in xrange(N):
    probabilities[i] = predictor(tuple(data[max(0,i-maxContextLength):i]), data[i])
  losses = -np.log(probabilities)/np.log(2)
  logloss = np.mean(losses)
  perplexity = 2**logloss
  return logloss, perplexity, probabilities
