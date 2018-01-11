#!/usr/bin/env python

"""
Usage:
./pathfinder2.py synapse_by_neuron.txt
"""

import sys
import numpy as np

def graph_dic( type_oi ):
    graph_dic, simple_graph = {}, {}
    with open( sys.argv[1] ) as f:
        count = 0
        for line in f:
            if count == 0:
                key = line.lstrip('>').rstrip('\r\n')
                count += 1
            elif count == 1:
                partners = line.rstrip('\r\n').split()
                count += 1
            elif count == 2:
                types = line.rstrip('\r\n').split()
                count += 1
            elif count == 3:
                line = line.rstrip('\r\n').split('\t')
                coords = [ np.array( coord.lstrip('(').rstrip(')').split() ).astype( 'float' ) \
                           for coord in line ]
                count = 0
                graph_dic[ key ] = make_entry( partners, types, coords, type_oi )
                partners_split = []
                for partner in partners:
                    partners_split = partners_split + partner.split(',')
                simple_graph[ key ] = partners_split
    return graph_dic, simple_graph
            
def make_entry( partners, types, coords, type_oi ):
    entry = {}
    for i in range( len( partners ) ):
        if types[i] == type_oi:
            for p in partners[i].split(','):
                if p in set( entry.keys() ):
                    entry[p].append( coords[i] )
                else:
                    entry[p] = [ coords[i] ]
    return entry
    
def find_strong_component( simple_graph ):
	for neuron in simple_graph.keys():
		print neuron
        
def main():
    coord_graph, simple_graph = graph_dic( 'post' )
    connected = find_strong_component( simple_graph )
    
main()