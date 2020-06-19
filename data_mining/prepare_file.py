#!/usr/bin/python3
import numpy as np
import ipaddress
import csv
import os 

def read_in_csv_file(path):
    # Read in csv file and return data as matrix
    matrix = np.array([['IP SRC', 'IP DST', 'PORT DST', 'PROTOCOL', 'COUNT']])
    with open(path, 'r', encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        for log in reader:
            row = []
            print(log[2])
            row.append(ipaddress.ip_address(log[2])) # IP SRC
            row.append(ipaddress.ip_address(log[4])) # IP DST
            row.append(log[5]) # PORT DST
            row.append(log[6]) # PROTOCOL
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
    print(dir_path)
    
    logs = read_in_csv_file("./../../data/logs_ana/log_firepower_new.csv")
    write_in_csv("./../../data/logs_ana/new.csv", logs)
    
