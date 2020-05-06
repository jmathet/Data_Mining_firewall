#!/usr/bin/python

from tools import read_in_csv_file
from create_primitive_rule_list import delete_redondancies
from filtering_rule_generation import filtering_rule_generation

import numpy as np

if __name__ == "__main__":
    # STEP 0: Read csv file
    data = read_in_csv_file("../../Logs/avec_ip/logs_test_simple.csv")
    
    # STEP 1: Generate primitive rules
    premitive_rules = delete_redondancies(data)
    matrix = np.delete(premitive_rules, 2, axis=1) # Delete column PORT SRC

    # STEP 2: Geralization of primitive rules to rules 
    rules = filtering_rule_generation(matrix)  

    # STEP 3: Ordering rules  

    # STEP 4 : Write in csv file
    
    # DISPLAYS
    print("Number initial of logs = ",len(matrix)-1)
    print("===============")
    print("Number final of rules = ",len(rules)-1)
    
    for rule in rules:
        print(rule)
