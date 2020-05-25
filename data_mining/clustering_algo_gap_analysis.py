#!/usr/bin/python
# PURPOSE : Create clusters from inputs (Clustering Algo bu Gap Analysis = CAGA)
# INPUT : List of IP addresses or port numbers and threshold (-1 if default)
# OUTPUT : List of clusters generated

import ipaddress
import numpy as np

def CAGA(list, threshold):
    delta = []
    clusters = []
    
    # STEP 1: to sort the list
    list.sort()

    # STEP 2: to compute the delta between 2 following items of the list
    delta.append(-1) # The first element cannot be compared with the previous element
    for i in range(1, len(list)):
        delta_i = int(list[i]) - int(list[i-1])
        delta.append(delta_i)

    if threshold==-1: # If argument is not gave
        """threshold = 0.2 * max(delta)"""
        threshold = 128
    
    print("threshold = " + str(threshold))

    # STEP 3 : to create clusters based on delta
    subcluster = []
    for i in range(0, len(list)):
        if delta[i] == 0:
            pass # Avoid repetition
        elif delta[i] <= threshold :
            subcluster.append(list[i])
        else :
            clusters.append(subcluster)
            subcluster = []
            subcluster.append(list[i])
    clusters.append(subcluster)

    return clusters

    