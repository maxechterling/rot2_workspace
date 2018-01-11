#!/usr/bin/env python

"""
Find the shortest path between neurons by distance
Usage:
./path_finder.py

"""
import sys
import pandas as pd 

def read_in_neurons():
	with open( sys.argv[1] ) as f:
		for line in f:
			print line

def main():
	read_in_neurons()

main()