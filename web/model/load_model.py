import pickle
from PIL import Image
import PIL.ImageOps 
import numpy as np
import os


directory = os.path.dirname(os.path.abspath(__file__))

def predict_model(data):
    with open(directory+"/"+"model.pickle", 'rb') as f:
        clf_load = pickle.load(f)
    
    return clf_load.predict(data)

def predict_model2(data):
    with open(directory+"/"+"model2.pickle", 'rb') as f:
        clf_load = pickle.load(f)
    
    return clf_load.predict(data)