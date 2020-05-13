#!/usr/bin/python

from tools import IP_src, IP_dst, PORT_dst, PROTO, list2string

def group_proto_ports(rules):
    # Group proto/ports
    for x in range(1, len(rules)-1):
        print("x",x)
        current_port = rules[x,PORT_dst]
        if current_port[0:3]!="tcp" and current_port[0:3]!="udp" and current_port[0:3]!="icmp": # If PORT_dst(x) is not already a cluster (=list)
            id_rules_to_be_clustered = [x]
            for y in range(x+1, len(rules)):
                print("y",y)
                if      (rules[y,IP_src]==rules[x,IP_src]) \
                    and (rules[y,IP_dst]==rules[x,IP_dst]):
                    id_rules_to_be_clustered.append(y)
            # Generate list of ports by protocol
            tcp_ports = []
            udp_ports = []
            icmp_ports = []
            for id in id_rules_to_be_clustered:
                if rules[id,PROTO]=="tcp":
                    tcp_ports.append(rules[id,PORT_dst])
                elif rules[id,PROTO]=="udp":
                    udp_ports.append(rules[id,PORT_dst])
                elif rules[id,PROTO]=="icmp":
                    icmp_ports.append(rules[id,PORT_dst])
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
    # Display proto/port when group not applicable
    for x in range(1, len(rules)):
        current_port = rules[x,PORT_dst]
        if current_port[0:3]!="tcp" and current_port[0:3]!="udp" and current_port[0:3]!="icmp": # If PORT_dst(x) is not already a cluster (=list)
            rules[x,PORT_dst] = rules[x,PROTO] + "/" + rules[x,PORT_dst]
    return rules