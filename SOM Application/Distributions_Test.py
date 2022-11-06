#Testing of SOMClustering Class
# Nishendran Naiker

# Importing Class and required libraries
from DistributionsClass import Distributions
import pandas as pd
import os

# Retrieving data from csv files. 
# The column names are also applied and the seperator defined
data = pd.read_csv('breast-cancer.csv', 
                    names=['clump_thickness', 'size_uniformity', 'shape_uniformity', 'marginal_adhesion',
                   'epithelial_size', 'bare_nucleoli', 'bland_chromatin', 'normal_nucleoli', 'mitoses', 'type'], sep=',')

feature = 'mitoses'

# Clearing Terminal
os.system('clear')

# Establishing instance variable of Distributions Class
Dist = Distributions(data)
print ('Instance Variable Successfully Created')

# Testing dataCleaning Method
Dist.dataCleaning()
print ('Data Successfully Cleaned')

# Testing benignDataSplit Method
Dist.benignDataSplit()
print ('Data Successfully Split')

# Testing setFeatureNames Method
Dist.setFeatureNames()
print ('Feature Names Successfully Set')

# Testing getFeatureNames Method
output = Dist.getFeatureNames()
print ('Feature Names Successfully Retrieved. The Feature Names are:\n', output)

# Testing calcFeatureStats Method
Dist.calcFeatureStats('clump_thickness')
print ('Feature Stats Successfully Calculated')

# Testing getBenignStats Method
mean,std = Dist.getBenignStats()
print ('Benign Stats Successfully Retrieved.\n', 'The mean is ', mean, 'and the standard deviation is ', std)

# Testing getMalignStats Method
mean,std = Dist.getMalignStats()
print ('Malign Stats Successfully Retrieved.\n', 'The mean is ', mean, 'and the standard deviation is ', std)

# Testing getDifference Method
diff = Dist.getDifference()
print ('Difference Successfully Retrieved.\n', 'The difference is ', diff)

# Testing getDistArrays Method
header, array = Dist.getDistArrays(2)
print ('Dist Arrays Successfully Retrieved\n',header, '\n', array)

# Testing plotDistributions Method
Dist.plotDistributions(feature)
print ('Bell Curves Successfully Plotted')

# Testing formatPlot Method
fig = Dist.formatPlot()
print ('Bell Curves Successfully Stored and Formatted')

# Testing showPlot Method
Dist.showPlot()
print ('Bell Curves Successfully Displayed')
