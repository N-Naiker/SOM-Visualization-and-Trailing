#Testing of TreeDecisionDiagram Class
# Nishendran Naiker

# Importing Class and required libraries
from TreeDecisionDiagramClass import TreeDecisionDiagram
import pandas as pd
import os

# Retrieving data from csv files. 
# The column names are also applied and the seperator defined
data = pd.read_csv('breast-cancer.csv', 
                    names=['clump_thickness', 'size_uniformity', 'shape_uniformity', 'marginal_adhesion',
                   'epithelial_size', 'bare_nucleoli', 'bland_chromatin', 'normal_nucleoli', 'mitoses', 'type'], sep=',')

# Clearing Terminal
os.system('clear')
print('---------TreeDecisionDiagram Class Testing---------')
# Establishing instance variable of TreeDecisionDiagram Class
TDD = TreeDecisionDiagram(data)
print('Instance Variable Successfully Created')

# Testing dataCleaning Method
TDD.dataCleaning()
print('Data Successfully Cleaned')

# Testing featureNames Method
TDD.featureNames()
print('Feature Names Successfully Retrieved')

# Testing dataSelecion Method
TDD.dataSelecion()
print('Data Successfully Selected')

# Testing formatClassLabels Method
TDD.formatClassLabels()
print('Class Labels Successfully Formatted')

# Testing setClassNames Method
TDD.setClassNames()
print('Class Names Successfully Retrieved & Set')

# Testing trainTestSplit Method
TDD.trainTestSplit()
print('Data Successfully Split Into Training & Testing Data')

# Testing buildTree Method
TDD.buildTree(3)
print('Tree Model Successully Built')

# Testing treeEvaluation Method
accuracy = TDD.treeEvaluation()
print('Tree Model Successfully Evaluated. \n The Tree Model Has An Accuracy of ', round(accuracy, 3))

# Testing getTextRepresentation Method
textTree = TDD.getTextRepresentation()
print('Text Representation of Tree Model Successfully Retrieved')
#print(textTree)

# Testing displayTree Method
TDD.plotTree()
print ('Tree Decision Diagram Successfully Plotted')

# Testing displayTree Method
out = TDD.formatPlot()
print ('Tree Decision Diagram Successfully Stored')

# Testing displayTree Method
TDD.displayTree()
print ('Tree Decision Diagram Successfully Displayed')