import pickle

modelo = '/model/modelo.pkl'

with open(modelo, 'rb') as f:
    classTree = pickle.load(f)

def predict(X_test):
    y = classTree.predict(X_test)