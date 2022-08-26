import pandas as pd

df_in = pd.read_csv('data/df_in.csv', index_col=False)

print(df_in.shape)

from sklearn.metrics import classification_report, f1_score, accuracy_score, recall_score, precision_score
def Metrics(y_test, pred):
	accuracy_ma = accuracy_score(y_test, pred)
	precision_ma = precision_score(y_test, pred, average='macro')
	recall_ma = recall_score(y_test, pred, average='macro')
	f1 = f1_score(y_test, pred, average='macro')
	print('Precision: '+str(precision_ma)+'\nRecall score:'+str(recall_ma)+'\nF1 score: '+str(f1)+'\nAccuracy score: '+str(accuracy_ma))
	print(classification_report(y_test, pred))



#exit()
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
RFClassifer = RandomForestClassifier(n_estimators=5, random_state=0)
DTClassifer = DecisionTreeClassifier(random_state=0, max_depth=3)
#print(df_in)
X = df_in.drop(columns=['class','class+1'])
y = df_in['class+1']
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
RFClassifer.fit(X_train, y_train)
DTClassifer.fit(X_train, y_train)
pred = RFClassifer.predict(X_test)
pred_DT = DTClassifer.predict(X_test)
Metrics(y_test, pred)
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