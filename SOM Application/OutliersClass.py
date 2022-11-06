#####-----------------------------------Overview-------------------------------------#####

# Outliers Class 
# Produces the outliers of the clusters of the SOM
# Nishendran Naiker 2022

#####--------------------------------Imports Section---------------------------------#####

import matplotlib.pyplot as plt
import seaborn as sns

#####-----------------------------Outliers Class Section-----------------------------#####

class Outliers:
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

    # Funtion to plot the outliers
    def plotOutliers(self):
        # This removes the class label of the dataset so that it may be used for 
        df = self.data.iloc[:, [1,5]]

        # Clearing pyplot
        plt.clf() 

        # Plotting of SOM data using seaborn. This will showcase the outliers with a 
        # lighter hue than those which are inliers
        sns.scatterplot(data=df, x='bare_nucleoli', y='size_uniformity', alpha=0.4)
        
        # Storing Figure
        fig = plt.gcf()

        # Return figure
        return fig

    # Function for showing SOM clusters plot
    def showPlot(self):
        plt.show()