#!/usr/bin/python

from tools import read_in_csv_file, write_in_csv_file, PROTO
from create_primitive_rule_list import delete_redondancies
from filtering_rule_generation import filtering_rule_generation
from group_proto_ports import group_proto_ports
from group_list_ip import group_list_ip

import numpy as np
import sys

if __name__ == "__main__":
    # Print in log file
    #old_stdout = sys.stdout
    #log_file = open("print.log","w")
    #sys.stdout = log_file

    # STEP 0: Read csv file
    data = read_in_csv_file("./../../data/logs_ana/results.csv")

    # STEP 1: Generate primitive rules
    premitive_rules = delete_redondancies(data)
    #premitive_rules = np.delete(premitive_rules, 2, axis=1) # Delete column PORT SRC (if necessary)

    # STEP 2: Geralization of primitive rules to rules 
    generalized_rules  = filtering_rule_generation(premitive_rules)
    generalized_rules = delete_redondancies(generalized_rules)
    
    # STEP 3: Group Proto/ports
    rules_port_group = group_proto_ports(generalized_rules)
    rules_port_group = np.delete(rules_port_group, PROTO, axis=1) # Delete column PROTOCOL
    rules_port_group = delete_redondancies(rules_port_group)

    # STEP 4 : Group list IP
    rules_ip_group = group_list_ip(rules_port_group)
    rules_ip_group = delete_redondancies(rules_ip_group)

    # STEP 5 : Ordering rules using COUNT
    rules = np.delete(rules_ip_group, 0, axis=0) # Delete first line 
    index_order = np.argsort(rules[:, -1])  # Get index order using the last column (COUNT)
    rules_ordered = rules[index_order[::-1]] # Reverse order to have max first

    # STEP 6 : Close the log file
    #sys.stdout = old_stdout
    #log_file.close()
    
    # STEP 7 : Write in csv file
    write_in_csv_file(rules_ordered, "./results_file.xlsx")

    print("Success \n >> Log file print.log generated in the current folder\n >> Results file resultat_file.xlsx generated in the current folder")
    print("Number initial of logs = " + str(len(premitive_rules)-1) + " >> Number final of rules = " + str(len(rules_ordered)-1))