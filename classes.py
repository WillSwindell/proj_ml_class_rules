import pandas as pd
import numpy as np

class Rule:
    def __init__(self, class_label):
        self.conditions = []  # list of conditions
        self.class_label = class_label  # rule class
        self.accuracy = 0.00
        self.coverage = 0

    def addCondition(self, condition):
        self.conditions.append(condition)

    def setParams(self, accuracy, coverage):
        self.accuracy = accuracy
        self.coverage = coverage

    # Human-readable printing of this Rule
    def __repr__(self):
        return "If {} then {}. Coverage:{}, accuracy: {}".format(self.conditions, self.class_label,
                                                                 self.coverage, self.accuracy)
class Condition:
    def __init__(self, attribute, value, true_false = None):
        self.attribute = attribute
        self.value = value
        self.true_false = true_false

    def __repr__(self):
        if self.true_false is None:
            return "{}={}".format(self.attribute, self.value)
        else:
            return "{}>={}:{}".format(self.attribute, self.value, self.true_false)
