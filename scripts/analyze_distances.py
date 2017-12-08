#!/usr/bin/env python

"""

Usage:

./analyze_distances.py distances.txt

"""

import sys
import numpy as np
import pandas as pd

def read_in_distances():
    dist_dic = {}
    count = 0
    with open( sys.argv[1] ) as f:
        for line in f:
            print count
            print line
            if count == 0:
                key = line.rstrip('\r\n')
                count += 1
            elif count == 1:
                count += 1
                val = [ float(x) for x in line.rstrip(']\r\n').lstrip('[').split(',') ]
                dist_dic[ key ] = val
            else:
                count = 0
    return dist_dic

def plot_histogram( dist_list, comboes, out_name=None ):
    plt.figure()
    for combo in comboes:
        plt.hist( dist_list[ combo ], bins=100, alpha=0.6, label=combo, histtype='step' )
    plt.xlabel( 'log10( distance )' )
    plt.ylabel( 'counts' )
    plt.legend()
    if out_name is None:
        plt.show()
    else:
        plt.savefig( out_name )
    plt.close()

def main():
    dist_dic = read_in_distances()
    combos = dist_dic.keys()
    print combos
    plot_histogram( dist_list, [ 'pre_pre', 'pre_all' ] )
    
main()
    
        