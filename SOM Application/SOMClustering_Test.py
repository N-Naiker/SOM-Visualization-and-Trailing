#Testing of SOMClustering Class
# Nishendran Naiker

# Importing Class and required libraries
from SOMClusteringClass import SOMClustering
import matplotlib
import pandas as pd
import os

# Retrieving data from csv files. 
# The column names are also applied and the seperator defined
data = pd.read_csv('breast-cancer.csv', 
                    names=['clump_thickness', 'size_uniformity', 'shape_uniformity', 'marginal_adhesion',
                   'epithelial_size', 'bare_nucleoli', 'bland_chromatin', 'normal_nucleoli', 'mitoses', 'type'], sep=',')

# Clearing Terminal
os.system('clear')

# Establishing instance variable of SOMClustering Class
SOMcl = SOMClustering(data)
print ('Instance Variable Successfully Created')

# Testing dataCleaning Method
SOMcl.dataCleaning()
print ('Data Successfully Cleaned')

# Testing Normalisation Method
SOMcl.normalise()
print('Data Successfully Normalised')

# Testing getPredictioInputs Method
predInputs = SOMcl.getPredictioInputs()
print('Inputs Successfully Retrieved:\n', predInputs)

# Testing SOMBuilding Method
SOMcl.SOMBuilding()
print('SOM Successfully Built')

# Testing getConfidenceUnseen Method
unseenConfidence, unseenSamples = SOMcl.getConfidenceUnseen()
print('Unseen Confidence Test Successfully Performed.\n', 'Based on a sample size of ', 
       unseenSamples, ' the some produced a confidence rating of ', str(unseenConfidence)+ 
       '%')

# Testing getConfidenceSeen Method
seenConfidence, seenSamples = SOMcl.getConfidenceUnseen()
print('Seen Confidence Test Successfully Performed.\n', 'Based on a sample size of ', 
       seenSamples, ' the some produced a confidence rating of ', str(seenConfidence)+
       '%')

# Testing plotSOM Method
SOMcl.plotSOM()
print('SOM Successfully Plotted')

# Testing plotPrediction Method
SOMcl.plotPrediction(0)
print('Predictions Successfully Plotted')


# Testing formatPlot Method
fig = SOMcl.formatPlot()
print('SOM Fig Successfully Set')

# Testing showPlot Method
SOMcl.showPlot()
print('SOM Plot Successfully Produced')




