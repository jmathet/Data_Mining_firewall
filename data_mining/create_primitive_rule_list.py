#!/usr/bin/python
# PURPOSE : Create Primitive Rule (Delete redondancy from logs)
# INPUT : Log file (extract from firewall)
# OUTPUT : File with primitive rules (= list og unique logs)

import numpy as np
from tools import read_in_csv_file

def get_premitive_rules(matrix):
    for x in range(1, len(matrix)-1):
        for y in range(x+1, len(matrix)-1):
            res = np.all(matrix[x,:] == matrix[y,:]) # True = all True / False = At least 1 False
            if(res): # True >> Row to delete
                print("Rows ",x," and ",y," --> Redondance found")
                matrix = np.delete(matrix, y, axis=0)
    return matrix

if __name__ == "__main__":
    matrix = read_in_csv_file("../../Logs/avec_ip/logs_test_simple.csv")
    print(matrix)
    print("Number initial of rules = ",len(matrix))

    matrix = get_premitive_rules(matrix)
    
    print("===============")
    print(matrix)
    print("Number final of rules = ",len(matrix))