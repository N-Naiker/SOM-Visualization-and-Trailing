#Testing of SOMClustering Class
# Nishendran Naiker

# Importing Class and required libraries
from OutliersClass import Outliers
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

print('-------Outlier Class Testing-------')

# Establishing instance variable of SOMClustering Class
Outlier = Outliers(data)
print ('Instance Variable Successfully Created')

# Testing dataCleaning Method
Outlier.dataCleaning()
print ('Data Successfully Cleaned')

# Testing plotSOM Method
fig = Outlier.plotOutliers()
print('Outliers Successfully Plotted')

# Testing showPlot Method
Outlier.showPlot()
print('Outliers Plot Successfully Produced')




