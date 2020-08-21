from keras import Model
from keras.applications.vgg16 import VGG16
import numpy as np
from keras.layers import Dropout, Flatten, Dense
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.vgg16 import preprocess_input
import os,sys

class VggModel:

    model = None
    img_width, img_height = 210, 210
    # TODO
    # Change labels to match with DB
    label_map = {'bench': 0, 'butterfly': 1, 'cycle': 2, 'legpress': 3, 'row': 4, 'treadmill': 5}


    def __init__(self):
        vgg_model = VGG16(weights='imagenet', include_top=False, input_shape=(210, 210, 3))
        for layer in vgg_model.layers:
            layer.trainable = False
        x = Flatten()(vgg_model.output)
        x = Dense(256, activation='relu')(x)
        x = Dropout(0.5)(x)
        x = Dense(6, activation='softmax')(x)
        self.model = Model(inputs=vgg_model.inputs, outputs=x)
        self.model.load_weights('./classifier/model.58-0.91.h5')  # swap out weights
        self.model.compile(loss='categorical_crossentropy',
                           optimizer='rmsprop',
                           metrics=['accuracy'])

    def predict(self, img):
        imag = load_img(img, target_size=(210, 210))
        x = img_to_array(imag)
        image = np.expand_dims((x.astype('float32')), axis=0)
        image = preprocess_input(image)
        image = image / 255
        preds = self.model.predict(image)
        y_classes = preds.argmax(axis=-1)
        labels = dict((v, k) for k, v in self.label_map.items())
        # print(labels[y_classes[0]])
        # print(preds)
        return labels[y_classes[0]]



