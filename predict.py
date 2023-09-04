import pickle
import pandas as pd

modelo = './model/modelo.pkl'

with open(modelo, 'rb') as f:
    classTree = pickle.load(f)

def predict(X_test):
    y = classTree.predict(X_test)
    return y

def doPredict(data_load):

    predictions = './predicted.csv'
    
    for i in data_load.columns:
        data_load[i] = data_load[i].astype('category')

    encoded_data = pd.get_dummies(data_load, drop_first=True)

    predicted_data = pd.DataFrame(data = predict(encoded_data), columns =['Prediction'])
    
    final_data = pd.concat([encoded_data, predicted_data], axis = 1)

    final_data.to_csv(predictions, index = False)
    

