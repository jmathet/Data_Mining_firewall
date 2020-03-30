import numpy as np
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import xlsxwriter
import string

def aggregated_data1():

    df = pd.read_excel('demo.xlsx')
    df.columns = ['Source IP', 'TCP/UDP', 'Service Port', 'Description of Service','Destination IP', 'Action']
    ips = df.groupby(['Source IP', 'TCP/UDP', 'Service Port', 'Destination IP', 'Action'])


    workbook = xlsxwriter.Workbook('aggregated_data1.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.set_column('A:A', 20)
    worksheet.set_column('B:B', 20)
    worksheet.set_column('C:C', 20)
    worksheet.set_column('D:D', 20)
    worksheet.set_column('E:E', 20)
    worksheet.set_column('F:F', 20)

    bold = workbook.add_format({'bold': True})

    worksheet.write('A1', 'Source IP', bold)
    worksheet.write('B1', 'TCP/UDP', bold)
    worksheet.write('C1', 'Service Port', bold)
    worksheet.write('D1', 'Description of Service', bold)
    worksheet.write('E1', 'Destination IP', bold)

    for index, inst in enumerate(ips):
        line = str(inst[0]).translate(str(inst[0]).maketrans('', '', '()'))
        data_line = line.split(",")
        src_host = data_line[0]
        dst_host = data_line[3]
        dst_port = data_line[2]
        protocol = data_line[1]

        worksheet.write(index+1, 0, src_host)
        worksheet.write(index+1, 1, protocol)
        worksheet.write(index+1, 2, dst_port)
        worksheet.write(index+1, 4, dst_host)


    workbook.close()

def aggregated_data2():

        df = pd.read_excel('aggregated_data1.xlsx')
        df.columns = ['Source IP', 'TCP/UDP', 'Service Port', 'Description of Service','Destination IP', 'Action']
        ips = df.groupby(['Source IP', 'TCP/UDP', 'Destination IP'])


        workbook = xlsxwriter.Workbook('aggregated_data2.xlsx')
        worksheet = workbook.add_worksheet()
        # Widen the first column to make the text clearer.
        worksheet.set_column('A:A', 20)
        worksheet.set_column('B:B', 20)
        worksheet.set_column('C:C', 80)
        worksheet.set_column('D:D', 20)
        worksheet.set_column('E:E', 20)

        bold = workbook.add_format({'bold': True})

        worksheet.write('A1', 'Source IP', bold)
        worksheet.write('B1', 'TCP/UDP', bold)
        worksheet.write('C1', 'Service Port', bold)
        worksheet.write('D1', 'Description of Service', bold)
        worksheet.write('E1', 'Destination IP', bold)


        for index, inst in enumerate(ips):
            line = str(inst[0]).translate(str(inst[0]).maketrans('', '', '()')) #delete the characters (('')) from the line

            data_line = line.split(",")
            src_host = data_line[0]
            dst_host = data_line[2]
            protocol = data_line[1]

            port_num = 7
            port_list = []
            for i, port in enumerate(str(inst[1]).split()):
                if i >= 14 and i%port_num == 0:
                    port_list = port_list + [port]


            worksheet.write(index+1, 0, src_host.translate(src_host.maketrans('', '', "''")))
            worksheet.write(index+1, 1, protocol.translate(protocol.maketrans('', '', "''")))
            worksheet.write(index+1, 2, str(port_list).translate(str(port_list).maketrans('', '', "'[]'")))
            worksheet.write(index+1, 4, dst_host.translate(dst_host.maketrans('', '', "''")))

        workbook.close()


def main():
    # aggregated_data1()
    aggregated_data2()

if __name__ == "__main__":
    main()
