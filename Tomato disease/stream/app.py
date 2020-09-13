import streamlit as st
from PIL import Image
from clf import predict
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

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.set_option('deprecation.showfileUploaderEncoding', False)

st.write(" Welcome to Indentification website. At first let me to tell you how to use it")

file_up = st.file_uploader("Upload an image", type=["jpg",'png','jpeg'])
if file_up is not None:
    image = Image.open(file_up,)
    img_array = np.array(image)
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    st.write("")
    st.write("Please wait...")
    labels = predict(img_array)

    # print out the top 5 prediction labels with scores
    st.write("Your tomato probably are", labels)
