############################################################
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import export_graphviz
import pydot
import matplotlib.pyplot as plt
import datetime
import datetime as dt

df = pd.read_csv("/Users/Ivan/Desktop/UBIQUM/NobismProject/NobismProject/Code/data/machine-learning_user36.csv")

############################################################
# EXPLORATIVE ANALYSIS:

df.shape
df.ndim

df.head()
df.tail()

df.dtypes

df.describe()

list(df.columns)

#################
# Symptomes df:
df_sy = df[df["Group"] == "sy"]
df_sy

df_sy.shape
df_sy.ndim

df_sy.head()
df_sy.tail()

df_sy.dtypes

df_sy.describe()

df_sy['Date_Hour'] = dt.datetime.combine(df_sy['Date/Time'], df_sy.Hour)

#################
# Medicine df:
df_me = df[df['Group'] == 'me']
df_me

df_me.shape
df_me.ndim

df_me.head()
df_me.tail()

df_me.dtypes

df_me.describe()

list(df.columns)

############################################################
# PREPROCESSING ON SYMPTOMES DF:

list(df_sy.columns)
list(df_me.columns)

# Deleting empty/unnecessery columns (Symptomes df):
del df_sy['Blood pressure (high)']  #only if there is no data
del df_sy['Blood pressure (low)']   #only if there is no data
del df_sy['Unnamed: 0.1']
del df_sy['Unnamed: 0.1.1']
del df_sy['Unnamed: 0.1.1.1']
del df_sy['Unnamed: 0.1.1.1.1']
del df_sy['Description']
del df_sy['Quantity'] 
del df_sy['Type']
del df_sy['Unit']
del df_sy['Last Modified']
del df_sy['Group']
del df_sy['Name']
del df_sy['Id']
del df_sy['Date/Time']
del df_sy['Date']
del df_sy['date']
del df_sy['Time']

# Deleting empty/unnecessery columns (Med df):
del df_me['Blood pressure (high)']  #only if there is no data
del df_me['Blood pressure (low)']   #only if there is no data
del df_me['Unnamed: 0.1']
del df_me['Unnamed: 0.1.1']
del df_me['Unnamed: 0.1.1.1']
del df_me['Unnamed: 0.1.1.1.1']
del df_me['Description']
del df_me['Quantity'] 
del df_me['Type']
del df_me['Unit']
del df_me['Last Modified']
del df_me['Group']
del df_me['Name']
del df_me['Id']
del df_me['Date/Time']
del df_me['Date']
del df_me['date']
del df_me['Time']
del df_me['Duration']
del df_me['Intensity']


df_sy = df_sy.rename(columns = {'Unnamed: 0': 'Index'})
df_me = df_me.rename(columns = {'Unnamed: 0': 'Index'})

remaining_columns = list(df_sy.columns)
remaining_columns

remaining_columns_me = list(df_me.columns)
remaining_columns_me

df_sy.dtypes
df_sy

# Removing NA:
df_sy.Intensity.isna().sum() #how many NA in Intensity column

# NAN in df_sy:
for column in remaining_columns:
    print("###############")
    print("Column %s has %d missing values." % (column, df_sy[column].isna().sum()))
    print(np.where(df_sy[column].isna())) 
    
# NAN in df_me:
for column in remaining_columns_me:
    print("###############")
    print("Column %s has %d missing values." % (column, df_me[column].isna().sum()))
    print(np.where(df_me[column].isna())) 

#removing rows with intensity value missing:
df_sy = df_sy.drop(df_sy.index[[117,  435, 1409, 1901, 1939, 1962, 1966, 2149, 2401, 2549, 2553]])

# replacing NAN in duration by the mean of the column:
df_sy = df_sy.fillna(df_sy.mean())

# Dummifying tag column in df_sy:
dummy_names = pd.get_dummies(df_sy['Tag'])
dummy_names.head()
dummy_names

# Dummifying tag column in df_me:
dummy_names_me = pd.get_dummies(df_me['Tag'])
dummy_names_me.head()
dummy_names_me

del df_sy['Tag']
del df_me['Tag']

# add dummified variables to the df_sy:
df_sy = pd.concat([df_sy, dummy_names], axis = 1)
df_sy
del df_sy['n']
list(df_sy.columns)

# add dummified variables to the df_me:
df_me = pd.concat([df_me, dummy_names_me], axis = 1)
df_me
list(df_me.columns)

#NAN check df_sy:
remaining_columns = list(df_sy.columns)
for column in remaining_columns:
    print("###############")
    print("Column %s has %d missing values." % (column, df_sy[column].isna().sum()))
    print(np.where(df_sy[column].isna())) 
    
############################################################
df_sy.Date   
df_sy_date_hour = df_sy.groupby(['Date', 'hour'])    
#df_sy_date_hour.describe()
    
    
############################################################
# TRAIN / TEST DATA:
    
y = df_sy.Intensity
x = df_sy.drop('Intensity', axis = 1)
x = x.drop('Index', axis = 1)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2)
x_train.head()

feature_list = list(x.columns)
features = np.array(x)
############################################################
# RANDOM FOREST:

rf = RandomForestRegressor(n_estimators = 1000, random_state = 42) #rf init

