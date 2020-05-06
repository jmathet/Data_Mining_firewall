#!/usr/bin/python

import csv
import numpy as np
import ipaddress

IP_src = 0
IP_dst = 1
PORT_dst = 2

def read_in_csv_file(path):
    # Read in csv file and return data as matrix
    matrix = np.array([['IP SRC', 'IP DST', 'PORT SRC', 'PORT DST', 'PROTOCOL', 'ACTION']])
    with open(path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            row[0] = ipaddress.ip_address(row[0])
            row[1] = ipaddress.ip_address(row[1])
            matrix = np.concatenate((matrix,[row]),axis=0) # Adds arr2 as rows to the end of matrix

    # Add count column (1 for each row)
    count = np.ones((len(matrix),1), dtype=np.int)
    matrix = np.concatenate((matrix,count),axis=1) # Adds arr2 as columns to the end of matrix
    matrix[0,6] = 'COUNT'     

    return matrix

def get_cluster_of_membership(clusters, member):
    for cluster in clusters:
        for element in cluster:
            if member==element:
                return cluster                
    return "cluster not found"

# Function to get unique values
def unique(list): 
    # insert the list to the set 
    list_set = set(list) 
    # convert the set to the list 
    unique_list = (list(list_set)) 