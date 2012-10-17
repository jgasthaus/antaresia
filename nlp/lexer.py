#!/bin/env python
import re
import sys

wordsRegex = re.compile(r"[A-Za-z]+(?:[-'@_.][A-Za-z]+)*")

def lex(regex, instring):
  return  regex.findall(instring)

def main():
  if len(sys.argv) == 1:
    regex = wordsRegex
  else:
    regex = re.compile(sys.argv[1])
  for line in sys.stdin:
    sys.stdout.write(' '.join(lex(regex, line)))
    sys.stdout.write('\n')

if __name__ == '__main__':
  main()
