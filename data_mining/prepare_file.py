#!/usr/bin/python3
import numpy as np
import ipaddress
import csv
import os 
import sys

def read_in_csv_file(path):
    # Variables to be defined 
    ip_src_i = 2
    ip_dst_i = 5
    port_dst_i = 6
    proto_i = 7

    # Read in csv file and return data as matrix
    matrix = np.array([['IP SRC', 'IP DST', 'PORT DST', 'PROTOCOL', 'COUNT']])
    with open(path, 'r', encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        for log in reader:
            row = []
            
            print("IP SRC ?", log[ip_src_i]) # To delete for more speed
            row.append(ipaddress.ip_address(log[ip_src_i])) # IP SRC
            
            print("IP DST ?",log[ip_dst_i]) # To delete for more speed
            row.append(ipaddress.ip_address(log[ip_dst_i])) # IP DST
            
            print("PORT DST ?",log[port_dst_i]) # To delete for more speed
            row.append(log[port_dst_i]) # PORT DST

            print("PROTO ?",log[proto_i]) # To delete for more speed
            row.append(log[proto_i]) # PROTOCOL

            row.append(1) # COUNT
            matrix = np.concatenate((matrix,[row]),axis=0) # Adds arr2 as rows to the end of matrix

    return matrix


def write_in_csv(path, matrix):
    with open(path, 'a', newline='') as file:
        writer = csv.writer(file)
        for row in matrix:
            writer.writerow(row)

if __name__ == "__main__":  
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print("Active directory =", dir_path)

    if len(sys.argv) == 3:
        path_file_src = sys.argv[1]
        path_file_dst = sys.argv[2]
        logs = read_in_csv_file(path_file_src)
        write_in_csv(path_file_dst, logs)
        print("\n *******************\n SUCESS READ / WRITE - new file generated \n *******************")
    else:
        print("USAGE : python prepare_file.py <path_file_src> <path_file_dst>")
        print("Relative path from active directory")
        print("Please check if the first line of the csv file is data.")

    # SRC "./../../data/logs_ana/log_firepower_new.csv"
    # DST "./../../data/logs_ana/new.csv"
    
