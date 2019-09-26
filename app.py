import os
# Import fast.ai Library
from fastai import *
from fastai.vision import *
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
import sys
import os
import glob
import re
from pathlib import Path

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

path = Path().cwd() / 'path' / 'models'
learner = load_learner(path, 'cancer.pkl')


@app.route('/', methods=['GET', 'POST'])
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
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Skin cancer classifier</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename) # Image is uploaded
    print(filename)
    print(full_filename)
    # Make prediction
    img = open_image(filename)
    cancer = learner.predict(img)
    return render_template('index.html', cancer_type = cancer)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

'''
@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    image = request.form['pic']
    print(type(image))
    print(image)
    return render_template('imageView.html', image = image)
'''

if __name__ == '__main__':
    app.run()
