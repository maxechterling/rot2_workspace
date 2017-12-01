#!/usr/bin/env python
import sys
with open( sys.argv[1] ) as f:
    for line in f:
        if line.startswith('mysql>'):
            print line.rstrip('\r\n').split()[-1]