# Distribution Class 
# Cleans Data, Calculates the Mean and Deviation for individual features. It the 
# finds the difference between the mean and one standard deviation between the benign
# and malign feature data. 
# Additionally, it finds the bellcurve for the selected data feature
# Nishendran Naiker 2022

# Imports
import seaborn as sns
import pandas as pd
import statistics
import matplotlib.pyplot as plt

# Distribution Class
class Distributions:
    # Initializing class variables for use between methods in class
    global benignData
    global malignData
    global feature_names
    global benignFeatureMean
    global benignFeatureSTDev
    global malignFeatureMean
    global malignFeatureSTDev
    global difference

    # Define Init funtion to allow instance variables of class to be created
    def __init__(self, data):
        self.data = data

    # This funtion is used to clean the data from the dataset
    def dataCleaning(self):
        # This deletes rows with unknown or missing data as this my misrepresent the 
        # data. This deletion is completed by "selecting" rows where some feature 
        # values are NaN. Afterwards, the index allocation on the data is reset to 
        # accompdate the deleted rows. Note that this data has no NaN or missing 
        # values at it has already had these values removed. This was done more so 
        # for demonstration purposes if applied to another dataset.
        self.data = self.data.dropna()
        self.data = self.data.reset_index(drop=True) 
    
    # This function splits the used breast cancer dataset into sub-datasets seperated 
    # by classification of the tumor cell. Simply, it has beed seperated by whether 
    # the data is benign or malign
    def benignDataSplit(self):
        # Selecting the data for each sub-dataset. This is done by selecting the data 
        # for each sub-dataset where the data in the column type is equal to either 
        # benign or malign
        self.benignData = self.data.loc[self.data['type'] == 'benign']
        self.malignData = self.data.loc[self.data['type'] == 'malign']

        # Reseting the index of the sub-datasets 
        self.benignData = self.benignData.reset_index(drop=True)
        self.malignData = self.malignData.reset_index(drop=True)

    # This function gets the feature names from the used dataset
    def setFeatureNames(self):
        self.feature_names = list(self.data.columns[0:9])
    
    # This function returns the feature names of the dataset
    def getFeatureNames(self):
        return self.feature_names

    # This function calculates the statistics of a feature of the sub-datasets. Namely, 
    # it calculates the mean, stamdard deviation and difference between the means with 
    # one standard deviation in the direction of the other sub-dataset
    def calcFeatureStats(self, feature):
        # Retrieving the data from the sub-datasets of a selected feature in the form of
        # a list for easy use of the statistics library
        bFeature = list(self.benignData[feature])
        mFeature = list(self.malignData[feature])

        # Calculating the mean of the selected feature of the benign and malign
        # sub-datasets 
        self.benignFeatureMean = statistics.mean(bFeature)
        self.malignFeatureMean = statistics.mean(mFeature)

        # Calculating the standard deviation of the selected feature of the benign and 
        # malign sub-datasets 
        self.benignFeatureSTDev = statistics.stdev(bFeature)
        self.malignFeatureSTDev = statistics.stdev(mFeature)

        # Calculating the difference of the mean with one standard deviation between 
        # the benign and malign of the selected feature.
        self.difference = (self.malignFeatureMean-self.malignFeatureSTDev)-(self.benignFeatureMean+self.benignFeatureSTDev)
    
    # Returns the calculated mean and standard deviation of the benign sub-dataset
    def getBenignStats(self):
        return self.benignFeatureMean, self.benignFeatureSTDev

    # Returns the calculated mean and standard deviation of the malign sub-dataset
    def getMalignStats(self):
        return self.malignFeatureMean, self.malignFeatureSTDev

    # Returns the calculated value of the difference of the mean with one standard 
    # deviation between the benign and malign of the selected feature.
    def getDifference(self):
        return self.difference

    def getDistArrays(self, n):
        distributionHeadings = ['Feature', 'Benign Mean', 'Benign STDdev', 'Malign Mean', 'Malign STDdev', 'Difference']
        distributionArray = []

        features = [x for x in self.data.drop('type', axis=1).head()]

        for f in features:
            self.calcFeatureStats(f)
            Bm, Bsd = self.getBenignStats()
            Mm, Msd = self.getMalignStats()
            Diff = self.getDifference()
            Data = [f, round(Bm, n), round(Bsd, n), round(Mm, n), round(Msd, n), round(Diff, n)]
            distributionArray = distributionArray + [Data]
        
        return distributionHeadings, distributionArray

    # Plots the bell curves for the selected feature according to the class label
    def plotDistributions(self, feature):
        # Resetting pyplot
        plt.clf() 

        # Using seaborn library to plot bell curve
        sns.kdeplot(data=self.data, x=self.data[feature], hue=self.data['type'], fill=True)

    # Formates and returns figure to be plotted
    def formatPlot(self):
        # Store plot in a figure
        fig = plt.gcf()

        # Return figure
        return fig

    # Shows Plots 
    def showPlot(self):
        plt.show()