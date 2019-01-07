import argparse
import admin as ad
from config import Config
import numpy as np

"""Bring in the configuration filename from the command line"""
parser = argparse.ArgumentParser(
description="Get input YAML file as inputFile")
parser.add_argument('inputFile',
                     help='The input YAML file to drive the simulation')

args = parser.parse_args()

yaml_data = ad.yaml_loader(args.inputFile)
config = Config(yaml_data)

""" Preallocate memory for the step outputs """
lineSteps = config.steps[1:]
initStep = config.steps[0]
stepOutput = np.zeros(initStep['dim'])

outputs = [stepOutput]
nOut = initStep['dim']
for step in lineSteps:
    nIn = nOut
    nOut = step['dim']

    stepOutput = np.zeros(nOut)
    outputs.append(stepOutput)

fd = open(config.outputFile, "w")

""" Time to run the line """
for sample in range(config.nSamples):

    iStep = 0
    stepType = initStep['type']
    ad.log(10, "Step {} is type '{}'.".format(iStep, stepType))
    for i in range(initStep['dim']):
        outputs[0][i] = np.random.normal(
           initStep['mean'][i],
           initStep['sigma'][i],
           1)
    nOut = initStep['dim']

    for step in lineSteps:
        iStep = iStep + 1
        stepType = step['type']
        ad.log(10, "Step {} is type '{}'.".format(iStep, stepType))
        nIn = nOut
        nOut = step['dim']


        outputs[iStep][:] = np.random.normal(step['mean'], step['sigma'], nOut)
        for outputKey in step['polynomials']:
            outputFunction = step['polynomials'][outputKey]
            toOutput = outputFunction['output']
            for monomialKey in outputFunction['terms']:
                monomial = outputFunction['terms'][monomialKey]
                contrib = 1.0
                (j, k) = monomial[0]
                for factor in monomial[1:]:
                    contrib *= factor[0] 
                    contrib *= outputs[iStep + j][k] ** factor[1]
            outputs[iStep][toOutput] += contrib

    tmp1 = np.array([])
    for tmp2 in outputs:
        tmp1 = np.concatenate([tmp1, np.array(tmp2)])

    fd.write(ad.array2csv(tmp1))
