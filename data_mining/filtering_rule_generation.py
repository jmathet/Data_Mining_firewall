#!/usr/bin/python
# INPUT : File with primitive rules (= matrix of unique logs)
# OUTPUT : Genetic rules

import numpy
import ipaddress
from clustering_algo_gap_analysis import CAGA
from create_primitive_rule_list import delete_redondancies
from tools import read_in_csv_file, IP_src, IP_dst, PORT_dst, PROTO, MIN_LENGTH_CLUSTER, get_cluster_of_membership, network, listString2int

def filtering_rule_generation(premitives_rules):
    # STEP 1: Group @IP SRC with fixed @IP DST and fixed PORT
    print(">>>> STEP 1: Group @IP SRC with fixed @IP DST and fixed PORT <<<<")
    for x in range(1, len(premitives_rules)-1):
        if type(premitives_rules[x,IP_src])!=list: # If IP_src(x) is not already a cluster (=list)
            id_rules_to_be_clustered = [x]
            for y in range(x+1, len(premitives_rules)):
                # If IP_dst(x)==IP_dst(y) and PORT_dst(x)==PORT_dst(y) and IP_src(x)!=IP_src(y) and IP_src(y) not a list
                if      (premitives_rules[y,IP_dst]==premitives_rules[x,IP_dst]) \
                    and (premitives_rules[y,PORT_dst]==premitives_rules[x,PORT_dst])\
                    and (type(premitives_rules[y,IP_src])!=list)\
                    and (premitives_rules[y,IP_src]!=premitives_rules[x,IP_src]):
                    id_rules_to_be_clustered.append(y)
            # Group IP_src --> CAGA
            if len(id_rules_to_be_clustered)>1: # If clustering is necessary
                clusters = CAGA(premitives_rules[id_rules_to_be_clustered, IP_src],-1) # Use CAGA with default threshold
                # Replace IP_src by cluster
                for id in id_rules_to_be_clustered:
                    cluster = get_cluster_of_membership(clusters, premitives_rules[id,IP_src]) # Find cluster
                    premitives_rules[id,IP_src] = cluster # Replace IP_src by the correct cluster
                # Display custers
                for x in range(len(clusters)):
                    print("IP_src CLUSTER ",x,"--> IP_dst =",premitives_rules[id,IP_dst],"PORT_dst =",  premitives_rules[id,PORT_dst])
                    for y in range(len(clusters[x])):
                        clusters[x][y] = ipaddress.ip_address(clusters[x][y])
                        print("   " + str(clusters[x][y]))

    # STEP 2: Group @IP DST with fixed @IP SRC and fixed PORT
    print(">>>> STEP 2: Group @IP DST with fixed @IP SRC and fixed PORT <<<<")
    for x in range(1, len(premitives_rules)-1):
        if type(premitives_rules[x,IP_dst])!=list: # If IP_dst(x) is not already a cluster (=list)
            id_rules_to_be_clustered = [x]
            # Search rules where IP_src(x)==IP_src(y) and PORT_dst(x)==PORT_dst(y) and IP_dst(x)!=IP_dst(y)
            for y in range(x+1, len(premitives_rules)):
                if      (premitives_rules[y,IP_src]==premitives_rules[x,IP_src]) \
                    and (premitives_rules[y,PORT_dst]==premitives_rules[x,PORT_dst]) \
                    and (type(premitives_rules[y,IP_dst])!=list)\
                    and (premitives_rules[y,IP_dst]!=premitives_rules[x,IP_dst]):
                    id_rules_to_be_clustered.append(y)
            # Group IP_dst --> CAGA
            if len(id_rules_to_be_clustered)>1: # If clustering is necessary
                clusters = CAGA(premitives_rules[id_rules_to_be_clustered, IP_dst],-1) # Use CAGA with default threshold
                # Replace IP_src by cluster
                for id in id_rules_to_be_clustered:
                    cluster = get_cluster_of_membership(clusters, premitives_rules[id,IP_dst]) # Find cluster
                    premitives_rules[id,IP_dst] = cluster # Replace IP_src by the correct cluster
                # Display custers
                for v in range(len(clusters)):
                    print("IP_dst CLUSTER ",x,"--> IP_src =",premitives_rules[x,IP_src],"PORT_dst =",  premitives_rules[x,PORT_dst])
                    for w in range(len(clusters[v])):
                        clusters[v][w] = ipaddress.ip_address(clusters[v][w])
                        print("   " + str(clusters[v][w]))

    # STEP 3: Regroupement    PORT   qui ont même @IP SRC et @IP DST
    print(">>>> STEP 3: Group PORT with fixed @IP SRC and fixed @IP DST <<<<")
    for x in range(1, len(premitives_rules)-1):
        if type(premitives_rules[x,PORT_dst])!=list: # If PORT_dst(x) is not already a cluster (=list)
            id_rules_to_be_clustered = [x]
            # Search rules where IP_src(x)==IP_src(y) and IP_dst(x)==IP_dst(y) and Proto(x)==Proto(y)
            for y in range(x+1, len(premitives_rules)):
                if      (premitives_rules[y,IP_src]==premitives_rules[x,IP_src]) \
                    and (premitives_rules[y,IP_dst]==premitives_rules[x,IP_dst]) \
                    and (type(premitives_rules[y,PORT_dst])!=list)\
                    and (premitives_rules[y,PROTO]==premitives_rules[x,PROTO]):
                    id_rules_to_be_clustered.append(y)
            # Create group of clusters (Nothing to do with ports <= 1024)
            id_rules_to_be_clustered_group1 = []
            id_rules_to_be_clustered_group2 = []
            for id in id_rules_to_be_clustered :
                p = int(premitives_rules[id,PORT_dst])
                if p>1024 and p<=49151 :
                    id_rules_to_be_clustered_group1.append(id)
                if p>49151:
                    id_rules_to_be_clustered_group2.append(id)
            # Group PORT_dst
            if len(id_rules_to_be_clustered_group1)>1: # If clustering is necessary in group 1
                clusters = CAGA(listString2int(premitives_rules[id_rules_to_be_clustered_group1, PORT_dst]), 1) # Use CAGA with threshold=1
                for id in id_rules_to_be_clustered_group1:
                    cluster = get_cluster_of_membership(clusters, premitives_rules[id,PORT_dst])# Find cluster
                    if len(cluster)>1: # If cluster is composed of more than 1 element
                        premitives_rules[id,PORT_dst] = cluster # Group adjacent ports
                # Display clusters
                for v in range(len(clusters)):
                    print("PORT_dst CLUSTER ",v,"--> IP_src =",premitives_rules[x,IP_src],"IP_dst =",  premitives_rules[x,IP_dst])
                    for w in range(len(clusters[v])):
                        print("   " + str(clusters[v][w]))
            if len(id_rules_to_be_clustered_group2)>=2: # If clustering is necessary in group 2 and size >2
                cluster = list(premitives_rules[id_rules_to_be_clustered_group2,PORT_dst])
                # Update ports with correct cluster
                for id in id_rules_to_be_clustered_group2:
                    premitives_rules[id,PORT_dst] = cluster # Replace PORT_dst by the correct cluster
                # Display custers
                print("PORT_dst CLUSTER >49151 --> IP_src =",premitives_rules[x,IP_src],"IP_dst =",  premitives_rules[x,IP_dst])
                for port in cluster:
                    print("   " + port)
                
    # STEP 4: Delete redondancies
    rules = delete_redondancies(premitives_rules)

    # STEP 5: Cluster generalization
    for i in range(1, len(rules)):
        if type(rules[i, IP_src])==list and len(rules[i, IP_src])>=MIN_LENGTH_CLUSTER: # If IP_src(x) is a cluster (=list) and len >= MIN_LENGTH_CLUSTER
            cluster_IP_src = rules[i, IP_src]
            net_IP_src = network(int(cluster_IP_src[0]), int(cluster_IP_src[-1])) # Netmask on the fist and the last element of the cluster
            rules[i, IP_src] = ipaddress.ip_network(net_IP_src)
        if type(rules[i, IP_dst])==list and len(rules[i, IP_dst])>=MIN_LENGTH_CLUSTER: # If IP_dst(x) is a cluster (=list)
            cluster_IP_dst = rules[i, IP_dst]
            net_IP_dst = network(int(cluster_IP_dst[0]), int(cluster_IP_dst[-1])) # Netmask on the fist and the last element of the cluster
            rules[i, IP_dst] = ipaddress.ip_network(net_IP_dst)
        if type(rules[i, PORT_dst])==list: # If PORT_dst(x) is a cluster (=list)
            cluster_PORT_dst = rules[i, PORT_dst]
            if int(cluster_PORT_dst[0])>1024 and int(cluster_PORT_dst[-1])<=49151 :
                if cluster_PORT_dst[0]==cluster_PORT_dst[-1]:
                    rules[i, PORT_dst] = cluster_PORT_dst[0]
                    print("UNIQUE", cluster_PORT_dst[0], cluster_PORT_dst[-1], rules[i, PORT_dst])
                else:
                    rules[i, PORT_dst] = str(cluster_PORT_dst[0]) + "-" + str(cluster_PORT_dst[-1])
                    print("RANGE", cluster_PORT_dst[0], cluster_PORT_dst[-1], rules[i, PORT_dst])
            elif int(cluster_PORT_dst[0])>49151 :
                rules[i, PORT_dst] = "49152-65535"
    return rules