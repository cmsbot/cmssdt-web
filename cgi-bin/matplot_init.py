#!/usr/bin/env python
import sys

try:
  import matplotlib
except:
  matplot = '/data/sdt/SDT/matplotlib-0.99.1.1/build/lib.linux-x86_64-2.4'
  numpy ='/data/sdt/SDT/numpy-1.3.0/build/lib.linux-x86_64-2.4'
  if numpy not in sys.path:
    sys.path.append(numpy)
  if matplot not in sys.path:
    sys.path.append(matplot) 

