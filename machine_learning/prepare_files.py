# from io import open
# import glob
# import os
#
# def findFiles(path): return glob.glob(path)
#
# print(findFiles('./*.txt'))
#
# import unicodedata
# import string

# import rhinoscriptsyntax as rs
# import json

import torch
import torch.nn as nn
from torch.autograd import Variable

import json

with open('logs.txt') as json_file:
    data = json.load(json_file)
    src_host = data['_source']['src_host']
    dst_host = data['_source']['dst_host']
    src_port = data['_source']['src_port']
    dst_port = data['_source']['dst_port']
    protocol = data['_source']['protocol']
    action = data['_source']['action']
    log_1 = [src_host, dst_host, src_port, dst_port, protocol, action]
    category_logs = {'true':{}, 'false':[]}
    category_logs['true'] = {'1':log_1}
    category_logs['false'] = {}

    # print(category_logs['true']['1'][0])
    # print(action)
    # for p in data['_source']['host']:
    #     print(p)
        # print('host: ' + p['host'])
        # print('src_port: ' + p['src_port'])
        # print('From: ' + p['from'])
        # print('')

def parseIP(ip):
    X = []
    x = ""
    for i in ip:
        if i == '.':
            X = X + [x]
            x = ""
            continue
        else:
            x=x+str(i)
    X = X + [x]
    return X
#
log_1 = category_logs['true']['1']
a = log_1[0]
# print("log = \n")
# print(log_1)
#
# print(a)
# print(type("111.222.222.555"))
# print(type(a))
# print(parseIP(a))
# print(parseIP("111.222.222.555"))


def logToTensor(log):
    tensor = torch.zeros(len(log), 1, 4)

    for i in range(0,4):
        # print(parseIP(log[0])[i])
        tensor[0][0][i] = int(parseIP(log[0])[i])
        tensor[1][0][i] = int(parseIP(log[1])[i])
    for i in range(2,4):
        tensor[i][0][0] = int(log[i])
    if log[4] == 'tcp':
        tensor[4][0][0] = 6
    elif log[4] == 'udp':
        tensor[4][0][0] = 17
    if log[5] == 'permitted':
        tensor[5][0][0] = 1
    else:
        tensor[5][0][1] = 1
    return tensor

print(logToTensor(log_1))
# print(logToTensor(log_1).size())

with open('logs.txt') as json_file:
    data = json.load(json_file)
    src_host = data['_source']['src_host']
    dst_host = data['_source']['dst_host']
    src_port = data['_source']['src_port']
    dst_port = data['_source']['dst_port']
    protocol = data['_source']['protocol']
    action = data['_source']['action']
    log_1 = [src_host, dst_host, src_port, dst_port, protocol, action]
    category_logs = {'true':{}, 'false':[]}
    category_logs['true'] = {'1':log_1}
    category_logs['false'] = {}

class RNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(RNN, self).__init__()

        self.hidden_size = hidden_size

        self.i2h = nn.Linear(input_size + hidden_size, hidden_size)
        self.i2o = nn.Linear(input_size + hidden_size, output_size)
        self.softmax = nn.LogSoftmax()

    def forward(self, input, hidden):
        combined = torch.cat((input, hidden), 1)
        hidden = self.i2h(combined)
        output = self.i2o(combined)
        output = self.softmax(output)
        return output, hidden

    def initHidden(self):
        return Variable(torch.zeros(1, self.hidden_size))

n_hidden = 128
n_categories = 2 #Bad or good log
input_size = 3*4 + 3*4 +65536*2 +3*2 + 10
rnn = RNN(input_size, n_hidden, n_categories)
log_1 = category_logs['true']['1']
input = logToTensor(log_1)
hidden = torch.zeros(1, n_hidden)

output, next_hidden = rnn(input[0], hidden)
print(output)
