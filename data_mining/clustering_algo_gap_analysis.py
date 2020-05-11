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
    delta.append(0)
    for i in range(1, len(list)):
        delta_i = int(list[i]) - int(list[i-1])
        delta.append(delta_i)

    if threshold==-1: # If argument is not gave
        """threshold = 0.2 * max(delta)"""
        threshold = 254
    
    print("threshold = " + str(threshold))

    # STEP 3 : to create clusters based on delta
    subcluster = []
    for i in range(0, len(list)):
        if delta[i] <= threshold :
            subcluster.append(list[i])
        else :
            clusters.append(subcluster)
            subcluster = []
            subcluster.append(list[i])
    clusters.append(subcluster)

    return clusters


if __name__ == "__main__":
    print("----------------- PORT CLUSTERING --------------------------")
    my_list_port = [1,3,4,9,6,4,89,43]
    res = CAGA(my_list_port,-1)
    for x in range(len(res)):
        print("CLUSTER " + str(x))
        for y in range(len(res[x])):
            print("   " + str(res[x][y]))


    print("----------------- IP CLUSTERING --------------------------")
    addr1 = ipaddress.ip_address('192.0.2.1')
    addr2 = ipaddress.ip_address('192.0.2.5')
    addr3 = ipaddress.ip_address('192.0.4.1')
    addr4 = ipaddress.ip_address('192.0.5.1')
    
    my_list_ip = [int(addr1), int(addr2), int(addr3), int(addr4)]
    
    res = CAGA(my_list_ip,-1)

    print("brut : " + str(res))

    for x in range(len(res)):
        print("CLUSTER " + str(x))
        for y in range(len(res[x])):
            res[x][y] = ipaddress.ip_address(res[x][y])
            print("   " + str(res[x][y]))

    