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

def network(ip1, ip2):
    tab1 = [None]*32
    tab2 = [None]*32
    q1=ip1
    q2=ip2
    for i in range(31,-1,-1):
        r1 = q1%2
        q1 = q1//2
        r2 = q2%2
        q2 = q2//2
        tab1[i] = r1
        tab2[i] = r2
    n = 0
    net = [0]*32
    for j in range(0,32):
        if tab1[j]==tab2[j]:
            n += 1
            net[j] = 1
    net_int = int("".join(str(x) for x in net), 2) 
    ip = ip1&net_int
    ip = str(ipaddress.IPv4Address(ip)) + "/" + str(n)
    return (ip)

def IP2Network(IP, net_bits, net_number):
    IP = str(ipaddress.IPv4Address(IP)) + "/" + str(net_number)
    return IP