import admin as ad
import os
""" simProcess config object """

supportedStepTypes = ['initial', 'polynomial']

reqAttribByType = {
    'initial': ['dim', 'mean', 'sigma'],
    'polynomial':  ['dim', 'polynomials']
}

optAttribByType = {
    'initial': [],
    'polynomial': []
}

class Config:
   def __init__(self, data):
      """ Deal with admin stuff first """
      if 'admin' in data:
          admin = data['admin']
          self.verbosity = 1
          if 'verbosity' in admin:
              self.verbosity = admin['verbosity']
          ad.log.setLevel(self.verbosity)
      else:
          self.verbosity = 1
          ad.log.setLevel(self.verbosity)
          ad.log(1,"No 'admin' section in input file")

      """ Deal with line definition section"""
      if 'line' in data:
          line = data['line']
          defaultMean = line['defaults']['mean']
          defaultSigma = line['defaults']['sigma']

          self.nSteps = line['nSteps']
          steps = line['steps']
          self.steps = []
          counter = 0
          for key in sorted(steps): #Dictionaries are inherently unsorted, so we rely on lexical ordering by step name.
             myStep = steps[key]

             stepSpec = dict()  # This will get added on to the list self.steps
             stepSpec['type'] = myStep['type']
             stepSpec['mean'] = myStep['mean']
             stepSpec['sigma'] = myStep['sigma']

             if myStep['type'] not in supportedStepTypes:
                print('FATAL ERROR: Step of unsupported type: '+ myStep['type']+ ' specified as input.')
                os.sys.exit(-1)

             reqAttrib = reqAttribByType[myStep['type']] # get list of required attributes for this step type

             for attrib in reqAttrib:  # address each of the required attributes one by one
                if attrib in myStep:   # if we have a locally defined attribute in the current step, use it
                   stepSpec[attrib] = myStep[attrib]
                elif attrib in line['defaults']:
                   stepSpec[attrib] = line['defaults'][attrib]
                else:
                   print('FATAL ERROR: Required attribute: '+ attrib +
                         ' not provided or defaulted in step:' + key)
                   os.sys.exit(-1)

             optAttrib = optAttribByType[myStep['type']] # get list of optional attributes for this step type
             for attrib in optAttrib:  # address each of the optional attributes one by one
                if attrib in myStep:   # if we have a locally defined attribute in the current step, use it
                   stepSpec[attrib] = myStep[attrib]
                elif attrib in line['defaults']:
                   stepSpec[attrib] = line['defaults'][attrib]


             stepSpec['stepNumber'] = counter # C style indexing of step numbers
             stepSpec['stepName'] = key
             self.steps.append(stepSpec)
             counter = counter + 1

          if len(self.steps) != self.nSteps:
             print('FATAL ERROR: Input file states nSteps = ' + str(self.nSteps) +
                   ' but specifies '+str(len(self.steps)))
             os.sys.exit(-1)

      if 'sampling' in data:
          sampling = data['sampling']
          self.nSamples = sampling['nSamples']
          self.outputFile = sampling['outputFile']
      else:
          self.nSamples = 1


   def printConfig(self):
      print("verbosity: ",self.v)
      print("nSteps: ",self.nSteps)

      for step in self.step:
         print('step: ', step['stepNumber'],') ', step['stepName'], ': type: ',step['type'])

         reqAttrib = reqAttribByType[step['type']] # get list of required attributes for this step type
         for attrib in reqAttrib:  # address each of the required attributes one by one
             print("     ", attrib, ": ", step[attrib])
         print("-------")

