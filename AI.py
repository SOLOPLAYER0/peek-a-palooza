from urllib.request import urlopen
from flask import Flask, jsonify, request
import numpy as np
import matplotlib.pyplot as mp
import cv2 as cv
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import datasets, layers, models

(training_images, training_labels), (testing_images, testing_labels) = datasets.cifar10.load_data()
training_images, testing_images = training_images/255, testing_images/255

class_names = ['Plane','Car','Bird','Cat','Deer','Dog','Frog','Horse','Ship','Truck']
for i in range(16):
    mp.subplot(4,4,i+1)
    mp.xticks([])
    mp.yticks([])
    mp.imshow(training_images[i], cmap=mp.cm.binary)
    mp.xlabel(class_names[training_labels[i][0]])

#mp.show(block=True)


model = models.Sequential()
model.add(layers.Conv2D(32, (3,3), activation='relu', input_shape=(32,32,3)))
model.add(layers.MaxPooling2D((2,2)))
model.add(layers.Conv2D(64,(3,3), activation='relu'))
model.add(layers.MaxPooling2D((2,2)))
model.add(layers.Conv2D(64,(3,3), activation='relu'))
model.add(layers.Flatten())
model.add(layers.Dense(64, activation = 'relu'))
model.add(layers.Dense(10, activation='softmax'))

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(training_images, training_labels, epochs=10, validation_data=(testing_images, testing_labels))
app = Flask(__name__)
@app.route('/image-uri', methods=['POST'])
def image_uri():
    data = request.get_json()
    uri = data['uri']

    resp = urlopen(uri)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv.imdecode(image, cv.IMREAD_COLOR)
    return 'OK'
app = Flask(__name__)
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()  # get image data from POST request
    img = np.array(data['image'])  # convert list to numpy array
    prediction = model.predict(img.reshape(-1, 32, 32, 3)/255)  # make prediction
    index = np.argmax(prediction)
    return jsonify({'result': class_names[index]})
