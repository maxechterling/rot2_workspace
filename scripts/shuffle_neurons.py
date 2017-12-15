#!/usr/bin/env python

"""
Usage:
./shuffle_neurons.py synapse_by_neuron.txt

"""

import sys
import pandas as pd
import numpy as np
from random import randint

def split_coord( coord ):
    coord = coord.lstrip('(').rstrip(')').split()
    return np.array( map( float, coord ) )
    
def read_synapse_by_neuron():
    neuro_dic, count = {}, 0
    with open( sys.argv[1] ) as f:
        for line in f:
            count += 1
            if line.startswith('>'):
                key, count = line.lstrip('>').rstrip('\n'), 1
            elif count == 2:
                syn_names = line.rstrip('\n').split('\t')
            elif count == 3:
                syn_type = line.rstrip('\n').split('\t')
            else:
                coords = line.rstrip('\n').split('\t')
                coords = [ split_coord( coord ) for coord in coords ]
                if len(syn_names) == len(syn_type) and len(syn_type) == len(coords):
                    neuro_dic[ key ] = pd.DataFrame( {'partner': syn_names, 'type': syn_type, \
                                                    'coord': coords} )
                else:
                    pass
    return neuro_dic
    
def extend_neuron_df( neuro_dic ):
    extended_dic = {}
    for neuron in neuro_dic.keys():
        extended = []
        for entry in neuro_dic[ neuron ].values:
            for synapse in entry[1].split(','):
                extended.append( [ entry[0], synapse, entry[2] ])
        extended_dic[ neuron ] = pd.DataFrame( extended, columns=['coord', 'partner', 'type'] )
    return extended_dic
    
def shuffle_df( neuron_df ):
    coords, partners, typ = neuron_df[['coord']].values, neuron_df[['partner']].values, \
                            neuron_df[['type']].values
    coords, partners, typ = [ entry[0] for entry in coords ], [ entry[0] for entry in partners ], [ entry[0] for entry in typ ]
    s_coords, s_partners, s_typ = [], [], []
    for i in range( len( coords ) ):
        x , y, z = randint( 0, len(coords) - 1 ), randint( 0, len(coords) - 1 ), randint( 0, len(coords) - 1 )
        s_coords.append( coords[x] ), s_partners.append( partners[y] ), s_typ.append( typ[z] )
        del coords[x]
        del partners[y]
        del typ[z]
    return s_coords, s_partners, s_typ
    
def print_output( neuron, s_coords, s_partners, s_type ):
    print '>%s' % (neuron)
    print '\t'.join( s_partners )
    print '\t'.join( s_type )
    t_coords = []
    for coord in s_coords:
        if len( coord ) != 0:
            c = '(%s   %s  %s)' % ( coord[0], coord[1], coord[2] )
            t_coords.append( c )
    print '\t'.join( t_coords )
    
def main():
    neuro_dic = extend_neuron_df( read_synapse_by_neuron() )
    for neuron in neuro_dic.keys():
        coords, partners, typ = shuffle_df( neuro_dic[ neuron ] ) 
        print_output( neuron, coords, partners, typ )
        
    #shuffle_df( neuro_dic['ADAR'] )
    
main()