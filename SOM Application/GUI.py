#####-----------------------------------Overview-------------------------------------#####

# GUI Program For SOM Visualization & Trailing 
# This Calls On All Previously Established Classes and Integrates Them Into One Seemless 
# GUI Program Using PySimpleGUI For Easy Use
# Nishendran Naiker 2022

#####--------------------------------Imports Section---------------------------------#####

# Base Libraries
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import matplotlib.pyplot as plt
import pandas as pd
import operator
import pyperclip as pc

# My Classes
from SOMClusteringClass import SOMClustering
from OutliersClass import Outliers
from DistributionsClass import Distributions
from TreeDecisionDiagramClass import TreeDecisionDiagram

#####-------------------------------Load Required Data-------------------------------#####

# Retrieving data from csv files. 
# The column names are also applied and the seperator defined
data = pd.read_csv('breast-cancer.csv', 
                    names=['clump_thickness', 'size_uniformity', 'shape_uniformity', 
                    'marginal_adhesion', 'epithelial_size', 'bare_nucleoli', 
                    'bland_chromatin', 'normal_nucleoli', 'mitoses', 'type'], sep=',')

#####----------------------------Load SOMClustering Class----------------------------#####

# See SOMClustering Class and its test file for further details
SOMcl = SOMClustering(data)
SOMcl.dataCleaning()
SOMcl.normalise()
SOMcl.SOMBuilding()
unseenConfidence, unseenSamples = SOMcl.getConfidenceUnseen()
seenConfidence, seenSamples = SOMcl.getConfidenceUnseen()

#####----------------------------Load Distribution Class-----------------------------#####

# See Distribution Class and its test file for further details
Dist = Distributions(data)
Dist.dataCleaning()
Dist.benignDataSplit()
Dist.setFeatureNames()
featureNames = Dist.getFeatureNames()
Dist.calcFeatureStats('clump_thickness')
mean,std = Dist.getBenignStats()
mean,std = Dist.getMalignStats()
diff = Dist.getDifference()

#####-----------------------Load Tree Decision Diagram Class-------------------------#####

# See Tree Decision Tree Class and its test file for further details
TDD = TreeDecisionDiagram(data)
TDD.dataCleaning()
TDD.featureNames()
TDD.dataSelecion()
TDD.formatClassLabels()
TDD.setClassNames()
TDD.trainTestSplit()

#####-------------------------------Load Outlier Class-------------------------------#####

# See Outlier Class and its test file for further details
Out = Outliers(data)
Out.dataCleaning()

#####---------------------------Matplitlib Helper Functions--------------------------#####

# Creating Class To Allow For Toolbar to Be Enabled
class Toolbar(NavigationToolbar2Tk):
    def __init__(self, *args, **kwargs):
        super(Toolbar, self).__init__(*args, **kwargs)

# Funtion to draw figure onto selected canvas
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)

# Funtion to draw figure onto selected canvas with toolbar
def draw_figure_toolbar(canvas, canvas2, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    toolbar = Toolbar(figure_canvas_agg, canvas2)
    toolbar.update()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=2)

# Funtion to clear selected canvas with tool bar
def clear_figure_toolbar(canvas, canvas2):
        if canvas.children:
            for child in canvas.winfo_children():
                child.destroy()
        # if canvas_toolbar has child
        if canvas2.children:
            for child in canvas2.winfo_children():
                child.destroy()

# Funtion to clear selected canvas
def clear_figure(canvas):
        if canvas.children:
            for child in canvas.winfo_children():
                child.destroy()

# Function to Create A Tanle Popup of Inputed Dataser
def tableBuilder(dataframe):
    data = dataframe.values.tolist()    # read everything else into a list of rows
    header_list = [x for x in dataframe.head()]     # Get data headers
    
    # table Layout set using table element
    layout = [
        [sg.Table(values=data,
                  headings=header_list,
                  key='-TABLE-',
                  display_row_numbers=True,
                  auto_size_columns=True,
                  num_rows=min(25, len(data)))]
    ]


    # Initializa Window
    window = sg.Window('Table', layout, grab_anywhere=False, finalize=True)

    # Bind copy function using Ctrl + C keys to window
    window.bind("<Control-C>", "Control-C")
    window.bind("<Control-c>", "Control-C")

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED: 
            break
        if event == "Control-C":
            items = values['-TABLE-']                           # Indexes for selection
            lst = list(map(lambda x:''.join(str(data[x])), items))  # Get data list 
            text = "".join(lst)                 # Each line for one selected row in table
            pc.copy(text)
    window.close()

