from flask import Flask, render_template, request, send_file
from flask_dropzone import Dropzone
from flask_uploads import UploadSet, configure_uploads, IMAGES

import os
import zipfile
import io
import pathlib

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
    base_path = pathlib.Path('inputs')
    data = io.BytesIO()
    with zipfile.ZipFile(data, mode='w') as zip_output:
        for file_name in base_path.iterdir():
            zip_output.write(file_name)
    data.seek(0)

    return send_file(
        data,
        mimetype='application/zip',
        as_attachment=True,
        attachment_filename='album.zip'
    )
