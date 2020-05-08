import numpy as np
import os
from flask import Flask, flash, request, redirect, url_for
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

def predict(fileloc):
    im = convert_image_to_array(sys.argv[1])
    np_image_li = np.array(im, dtype=np.float16) / 225.0
    npp_image = np.expand_dims(np_image_li, axis=0)
    result=model_disease.predict(npp_image)
    itemindex = np.where(result==np.max(result))
    return ("probability:"+str(np.max(result))+" Disease: "+classess[itemindex[1][0]])

UPLOAD_FOLDER = '/root/tysis-backend/public/images'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return (UPLOAD_FOLDER+filename)

# start flask app
app.run(host="127.0.0.1", port=5000)