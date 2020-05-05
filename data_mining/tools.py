#!/usr/bin/python

import csv
import numpy as np

def read_in_csv_file(path):
    matrix = np.array([['IP SRC', 'IP DST', 'PORT SRC', 'PORT DST', 'PROTO', 'ACTION']])
    with open(path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            matrix = np.concatenate((matrix,[row]),axis=0) # Adds arr2 as rows to the end of arr1
    return matrix

if __name__ == "__main__":
    matrix = read_in_csv_file("../../Logs/avec_ip/logs_test2.csv")
    print(matrix)
    print(matrix[5,5])