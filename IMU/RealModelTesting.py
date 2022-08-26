
"""
This files is used to test the loading and predict of trained model


"""


import sklearn
import joblib
import pickle
import pandas as pd

filename_jb = 'RFmodel_F2_jb.sav'
filename_jb_p2 = 'RFmodel_F2_jb_p2.sav'

filename_pe = 'RFmodel_F2_pe_p2.sav'


df_test = pd.DataFrame(columns=[])
new_data = {
    'x-acc':-8.827197, 'y-acc':-8.798006, 'z-acc':0.418321,
    'x-aVec':0.430856, 'y-aVec':4.913393, 'z-aVec':4.911049,
    'x-EDeg':-30.002198,'x-EDeg-1':-20.001264,
    'y-EDeg':-60.005930,'y-EDeg-1':-60.010847,
    'z-EDeg':237,'z-EDeg-1':237.1
    }
df_test = df_test.append(new_data, ignore_index=True)
# load the model from disk
try:
    loaded_model_jb = joblib.load(filename_jb_p2)
    loaded_model_jb = joblib.load(filename_jb)
    print("Both Joblib model is loaded successfully.")
except Exception as e:
    print("Joblib model cant be loaded")
    print(e)
    try:
        loaded_model_pe = pickle.load(open(filename_pe, 'rb'))
        print("pickle model is loaded successfully.")
    except Exception as e:
        print("pickle model cant be loaded")
        print(e)

y_pred = loaded_model_jb.predict(df_test)
print('predicted as class:')
print(y_pred)