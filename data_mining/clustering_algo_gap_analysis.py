# PURPOSE : Create clusters from inputs (Clustering Algo bu Gap Analysis = CAGA)
# INPUT : List of IP addresses or port numbers
# OUTPUT : List of clusters generated

def CAGA(list):
    delta = []
    cluters = []
    # STEP 1: to sort the list
    list.sort()
    print(list)
    # STEP 2: to compute the delta between 2 following items of the list
    print("longeur list")
    print(len(list))
    for i in range(0, len(list)-1):
        delta_i = list[i+1]-list[i]
        print(delta_i)
        delta.append(delta_i)
    print(delta)
    return delta


if __name__ == "__main__":
    my_list = [1,3,4,9,0,4,89,43]
    print(CAGA(my_list))