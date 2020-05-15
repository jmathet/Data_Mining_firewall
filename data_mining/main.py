#!/usr/bin/python

from tools import read_in_csv_file, write_in_csv_file
from create_primitive_rule_list import delete_redondancies
from filtering_rule_generation import filtering_rule_generation
from group_proto_ports import group_proto_ports

import numpy as np

if __name__ == "__main__":
    # STEP 0: Read csv file
    data = read_in_csv_file("./new_test.csv")
    
    # STEP 1: Generate primitive rules
    premitive_rules = delete_redondancies(data)
    matrix = np.delete(premitive_rules, 2, axis=1) # Delete column PORT SRC

    # STEP 2: Geralization of primitive rules to rules 
    rules = filtering_rule_generation(matrix)
    
    # STEP 3: Group Proto/ports
    rules = group_proto_ports(rules)
    rules = np.delete(rules, 3, axis=1) # Delete column PROTOCOL
    rules = delete_redondancies(rules)

    # STEP 4: Ordering rules  
    rules = np.delete(rules, 0, axis=0) # Delete first line 
    index_order = np.argsort(rules[:, -1])  # Ordering
    rules_ordered = rules[index_order[::-1]] # Reverse order

    # STEP 5 : Write in csv file
    write_in_csv_file(rules_ordered, "./resultat_file.xlsx")
    print("Number initial of logs = " + str(len(matrix)-1) + " >> Number final of rules = " + str(len(rules)-1))