rf.fit(x_train, y_train)

# Use the forest's predict method on the test data
predictions = rf.predict(x_test)

# Calculate the absolute errors
errors = abs(predictions - y_test)
print('Mean Absolute Error:', round(np.mean(errors), 2))

# Calculate mean absolute percentage error (MAPE)
mape = 100 * (errors / y_test)

# Calculate and display accuracy
accuracy = 100 - np.mean(mape)
print('Accuracy:', round(accuracy, 2), '%.')

############################################################
# MODEL VISUALISATION:

# Pull out one tree from the forest
tree = rf.estimators_[5]

# Export the image to a dot file
export_graphviz(tree, out_file = 'tree.dot', feature_names = feature_list, rounded = True, precision = 1)

# Use dot file to create a graph
(graph, ) = pydot.graph_from_dot_file('tree.dot')

# Write graph to a png file
graph.write_png('tree.png')

# Limit depth of tree to 3 levels
rf_small = RandomForestRegressor(n_estimators=10, max_depth = 3)
rf_small.fit(x_train, y_train)

# Extract the small tree
tree_small = rf_small.estimators_[5]

# Save the tree as a png image
export_graphviz(tree_small, out_file = 'small_tree.dot', feature_names = feature_list, rounded = True, precision = 1)
(graph, ) = pydot.graph_from_dot_file('small_tree.dot')
graph.write_png('small_tree.png') #small decision tree to see the relationships
  

# VARIABLE IMPORTANCE:
# Get numerical feature importances
importances = list(rf.feature_importances_)

# List of tuples with variable and importance
feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(feature_list, importances)]

# Sort the feature importances by most important first
feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)

# Print out the feature and importances 
[print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importances]; #remove features with 0 importance

# UPDATED RF MODEL USING ONLY THE MOST IMPORTANT FEATURES:
# New random forest with only  most important variables
rf_most_important = RandomForestRegressor(n_estimators= 1000, random_state=42)

# Extract the most important features
important_indices = [feature_list.index('Duration'), feature_list.index('day'),
                     feature_list.index('hour'), feature_list.index('month'),
                     feature_list.index('year'), feature_list.index('14sy'),
                     feature_list.index('33sy'), feature_list.index('38sy'),
                     feature_list.index('42sy'), feature_list.index('55sy'),
                     feature_list.index('75sy'), feature_list.index('75sy'),
                     feature_list.index('89sy')]



train_important = x_train.iloc[:, important_indices] 

test_important = x_test.iloc[:, important_indices] 

# Train the random forest
rf_most_important.fit(train_important, y_train)

# Make predictions and determine the error
predictions = rf_most_important.predict(test_important)
errors = abs(predictions - y_test)

# Display the performance metrics
print('Mean Absolute Error:', round(np.mean(errors), 2))
mape = np.mean(100 * (errors / y_test))
accuracy = 100 - mape
print('Accuracy:', round(accuracy, 2), '%.')

############################################################
# VISUALISATIONS:

%matplotlib inline

# Set the style
plt.style.use('fivethirtyeight')

####### RUN AS ONE BLOCK #######
# list of x locations for plotting
x_values = list(range(len(importances)))

# Make a bar chart of predictor variables:
plt.bar(x_values, importances, orientation = 'vertical')

# Tick labels for x axis
plt.xticks(x_values, feature_list, rotation='vertical')

# Axis labels and title
plt.ylabel('Importance'); plt.xlabel('Variable'); plt.title('Variable Importances');
####### END OF THE BLOCK #######

######################

# Dates of training values
months = features[:, feature_list.index('month')]
days = features[:, feature_list.index('day')]
years = features[:, feature_list.index('year')]

# List and then convert to datetime object
dates = [str(int(year)) + '-' + str(int(month)) + '-' + str(int(day)) for year, month, day in zip(years, months, days)]
dates = [datetime.datetime.strptime(date, '%Y-%m-%d') for date in dates]

# Dataframe with true values and dates
true_data = pd.DataFrame(data = {'date': dates, 'actual': y})

# Dates of predictions
months = x_test.iloc[:, feature_list.index('month')]
days = x_test.iloc[:, feature_list.index('day')]
years = x_test.iloc[:, feature_list.index('year')]

# Column of dates
test_dates = [str(int(year)) + '-' + str(int(month)) + '-' + str(int(day)) for year, month, day in zip(years, months, days)]

# Convert to datetime objects
test_dates = [datetime.datetime.strptime(date, '%Y-%m-%d') for date in test_dates]

# Dataframe with predictions and dates
predictions_data = pd.DataFrame(data = {'date': test_dates, 'prediction': predictions})

####### RUN AS ONE BLOCK #######
# Plot the actual values
plt.plot(true_data['date'], true_data['actual'], 'b-', label = 'actual')

# Plot the predicted values
plt.plot(predictions_data['date'], predictions_data['prediction'], 'ro', label = 'prediction')
plt.xticks(rotation = '60'); 
plt.legend()

# Graph labels
plt.xlabel('Date'); plt.ylabel('Maximum Temperature (F)'); plt.title('Actual and Predicted Values');
####### END OF THE BLOCK #######
