#!/usr/bin/python
# INPUT : list of rules
# OUTPUT : list of rules with IP_dst group (if IP_src and port are equals) IP_src group (if IP_dst and port are equals)

from tools import IP_src, IP_dst, PORT_dst, PROTO, join_list_element

def group_list_ip(rules):
    # Group IP DST
    for x in range(1, len(rules)-1):
        id_rules_to_be_clustered = [x]
        list_ip_dst = []
        list_ip_dst = join_list_element(list_ip_dst, rules[x, IP_dst])
        for y in range(x+1, len(rules)):
            if      (rules[y,IP_src]==rules[x,IP_src]) \
                and (rules[y,PORT_dst]==rules[x,PORT_dst]):
                id_rules_to_be_clustered.append(y)
                list_ip_dst = join_list_element(list_ip_dst, rules[y, IP_dst])
        if len(id_rules_to_be_clustered)>1: # If group is necessary
            for id in id_rules_to_be_clustered:
                rules[id, IP_dst] = list_ip_dst

    # Group IP SRC
    for x in range(1, len(rules)-1):
        id_rules_to_be_clustered = [x]
        list_ip_src = []
        list_ip_src = join_list_element(list_ip_src, rules[x, IP_src])
        for y in range(x+1, len(rules)):
            if      (rules[y,IP_dst]==rules[x,IP_dst]) \
                and (rules[y,PORT_dst]==rules[x,PORT_dst]):
                id_rules_to_be_clustered.append(y)
                list_ip_src = join_list_element(list_ip_src, rules[y, IP_src])
        if len(id_rules_to_be_clustered)>1: # If group is necessary
            for id in id_rules_to_be_clustered:
                rules[id, IP_src] = list_ip_src
    return rules