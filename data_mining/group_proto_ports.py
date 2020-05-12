#!/usr/bin/python

from tools import IP_src, IP_dst, PORT_dst, PROTO, list2string

def group_proto_ports(rules):
    # STEP 1: Lists creation
    for x in range(1, len(rules)-1):
        print(rules[x])
        if type(rules[x,PORT_dst])!=list: # If PORT_dst(x) is not already a cluster (=list)
            id_rules_to_be_clustered = [x]
            for y in range(x+1, len(rules)):
                if      (rules[y,IP_src]==rules[x,IP_src]) \
                    and (rules[y,IP_dst]==rules[x,IP_dst]):
                    id_rules_to_be_clustered.append(y)
            # Generate list of ports by protocol
            tcp_ports = []
            udp_ports = []
            icmp_ports = []
            for id in id_rules_to_be_clustered:
                if rules[id,PROTO]=="tcp":
                    tcp_ports.append(rules[y,PORT_dst])
                elif rules[id,PROTO]=="udp":
                    udp_ports.append(rules[y,PORT_dst])
                elif rules[id,PROTO]=="icmp":
                    icmp_ports.append(rules[y,PORT_dst])
            print(tcp_ports)
            print(udp_ports)
            print(icmp_ports)
            # Replace PORT_dst by lists
            for id in id_rules_to_be_clustered:
                ports_list_in_string = str()
                if len(tcp_ports)!=0:
                    ports_list_in_string = ports_list_in_string + "tcp/" + list2string(tcp_ports)
                if len(udp_ports)!=0:
                    ports_list_in_string = ports_list_in_string + "\nudp/" + list2string(udp_ports)
                if len(icmp_ports)!=0:
                    ports_list_in_string = ports_list_in_string + "\nicmp/" + list2string(icmp_ports)
                rules[id,PORT_dst] = ports_list_in_string # Replace PORT_dst by list

    return rules