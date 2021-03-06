

# -*- coding:utf-8 -*-
import os
import time
import sys
import numpy

#altered from conflict_finder import Conflict_finder
from conflict_finder_altered import Conflict_finder

#altered
from sentence_similarity.SimilarityChecker import SimilarityChecker

#altered
import string

TP              = 0
TN              = 1
FP              = 2
FN              = 3

THRESHOLD_RANGE_EUCLIDEAN = [1.5, 1.8, 2.15, 2.5, 3.0]
THRESHOLD_RANGE_COSINE = [0.05, 0.075, 0.1, 0.15, 0.17, 0.2, 0.22, 0.24, 0.25, 0.3]

class Test_Conf_Finder:

    """
        Test conflict_finder.py by passing a series of thresholds to the class.
        For each threshold, measure how much true and false positives they generate.
        We consider true positives when the conflict_finder finds potential conflicts
        that were manually inserted in the contracts.
        Whereas, we consider false positives those potential conflicts found that are not
        in the list of inserted conflicts.
    """

    def __init__(self, folders_path, similarityCriteria):

        self.folders_path = folders_path        # Path to the folder where contracts w/ inserted conflicts are located.
        self.dict_thr_tp_fp = dict()            # Dictionary to store true and false positives for each threshold.
        self.list_of_conf_norms_found = dict()
        
        #altered
        print 'Instanciating sent2vec Similarity Checker...'
        self.similarityChecker = SimilarityChecker()
        print 'Similarity Checker ready.'
        self.similarityCriteria = similarityCriteria
        if self.similarityCriteria == 'euclidean':
          self.threshold_range = THRESHOLD_RANGE_EUCLIDEAN
        else:
          self.threshold_range = THRESHOLD_RANGE_COSINE# List of thresholds.
        
        for thr in self.threshold_range:
            # Create a dict in which each key leads to a tuple where the first position is
            # the number of true positives and the second is the number of false positives.
            self.dict_thr_tp_fp[thr] = [0, 0, 0, 0]  # Sequence: True positives, True Negatives, False Positives, False Negatives.
            self.list_of_conf_norms_found[thr] = []

    def test_identifier(self):
        # Check each folder in the folders_path and then each contract in the folder.
        # Process contracts and compute true and false positives.

        folders_list = os.listdir(self.folders_path)

        for folder in folders_list:

            folder_files = os.listdir(self.folders_path + folder)

            print "Processing " + self.folders_path + folder

            for file in folder_files:

                print "\tProcessing contract " + self.folders_path + folder + "/" + file

                if 'new_norms' not in file:

                    contract_path = self.folders_path + folder + "/" + file
                    new_contract_path = self.folders_path + folder + "/new_norms_" + file

                    self.process_contract(contract_path, new_contract_path)
                    
        #altered self.write_results()
        self.write_results_csv()

    def process_contract(self, contract_path, new_contract_path):
        # Read contract path and inserted conflicts file and identify potential conflicts.
        print "\tProcessing Contract..."

        c_finder = Conflict_finder(self.similarityChecker, self.similarityCriteria)
        potential_conflicts = c_finder.process(contract_path, self.threshold_range)

        inserted_conflicts = [sent[:-1] for sent in open(new_contract_path, 'r').readlines()]

        self.process_result(potential_conflicts, inserted_conflicts)

    def process_result(self, result, inserted_conflicts):
        # Compute the true and false positives based on the results of process_contracts.
        # Add 1 to true positive

        print "\tProcessing the result..."

        for thr in self.threshold_range:
            self.dict_thr_tp_fp[thr][TN] += result[-1] - len(inserted_conflicts)      # True negatives
            self.dict_thr_tp_fp[thr][FN] += len(inserted_conflicts)                   # False negatives

        for p_conflict in result[:-1]:

            thr = p_conflict[0]

            if self.dict_thr_tp_fp.has_key(thr):
                
                # Check if one of the norms in the potential conflict is in the set of inserted conflicts.
                if p_conflict[1] in inserted_conflicts and p_conflict[1] not in self.list_of_conf_norms_found[thr]: 
                    self.dict_thr_tp_fp[thr][TP] += 1
                    self.dict_thr_tp_fp[thr][FN] -= 1
                    self.list_of_conf_norms_found[thr].append(p_conflict[1])

                elif p_conflict[2] in inserted_conflicts and p_conflict[2] not in self.list_of_conf_norms_found[thr]:
                    self.dict_thr_tp_fp[thr][TP] += 1
                    self.dict_thr_tp_fp[thr][FN] -= 1
                    self.list_of_conf_norms_found[thr].append(p_conflict[2])

                else:
                    self.dict_thr_tp_fp[thr][FP] += 1
                    self.dict_thr_tp_fp[thr][TN] -= 1

            else:
                sys.exit("Something's wrong, I don't know this threshold %.1f!!!" % p_conflict[0])

    def write_results(self):

        output_file = "thr_tr_and_fl_positives.txt"
        wrt_file = open(output_file, 'w')

        for key in sorted(self.dict_thr_tp_fp.keys()):

            accuracy = (self.dict_thr_tp_fp[key][TP] + self.dict_thr_tp_fp[key][TN])/float(self.dict_thr_tp_fp[key][TP] + self.dict_thr_tp_fp[key][TN] + self.dict_thr_tp_fp[key][FP] + self.dict_thr_tp_fp[key][FN])
            precision = self.dict_thr_tp_fp[key][TP]/float(self.dict_thr_tp_fp[key][TP] + self.dict_thr_tp_fp[key][FP])
            recall = self.dict_thr_tp_fp[key][TP]/float(self.dict_thr_tp_fp[key][TP] + self.dict_thr_tp_fp[key][FN])
            f_measure = 2 * ((precision * recall)/(precision + recall))
            sensitivity = recall
            specificity = self.dict_thr_tp_fp[key][TN]/float(self.dict_thr_tp_fp[key][FP] + self.dict_thr_tp_fp[key][TN])
            fallout = self.dict_thr_tp_fp[key][FP]/float(self.dict_thr_tp_fp[key][FP] + self.dict_thr_tp_fp[key][TN])

            wrt_file.write("""For threshold %.1f:\n\tTrue positives: %d\n\tFalse positives: %d\n\tTrue negatives: %d\n\tFalse negatives: %d\n\tAccuracy: %.2f\n\tPrecision: %.2f\n\tRecall: %.2f\n\tF-Measure: %.2f
                            \n\tSensitivity: %.2f\n\tSpecificity: %.2f\n\tFall-out: %.2f\n\n""" % (key, self.dict_thr_tp_fp[key][TP], self.dict_thr_tp_fp[key][FP],
                             self.dict_thr_tp_fp[key][TN], self.dict_thr_tp_fp[key][FN], accuracy, precision, recall, f_measure, sensitivity, specificity, fallout))

        print "Writing is done."
        wrt_file.close()



    #altered -- This function substitutes the one above.
    #It writes output results directly to csv in a latex friendly syntax
    def write_results_csv(self):

        output_file = "thr_tr_and_fl_positives.csv"
        wrt_file = open(output_file, 'w')
        
        orderedKeys = sorted(self.dict_thr_tp_fp.keys())
        tableHeader = 'Threshold'
        outputRows = []
        
        for key in orderedKeys:
            #Complete the header with all thresholds
            tableHeader = string.join((tableHeader, ',$%.2f$' % key), '')
            
            #Calculate all important measures
            accuracy = (self.dict_thr_tp_fp[key][TP] + self.dict_thr_tp_fp[key][TN])/float(self.dict_thr_tp_fp[key][TP] + self.dict_thr_tp_fp[key][TN] + self.dict_thr_tp_fp[key][FP] + self.dict_thr_tp_fp[key][FN])
            precision = self.dict_thr_tp_fp[key][TP]/float(self.dict_thr_tp_fp[key][TP] + self.dict_thr_tp_fp[key][FP])
            recall = self.dict_thr_tp_fp[key][TP]/float(self.dict_thr_tp_fp[key][TP] + self.dict_thr_tp_fp[key][FN])
            f_measure = 2 * ((precision * recall)/(precision + recall))
            sensitivity = recall
            specificity = self.dict_thr_tp_fp[key][TN]/float(self.dict_thr_tp_fp[key][FP] + self.dict_thr_tp_fp[key][TN])
            fallout = self.dict_thr_tp_fp[key][FP]/float(self.dict_thr_tp_fp[key][FP] + self.dict_thr_tp_fp[key][TN])
            
            #Save the measures in a row in outputRows. Each row corresponds to the results of one threshold
            outputRows.append([self.dict_thr_tp_fp[key][TP],
                               self.dict_thr_tp_fp[key][TN],
                               self.dict_thr_tp_fp[key][FP],
                               self.dict_thr_tp_fp[key][FN],
                               accuracy, precision, recall, f_measure,
                               sensitivity, specificity, fallout
                               ])
        
        wrt_file.write(tableHeader+'\n')
        
        # Names of each subsequent table row
        rowNames = ['True positives',
                    'True negatives',
                    'False positives',
                    'False negatives',
                    'Accuracy',
                    'Precision',
                    'Recall',
                    'F-score',
                    'True positive rate',
                    'Specificity',
                    'False positive rate'
                    ]
        
        # Using numpy to easily work with colums
        npOutputRows = numpy.array(outputRows)
        # each colum of the output rows corresponds to one specific measure of all threasholds
        for i in range(len(npOutputRows[0])):
            tempString = rowNames[i]
            # All values in the colum i are formated to a string and concatenated
            tempString2 = string.join([ tableFormat(n) for n in npOutputRows[:, i] ], '')
            # Print in output file the name of the row concatenated with the formatted values
            wrt_file.write(string.join((tempString, tempString2, '\n'), ''))
          
        print "Writing is done."
        wrt_file.close()

# Quick global function to format a given number into a string.
# The result is in the format $d.dd$
def tableFormat(i):
    return ',$%.2f$' % i


if __name__ == "__main__":
    if len(sys.argv)>1:
      similarityCriteria = sys.argv[1]
    else:
      similarityCriteria = 'euclidean'
    start = time.time()
    tcf = Test_Conf_Finder('data/conflicting_contracts/', similarityCriteria)
    tcf.test_identifier()
    print 'Elapsed time', time.time() - start
