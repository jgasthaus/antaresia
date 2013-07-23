class Dictionary():
  def __init__(self):
    self.counter = 1
    self.forward = {}
    self.backward = ["[OOV]"]
    self.freq = [0]

  def insert(self, token):
    if not token in self.forward:
      self.forward[token] = self.counter
      self.backward.append(token)
      self.freq.append(1)
      self.counter += 1
      return self.counter - 1
    else:
      self.freq[self.forward[token]] += 1
    return self.forward[token]

  def mapForward(self, token, update=False):
    if update:
      return self.insert(token)
    else:
      if token in self.forward:
        return self.forward[token]
      else:
        return 0
  
  def mapBackward(self, id):
    if id < len(self.backward):
      return self.backward[id]
    else:
      return "[OOV]"

  def insertAll(self,l):
    for i in l:
      self.insert(i)

  def prune(self, min_freq):
    """Prune dictionary to only contain types
    that occur more than min_freq times."""
    new_forward = {}
    new_backward = ["OOV"]
    new_freq = [0]
    j = 1
    for i in xrange(1,len(self.backward)):
      f = self.backward[i]
      if self.freq[i] >= min_freq:
        new_forward[f] = j
        new_backward.append(f)
        new_freq.append(self.freq[i])
        j += 1
    self.forward = new_forward
    self.backward = new_backward
    self.freq = new_freq
    self.counter = j
    
  def loadFromFile(self, filename):
    self.forward = {}
    self.counter = 1
    self.backward = ["[OOV]"]
    self.freq = [0]
    f = open(filename, 'r')
    for line in f:
      items = line[:-1].split('\t')
      if len(items) == 2:
        type = items[1]
        freq = int(items[0])
      else:
        type = items[0]
        freq = 0
      self.forward[type] = self.counter
      self.backward.append(type)
      self.freq.append(freq)
      self.counter += 1
    f.close()

  def saveToFile(self, filename):
    f = open(filename, 'w')
    for i in xrange(1,len(self.backward)):
      f.write(''.join([str(self.freq[i]), '\t', self.backward[i], '\n']))
    f.close()


  def __getitem__(self, key):
    if key < len(self.backward):
      return self.backward[key]
    else:
      return "[OOV]"


