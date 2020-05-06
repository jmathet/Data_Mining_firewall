#!/usr/bin/python
# INPUT : File with primitive rules (= matrix of unique logs)
# OUTPUT : Genetic rules

import numpy
import ipaddress
from clustering_algo_gap_analysis import CAGA
from create_primitive_rule_list import delete_redondancies
from tools import read_in_csv_file, IP_src, IP_dst, PORT_dst, get_cluster_of_membership

def filtering_rule_generation(premitives_rules):
    # STEP 1: Group @IP SRC with fixed @IP DST and fixed PORT
    print(">>>> STEP 1: Group @IP SRC with fixed @IP DST and fixed PORT <<<<")
    for x in range(1, len(premitives_rules)-1):
        if type(premitives_rules[x,IP_src])!=list: # If IP_src(x) is not already a cluster (=list)
            id_rules_to_be_clustered = [x]
            for y in range(x+1, len(premitives_rules)):
                # If IP_dst(x)==IP_dst(y) and PORT_dst(x)==PORT_dst(y) and IP_src(x)==IP_src(y)
                if      (premitives_rules[y,IP_dst]==premitives_rules[x,IP_dst]) \
                    and (premitives_rules[y,PORT_dst]==premitives_rules[x,PORT_dst])\
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
                    print("CLUSTER " + str(x))
                    for y in range(len(clusters[x])):
                        clusters[x][y] = ipaddress.ip_address(clusters[x][y])
                        print("   " + str(clusters[x][y]))
    # STEP 2: Group @IP DST with fixed @IP SRC and fixed PORT
    print(">>>> STEP 2: Group @IP DST with fixed @IP SRC and fixed PORT <<<<")
    for x in range(1, len(premitives_rules)-1):
        if type(premitives_rules[x,IP_dst])!=list: # If IP_dst(x) is not already a cluster (=list)
            id_rules_to_be_clustered = [x]
            # Search rules where IP_src(x)==IP_src(y) and PORT_dst(x)==PORT_dst(y) and IP_dst(x)==IP_dst(y)
            for y in range(x+1, len(premitives_rules)):
                if      (premitives_rules[y,IP_src]==premitives_rules[x,IP_src]) \
                    and (premitives_rules[y,PORT_dst]==premitives_rules[x,PORT_dst]) \
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
                for x in range(len(clusters)):
                    print("CLUSTER " + str(x))
                    for y in range(len(clusters[x])):
                        clusters[x][y] = ipaddress.ip_address(clusters[x][y])
                        print("   " + str(clusters[x][y]))

    # STEP 3: Regroupement    PORT   qui ont même @IP SRC et @IP DST
    print(">>>> STEP 3: Group PORT with fixed @IP SRC and fixed @IP DST <<<<")
    for x in range(1, len(premitives_rules)-1):
        if type(premitives_rules[x,PORT_dst])!=list: # If PORT_dst(x) is not already a cluster (=list)
            id_rules_to_be_clustered = [x]
            # Search rules where IP_src(x)==IP_src(y) and IP_dst(x)==IP_dst(y)
            for y in range(x+1, len(premitives_rules)):
                if      (premitives_rules[y,IP_src]==premitives_rules[x,IP_src]) \
                    and (premitives_rules[y,IP_dst]==premitives_rules[x,IP_dst]):
                    id_rules_to_be_clustered.append(y)
            # Create group of clusters (Nothing to do with ports <= 1024)
            id_rules_to_be_clustered_group1 = []
            id_rules_to_be_clustered_group2 = []
            for id in id_rules_to_be_clustered :
                p = int(premitives_rules[x,PORT_dst])
                if p>1024 and p<=49151 :
                    id_rules_to_be_clustered_group1.append(id)
                if p > 49151:
                    id_rules_to_be_clustered_group2.append(id)
            # Group PORT_dst
            if len(id_rules_to_be_clustered_group1)>1: # If clustering is necessary in group 1
                clusters = CAGA(premitives_rules[id_rules_to_be_clustered_group1, PORT_dst], 1) # Use CAGA with threshold=1
                for id in id_rules_to_be_clustered_group1:
                    cluster = get_cluster_of_membership(clusters, premitives_rules[id,PORT_dst])# Find cluster
                    premitives_rules[id,PORT_dst] = cluster # Group adjacent ports
                    print(cluster)
                # Display clusters
                for x in range(len(clusters)):
                    print("CLUSTER " + str(x))
                    for y in range(len(clusters[x])):
                        print("   " + str(clusters[x][y]))
            if len(id_rules_to_be_clustered_group2)>=2: # If clustering is necessary in group 2 and size >2
                cluster = list(premitives_rules[id_rules_to_be_clustered_group2,PORT_dst])
                # Update ports with correct cluster
                for id in id_rules_to_be_clustered_group2:
                    premitives_rules[id,PORT_dst] = cluster # Replace PORT_dst by the correct cluster
                # Display custers
                print("CLUSTER > 49151")
                for port in cluster:
                    print("   " + port)
                
    # STEP 4: Delete redondancies
    rules = delete_redondancies(premitives_rules)

    # STEP 5: Cluster generalization

    return rules