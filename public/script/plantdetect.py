import numpy as np
import os
from flask import Flask, flash, request, redirect, url_for, json, jsonify
from werkzeug.utils import secure_filename
import pickle5 as pickle
import cv2
import sys
from keras.models import load_model
from keras.preprocessing import image
from keras.preprocessing.image import img_to_array

default_image_size = tuple((256, 256))

model_disease=load_model("cnn_model.h5")
loaded_model = pickle.load(open('cnn_model.pkl', 'rb'))
model_disease=loaded_model

def convert_image_to_array(image_dir):
    try:
        image = cv2.imread(image_dir)
        if image is not None :
            image = cv2.resize(image, default_image_size)   
            return img_to_array(image)
        else :
            return np.array([])
    except Exception as e:
        print(f"Error : {e}")
        return None

classess = np.array(['Pepper__bell___Bacterial_spot', 'Pepper__bell___healthy',
 'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy',
 'Tomato_Bacterial_spot', 'Tomato_Early_blight', 'Tomato_Late_blight',
 'Tomato_Leaf_Mold', 'Tomato_Septoria_leaf_spot',
 'Tomato_Spider_mites_Two_spotted_spider_mite', 'Tomato__Target_Spot',
 'Tomato__Tomato_YellowLeaf__Curl_Virus', 'Tomato__Tomato_mosaic_virus',
 'Tomato_healthy'])
def predict(files):
    im = convert_image_to_array(files)
    np_image_li = np.array(im, dtype=np.float16) / 225.0
    npp_image = np.expand_dims(np_image_li, axis=0)
    result=model_disease.predict(npp_image)
    itemindex = np.where(result==np.max(result))
    return ("probability:"+str(np.max(result))+" Disease: "+classess[itemindex[1][0]])

app = Flask(__name__)
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        #file = request.files['image']
        #if file:
        f = open('1.jpg','r')
        msg = (predict(f))
        return jsonify(
            message=msg
        )


app.run(host="0.0.0.0", port=5000)