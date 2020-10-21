import numpy as np

from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.densenet import DenseNet121
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions

DX_Chest = DenseNet121(weights='./DenseNet121-ImageNet.h5')     # Path to model weight file.

def prep(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return x

def predict(img_path, model):
    preds = model.predict(prep(img_path))
    result = decode_predictions(preds, top=1)[0]
    pred = str(result[0][1])
    return pred