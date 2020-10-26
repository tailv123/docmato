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

# For downloading the image.
import matplotlib.pyplot as plt
import tempfile # Generate temporary files and directories
from six.moves.urllib.request import urlopen #https://docs.python.org/3/library/urllib.request.html
from six import BytesIO

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

def display_image(image):
    fig = plt.figure(figsize=(20, 15))
    plt.grid(False)
    plt.imshow(image)


def download_and_resize_image(url, new_width=256, new_height=256,
                              display=False):
    _, filename = tempfile.mkstemp(suffix=".jpg")
    response = urlopen(url)
    image_data = response.read()
    image_data = BytesIO(image_data)
    pil_image = Image.open(image_data)
    pil_image = ImageOps.fit(pil_image, (new_width, new_height), Image.ANTIALIAS)
    pil_image_rgb = pil_image.convert("RGB")
    pil_image_rgb.save(filename, format="JPEG", quality=90)
    print("Image downloaded to %s." % filename)
    if display:
        display_image(pil_image)
    return filename


def draw_bounding_box_on_image(image,
                               ymin,
                               xmin,
                               ymax,
                               xmax,
                               color,
                               font,
                               thickness=4,
                               display_str_list=()):
    draw = ImageDraw.Draw(image)
    im_width, im_height = image.size
    (left, right, top, bottom) = (xmin * im_width, xmax * im_width,
                                ymin * im_height, ymax * im_height)
    draw.line([(left, top), (left, bottom), (right, bottom), (right, top),
             (left, top)],
            width=thickness,
            fill=color)

    # If the total height of the display strings added to the top of the bounding
    # box exceeds the top of the image, stack the strings below the bounding box
    # instead of above.
    display_str_heights = [font.getsize(ds)[1] for ds in display_str_list]
    # Each display_str has a top and bottom margin of 0.05x.
    total_display_str_height = (1 + 2 * 0.05) * sum(display_str_heights)

    if top > total_display_str_height:
        text_bottom = top
    else:
        text_bottom = top + total_display_str_height
    # Reverse list and print from bottom to top.
    for display_str in display_str_list[::-1]:
        text_width, text_height = font.getsize(display_str)
        margin = np.ceil(0.05 * text_height)
        draw.rectangle([(left, text_bottom - text_height - 2 * margin),
                        (left + text_width, text_bottom)],
                       fill=color)
        draw.text((left + margin, text_bottom - text_height - margin),
                  display_str,
                  fill="black",
                  font=font)
        text_bottom -= text_height - 2 * margin


def draw_boxes(image, boxes, class_names, scores, max_boxes=10, min_score=0.1):
    colors = list(ImageColor.colormap.values())

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Regular.ttf",
                          25)
    except IOError:
        print("Font not found, using default font.")
        font = ImageFont.load_default()

    for i in range(min(boxes.shape[0], max_boxes)):
        if scores[i] >= min_score:
            ymin, xmin, ymax, xmax = tuple(boxes[i])
            display_str = "{}: {}%".format(class_names[i].decode("ascii"),
                                         int(100 * scores[i]))
            color = colors[hash(class_names[i]) % len(colors)]
            image_pil = Image.fromarray(np.uint8(image)).convert("RGB")
            draw_bounding_box_on_image(
              image_pil,
              ymin,
              xmin,
              ymax,
              xmax,
              color,
              font,
              display_str_list=[display_str])
            np.copyto(image, np.array(image_pil))
            return image


#####

module_handle = "https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1" #@param ["https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1", "https://tfhub.dev/google/faster_rcnn/openimages_v4/inception_resnet_v2/1"]

detector = hub.load(module_handle).signatures['default']

def load_img(image):
    img = tf.convert_to_tensor(image, dtype=tf.uint8)
#     img = tf.image.decode_jpeg(img, channels=3) #Decode a JPEG-encoded image to a uint8 tensor.
    return img


from skimage.transform import resize    
    ###################

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

def predict(image_data,model):
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


