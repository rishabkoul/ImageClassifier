# -*- coding: utf-8 -*-
"""

"""

from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import re
import numpy as np

# Keras
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input
import numpy as np

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
#from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)

# Model saved with Keras model.save()
MODEL_PATH = 'model_vgg19.h5'

# Load your trained model
model = load_model(MODEL_PATH)


def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224))
    vechicle = ['bike', 'boat', 'bus', 'car', 'cycle',
                'helicopter', 'plane', 'scooty', 'train', 'truck']

    # Preprocessing the image
    x = image.img_to_array(img)
    # x = np.true_divide(x, 255)
    # Scaling
    # x = x/255
    x = np.expand_dims(x, axis=0)

    # Be careful how your trained model deals with the input
    # otherwise, it won't make correct prediction!
    x = preprocess_input(x)

    preds = model.predict(x)

    top3 = sorted(range(len(preds[0])), key=lambda i: preds[0][i])[-3:]
    top3.reverse()

    sentence = ""
    for i in top3:
        sentence = sentence+str(vechicle[i])+": %"+str(preds[0][i]*100)+"\n"

    return sentence


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)
        return preds
    return None


if __name__ == '__main__':
    app.run(debug=True)
