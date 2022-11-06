#####-----------------------------------Overview-------------------------------------#####

# SOMClustering Class 
# Cleans Data, Bulids SOM Model & Plots SOM Clustering and Classification Data
# Additionally, it plots centroids of clusters as well as predictions on input Data
# Nishendran Naiker 2022

#####--------------------------------Imports Section---------------------------------#####

# Required Imports
from minisom import MiniSom
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

#####--------------------------SOM Clustering Class Section--------------------------#####

# Clustering Class
class SOMClustering:
    # Initializing class variables for use between methods in class
    global dataUnseenClassifications
    global dataSeenClassifications
    global dataUnseen
    global dataSeen
    global cluster_index
    global som
    global som_shape
    global predInputs
    global predUnseen
    
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

    # Funtion for normalising and setting up training and testing data    
    def normalise(self):
        # Storing Unseen Results
        self.dataUnseenClassifications = self.data[-68:]
        self.dataUnseenClassifications = list(self.dataUnseenClassifications['type'])

        # Storing Seen Results
        self.dataSeenClassifications = self.data[-136:-69]
        self.dataSeenClassifications = list(self.dataSeenClassifications['type'])

        # Storing Prediction Inputs
        self.predInputs = self.data[-6:]
        self.predInputs = self.predInputs.reset_index(drop=True) 

        # This removes the class label of the dataset so that it may be used for 
        # unsupervised learning for testing and the purposes of this thesis
        self.data = self.data.drop('type', axis=1)

        # Here the data is normalised by dividing the difference between the data
        # and the mean of the data by the standard deviation of the data 
        # Note that this is only possible for numerical data
        self.data = (self.data - np.mean(self.data, axis=0)) / np.std(self.data, axis=0)

        # Storing Unseen testing
        self.predUnseen= self.data[-6:]

        # Getting values compatible with numpy class
        self.dataUnseen = self.data[-68:].values
        self.dataSeen = self.data[-136:-69].values

        # Here the .values funtion return a numpy representation of the data
        # within the dataframe. Additionally, 10% of the data has been truncated
        # from the dataset to be used for validation testing on unseen data.
        # Note that this will be in conjunction with testing the SOM on seen data.
        self.data = self.data[:-68].values
    
    # Function for retrieving predictions to be used to plotting
    def getPredictioInputs(self):
        # Returning prediction inputs
        return self.predInputs

    # Funtion for building and training the SOM
    def SOMBuilding(self):
        # This funtion initializes and trains the SOM model using the minisom 
        # library
        # Here the size and shape of the som to be established is defined
        self.som_shape = (1, 2)

        # Here the SOM model is trained using the SOM Shape for reference and the 
        # required dataset. Additionally, the signma and learning rate are also 
        # defined. These will be used in the building of the som as well as the 
        # training respectively. The learning rate will be applied to the competative 
        # algorithm and be reduced over iterations to maintain neighbour relations 
        # within the data along with a guassian method as defined within the minisom 
        # library.
        self.som = MiniSom(self.som_shape[0], self.som_shape[1], self.data.shape[1], sigma=.5, learning_rate=.5,
                      neighborhood_function='gaussian', random_seed=10)

        # Training of SOM model over 500 iterations using minisom library
        self.som.train_batch(self.data, 1000, verbose=True)

    
        # Selecting BMU for each sample in training dataset where each neuron is a 
        # cluster of data points
        winner_coordinates = np.array([self.som.winner(x) for x in self.data]).T

        # Converting winner coordinates to a monodimensional index
        self.cluster_index = np.ravel_multi_index(winner_coordinates, self.som_shape)

    # This function performs a confidence test on unseen data
    def getConfidenceUnseen(self):
        # Selecting BMU for each sample in unseen test dataset where each neuron is 
        # a cluster of data points
        winner_coordinates = np.array([self.som.winner(x) for x in self.dataUnseen]).T

        # Converting winner coordinates to a monodimensional index
        ci = np.ravel_multi_index(winner_coordinates, self.som_shape)

        # Converting cluster_index into a list form for simplicity and processing
        unseenPredictions = list(ci)
        
        # Replacing the unseen classifications applied to each cluster, which starts 
        # at and index of zero and increased with each subsequent cluster, with the 
        # class label we know it to have. This is done so the reserved class labeled 
        # for the unseen data can easily be compared to determin if the predictions 
        # were correct
        for i in range(len(unseenPredictions)):
            if unseenPredictions[i] == 0:
                unseenPredictions[i] = 'benign'
            if unseenPredictions[i] == 1:
                unseenPredictions[i] = 'malign'

        # Getting total number of samples for use to get confidence percentage
        total_samples = len(unseenPredictions)

        # Initialising matching samples variable to count how many samples match 
        # from predictions compared to the class we know them to belong.
        matching_samples = 0

        # Counting the number of matching samples (correct predictions)
        for i in range(len(unseenPredictions)):
            if unseenPredictions[i] == self.dataUnseenClassifications[i]:
                matching_samples = matching_samples + 1

        # Calculating the confidence percentage based on the number of correct 
        # predictions versus the total number of samples
        confidence_level = (matching_samples/total_samples)*100

        # Return Confidence level
        return confidence_level, total_samples

    # This function performs a confidence test on seen data
    def getConfidenceSeen(self):
        # Selecting BMU for each sample in Seen test dataset where each neuron is 
        # a cluster of data points
        winner_coordinates = np.array([self.som.winner(x) for x in self.dataSeen]).T

        # Converting winner coordinates to a monodimensional index
        ci = np.ravel_multi_index(winner_coordinates, self.som_shape)

        # Converting cluster_index into a list form for simplicity and processing
        seenPredictions = list(ci)
        
        # Replacing the seen classifications applied to each cluster, which starts 
        # at and index of zero and increased with each subsequent cluster, with the 
        # class label we know it to have. This is done so the reserved class labeled 
        # for the seen data can easily be compared to determin if the predictions 
        # were correct
        for i in range(len(seenPredictions)):
            if seenPredictions[i] == 0:
                seenPredictions[i] = 'benign'
            if seenPredictions[i] == 1:
                seenPredictions[i] = 'malign'

        # Getting total number of samples for use to get confidence percentage
        total_samples = len(seenPredictions)

        # Initialising matching samples variable to count how many samples match 
        # from predictions compared to the class we know them to belong.
        matching_samples = 0

        # Counting the number of matching samples (correct predictions)
        for i in range(len(seenPredictions)):
            if seenPredictions[i] == self.dataSeenClassifications[i]:
                matching_samples = matching_samples + 1

        # Calculating the confidence percentage based on the number of correct 
        # predictions versus the total number of samples
        confidence_level = (matching_samples/total_samples)*100

        # Return Confidence level
        return confidence_level, total_samples

    # Function for plotting and storing SOM clusters
    def plotSOM(self):
        plt.clf() 

        # Plotting the SOM training Data (Clustering Data)
        for c in np.unique(self.cluster_index):
            plt.scatter(self.data[self.cluster_index == c, 0],
                        self.data[self.cluster_index == c, 1],  label='cluster='+str(c), alpha=.7)

        # Plotting centroids of each cluster
        for centroid in self.som.get_weights():
            plt.scatter(centroid[:, 0], centroid[:, 1], marker='.', 
                        s=40, linewidths=15, color='k', label='centroid')

    # # Function for plotting and storing SOM clusters with predictions
    def plotPrediction(self, index):
        pred = self.predUnseen

        if index == 0:
            pred = self.predUnseen[0:1].values
        elif index == 1:
            pred = self.predUnseen[1:2].values
        elif index == 2:
            pred = self.predUnseen[2:3].values
        elif index == 3:
            pred = self.predUnseen[3:4].values
        elif index == 4:
            pred = self.predUnseen[4:5].values
        elif index == 5:
            pred = self.predUnseen[5:6].values

        # Plotting Prediction Data
        predCOORD = np.array(self.som.winner(pred)).T
        ci = np.ravel_multi_index(predCOORD, self.som_shape)

        # Plotting predictions
        for c in np.unique(ci):
            plt.scatter(pred[0,0], pred[0,1], marker='x', 
                        s=15, linewidths=15, color='k', label='Predict: Class ' + str(c))

    # Formates and returns figure to be plotted
    def formatPlot(self):
        # Showing Plots with legends
        plt.legend()
        plt.xlabel('Bare Nucleoli')
        plt.ylabel('Size Uniformity')

        # Store plot in a figure
        fig = plt.gcf()

        # Return figure
        return fig

    # Function for showing SOM clusters plot
    def showPlot(self):
        plt.show()