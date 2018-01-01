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
    
def group_by_partner( neuro_dic, min_group_size ):
    out_grouped_dic = {}
    for neuron in neuro_dic.keys():
        grouped_dic, group_size = {}, {}
        ## partner: [(coord1), (coord2), ..., (coordn)]
        for line in neuro_dic[ neuron ].values:
            if line[1] in grouped_dic.keys():
                grouped_dic[ line[1] ].append( line[0] )
                group_size[ line[1] ] += 1
            else:
                grouped_dic[ line[1] ] = [ line[0] ]
                group_size[ line[1] ] = 1
        cent_std = find_centroids_stds( grouped_dic, group_size, min_group_size )
        neuron_groups = []
        for partner in cent_std.keys():
            neuron_groups.append( [ partner, cent_std[partner][0], cent_std[partner][1], cent_std[partner][2] ] )
        df = pd.DataFrame( neuron_groups, columns=[ 'partner', 'stdev', 'centroid', 'group_size' ] )
        if df.shape[0] != 0:
            out_grouped_dic[ neuron ] = df
    return out_grouped_dic
        
def find_centroids_stds( centroid_dic, group_size, min_group_size ):
    std_dic = {}
    for partner in centroid_dic.keys():
        distances = []
        centroid = np.mean( centroid_dic[ partner ], axis=0 )
        for coord in centroid_dic[ partner ]:
            distances.append( norm( coord - centroid ) )
        if group_size[ partner ] >= min_group_size:
            std_dic[ partner] = [ np.std( distances ), centroid, group_size[ partner ] ]
    return std_dic

def get_all_neighbors( grouped_dic ):
    neighbors = []
    for neuron in grouped_dic:
        for line in grouped_dic[ neuron ].values:
            top_ind, dist = nearest_neighbor( line[2], grouped_dic[ neuron ][['centroid']].values )
            dist_stdev = dist + line[1] + grouped_dic[ neuron ]['stdev'].values[ top_ind ]
            if math.isnan( dist_stdev ) == False and dist_stdev < 10000000q:
                print line[0], grouped_dic[ neuron ]['partner'].values[ top_ind ], dist_stdev
                neighbors.append( dist_stdev )
    return neighbors
            
def nearest_neighbor( coord, coord_lst ):
    dist_lst = []
    for coord2 in coord_lst:
        if len( coord2[0] ) < 3:
            dist_lst.append( 100000000 )
        elif coord[0] == coord2[0][0] and coord[1] == coord2[0][1] and coord[2] == coord2[0][2]:
            dist_lst.append( 100000000 )
        elif coord != coord2:
            dist_lst.append( norm( coord - coord2[0] ) )
    if len(dist_lst) == 0:
        pass
    else:
        return dist_lst.index( min( dist_lst ) ), min( dist_lst )
        
def plot_histogram( neighbors1, neighbors2, neighbors3 ):
    plt.figure()
    plt.hist( neighbors1, bins=300, color='red', alpha=0.8, label='1' )
    plt.hist( neighbors2, bins=300, color='gray', alpha=0.8, label='4' )
    plt.hist( neighbors3, bins=300, color='black', alpha=0.8, label='6' )
    plt.legend()
    plt.xlabel( 'distance + SDs')
    plt.ylabel( 'count' )
    plt.savefig( 'paired_distance_grouping_histogram' )
    plt.close()
    
def main():
    neuro_dic = extend_neuron_df( read_synapse_by_neuron() )
    #grouped_dic = group_by_partner( neuro_dic, 1 )
    #grouped_dic5 = group_by_partner( neuro_dic, 4 )
    grouped_dic8 = group_by_partner( neuro_dic, 6 )
    #neighbors1 = get_all_neighbors( grouped_dic )
    #neighbors2 = get_all_neighbors( grouped_dic5 )
    neighbors3 = get_all_neighbors( grouped_dic8 )
    #plot_histogram( neighbors1, neighbors2, neighbors3 )
    
    
    
main()