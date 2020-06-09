#!/usr/bin/python3
import numpy as np
import ipaddress
import csv

def read_in_csv_file(path):
    # Read in csv file and return data as matrix
    matrix = np.array([['IP SRC', 'IP DST', 'PORT DST', 'PROTOCOL', 'COUNT']])
    with open(path, 'r', encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        for log in reader:
            row = []
            row.append(ipaddress.ip_address(log[0])) # IP SRC
            row.append(ipaddress.ip_address(log[1])) # IP DST
            row.append(log[2]) # PORT DST
            row.append('udp')
            row.append(log[3]) # COUNT
            matrix = np.concatenate((matrix,[row]),axis=0) # Adds arr2 as rows to the end of matrix

    return matrix


def write_in_csv(path, matrix):
    with open(path, 'a', newline='') as file:
        writer = csv.writer(file)
        for row in matrix:
            writer.writerow(row)

if __name__ == "__main__":
    
    logs = read_in_csv_file("./data/logs_ana/logs_ana_udp.csv")
    write_in_csv("./data/logs_ana/results.csv", logs)