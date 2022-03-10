# (c) Will Swindell 2022

import numpy as np
import pandas as pd
from classes import *



def learn_one_rule(columns, data, class_label, rule = None, min_coverage=30, min_accuracy=0.6):
    covered = data.copy()
    accuracy = 0.00
    coverage = 0
    if(rule != None):
        current_rule = rule
        accuracy = rule.accuracy
        coverage = rule.coverage
    else:
        current_rule = Rule(class_label)

    best_accuracy = 0.00
    best_coverage = 0
    attr = None
    val = None
    true_false = None

    for col in columns[:-1]:
        options = covered[col].unique().tolist()
        for option in options:
            if (isinstance(option, int) or isinstance(option, float)):
                split1 = covered[covered[col] >= option]
                split2 = covered[covered[col] < option]
                if(len(split1) == 0):
                    true_acc = 0.0
                else:
                    true_acc = len(split1[(split1[columns[-1]] == class_label)])/len(split1)
                if(len(split2) == 0):
                    false_acc = 0.0
                else:
                    false_acc = len(split2[(split2[columns[-1]] == class_label)])/len(split2)
                true_false = (true_acc > false_acc)
                curr_acc = max(true_acc, false_acc)
                curr_cov = 0
                if(true_false == True):
                    curr_cov = len(split1)
                else:
                    curr_cov = len(split2)

                if(curr_acc > best_accuracy or (curr_acc == best_accuracy and curr_cov > best_coverage)):
                    best_accuracy = curr_acc
                    best_coverage = curr_cov
                    attr = col
                    val = option

            else:
                split = covered[covered[col] == option]
                curr_acc = len(split[(split[columns[-1]] == class_label)])/len(split)
                curr_cov = len(split)

                if(curr_acc > best_accuracy or (curr_acc == best_accuracy and curr_cov > best_coverage)):
                    true_false = None
                    best_accuracy = curr_acc
                    best_coverage = curr_cov
                    attr = col
                    val = option


    if(best_accuracy == 1.0 and best_coverage >= min_coverage):
        cond = Condition(attr, val, true_false)
        current_rule.addCondition(cond)
        current_rule.setParams(best_accuracy, best_coverage)
        if(true_false is not None):
            if(true_false == True):
                covered = covered[(covered[attr] >= val)]
            else:
                covered = covered[(covered[attr] < val)]
        else:
            covered = covered[(covered[attr] == val)]


        return (current_rule, covered)

    else:

#        if(len(columns) <= 2):
#            if(best_accuracy >= min_accuracy and best_coverage >= min_coverage):
#                cond = Condition(attr, val, true_false)
#                current_rule.addCondition(cond)
#                current_rule.setParams(best_accuracy, best_coverage)
#                if(true_false is not None):
#                    if(true_false == True):
#                        covered = covered[(covered[attr] >= val)]
#                    else:
#                        covered = covered[(covered[attr] < val)]
#                else:
#                    covered = covered[(covered[attr] == val)]
#
#                return (current_rule, covered)
#            else:
#                return (None, covered)
#
#        else:
        if(attr == None):
            return(None, covered)
        cond = Condition(attr, val, true_false)
        current_rule.addCondition(cond)
        current_rule.setParams(best_accuracy, best_coverage)
        if(true_false is not None):
            if(true_false == True):
                covered = covered[(covered[attr] >= val)]
            else:
                covered = covered[(covered[attr] < val)]
        else:
            covered = covered[(covered[attr] == val)]
        #print(covered)
        copy = columns.copy()
        copy.remove(attr)

        new = (min_coverage+1)
        return learn_one_rule(copy, covered, class_label, current_rule, min_coverage, min_accuracy)


    return None



def learn_rules (columns, data, classes=None,
                 min_coverage = 30, min_accuracy = 0.6):
    # List of final rules
    rules = []

    # If list of classes of interest is not provided - it is extracted from the last column of data
    if classes is not None:
        class_labels = classes
    else:
        class_labels = data[columns[-1]].unique().tolist()

    current_data = data.copy()

    # This follows the logic of the original PRISM algorithm
    # It processes each class in turn.
    for class_label in class_labels:
        done = False

        while len(current_data) > min_coverage and not done:
            # Learn one rule
            rule, subset = learn_one_rule(columns, current_data, class_label, min_coverage=min_coverage, min_accuracy=min_accuracy)

            # If the best rule does not pass the coverage threshold - we are done with this class
            if rule is None:
                done = True
                continue

            # If we get the rule with accuracy and coverage above threshold

            if rule.accuracy >= min_accuracy:
                rules.append(rule)

                # remove rows covered by this rule
                # you have to remove the rows where all of the conditions hold
                #print(current_data)
                #current_data = current_data[(current_data['astigmatism'] != 'yes')]
                #current_data = current_data[(current_data['tear production rate'] != 'reduced')]

                current_data = (current_data[~current_data.isin(subset).all(1)])



            else:
                done = True

    return rules

if __name__ == "__main__":

    data_file = "../../Datasets/covid_categorical_good.csv"
    data = pd.read_csv(data_file)
    data = data.dropna(how="any")
    column_list = data.columns.to_numpy().tolist()
    rules = learn_rules (column_list, data, None, 2, 0.9)
    for rule in rules[:20]:
        print(rule)
