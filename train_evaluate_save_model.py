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
import weka.core.typeconv as typeconv
import weka.core.serialization as serialization

# cls = Classifier(classname="weka.classifiers.trees.J48")
# cls.options = ["-C", "0.3"]

def main():
        # load a dataset
    loader = Loader(classname="weka.core.converters.ArffLoader")
    train_data = loader.load_file("/home/atos-user/project/Logs/arff/logs_training.arff")

    train_data.class_is_last() # set class attribute

    classifier = Classifier(classname="weka.classifiers.rules.PART", options=["-C", "0.25", "-M", "2", "-Q", "1"])
    # classifier = Classifier(classname="weka.classifiers.rules.JRip", options=["-F", "3", "-N", "2.0", "-O", "2", "-S", "1"])
    # classifier = Classifier(classname="weka.classifiers.trees.RandomForest",  options=["-P", "100", "-I", "100", "-num-slots", "1", "-S", "1", "-K", "0", "-M", "1.0", "-V", "0.001"])
    # classifier = Classifier(classname="weka.classifiers.functions.MultilayerPerceptron",  options=["-L", "0.3", "-M", "0.2", "-N", "500", "-S", "0", "-V", "0", "-E", "20", "-H", "a"])
    classifier.build_classifier(train_data)

    predicted_index = 0
    notpredicted_index = 0
    index = 0
    index_predicted = 0
    index_notpredicted = 0
    fauxpositif1 = 0
    fauxpositif2 = 0
    for index, pred in enumerate(evaluation.predictions):

        if pred.predicted == 1.0 and pred.actual == 1.0 :
            index_predicted +=1
        if pred.predicted == 0.0 and pred.actual == 0.0 :
            index_notpredicted +=1
        if pred.predicted == 1.0 and pred.actual == 0.0 :
            fauxpositif1 +=1
        if pred.predicted == 0.0 and pred.actual == 1.0 :
            fauxpositif2 +=1


    print("index_predicted = ", index_predicted)
    print("index_notpredicted = ", index_notpredicted)
    print("fauxpositif1 = ", fauxpositif1)
    print("fauxpositif2 = ", fauxpositif2)
    print(evaluation.summary())

    serialization.write("/home/atos-user/project/project_files/PART.model", classifier) # save model


if __name__ == "__main__":
    try:
        jvm.start(max_heap_size="2g")
        main()
    except Exception as e:
        print(traceback.format_exc())
    finally:
        jvm.stop()
