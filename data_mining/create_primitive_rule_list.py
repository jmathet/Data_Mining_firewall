#!/usr/bin/python
# PURPOSE : Create Primitive Rule (Delete redondancy from logs)
# INPUT : Log file (extract from firewall)
# OUTPUT : File with primitive rules (= list og unique logs)

import numpy as np
from tools import read_in_csv_file

def delete_redondancies(matrix):
    id_rules_to_delete = []
    colums_count = np.size(matrix,1)-1
    for x in range(1, len(matrix)-1):
        for y in range(x+1, len(matrix)):
            res = np.all(matrix[x,0:colums_count] == matrix[y,0:colums_count]) # True = all True / False = At least 1 False
            if res and int(matrix[y,colums_count])!=0: # If True 
                print("Rows ",x," and ",y," --> Redondance found")
                id_rules_to_delete.append(y)
                matrix[x,colums_count] = int(matrix[x,colums_count]) + int(matrix[y,colums_count])
                matrix[y,colums_count] = 0
    id_rules_to_delete = sorted(id_rules_to_delete,reverse=True)
    for id in id_rules_to_delete: # Delete from the end to the begining
        matrix = np.delete(matrix, id, axis=0) # Row to delete
    return matrix