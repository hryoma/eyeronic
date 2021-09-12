from flask import Flask, render_template, request, send_file
from flask_dropzone import Dropzone
from flask_uploads import UploadSet, configure_uploads, IMAGES

import os
import zipfile
import io
import pathlib
import shutil

import facedetect
import tensorflow as tf
import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import dropout, fully_connected
from tflearn.layers.estimator import regression
import numpy as np
from PIL import Image
from skimage import transform

app = Flask(__name__)
dropzone = Dropzone(app)

# Dropzone settings
app.config['DROPZONE_UPLOAD_MULTIPLE'] = True
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image/*'
app.config['DROPZONE_REDIRECT_VIEW'] = 'download'

# Uploads settings
photos = UploadSet("photos", IMAGES)
app.config["UPLOADED_PHOTOS_DEST"] = "album"
app.config["SECRET_KEY"] = os.urandom(24)
configure_uploads(app, photos)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        for f in request.files:
            file = request.files.get(f)
            photos.save(file, name=file.filename)

        return "uploading"

    return render_template('index.html')


@app.route('/download')
def download():
    album_path = pathlib.Path('album')

    # set up eyes directory
    eyes_path = pathlib.Path('eyes')
    if not (os.path.exists('eyes') and os.path.isdir('eyes')):
        os.mkdir('eyes')

    data = io.BytesIO()

    # set up DNN
    tf.compat.v1.reset_default_graph()
    convnet = tflearn.input_data(shape=[None, 50, 50, 1], name='input')

    convnet = conv_2d(convnet, 32, 5, activation='relu')
    convnet = max_pool_2d(convnet, 5)

    convnet = conv_2d(convnet, 64, 5, activation='relu')
    convnet = max_pool_2d(convnet, 5)

    convnet = conv_2d(convnet, 128, 5, activation='relu')
    convnet = max_pool_2d(convnet, 5)

    convnet = conv_2d(convnet, 64, 5, activation='relu')
    convnet = max_pool_2d(convnet, 5)

    convnet = conv_2d(convnet, 32, 5, activation='relu')
    convnet = max_pool_2d(convnet, 5)

    convnet = fully_connected(convnet, 1024, activation='relu')
    convnet = dropout(convnet, 0.8)

    convnet = fully_connected(convnet, 2, activation='softmax')
    convnet = regression(convnet, optimizer='adam', learning_rate=1e-3,
                         loss='categorical_crossentropy', name='targets')

    model = tflearn.DNN(convnet, tensorboard_dir='log')
    model.load('EyeDet.h5')

    # process each input image
    for ind, filepath in enumerate(album_path.iterdir()):
        facedetect.find_eyes(str(filepath))

    for image_dir in eyes_path.iterdir():
        keep_img = False
        print('img dir: ', str(image_dir))

        # process each eye for the input image
        for eyes_path in image_dir.iterdir():
            eyes_img = Image.open(str(eyes_path))
            eyes_img = np.array(eyes_img).astype('float32') / 255
            eyes_img = transform.resize(eyes_img, (50, 50, 1))
            eyes_img = np.expand_dims(eyes_img, axis=0)

            prediction = model.predict(eyes_img)[0]
            if prediction[0] > prediction[1]:
                # opened - keeping looking for a closed eye
                continue
            else:
                # closed - can put image in output
                keep_img = True
                break

        # remove the image with only open eyes from the album
        if not keep_img:
            image_name = str(image_dir).split('/')[1]
            os.remove('album/' + image_name)  # todo: figure out the right path

    with zipfile.ZipFile(data, mode='w') as zip_output:
        for file_path in album_path.iterdir():
            zip_output.write(file_path)
    data.seek(0)

    # clean up - delete all images
    shutil.rmtree('album')
    shutil.rmtree('eyes')

    return send_file(
        data,
        mimetype='application/zip',
        as_attachment=True,
        attachment_filename='album.zip'
    )
