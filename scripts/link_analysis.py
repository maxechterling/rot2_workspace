#!/usr/bin/env python

"""

Usage:
./link_analysis.py pre_post_dist.link pre_pre_dist.link

"""

import sys
import pandas as pd

def read_link( link ):
    neuron_dic = {}
    with open( link ) as f:
        first = True
        matrix = []
        for line in f:
            if line.startswith( '##' ):
                neurons = line.lstrip('##COLUMNS: ').rstrip('\r\n').split(', ')
            elif line.startswith( '>' ) and first is True:
                first = False
                key = line.lstrip('>').rstrip('\r\n')
            elif line.startswith( '>' ) and first is False:
                neuron_dic[ key ] = pd.DataFrame( matrix, columns=neurons, index=neurons )
                key = line.lstrip('>').rstrip('\r\n')
                matrix = []
            elif line.startswith( 'END' ):
                neuron_dic[ key ] = pd.DataFrame( matrix, columns=neurons, index=neurons )
            else:
                matrix.append( line.rstrip('\r\n').split(', ') )
    return neuron_dic
    
def pull_interacting_neurons( neuron_df ):
    print neuron_df.convert_objects( convert_numeric=True )
    pass
    
def main():
    pre_post_dic = read_link( sys.argv[1] )
    pull_interacting_neurons( pre_post_dic[ 'AVAR' ] )

main()