#!/usr/bin/python

from tools import read_in_csv_file
from create_primitive_rule_list import delete_redondancies
from filtering_rule_generation import filtering_rule_generation

import numpy as np

if __name__ == "__main__":
    # STEP 0: Read csv file
    matrix = read_in_csv_file("../../Logs/avec_ip/logs_test_simple.csv")
    
    # STEP 1: Generate primitive rules
    premitive_rules = delete_redondancies(matrix)
    matrix = np.delete(matrix, 2, axis=1) # Delete column PORT SRC

    
    # STEP 2: Geralization of primitive rules to rules 
    rules = filtering_rule_generation(premitive_rules)  

    # STEP 3: Ordering rules  

    # STEP 4 : Write in csv file
    
    # DISPLAYS
    print(matrix)
    print("Number initial of logs = ",len(matrix)-1)
    print("===============")
    print(rules)
    print("Number final of rules = ",len(rules)-1)
