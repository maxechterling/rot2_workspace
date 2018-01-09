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
    
# def connected_components( simple_graph ):
#     explored, queue = [], [ simple_graph.keys()[0] ]
#     while queue:
#         if queue[0] not in set( explored ):
#             explored.append( queue[0] )
#             if queue[0] in simple_graph.keys():
#                 to_visit = set( simple_graph[ queue[0] ] ) - set( explored )
#                 queue = queue + list( to_visit )
#         del queue[0]
#     #print set( simple_graph.keys() ) - set( explored )
        
def main():
    coord_graph, simple_graph = graph_dic( 'post' )
    print len( simple_graph.keys() )
    connected = connected_components( simple_graph )
    
main()