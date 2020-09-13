from torchvision import models, transforms
import torch
import numpy as np
import pickle
import cv2
from os import listdir
from sklearn.preprocessing import LabelBinarizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Activation, Flatten, Dropout, Dense
from tensorflow.keras import backend as K
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import img_to_array
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
from pickle import load
import tensorflow as tf



def convert_image_to_array(image_data):
    default_image_size = tuple((256, 256))
    try:
        image = cv2.cvtColor(image_data, cv2.COLOR_RGB2BGR)
        if image is not None :
            image = cv2.resize(image, default_image_size)
            return img_to_array(image)
        else :
            return np.array([])
    except Exception as e:
        print(f"Error : {e}")
        return None


def predict(image_data):
    # resnet = models.resnet101(pretrained=True)
    # lb = load(open('label_transform.pkl', 'rb'))
    model = tf.keras.models.load_model('model_best_weights.h5')

    img_reshape = convert_image_to_array(image_data)/255

    prediction = model.predict(img_reshape[tf.newaxis,...])
    num_label=np.argmax(prediction,axis=-1)[0]
    label=''
    if num_label==0:
        label='Bacterial spot disease infected'
    elif num_label== 1:
        label='Early blight disease infected'
    elif num_label == 2:
        label = 'Late blight disease infected'
    elif num_label == 3:
        label = 'Leaf Mold disease infected'
    elif num_label == 4:
        label = 'Septoria leaf spot disease infected'
    elif num_label == 5:
        label = 'Spider mites Two spotted spider mite disease infected'
    elif num_label == 6:
        label = 'Target Spot disease infected'
    elif num_label == 7:
        label = 'Yellow Leaf Curl Virus infected'
    elif num_label == 8:
        label = 'Mosaic virus infected'
    elif num_label == 9:
        label = 'Healthy'


    return (label)


