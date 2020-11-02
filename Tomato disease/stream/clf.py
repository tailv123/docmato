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
import tensorflow_hub as hub


# For drawing onto the image.
import numpy as np
from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps

# For measuring the inference time.
import time


####Object detection

module_handle = "https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1" #@param ["https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1", "https://tfhub.dev/google/faster_rcnn/openimages_v4/inception_resnet_v2/1"]

detector = hub.load(module_handle).signatures['default']

def load_img(image):
    img = tf.convert_to_tensor(image, dtype=tf.uint8)

    return img


from skimage.transform import resize    


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
    
model1 = tf.keras.models.load_model('./converted_keras/keras_model.h5')

model = tf.keras.models.load_model('model_best_weights.h5')

def predict(image_data):
    img = load_img(image_data)
    (frame_height, frame_width) = img.shape[:2]
    converted_img  = tf.image.convert_image_dtype(img, tf.float32)[tf.newaxis, ...]
    result = detector(converted_img)
    boxes = result["detection_boxes"]
    scores=result['detection_scores']
    label=result['detection_class_entities']
    if b'Plant'in np.squeeze(label):
        print('appropriate image')
    else:
        label='Your uploaded image is not appropriate. \n Please read how to use to prepare an tomato leaf image'
        return (label)
    
    
    test=cv2.resize(image_data,tuple((224, 224)))/225
    
    result=model1.predict((test)[np.newaxis,...])[0][0]
    
    if result < 0.6:
        label='It look like your uploaded leaf image is not tomato leaf'
        return (label)
    
    img_reshape = convert_image_to_array(image_data)/255

    prediction = model.predict(img_reshape[tf.newaxis,...])
    num_label=np.argmax(prediction,axis=-1)[0]
    label = ''

    if num_label==0:
        label='Your tomato probably are Bacterial spot disease infected'
    elif num_label== 1:
        label='Your tomato probably are Early blight disease infected'
    elif num_label == 2:
        label = 'Your tomato probably are Late blight disease infected'
    elif num_label == 3:
        label = 'Your tomato probably are Leaf Mold disease infected'
    elif num_label == 4:
        label = 'Your tomato probably are Septoria leaf spot disease infected'
    elif num_label == 5:
        label = 'Your tomato probably are Spider mites Two spotted spider mite disease infected'
    elif num_label == 6:
        label = 'Your tomato probably are Target Spot disease infected'
    elif num_label == 7:
        label = 'Your tomato probably are Yellow Leaf Curl Virus infected'
    elif num_label == 8:
        label = 'Your tomato probably are Mosaic virus infected'
    elif num_label == 9:
        label = 'Your tomato probably are Healthy'

    return (label)


