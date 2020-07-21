#!/usr/bin/python

from tools import read_in_csv_file, write_in_csv_file, PROTO
from create_primitive_rule_list import delete_redondancies
from filtering_rule_generation import filtering_rule_generation
from group_proto_ports import group_proto_ports
from group_list_ip import group_list_ip

import numpy as np
import sys

if __name__ == "__main__":

    if len(sys.argv) == 2:
        path_file_src = sys.argv[1]
    else:
        print("USAGE : python main.py <path_file_src>")
        print("Relative path from main.py folder")
        

    # Print in log file
    old_stdout = sys.stdout
    log_file = open("print.log","w")
    sys.stdout = log_file
    print("Running ...", file=old_stdout)

    # STEP 0: Read csv file
    print("        ... Reading csv file - ", file=old_stdout, end = '', flush=True)
    data = read_in_csv_file(path_file_src) # The first line need to be a data line (no title)
    print(str(len(data)-1), file=old_stdout, end = '', flush=True)
    print(" - OK", file=old_stdout)

    # STEP 1: Generate primitive rules
    print("        ... Generating primitive rules - ", file=old_stdout, end = '', flush=True)
    premitive_rules = delete_redondancies(data)
    print(str(len(premitive_rules)-1), file=old_stdout, end = '', flush=True)
    print(" - OK", file=old_stdout)
    

    # STEP 2: Geralization of primitive rules to rules 
    print("        ... Geralization of primitive rules to rules - ", file=old_stdout, end = '', flush=True)
    generalized_rules  = filtering_rule_generation(premitive_rules)
    generalized_rules = delete_redondancies(generalized_rules)
    print(str(len(generalized_rules)-1), file=old_stdout, end = '', flush=True)
    print(" - OK", file=old_stdout)
    
    # STEP 3: Group Proto/ports
    print("        ... Group Proto/ports - ", file=old_stdout, end = '', flush=True)
    rules_port_group = group_proto_ports(generalized_rules)
    rules_port_group = np.delete(rules_port_group, PROTO, axis=1) # Delete column PROTOCOL
    rules_port_group = delete_redondancies(rules_port_group)
    print(str(len(rules_port_group)-1), file=old_stdout, end = '', flush=True)
    print(" - OK", file=old_stdout)

    # STEP 4 : Group list IP
    print("        ... Group list IP - ", file=old_stdout, end = '', flush=True)
    rules_ip_group = group_list_ip(rules_port_group)
    rules_ip_group = delete_redondancies(rules_ip_group)
    print(str(len(rules_ip_group)-1), file=old_stdout, end = '', flush=True)
    print(" - OK", file=old_stdout)

    # STEP 5 : Ordering rules using COUNT
    print("        ... Ordering rules using COUNT", file=old_stdout, end = '', flush=True)
    rules = np.delete(rules_ip_group, 0, axis=0) # Delete first line 
    index_order = np.argsort(rules[:, -1])  # Get index order using the last column (COUNT)
    rules_ordered = rules[index_order[::-1]] # Reverse order to have max first
    print(" - OK", file=old_stdout)

    # STEP 6 : Close the log file
    sys.stdout = old_stdout
    log_file.close()
    
    # STEP 7 : Write in xlsx file
    print("        ... Writing rules in xlsx file ", end  = '', flush=True)
    write_in_csv_file(rules_ordered, "./results_file.xlsx")
    print(" - OK")

    print("Work done ! \n >> Log file print.log generated in the current folder\n >> Results file resultat_file.xlsx generated in the current folder")
    print("Number initial of logs = " + str(len(data)-1) + " >> Number final of rules = " + str(len(rules_ordered)-1))