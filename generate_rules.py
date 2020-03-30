import os
import traceback
import weka.core.jvm as jvm

import weka.core.converters as converters
from weka.core.converters import Loader, Saver
# import weka.examples.helper as helper
# from weka.core.converters import Loader
from weka.classifiers import Classifier, SingleClassifierEnhancer, MultipleClassifiersCombiner, FilteredClassifier, PredictionOutput, Kernel, KernelClassifier
from weka.classifiers import Evaluation
from weka.filters import Filter
from weka.core.classes import Random, from_commandline
import weka.plot.classifiers as plot_cls
import weka.plot.graph as plot_graph
import weka.core.serialization as serialization
import weka.core.typeconv as typeconv


import xlsxwriter

def main():

    workbook = xlsxwriter.Workbook('../data/demo.xlsx')
    worksheet = workbook.add_worksheet()
    # Widen the first column to make the text clearer.
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
    worksheet.write('F1', 'Action', bold)

        # load a dataset
    loader = Loader(classname="weka.core.converters.ArffLoader")

    test_data = loader.load_file("../Logs/arff/logs_training_test.arff")
    test_data.class_is_last() # set class attribute
    #
    # classifier2 = Classifier(classname="weka.classifiers.trees.J48", options=["-C", "0.3"])
    # classifier2.build_classifier(test_data)


    #    # evaluate model on train/test split
    objects = serialization.read_all("../out.model")
    classifier2 = Classifier(jobject=objects[0])
    evaluation = Evaluation(test_data)
    evl = evaluation.test_model(classifier2, test_data)
    # print(evl)
    # evaluation.evaluate_train_test_split(classifier2, test_data, 66.0, Random(1))

    # print(evaluation.predictions)
    # evaluation.evaluate_train_test_split(classifier2, test_data, 66.0, Random(1))
    #
    # print(list(enumerate(test_data)))
    i = 0
    for index, inst in enumerate(test_data):
        pred = classifier2.classify_instance(inst)
        dist = classifier2.distribution_for_instance(inst)
        data_line = str(inst).split(",")
        src_host = data_line[0]
        dst_host = data_line[1]
        dst_port = data_line[3]
        protocol = data_line[4]
        # print(int(pred))
        if int(pred) == 1:
            action = "permitted"
            # print(action)
            # print(src_host)
            worksheet.write(i+1, 0, src_host)
            worksheet.write(i+1, 1, protocol)
            worksheet.write(i+1, 2, dst_port)
            worksheet.write(i+1, 4, dst_host)
            worksheet.write(i+1, 5, action)
            i = i+1



        # print(str(inst).split(","))
        # print(len(inst))

        # print(str(pred))
        # print(str(index+1) + ": label index=" + str(pred) + ", class distribution=" + str(dist))


    print(evaluation.summary())
    workbook.close()

if __name__ == "__main__":
    try:
        jvm.start(max_heap_size="2g")
        main()
    except Exception as e:
        print(traceback.format_exc())
    finally:
        jvm.stop()
