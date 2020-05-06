#!/usr/bin/python
# INPUT : File with primitive rules (= matrix of unique logs)
# OUTPUT : Genetic rules

import numpy
from clustering_algo_gap_analysis import CAGA
from create_primitive_rule_list import delete_redondancies
from tools import read_in_csv_file, IP_src, IP_dst, PORT_dst, get_cluster_if_membership

def filtering_rule_generation(premitives_rules):
    # STEP 1: Group @IP SRC with fixed @IP DST and fixed PORT
    print(">>>> STEP 1: Group @IP SRC with fixed @IP DST and fixed PORT <<<<")
    for x in range(1, len(premitives_rules)-1):
        #print("x ",x)
        if type(premitives_rules[x,IP_src])!=list: # If IP_src(x) is not already a cluster (=list)
            id_rules_to_be_clustered = [x]
            for y in range(x+1, len(premitives_rules)):
                #print("y = " + str(y))
                # If IP_dst(x)==IP_dst(y) and PORT_dst(x)==PORT_dst(y)
                if (premitives_rules[y,IP_dst]==premitives_rules[x,IP_dst]) and (premitives_rules[y,PORT_dst]==premitives_rules[x,PORT_dst]):
                    #print(premitives_rules[y,IP_dst])
                    #print(premitives_rules[x,IP_dst])
                    #print(premitives_rules[y,IP_dst]==premitives_rules[x,IP_dst])
                    #print(premitives_rules[y,PORT_dst])
                    #print(premitives_rules[x,PORT_dst])
                    #print(premitives_rules[y,PORT_dst]==premitives_rules[x,PORT_dst])
                    id_rules_to_be_clustered.append(y)
            # Group IP_src --> CAGA
            #print("id_rules_to_be_clustered",id_rules_to_be_clustered)
            if len(id_rules_to_be_clustered)>1: # If clustering is necessary
                #print(">>>>>>",premitives_rules[id_rules_to_be_clustered, IP_src])
                clusters = CAGA(premitives_rules[id_rules_to_be_clustered, IP_src])
                for id in id_rules_to_be_clustered:
                    # Find cluster
                    cluster = get_cluster_if_membership(clusters, premitives_rules[id,IP_src])
                    # Replace IP_src by the correct cluster
                    premitives_rules[id,IP_src] = cluster
                    #print(premitives_rules[id,IP_src])
                    #print("cluster found", cluster)

    # STEP 2: Group @IP DST with fixed @IP SRC and fixed PORT
    print(">>>> STEP 2: Group @IP DST with fixed @IP SRC and fixed PORT <<<<")
    for x in range(1, len(premitives_rules)-1):
        #print("x ",x)
        if type(premitives_rules[x,IP_dst])!=list: # If IP_dst(x) is not already a cluster (=list)
            id_rules_to_be_clustered = [x]
            for y in range(x+1, len(premitives_rules)):
                #print("y = " + str(y))
                # If IP_src(x)==IP_src(y) and PORT_dst(x)==PORT_dst(y)
                if (premitives_rules[y,IP_src]==premitives_rules[x,IP_src]) and (premitives_rules[y,PORT_dst]==premitives_rules[x,PORT_dst]):
                    #print(premitives_rules[y,IP_src])
                    #print(premitives_rules[x,IP_src])
                    #print(premitives_rules[y,IP_src]==premitives_rules[x,IP_src])
                    #print(premitives_rules[y,PORT_dst])
                    #print(premitives_rules[x,PORT_dst])
                    #print(premitives_rules[y,PORT_dst]==premitives_rules[x,PORT_dst])
                    id_rules_to_be_clustered.append(y)
            # Group IP_src --> CAGA
            #print("id_rules_to_be_clustered",id_rules_to_be_clustered)
            if len(id_rules_to_be_clustered)>1: # If clustering is necessary
                #print(">>>>>>",premitives_rules[id_rules_to_be_clustered, IP_src])
                clusters = CAGA(premitives_rules[id_rules_to_be_clustered, IP_dst])
                for id in id_rules_to_be_clustered:
                    # Find cluster
                    cluster = get_cluster_if_membership(clusters, premitives_rules[id,IP_dst])
                    # Replace IP_src by the correct cluster
                    premitives_rules[id,IP_dst] = cluster
                    #print(premitives_rules[id,IP_dst])
                    #print("cluster found", cluster)

    # STEP 3: Regroupement    PORT   qui ont même @IP SRC et @IP DST

    # STEP 4: Delete redondancies
    rules = delete_redondancies(premitives_rules)

    #STEP 5: Cluster generalization

    return rules