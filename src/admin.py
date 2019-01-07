# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 15:17:12 2018

@author: maxim

 Just a bunch of administrative OS-level function.

"""

import yaml
import numpy as np
from sys import stdout

def yaml_loader(filepath):
    """ load up a YAML file"""
    with open(filepath, "r") as fd:
        data = yaml.load(fd)
    return data

def yaml_dump(filepath, data):
    """ dump data to a YAML file"""
    with open(filepath, "w") as fd:
        yaml.dump(data, fd)

if __name__ == "__main__":
    print("Not a main program, use only as library.")


def array2csv(a, precision=5):

    csv =  "{:" + "{}".format(precision) + "f}"
    csv = csv.format(a[0])
    myFormat = ", {:" + "{}".format(precision) + "f}"
    for f in a[1:]:
        csv = csv + myFormat.format(f)
    csv = csv + "\n"
    return csv

""" Higher priority is lower number """
class Log:
    def __init__(self, level, output=None):
        self.level = level
        if output is not None:
            self.fd = fd.open(output, "w")
        else:
            self.fd = stdout

    def __call__(self, v, message):
        if v <= self.level:
            self.fd.write(message + "\n")

    def setLevel(self, level):
        self.level = level
        self.fd.write("Setting verbosity to {}.\n".format(self.level))

log = Log(0)
