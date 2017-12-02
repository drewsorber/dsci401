#Assignment #3
#DSCI401B
#William (Greg) Phillips
#Working State

import pandas as pd
import pprint
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn import neighbors
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import confusion_matrix

# -------------------------------------- #
# --- Section 0: Meta Data & Caveats --- #
# -------------------------------------- #

# ----------------------------------------------------------- #
# --- Section 1: Load in Data and drop what we don't need --- #
# ----------------------------------------------------------- #

#data for building the model
churn_data = pd.read_csv('./data/churn_data.csv');
#CustID won't be needed; its a primary or unique identifier with no bearing on the outcome
churn_data = churn_data.drop('CustID', axis = 1); 
#data for validing the predictions
churn_vald = pd.read_csv('./data/churn_validation.csv');
#CustID won't be needed; its a primary or unique identifier with no bearing on the soutcome
churn_vald = churn_vald.drop('CustID', axis = 1); 

# ----------------------------------------------- #
# --- Section 2: Define some utility functions --- #
# ----------------------------------------------- #

# Get a list of the categorical features for a given dataframe.
def cat_features(dataframe):
	td = pd.DataFrame({'a':[1,2,3], 'b':[1.0, 2.0, 3.0]})
	return filter(lambda x: not(dataframe[x].dtype in [td['a'].dtype, td['b'].dtype]), list(dataframe))

# Get the indices of the categorical features for a given dataframe.
def cat_feature_inds(dataframe):
	td = pd.DataFrame({'a':[1,2,3], 'b':[1.0, 2.0, 3.0]})
	enums = zip(list(dataframe), range(len(list(dataframe))))
	selected = filter(lambda (name, ind): not(dataframe[name].dtype in [td['a'].dtype, td['b'].dtype]), enums)
	return map(lambda (x, y): y, selected);

#Function pulls out each column where there is a missing value
#returns a list of column names
def missing_cols(df):
	a = [col for col in df.columns if df[col].isnull().any()]
	return a;

#Function checks to see if there are missing values within the dataframe
#If true, prints number of missing values, then calls missing_cols to 
#list rows with missing values
def check_missing_data(df):
	b = df.isnull().any().any();
	if(b):
		print('No of missing vals: ' + str(df.isnull().sum().sum()));
		a = missing_cols(df); 
		print('Cols without values: ' + str(a)); 
	return b;

#Function moves specified column to a specified index
def move_to_index(df, colName, index=0):
	cols = list(df); 
	cols.insert(index, cols.pop(cols.index(colName)));
	df = df.ix[:, cols]; 
	return df; 

#Function shows the DataFrame name
def show_name(df):
	name = [x for x in globals() if globals()[x] is df][0]; 
	print("DataFrame Name is: %s" %name); 

# -------------------------------------- #
# --- Section 3: Data transformation --- #
# -------------------------------------- #

#move Churn to the 0 index in housebild
#becaue I'm picky about locations
churn_data = move_to_index(churn_data, 'Churn'); 
#let's do the same for the validation data
churn_vald = move_to_index(churn_vald, 'Churn'); 

#let's check to see if there's missing data
#take a look at the test data
b1 = check_missing_data(churn_data); 
if(b1):
	print('Found Missing Data'); 
	show_name(churn_data); 
	print('\n');
else:
	print('No Missing Data!');
	show_name(churn_data); 
	print('\n');

#take a look at the validation data
b2 = check_missing_data(churn_vald); 
if(b2):
	print('Found Missing Data');
	show_name(churn_vald);  
	print('\n');
else:
	print('No Missing Data!');
	show_name(churn_vald);
	print('\n'); 

#transform the dfs to a one-hot encoding
churn_data = pd.get_dummies(churn_data, columns=cat_features(churn_data));
churn_vald = pd.get_dummies(churn_vald, columns=cat_features(churn_vald));

# ------------------------------------ #
# --- Section 4: Split up the Data --- #
# ------------------------------------ #

#much easier after rearranging

#independent / (predictor/ explanatory) variables
churn_data_x = churn_data[list(churn_data)[1:]];
churn_vald_x = churn_vald[list(churn_vald)[1:]];

#dependent/ response variable (in this case 'Churn')
churn_data_y = churn_data[list(churn_data)[0]];
churn_vald_y = churn_vald[list(churn_vald)[0]];

#split training and test sets from main data
x_train_data, x_test_data, y_train_data, y_test_data = train_test_split(churn_data_x, churn_data_y, 
	test_size = 0.2, random_state = 4);

#split training and test sets from main data
x_train_vald, x_test_vald, y_train_vald, y_test_vald = train_test_split(churn_vald_y, churn_vald_y, 
	test_size = 0.2, random_state = 4); 

# --------------------------------------- #
# --- Section 5: K-Nearest Evaluation --- #
# --------------------------------------- #

print('end\n');