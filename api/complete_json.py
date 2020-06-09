import json
import xlrd 
import numpy as np
import copy

def complete_json(path_xlsx_file):
  # Opening json base request
  with open('base_request.json') as f:
    rule_model = json.load(f)

  # Initialisation of data to be posted
  post_data = []

  # Reading data from xlsx file and storage in numpy matrix
  wb = xlrd.open_workbook(path_xlsx_file) 
  sheet = wb.sheet_by_index(0) 
  nb_rows = sheet.nrows
  nb_cols = sheet.ncols
  matrix = np.array([['IP SRC', 'IP DST', 'PORT DST']])
  for x in range(1, nb_rows):
      row = [None]*3
      for y in range(0, nb_cols-1):
          row[y] = sheet.cell_value(x,y)
      matrix = np.concatenate((matrix,[row]),axis=0) # Adds row as rows to the end of matrix

  # Completion json file with data from the numpy matrix
  for id_rule in range(1, np.size(matrix,0)):
    new_rule = []
    new_rule = copy.deepcopy(rule_model) # Compulsary for object copy (= statement do not create a new object)
    new_rule["name"] = "RULE " + str(id_rule)
    list_ip_src = matrix[id_rule][0].split(",")
    for ip_src in list_ip_src:
      if ip_src.find("/")==-1: # "/" not found
        new_rule["sourceNetworks"]["literals"].append({"type": "Host", "value": ip_src})
      else: # "/" found
        new_rule["sourceNetworks"]["literals"].append({"type": "Network", "value": ip_src})

    list_ip_dst = matrix[id_rule][1].split(",")
    for ip_dst in list_ip_dst:
      if ip_dst.find("/")==-1: # "/" not found
        new_rule["destinationNetworks"]["literals"].append(
                {"type": "Host", "value": ip_dst})
      else: # "/" found
        new_rule["destinationNetworks"]["literals"].append(
                {"type": "Network", "value": ip_dst})

    list_ports_dst = matrix[id_rule][2].split(";")
    for i in range(0, len(list_ports_dst)):
      if list_ports_dst[i][0:4]=="tcp/":
        sublist_ports_dst = list_ports_dst[i][4::].split(",")
        for p in sublist_ports_dst:
          new_rule["destinationPorts"]["literals"].append(
                {"type": "PortLiteral", "port": p, "protocol": "6"})
      elif list_ports_dst[i][0:4]=="udp/":
        sublist_ports_dst = list_ports_dst[i][4::].split(",")
        for p in sublist_ports_dst:
          new_rule["destinationPorts"]["literals"].append(
                {"type": "PortLiteral", "port": p, "protocol": "17"})
      elif list_ports_dst[i][0:5]=="icmp/":
          new_rule["destinationPorts"]["literals"].append(
                {"type": "ICMPv4PortLiteral", "protocol": "1", "icmpType": "Any"})
    post_data.append(new_rule)

  # Display
  # print(json.dumps(post_data, indent = 4, sort_keys=True))
  
  return(post_data)