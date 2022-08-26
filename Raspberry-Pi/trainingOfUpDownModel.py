import pandas as pd
# Test 1
#df_test1 = pd.read_csv('data/IMU-2021-11-29_7 test1.csv', index_col=0)
#df_test1_A2 = pd.read_csv('data/IMU-2021-11-29_11 test1-2.csv', index_col=0)

# Test 2
#df_test2_All = pd.read_csv('data/IMU-2021-11-29_8 test2-1.csv', index_col=0)
df_test2_UpdownOnly = pd.read_csv('data/IMU-2021-11-29_9 test2-2.csv', index_col=0)
df_test2_All_A2 = pd.read_csv('data/IMU-2021-11-29_13 test2-1-2.csv', index_col=0)
df_test2_UpdownOnly_A2 = pd.read_csv('data/IMU-2021-11-29_14 test2-2-2.csv', index_col=0)

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
        df = df[df['class2'].notna()]
        df_merged = df_merged.append(df)
    return df_merged

def prevToCurrent(df):
    cols_in_df = list(df.columns)
    new_df = pd.DataFrame()

    for i in range(1, len(df)):
        for col in cols_in_df:
            new_df.loc[i, col] = df.loc[i, col]
            new_df.loc[i, col+'-1'] = df.loc[i-1, col]

    try: 
        new_df = new_df.drop(columns=['class2-1'])
    except KeyError:
        print("KeyError: There is no class-1 and drop skipped")    
    return new_df

from sklearn.metrics import classification_report, f1_score, accuracy_score, recall_score, precision_score
def Metrics(y_test, pred):
    precision_ma = precision_score(y_test, pred, average='macro')
    recall_ma = recall_score(y_test, pred, average='macro')
    f1 = f1_score(y_test, pred, average='macro')
    print('Precision: '+str(precision_ma)+'\nRecall score:'+str(recall_ma)+'\nF1 score: '+str(f1))
    print(classification_report(y_test, pred))

df_collections_ToUse = [df_test2_All_A2, df_test2_UpdownOnly, df_test2_UpdownOnly_A2, df_test3, df_test4]

df_collections_F1 = []
for i in range(len(df_collections_ToUse)):
    print('Handling: '+str(i))
    new_df = prevToCurrent(df_collections_ToUse[i])
    df_collections_F1.append(new_df)
    print('Index: '+str(i)+' is finished')


colsToDrop = ['x-magnetField', 'y-magnetField', 'z-magnetField', 'datetime']
colsToDrop2 = colsToDrop + ['x-magnetField-1', 'y-magnetField-1', 'z-magnetField-1', 'datetime-1', 'class', 'class-1', 'Unnamed: 15', 'Unnamed: 15-1']
for i in range(len(df_collections_F1)):
    for col in colsToDrop2:
        try:
            df_collections_F1[i] = df_collections_F1[i].drop(columns=[col])
        except KeyError:
            continue

print("After dropping magneticfield, class etc")
for df in df_collections_F1:
    printDFShape(df)

new_features_name2 = ['x-acc-1','y-acc-1','z-acc-1','x-aVec-1','y-aVec-1','z-aVec-1']
for i in range(len(df_collections_F1)):
    df_collections_F1[i] = df_collections_F1[i].drop(columns=new_features_name2)


print("After dropping acc's and aVec's -1")
for df in df_collections_F1:
    printDFShape(df)

from sklearn.ensemble import RandomForestClassifier
RFClassifer = RandomForestClassifier(n_estimators=5, random_state=0)
df_in = dfMerger(df_collections_F1)
#print(df_in)
X = df_in.drop(columns=['class2'])
y = df_in['class2']
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
RFClassifer.fit(X_train, y_train)
pred = RFClassifer.predict(X_test)
Metrics(y_test, pred)

print(df_in.head())
# Train model with all data
RFClassifer.fit(X, y)
print("Model is trained.")

# Export the model
import joblib
joblib.dump(RFClassifer, "RFupdownModel_F2_jb.sav")
joblib.dump(RFClassifer, "RFupdownModel_F2_jb_p2.sav", protocol=2)
print("Model is saved.")