#!/usr/bin/env python

"""
Usage:
./density_mapper.py synapse_by_neuron.txt
"""

import sys

def read_all_coords():
    with open( sys.argv[1] ) as f:
        coords = []
        for line in f:
            if line.startswith('('):
                for c in line.rstrip('\r\n').split('\t'):
                    line = c.lstrip('(').rstrip(')').split()
                    coords.append( [ float(n) for n in line ] )
        return coords
      
def min_max( coords ):
    x, y, z = [ i[0] for i in coords ], [ i[1] for i in coords ], [ i[2] for i in coords ]
    return [ max(x), min(x), max(y), min(y), max(z), min(z) ]
    
def group_coords( coords, bounds, step ):
    x_start, y_start, z_start = bounds[1], bounds[3], bounds[5]
    x_stop, y_stop, z_stop = bounds[0], bounds[2], bounds[4]
    for x in range( int(x_start), int(x_stop), 200 ):
        for x in range( int( x_start ) ):
            print x
               
def main():
    coords = read_all_coords()
    bounds = min_max( coords )
    group_coords( coords, bounds, 200 )

main()
