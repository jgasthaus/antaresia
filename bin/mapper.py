#!/usr/bin/env python
from antaresia.nlp import Dictionary
import sys
from optparse import OptionParser
from os.path import exists
from array import array

def mapForward(infile, d, modifyDict=False, separator = ' '):
    for line in infile:
        yield ' '.join([str(d.mapForward(w, modifyDict)) 
                       for w in line.strip().split(separator) if w != '']) + '\n'

def mapForwardBinary(infile, d, modifyDict=False, separator = ' '):
    for line in infile:
      a = array("i")
      a.extend([d.mapForward(w, modifyDict) 
                       for w in line.strip().split(separator) if w != ''])
      a.append(0) # EOL marker
      yield a.tostring() 

def mapBackward(infile, d, separator = ' '):
    for line in infile:
        yield ' '.join([str(d.mapBackward(int(w))) 
                        for w in line.strip().split(separator) if w != '']) + '\n'

def make_dict(in_list):
    d = Dictionary()
    for line in in_list:
        for w in line:
            d.insert(w)
    return d

def write_dict(d, outfile):
    f = open(outfile,'w')
    for w in d.backward:
        f.write(w + '\n')

def main():
    usage = "usage: %s [options] [infile] [outfile]" % (sys.argv[0],)
    o = OptionParser(usage=usage)
    o.add_option("-d", "--dictfile", type="string",
            help="File name of the dictionary file", dest="dictfile",
            metavar="DICTFILE")
    o.add_option("-f", "--fix-dict", action="store_true", dest="fix_dict",
            help="Keep dictionary fixed (i.e. do not insert new types",
            default=False)
    o.add_option("--readonly", action="store_true", dest="readonly",
            help="don't Write new or updated dictionary to DICTFILE",
            default=False)
    o.add_option("-b", "--backward", action="store_true", dest="backward", 
        help="Map backwords from ids to dictionary entries")
    o.add_option("-s", "--separator", type="string", dest="separator", 
        help="Charcter(s) used as separator between words")
    o.add_option("--binary", action="store_true", dest="binary", 
        help="Write output file as binary 32 bit ints")

    (options,args) = o.parse_args()

    if len(args) < 1:
        infile = sys.stdin
    else: 
        infile = open(args[0],'r')
    if len(args) < 2:
        outfile = sys.stdout
    else:
        outfile = open(args[1],'wb')


    d = Dictionary()
    if options.dictfile != None and exists(options.dictfile):
        print >> sys.stderr,  "loading dictionary from " + options.dictfile
        d.loadFromFile(options.dictfile)

    if options.backward:
      out = mapBackward(infile, d, options.separator)
    else:
      if options.binary:
        out = mapForwardBinary(infile, d, not options.fix_dict, options.separator)
      else:
        out = mapForward(infile, d, not options.fix_dict, options.separator)

    for l in out:
        outfile.write(l)
    
    if (not options.backward 
        and options.dictfile != None 
        and not options.readonly):
      print >> sys.stderr, "writing dictionary to " + options.dictfile
      d.saveToFile(options.dictfile)
    
main()
