#!/usr/bin/env python

"""

"""

import sys
import pandas as pd
import numpy as np
from numpy.linalg import norm
import matplotlib.pyplot as plt
import math

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

def five_hit_list( neuro_dic ):
    neuro_hits_dic = {}
    for neuron in neuro_dic.keys():
        neuron_df = neuro_dic[ neuron ]
        hits, hits_dic = [], {}
        for partner in neuron_df['partner'].values:
            if partner in hits_dic.keys():
                hits_dic[ partner ] += 1
            else:
                hits_dic[ partner ] = 1
        for partner in hits_dic.keys():
            if hits_dic[ partner ] >= 5:
                hits.append( partner )
        if len( hits ) != 0:
            neuro_hits_dic[ neuron ] = hits
    return neuro_hits_dic
    
def five_hit_centroids( neuro_dic, neuro_hits_dic ):
    five_hit_std_dic = {}
    for neuron in neuro_hits_dic.keys():
        centroid_dic = {}
        if len( neuro_hits_dic[ neuron ] ) == 0:
            pass
        else:
            for line in neuro_dic[ neuron ].values:
                if line[1] in set( neuro_hits_dic[ neuron ] ):
                    if line[1] in set( centroid_dic.keys() ):
                        centroid_dic[ line[1] ].append( line[0] )
                    else:
                        centroid_dic[ line[1] ] = [ line[0] ]
        sd_dic = find_std_from_centroids( centroid_dic )
        five_hit_std_dic[ neuron ] = sd_dic
    return five_hit_std_dic
    
def find_std_from_centroids( centroid_dic ):
    std_dic = {}
    for partner in centroid_dic.keys():
        distances = []
        centroid = np.mean( centroid_dic[ partner ], axis=0 )
        for coord in centroid_dic[ partner ]:
            distances.append( norm( coord - centroid ) )
        std_dic[ partner] = np.std( distances )
    return std_dic
    
def plot_stds( std_dic ):
    plt.figure()
    last = 0
    for neuron in std_dic.keys():
        x = [ x + last for x in range( len( std_dic[ neuron ].keys() ) ) ]
        last = x[-1] + 2
        plt.bar( x, std_dic[ neuron ].values() )
    plt.ylabel( 'stdev of distance from centroid')
    plt.savefig( 'five_hit_deviance_plot.png' )
    plt.close()
    
def std_histogram( std_dic ):
    stds = []
    for neuron in std_dic.keys():
        for partner in std_dic[ neuron ].keys():
            if math.isnan( std_dic[ neuron ][ partner ] ) == True:
                pass
            else:
                stds.append( std_dic[ neuron ][ partner ] )
    plt.figure()
    plt.hist( stds, bins=180, color='red' )
    plt.xlabel( 'stdev of distance from centroid')
    plt.ylabel( 'count' )
    plt.savefig( 'five_hit_deviance_hist.png' )
    plt.close()
    
def find_min_deviants( std_dic ):
    for neuron in std_dic.keys():
        for partner in std_dic[ neuron ].keys():
            print '%s\t%s\t%s' % ( neuron, partner, std_dic[ neuron ][ partner ] )
        
def main():
    neuro_dic = extend_neuron_df( read_synapse_by_neuron() )
    neuro_hits_dic = five_hit_list( neuro_dic )
    std_dic = five_hit_centroids( neuro_dic, neuro_hits_dic )
    #plot_stds( std_dic )
    find_min_deviants( std_dic )
    std_histogram( std_dic )
    
main()