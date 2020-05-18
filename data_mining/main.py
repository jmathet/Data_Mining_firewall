#!/usr/bin/python

from tools import read_in_csv_file, write_in_csv_file, PROTO
from create_primitive_rule_list import delete_redondancies
from filtering_rule_generation import filtering_rule_generation
from group_proto_ports import group_proto_ports

import numpy as np
import sys

if __name__ == "__main__":
    # Print in log file
    old_stdout = sys.stdout
    log_file = open("print.log","w")
    sys.stdout = log_file

    # STEP 0: Read csv file
    data = read_in_csv_file("./../../data/logs_ana/results.csv")

    # STEP 1: Generate primitive rules
    premitive_rules = delete_redondancies(data)
    #premitive_rules = np.delete(premitive_rules, 2, axis=1) # Delete column PORT SRC (if necessary)

    # STEP 2: Geralization of primitive rules to rules 
    rules = filtering_rule_generation(premitive_rules)
    
    # STEP 3: Group Proto/ports
    rules = delete_redondancies(rules)
    rules = group_proto_ports(rules)
    rules = np.delete(rules, PROTO, axis=1) # Delete column PROTOCOL
    rules = delete_redondancies(rules)

    # STEP 4: Ordering rules  
    rules = np.delete(rules, 0, axis=0) # Delete first line 
    index_order = np.argsort(rules[:, -1])  # Ordering
    rules_ordered = rules[index_order[::-1]] # Reverse order

    # STEP 5 : Write in csv file
    write_in_csv_file(rules_ordered, "./results_file.xlsx")
    print("Number initial of logs = " + str(len(premitive_rules)-1) + " >> Number final of rules = " + str(len(rules)-1))

    # Close the log file
    sys.stdout = old_stdout
    log_file.close()

    print("Success \n >> Log file print.log generated in the current folder\n >> Results file resultat_file.xlsx generated in the current folder")