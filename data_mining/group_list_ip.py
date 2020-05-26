#!/usr/bin/python
# INPUT : list of rules
# OUTPUT : list of rules with IP_dst group (if IP_src and port are equals) IP_src group (if IP_dst and port are equals)

from tools import IP_src, IP_dst, PORT_dst, PROTO, join_list_element
import numpy as np

def group_list_ip(rules):
    # Group IP SRC
    group_ip_src_done =  [None] * len(rules)
    for x in range(1, len(rules)-1):
        id_rules_to_be_clustered = [x]
        list_ip_src = []
        list_ip_src = join_list_element(list_ip_src, rules[x, IP_src])
        for y in range(x+1, len(rules)):
            if      (rules[y,IP_dst]==rules[x,IP_dst]) \
                and (rules[y,PORT_dst]==rules[x,PORT_dst])\
                and (group_ip_src_done[y]!='YES'):
                id_rules_to_be_clustered.append(y)
                group_ip_src_done[y] = 'YES' # Avoid already used rules
                list_ip_src = join_list_element(list_ip_src, rules[y, IP_src]) # Add IP of y to the group of IP
        if len(id_rules_to_be_clustered)>1: # If group is necessary
            for id in id_rules_to_be_clustered:
                rules[id, IP_src] = list_ip_src # Replace initial list by the gourp of IP list

    # Group IP DST
    group_ip_dst_done =  [None] * len(rules)
    for x in range(1, len(rules)-1):
        id_rules_to_be_clustered = [x]
        list_ip_dst = []
        list_ip_dst = join_list_element(list_ip_dst, rules[x, IP_dst])
        for y in range(x+1, len(rules)):
            if      (rules[y,IP_src]==rules[x,IP_src]) \
                and (rules[y,PORT_dst]==rules[x,PORT_dst])\
                and (group_ip_dst_done[y]!='YES')\
                and (group_ip_src_done[y]!='YES'):
                id_rules_to_be_clustered.append(y)
                group_ip_dst_done[y] = 'YES' # Avoid already used rules
                list_ip_dst = join_list_element(list_ip_dst, rules[y, IP_dst]) # Add IP of y to the group of IP
        if len(id_rules_to_be_clustered)>1: # If group is necessary
            for id in id_rules_to_be_clustered:
                rules[id, IP_dst] = list_ip_dst # Replace initial list by the gourp of IP list

    return rules