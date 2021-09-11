from flask import Flask, render_template, request, send_file
from flask_dropzone import Dropzone
from flask_uploads import UploadSet, configure_uploads, IMAGES

import os
import zipfile
import io
import pathlib

import facedetect
import tflearn
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
app.config["UPLOADED_PHOTOS_DEST"] = "inputs"
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
    inputs_path = pathlib.Path('inputs')
    data = io.BytesIO()

    with zipfile.ZipFile(data, mode='w') as zip_output:
        for file_path in inputs_path.iterdir():
            facedetect.find_eyes(str(file_path))
            zip_output.write(file_path)
    data.seek(0)

    convnet = tflearn.input_data(shape=[None, 50, 50, 1], name='input')
    model = tflearn.DNN(convnet)
    model.load('EyeDet.h5')

    eyes_path = pathlib.Path('eyes')
    for file_path in eyes_path.iterdir():
        print(str(file_path))

        def load(filename):
            np_image = Image.open(filename)
            np_image = np.array(np_image).astype('float32') / 255
            np_image = transform.resize(np_image, (50, 50, 1))
            np_image = np.expand_dims(np_image, axis=0)
            return np_image

        image = load(str(file_path))
        print(model.predict(image))

    return send_file(
        data,
        mimetype='application/zip',
        as_attachment=True,
        attachment_filename='album.zip'
    )