# Method for Sorting table elements
def sort_table(table, cols):
    for col in reversed(cols):
        try:
            table = sorted(table, key=operator.itemgetter(col))
        except Exception as e:
            sg.popup_error('Error', 'Exception in table', e)
    return table

# Method to enable double clicks on table headers
def double_click(eventDist):
    region = table.identify("region", eventDist.x, eventDist.y)
    if region == 'heading':                                 
        cid = int(table.identify_column(eventDist.x)[1:])-1     
        windowDist.write_event_value("-TABLE-DOUBLE-CLICK-", cid)

#####--------------------------------GUI Code Section--------------------------------#####

# Setting up layout for main window
layoutMain = [
            [sg.Text("Self-Organising Maps", font=('Arial', 22) , justification='centre')],
            [sg.Text("Visualization & Trailing",  font=('Arial', 14), justification='centre')],
            [sg.Text("of",  font=('Arial', 14), justification='centre')],
            [sg.Text("Prediction Data for",  font=('Arial', 14), justification='centre')],
            [sg.Text("Early Disease Detection",  font=('Arial', 14), justification='centre')],
            [sg.Button("Exit", size = (6, 1)), sg.Button("Info", size = (6, 1)), 
            sg.Button("Interactive Tool"), sg.Button("Proceed", size = (6, 1))],
]

# Setting up main page window
windowMain = sg.Window("Main Page", layoutMain, element_justification='c')

# Tracking for Index page's current active state
winowIndex_active=False

