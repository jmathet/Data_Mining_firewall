# INPUT : File with primitive rules (= list og unique logs)
# OUTPUT : Genetic rules

import numpy
from clustering_algo_gap_analysis.py import CAGA

def get_cluster(element, clusters):
    for cluster in clusters:
        if element in cluster:
            break
    return cluster

def filtering_rule_generation(premitives_rules):
    
    IP_src = premitives_rules[:,0]
    IP_dest = premitives_rules[:,1]
    Port_src = premitives_rules[:,2]
    Port_dst = premitives_rules[:,3]

    IP_src_clusters = CAGA(IP_src)

    for i in range(len(premitives_rules)):
        # IP_src --> IP_src_cluster
        premitives_rules[i,0] = get_cluster(premitives_rules[i,0], IP_src_clusters)

    return premitives_rules

def if __name__ == "__main__":
    rules = numpy.zeros((5, 5))
    rules[]
