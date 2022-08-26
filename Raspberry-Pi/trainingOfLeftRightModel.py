# This file is used to train the model in python 2.7 in raspberry pi
# the processed dataframe (df_in) will be saved and you may run trainingOfLeftRightModel.py
# to save processing time and train another model

import pandas as pd
# Test 1
df_test1 = pd.read_csv('data/IMU-2021-11-29_7 test1.csv', index_col=0)
df_test1_A2 = pd.read_csv('data/IMU-2021-11-29_11 test1-2.csv', index_col=0)

# Test 2
df_test2_All = pd.read_csv('data/IMU-2021-11-29_8 test2-1.csv', index_col=0)
#df_test2_UpdownOnly = pd.read_csv('data/IMU-2021-11-29_9 test2-2.csv', index_col=0)
df_test2_All_A2 = pd.read_csv('data/IMU-2021-11-29_13 test2-1-2.csv', index_col=0)
#df_test2_UpdownOnly_A2 = pd.read_csv('data/IMU-2021-11-29_14 test2-2-2.csv', index_col=0)

# Test 3 & 4
df_test3 = pd.read_csv('data/IMU-2021-11-29_15 test3(1).csv', index_col=0)
df_test4 = pd.read_csv('data/IMU-2021-11-29_17 test4.csv', index_col=0)

def printDFShape(df):
    if type(df) is list:
        for x in df:
            print('shape of df: '+str(df.shape))
    else:
        print('shape of df: '+str(df.shape))

def dfMerger(dfs):
    df_merged = pd.DataFrame()
    for df in dfs:
        df = df[df['class'].notna()]
        df_merged = df_merged.append(df)
    return df_merged

def prevToCurrent(df):
    cols_in_df = list(df.columns)
    new_df = pd.DataFrame()

    for i in range(1, len(df)):
        for col in cols_in_df:
            new_df.loc[i, col] = df.loc[i, col]
            new_df.loc[i, col+'-1'] = df.loc[i-1, col]
    for i in range(len(df)-1):
        new_df.loc[i, 'class+1'] = df.loc[i+1, 'class']
    #new_df = new_df.drop(columns=['class-1']) # Drop previous class
    return new_df

from sklearn.metrics import classification_report, f1_score, accuracy_score, recall_score, precision_score
def Metrics(y_test, pred):
    precision_ma = precision_score(y_test, pred, average='macro')
    recall_ma = recall_score(y_test, pred, average='macro')
    f1 = f1_score(y_test, pred, average='macro')
    print('Precision: '+str(precision_ma)+'\nRecall score:'+str(recall_ma)+'\nF1 score: '+str(f1))
    print(classification_report(y_test, pred))

df_collections_ToUse = [df_test1, df_test1_A2, df_test2_All, df_test2_All_A2, df_test3, df_test4]

df_collections_F1 = []
for i in range(len(df_collections_ToUse)):
    print('handling:'+str(i))
    new_df = prevToCurrent(df_collections_ToUse[i])
    df_collections_F1.append(new_df)
    print('index:'+str(i)+' is finished')


colsToDrop = ['x-magnetField', 'y-magnetField', 'z-magnetField', 'datetime']
colsToDrop2 = colsToDrop + ['x-magnetField-1', 'y-magnetField-1', 'z-magnetField-1', 'datetime-1', 'class2', 'class2-1', 'class-1','class-1','Unnamed: 15', 'Unnamed: 15-1']
for i in range(len(df_collections_F1)):
    for col in colsToDrop2:
        try:
            df_collections_F1[i] = df_collections_F1[i].drop(columns=[col])
        except KeyError:
            continue

print("After dropping magneticfield, class2, etc.")
for df in df_collections_F1:
    printDFShape(df)

new_features_name2 = ['x-acc-1','y-acc-1','z-acc-1','x-aVec-1','y-aVec-1','z-aVec-1']
for i in range(len(df_collections_F1)):
    df_collections_F1[i] = df_collections_F1[i].dropna().drop(columns=new_features_name2)


print("After dropping acc's and aVec's -1")
for df in df_collections_F1:
    printDFShape(df)

from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
RFClassifer = RandomForestClassifier(n_estimators=5, random_state=0)
DTClassifer = DecisionTreeClassifier(random_state=0, max_depth=3)
df_in = dfMerger(df_collections_F1)
#print(df_in)
df_in.to_csv("data/df_in.csv", index=False)
X = df_in.drop(columns=['class','class+1'])
y = df_in['class+1']
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
RFClassifer.fit(X_train, y_train)
DTClassifer.fit(X_train, y_train)
pred = RFClassifer.predict(X_test)
pred_DT = DTClassifer.predict(X_test)
print("RandomForestClassifier:")
Metrics(y_test, pred)
print("DecisionTreeClassifier:")
Metrics(y_test, pred_DT)




# Train model with all data
RFClassifer.fit(X, y)
DTClassifer.fit(X, y)
print("Model is trained.")


import joblib
# F2: predict current, F3 predict future
joblib.dump(RFClassifer, "RFmodel_F3_jb_03-21-22.sav")
joblib.dump(DTClassifer, "DTmodel_F3_jb_03-28-22.sav")
print("Model is saved.")
