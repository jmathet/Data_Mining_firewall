#!/usr/bin/python

import csv
import numpy as np
import ipaddress
import xlsxwriter
import sys

IP_src = 0
IP_dst = 1
PORT_dst = 2
PROTO = 3
MIN_LENGTH_CLUSTER = 10

def read_in_csv_file(path):
    # Read in csv file and return data as matrix
    matrix = np.array([['IP SRC', 'IP DST', 'PORT SRC', 'PORT DST', 'PROTOCOL', 'ACTION']])
    try:
        with open(path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if (row[-1]=='permitted'):
                    row[0] = ipaddress.ip_address(row[0])
                    row[1] = ipaddress.ip_address(row[1])
                    matrix = np.concatenate((matrix,[row]),axis=0) # Adds arr2 as rows to the end of matrix

        # Add count column (1 for each row)
        count = np.ones((len(matrix),1), dtype=np.int)
        matrix = np.concatenate((matrix,count),axis=1) # Adds arr2 as columns to the end of matrix
        matrix[0,6] = 'COUNT'   
    except IOError:
        sys.exit("/!\ Cannot open " + str(path))
    else :
        print ("Read in file OK")

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
    while (n<32) and (tab1[n]==tab2[n]):
        net[n] = 1
        n += 1
    net_int = int("".join(str(x) for x in net), 2) 
    ip = ip1&net_int
    ip = str(ipaddress.IPv4Address(ip)) + "/" + str(n)
    return (ip)

def IP2Network(IP, net_bits, net_number):
    IP = str(ipaddress.IPv4Address(IP)) + "/" + str(net_number)
    return IP

def list2string(data):
    cell = str()
    for list_element in data:
        if len(cell)==0:
            cell = str(list_element)
        else:
            cell = cell + "," + str(list_element)
    return cell

def write_in_csv_file(data, path):
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet()
    # Widen the first column to make the text clearer.
    worksheet.set_column('A:A', 20)
    worksheet.set_column('B:B', 20)
    worksheet.set_column('C:C', 20)
    worksheet.set_column('D:D', 20)
    worksheet.set_column('E:E', 20)
    worksheet.set_column('F:F', 20)

    cell_format = workbook.add_format()
    cell_format.set_text_wrap()

    bold = workbook.add_format({'bold': True})

    worksheet.write('A1', 'IP SRC', bold)
    worksheet.write('B1', 'IP DST', bold)
    worksheet.write('C1', 'PORT DST', bold)
    worksheet.write('D1', 'ACTION', bold)
    worksheet.write('E1', 'COUNT', bold)
    
    for x in range(0, np.size(data,0)):
        for y in range(0,np.size(data,1)):
            if type(data[x,y])==list:
                cell = list2string(data[x,y])
            else:
                cell = str(data[x,y])       
            worksheet.write(x+1, y, cell, cell_format)
    while True:
        try:
            workbook.close()
        except xlsxwriter.exceptions.FileCreateError as e:
            decision = input("/!\ Error %s\n"
                                "Please close the file if it is open in Excel.\n"
                                "Try to write file again? [Y/n]: " % e)
            if decision != 'n':
                continue
            else:
                sys.exit("/!\ Error during saving data")
        else :
            print ("Write results in file " + str(path))
        break