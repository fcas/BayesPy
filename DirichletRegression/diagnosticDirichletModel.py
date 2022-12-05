#!/usr/bin/python

# A sample of a file to pipe into this python script is given by logisticRegressionTest.csv

# ex
# python diagnosticDirichletModel.py -m model.txt -k 3

# Each row contains first the label, then a series of feature:value pairs separated by tabs
# If the feature isn't given at all, it is assumed to be 0
# If the feature is give with no value, the value is assumed to be 1

import sys
import csv
import math
import random
import time
from optparse import OptionParser
import logging
from random import shuffle

startTime = time.time()
parser = OptionParser()
parser.add_option('-m', '--model', dest='model', help='File containing the logistic model')
parser.add_option('-K', '--K', dest='k', help='Number of Categories')
parser.add_option("-L", '--loglevel', action="store", dest="loglevel", default='DEBUG', help="don't print status messages to stdout")

(options, args) = parser.parse_args()

#Set the log level
log_level = options.loglevel
numeric_level = getattr(logging, log_level, None)
if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % loglevel)
logging.basicConfig(level=numeric_level)

#####
# Load Data
#####

csv.field_size_limit(1000000000)
logging.debug("Loading model")

featureWeights = {}
featureProbs = {}
numFeatures = 0
K = int(options.k)
for line in open(options.model, 'r'):
  row = line.split('\t')
  scores = [0.0]*K
  for k in range(0, K): 
    if (len(row) > k + 1):
      scores[k] = float(row[k + 1])
  featureWeights[row[0]] = scores
  
  expScores = map(math.exp, scores)
  sumExpScores = sum(expScores)
  featureProbs[row[0]] = map(lambda x: x / sumExpScores, expScores)
  numFeatures += 1

for k in range(0, K):
  print "****** Superlatives for classification %s ******" % k
  print "Top 20"
  bests = sorted(featureProbs.items(), key=lambda x: -1 * featureProbs[x[0]][k])
  for i in range(0, 20):
    (feature, probDist) = bests[i]
    print str(i) + "\t" + feature + "\t" + str(probDist)

calcTime = time.time()
logging.debug("runnning time: %s " % (calcTime - startTime))