# Creating continuous window that will remain open through many reads
while True:
    # Creating event and value variables for main page
    eventMain, valuesMain = windowMain.read()

    # This section checks for specified event occurences
    if eventMain in (sg.WIN_CLOSED, "Exit"):
        break
    
    # Display Info About Application
    if eventMain == "Info":             # Check if Info Button Clicked
        sg.popup("Application Info", "Hello There! This Program is concerned with understanding and" + 
                 " utilizing SOMs", "This software makes use of the Wisconsin Breast Cancer Dataset" + 
                 " in conjunction with SOMs to better", "understand SOM predictive results obtained" + 
                 " in the efforts of the early detection of diseases")
    
    # Display Info About AIVirtual Mouse
    if eventMain == "Interactive Tool": # Check if Interactive Tool Button Clicked
        sg.popup("Virtual Mouse", "Additionally, the use of a virtual mouse programmed using machine" + 
                 " learning in OpenCV", "in order to increase the potental interactive capabilities" + 
                 " of the software\n", "---Instructions For Use---", "1.) Mouse Follows Index Finger",
                 "2.) Index Finger to Thumb Left Clicks", "3.) Middle Finger to Thumb Right Clicks",
                 "4.) Ring Finger to Thumb Holds Down Left Click", "5.) Pinky Releases Left Click Hold")
    
    # Launches Index Page
    if eventMain == "Proceed" and not winowIndex_active:    # Check if Info Button Clicked
        winowIndex_active=True  # Tracking Current Page
        windowMain.Hide()       # Hides Previous Page
        
        # Setting up layout for Index page
        layoutIndex = [
                [sg.Button("1.", size = (3, 1)), sg.Text("SOM Clustering", font=('Arial', 12))],
                [sg.Button("2.", size = (3, 1)), sg.Text("Distributions", font=('Arial', 12))],
                [sg.Button("3.", size = (3, 1)), sg.Text("Tree Decision Diagram", font=('Arial', 12))],
                [sg.Button("Return to Main Page", size = (20, 1))],
        ]

        # Activate Window and its Element
        windowIndex = sg.Window("Index Page", layoutIndex, resizable=False, finalize=True)
        
        # Setting other Windows to False for tracking
        windowSOM_active=False
        windowDist_active=False
        windowTree_active = False

        while True:
            eventIndex, ValuesIndex = windowIndex.read()        # Event Detection and Value retrieval

            # Check if window closed to return user t main page
            if eventIndex == sg.WIN_CLOSED or eventIndex == 'Return to Main Page':
                windowIndex.close()     # Index Window Closed
                winowIndex_active = False   # Som Clustering Window Set to True
                windowMain.UnHide()     # Main Menu set to visable again
                break
            
            # Check if SOM Clustering Page Selected
            if eventIndex == "1." and not windowSOM_active:
                # Set figure Size
                fig = plt.figure(figsize=(9.6, 7.2))

                # Window Tracking
                windowSOM_active=True   # Som Clustering Window Set to True
                windowIndex.Hide()      # Hide Index Window

                # Plotting and Storing SOM Clustering
                SOMcl.plotSOM()
                figSOM = SOMcl.formatPlot()

                # Setting up layout for SOM Clustering Page
                layoutSOM = [
                    [sg.Canvas(key='-TOOLBAR_SOM-')],
                    [sg.Canvas(key='-CANVAS_SOM-')],
                    [sg.Listbox([f'Sample {i+1}' for i in range(6)], size=(17, 2), 
                                enable_events=True, key='-LIST_SOM-'), 
                     sg.Button('Default'), sg.Button('Outliers'), sg.Button('Inputs'), 
                     sg.Button('Dataset'), sg.Button('Confidence'), sg.Button('Close')]]
                
                # Initializing of SOM Clustering window
                windowSOM = sg.Window("SOM Clustering", layoutSOM, auto_size_buttons=True, 
                                      finalize=True)

                # Clearing canvases and redrawing elements to update page elements
                clear_figure_toolbar(windowSOM['-CANVAS_SOM-'].TKCanvas, 
                                     windowSOM['-TOOLBAR_SOM-'].TKCanvas)
                draw_figure_toolbar(windowSOM['-CANVAS_SOM-'].TKCanvas,
                                    windowSOM['-TOOLBAR_SOM-'].TKCanvas, figSOM)

                while True:
                    eventSOM, ValuesSOM = windowSOM.read()  # Event detection and Value retrieval
                    
                    # Reutrns user to Index Page and Closes SOM Clustering Page
                    if eventSOM == sg.WIN_CLOSED or eventSOM == 'Close':
                        windowSOM.close()
                        windowSOM_active = False
                        windowIndex.UnHide()
                        break
                    
                    # Checks if selection on listbox has been made
                    if eventSOM == '-LIST_SOM-':
                        index = 0   # Initialize index value

                        # Change index according to sample selected
                        if ValuesSOM['-LIST_SOM-'] == ['Sample 1']:
                            index = 0
                        elif ValuesSOM['-LIST_SOM-'] == ['Sample 2']:
                            index = 1
                        elif ValuesSOM['-LIST_SOM-'] == ['Sample 3']:
                            index = 2
                        elif ValuesSOM['-LIST_SOM-'] == ['Sample 4']:
                            index = 3
                        elif ValuesSOM['-LIST_SOM-'] == ['Sample 5']:
                            index = 4
                        elif ValuesSOM['-LIST_SOM-'] == ['Sample 6']:
                            index = 5

                        # Replot SOM lustering with Index correlating to a 
                        # input prediction
                        SOMcl.plotSOM()
                        SOMcl.plotPrediction(index)
                        figSOMPrediction = SOMcl.formatPlot()

                        # Clearing canvases and redrawing elements to update page elements
                        clear_figure_toolbar(windowSOM['-CANVAS_SOM-'].TKCanvas, 
                                             windowSOM['-TOOLBAR_SOM-'].TKCanvas)
                        draw_figure_toolbar(windowSOM['-CANVAS_SOM-'].TKCanvas, 
                                            windowSOM['-TOOLBAR_SOM-'].TKCanvas, figSOM)

                    # Replots default SOM Clusters that display when page opened
                    if eventSOM == 'Default':
                        # Plotting SOM and storing in a figure
                        SOMcl.plotSOM()
                        figSOM = SOMcl.formatPlot()

                        # Enable use of list box when defauly plot displayed
                        windowSOM['-LIST_SOM-'].update(disabled=False)

                        # Clearing canvases and redrawing elements to update page elements
                        clear_figure_toolbar(windowSOM['-CANVAS_SOM-'].TKCanvas, 
                                             windowSOM['-TOOLBAR_SOM-'].TKCanvas)
                        draw_figure_toolbar(windowSOM['-CANVAS_SOM-'].TKCanvas, 
                                            windowSOM['-TOOLBAR_SOM-'].TKCanvas, figSOM)

                    # Plots outlies to clusters from SOM
                    if eventSOM == 'Outliers':
                        figSOMOutliers = Out.plotOutliers()

                        # Disables use of list box when defauly plot displayed
                        windowSOM['-LIST_SOM-'].update(disabled=True)

                        # Clearing canvases and redrawing elements to update page elements
                        clear_figure_toolbar(windowSOM['-CANVAS_SOM-'].TKCanvas, 
                                             windowSOM['-TOOLBAR_SOM-'].TKCanvas)
                        draw_figure_toolbar(windowSOM['-CANVAS_SOM-'].TKCanvas, 
                                            windowSOM['-TOOLBAR_SOM-'].TKCanvas, figSOM)

                    # Provides table of inputs and displays all samples when clicked
                    if eventSOM == 'Inputs':
                        # Re-eable use of listbox
                        windowSOM['-LIST_SOM-'].update(disabled=False)

                        # Retrieve stored predictions
                        pred = SOMcl.getPredictioInputs()
                        
                        # Replot SOM
                        SOMcl.plotSOM()

                        # Plot predictions across all stored values of pred
                        for i in range(len(pred)):
                            SOMcl.plotPrediction(i)

                        # Format plot
                        figSOMPrediction = SOMcl.formatPlot()

                        # Clearing canvases and redrawing elements to update page elements
                        clear_figure_toolbar(windowSOM['-CANVAS_SOM-'].TKCanvas, 
                                             windowSOM['-TOOLBAR_SOM-'].TKCanvas)
                        draw_figure_toolbar(windowSOM['-CANVAS_SOM-'].TKCanvas, 
                                            windowSOM['-TOOLBAR_SOM-'].TKCanvas, figSOM)

                        # Use table builder method to create table popup of inputs
                        tableBuilder(pred)

                    if eventSOM == 'Dataset':
                        # Use table builder method to create table popup of dataset use din training
                        tableBuilder(data)

                    # Return Confidence levels in form of accuracy rating for seen and unseen data
                    if eventSOM == 'Confidence':
                        sg.popup("--Confidence Test--", 'Unseen Confidence Test Successfully Performed.' 
                                 + ' Based on a sample size of ' + str(unseenSamples) + ' the some' + 
                                'produced a confidence rating of ' + str(unseenConfidence)+ '%', 
                                'Seen Confidence Test Successfully Performed. Based on a sample size of ' 
                                + str(seenSamples) + ' the some produced a confidence rating of ' + 
                                str(seenConfidence)+ '%')

                # Close window when while loop broken
                windowSOM.close()

            # Launches Distributions Page
            if eventIndex == "2." and not windowDist_active:
                # Set Figure Size
                fig = plt.figure(figsize=(6.4, 4.8))

                # Window Tracking
                windowDist_active=True
                windowIndex.Hide()

                # Plot Distributions
                Dist.plotDistributions('clump_thickness')
                figDist = Dist.formatPlot()

                # Retrieve feature names exluding class labels
                features = [x for x in data.drop('type', axis=1).head()]

                # Getting array values for table building
                distributionHeadings, distributionArray = Dist.getDistArrays(5)
               
               # Setting layout for Distributions page
                layoutDist = [
                    [sg.Listbox(features, size=(17, 28), enable_events=True, key='-LIST-'), 
                     sg.Canvas(key='-CANVAS_Dist-')],
                    [sg.Table(values=distributionArray, headings = distributionHeadings, 
                              max_col_width=15,
                              auto_size_columns=True,
                              display_row_numbers=False,
                              justification='right',
                              num_rows=10,
                              key='-TABLE-',
                              enable_events=True,
                              expand_x=True,
                              expand_y=True,
                              enable_click_events=True,
                             row_height=20)],
                    [sg.Button('Reset Table'), sg.Button('Close')]]
                
                # Initialize Distributions window
                windowDist= sg.Window("Distributions", layoutDist, finalize=True, auto_size_buttons=True, 
                                      resizable=False,  element_justification='center')

                # Bind copt function using CTRL + C to window to copy values of off the table
                windowDist.bind("<Control-C>", "Control-C")
                windowDist.bind("<Control-c>", "Control-C")

                # Bind double click event to table to sort on double click by header
                table = windowDist['-TABLE-'].Widget
                table.bind('<Double-1>', double_click, add='+')
                
                # Clearing canvases and redrawing elements to update page elements
                clear_figure(windowDist['-CANVAS_Dist-'].TKCanvas)
                draw_figure(windowDist['-CANVAS_Dist-'].TKCanvas, figDist)

                while True:
                    eventDist, ValuesDist= windowDist.read()    # Read event and Values from page
                    
                    # Return user to Index page
                    if eventDist == sg.WIN_CLOSED or eventDist == 'Close':
                        windowDist.close()
                        windowDist_active = False
                        windowIndex.UnHide()
                        break
                    
                    # Detects of copy function triggered. then sored item to clipboard
                    if eventDist == "Control-C":
                        items = ValuesDist['-TABLE-']                           
                        lst = list(map(lambda x:''.join(str(distributionArray[x])), items))  
                        text = "".join(lst)                              
                        pc.copy(text)
                    
                    # Checkis if item selected from listbox. Displays corresponding 
                    # bellcurve distribution brapg on adjacent canvas
                    if eventDist== '-LIST-':
                        for i in range(len(features)):
                            if ValuesDist['-LIST-'] == [features[i]]:
                                Dist.plotDistributions(features[i])
                                figDist = Dist.formatPlot()

                        # Clearing canvases and redrawing elements to update page elements
                        clear_figure(windowDist['-CANVAS_Dist-'].TKCanvas)
                        draw_figure(windowDist['-CANVAS_Dist-'].TKCanvas, figDist)

                    # Reset order of table
                    if eventDist == 'Reset Table':
                        tempHeaders, tempArray = Dist.getDistArrays(5)
                        windowDist['-TABLE-'].update(values=tempArray)

                    # Sorts table in decending order of values in table when a header 
                    # is double clicked
                    if eventDist == '-TABLE-DOUBLE-CLICK-':
                        column = ValuesDist[eventDist]
                        if column == 0:
                            temp = distributionArray
                            temp.sort(key=lambda x: x[column])
                            windowDist['-TABLE-'].update(values=temp)
                        else:
                            temp = distributionArray
                            temp.sort(key=lambda x: x[column], reverse=True)
                            windowDist['-TABLE-'].update(values=temp)

                # Close window when while loop broken
                windowDist.close()

            # Launch Distribution Tree Diagram Page
            if eventIndex == "3." and not windowTree_active:
                # Window Tracking
                windowTree_active=True
                windowIndex.Hide()
                
                # Setting layout of Distribution Tree Diagram Page
                layoutTree = [
                    [sg.Canvas(key='-CANVAS_Tree-')],
                    [sg.Text('Tree Layer Depth:'), sg.Slider(range=(1,5), default_value=3, 
                                                             enable_events = True, size=(16, 20), 
                                                             key='-SLIDER-', orientation='horizontal', 
                                                             font=('Helvetica', 12))], 
                    [sg.Button('Text Decision Tree Diagram'), sg.Button('Accuracy'), 
                     sg.Button('Close')]]
                
                # initialize Distribution Tree Diagram Page
                windowTree= sg.Window("Decision Tree Diagram", layoutTree, finalize=True, 
                                      element_justification='center')

                #Building and exaluating tree. See test code and class code for in depth explaination
                TDD.buildTree(3)
                treeAccuracy = TDD.treeEvaluation()
                textTree = TDD.getTextRepresentation()

                # Plotting and formating tree diagram
                TDD.plotTree()
                figTree = TDD.formatPlot()

                # Clearing canvases and redrawing elements to update page elements
                clear_figure(windowTree['-CANVAS_Tree-'].TKCanvas)
                draw_figure(windowTree['-CANVAS_Tree-'].TKCanvas, figTree)
                
                # Initialize variable to track current value of slider page element
                currentValue = 0

                while True:
                    eventTree, ValuesTree= windowTree.read()    # Read event and values on page
                    
                    # Close window and return user to Index Page
                    if eventTree == sg.WIN_CLOSED or eventTree == 'Close':
                        windowTree.close()
                        windowTree_active = False
                        windowIndex.UnHide()
                        break
                    
                    # Check current value of slider and recontruct and plot tree diagram
                    # according to current selected depth using slider
                    if int(ValuesTree['-SLIDER-']) != currentValue-1:
                        # Update value of current value of slider
                        currentValue = int(ValuesTree['-SLIDER-'])

                        # Build and Plot tree
                        TDD.buildTree(currentValue)
                        treeAccuracy = TDD.treeEvaluation()
                        textTree = TDD.getTextRepresentation()
                        TDD.plotTree()
                        figTree = TDD.formatPlot()

                        # Clearing canvases and redrawing elements to update page elements
                        clear_figure(windowTree['-CANVAS_Tree-'].TKCanvas)
                        draw_figure(windowTree['-CANVAS_Tree-'].TKCanvas, figTree)
                
                    # Update slider element to current value
                    windowTree['-SLIDER-'].update(currentValue)
                    
                    # Created popup of text representation of tree diagram
                    if eventTree == 'Text Decision Tree Diagram':
                        sg.popup(textTree, title='Text Tree')

                    # Evaluestes current tree model based on the current depth
                    if eventTree == 'Accuracy':
                        sg.popup('Tree Model Successfully Evaluated. The Tree Model Has An Accuracy of ' 
                                 + str(round(treeAccuracy, 1)) + '%')
                
                # Close Tree window when while loop broken
                windowTree.close()

# Close Main Window when loop broken
windowMain.close()

