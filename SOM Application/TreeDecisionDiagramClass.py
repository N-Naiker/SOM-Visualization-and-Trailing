# TreeDecisionDiagram Class 
# Cleans Data, Bulids Tree Model & Displays Tree Decision Diagram
# Additionally, Returns The Test Representation of The Tree Diagram
# Nishendran Naiker 2022

# Imports
from matplotlib import pyplot as plt

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn import tree

# Tree Diagram Class
class TreeDecisionDiagram:
    # Initializing class variables for use between methods in class
    global feature_names
    global X
    global Y
    global le
    global class_names
    global X_train
    global X_test
    global Y_train
    global Y_test 
    global tree_classifier

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

    # This function  is used to retrieve the feature names of the data
    def featureNames(self):
        # This retrieves the feature names frome the clolumn names from the dataset.
        # Note that if the feature names are not present but know, the can be manually 
        # anotated in the form of ['feature 1', ..., 'feature N']
        self.feature_names = list(self.data.columns[0:9])

    # This function selects the X and Y data to be used from the dataset
    def dataSelecion(self):
        # Setting X to equal the feature values
        self.X = self.data[self.feature_names]

        # Setting Y to equal the class label values
        self.Y = self.data['type']

    # This function formates the class labels present in the dataset as they are of type 
    # string and not numerical. Thus, they are encoded
    def formatClassLabels(self):
        # Establishing label encoder and fitting it to data of variable Y
        self.le = LabelEncoder()
        self.le.fit(self.Y)

        # Using lable encoder to transform data of variable Y into normalised encoding 
        # and reassigning it to variable Y
        self.Y = self.le.transform(self.Y)

    # This function stores the class names from encoder
    def setClassNames(self):
        self.class_names = list(self.le.classes_)

    # This function splits the dataset into training and testing data
    def trainTestSplit(self):
        self.X_train, self.X_test, self.Y_train, self.Y_test = train_test_split(self.X, self.Y, test_size=0.2, random_state=42)

    # This function creates and trains the tree model
    def buildTree(self, depth):
        # Using sklearn's DecisionTreeClassifier to train and fir tree model
        self.tree_classifier = DecisionTreeClassifier(max_depth=depth)
        self.tree_classifier.fit(self.X, self.Y)



    # This function evaluates the tree model
    def treeEvaluation(self):
        # Making predictions using test data split
        predictionY = self.tree_classifier.predict(self.X_test)

        # Calculating accuracy of predictions by comparing the results to 
        # the test data splits known classifications
        accuracy = accuracy_score(self.Y_test, predictionY)*100

        # Returning the accuracy of the tree model
        return accuracy

    # This function gets the text representation of the tree model
    def getTextRepresentation(self):
        # Establishing text Tree Decision Diagram using sklearn inbuilt 
        # method of tree and its method export_text(tree_model)
        text_tree = tree.export_text(self.tree_classifier,
                                     feature_names=self.feature_names)

        # Returning the text representation of the tree model
        return text_tree

    # This function plots the tree model graphically
    def plotTree(self):
        # Using Pyplot to set figure size for displaying tree diagram
        plt.figure(figsize=(12,6))

        # Using Sklearn's Tree child class to plot the tree using the 
        # datasets provided information through the use of the plot_tree 
        # method
        _ = tree.plot_tree(self.tree_classifier, 
                   feature_names=self.feature_names,  
                   class_names=self.class_names,
                   impurity=False,
                   filled=True)
        
    # Stores and returns figure to be plotted
    def formatPlot(self):
        # Store plot in a figure
        fig = plt.gcf()

        # Return figure
        return fig
    
    # This function displays the tree model
    def displayTree(self):
        # Showing plot
        plt.show()
