from flask import Flask, render_template, request, flash, redirect, url_for, abort, send_from_directory, session  # noqa : E501
from werkzeug.exceptions import RequestEntityTooLarge
from random import choices
from string import ascii_uppercase, digits
import os
from flask_session import Session
from trimmer import trim_video
from scheduler import scheduler
from constants import UPLOAD_FOLDER


class Config:
    SCHEDULER_API_ENABLED = True


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
app.secret_key = "hsfvdsbrfgi67548hfjbg478gfbhe"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.config.from_object(Config())

scheduler.start()


def allowed_file(filename):
    file_format = filename.split(".")[1]
    if file_format == "mp4":
        return True
    return False


@app.route("/")
def home():
    return render_template('index.html')


@app.route('/upload')
def upload():
    return render_template('upload.html')


@app.route("/process", methods=['GET', 'POST'])
def process():

    if request.method == 'POST':

        # check if the size of the file is within limit
        try:
            if 'file' not in request.files:
                flash('No file part')
                return redirect(url_for('home'))
            file = request.files['file']
        except RequestEntityTooLarge:
            flash("Too Large")
            return redirect(url_for('home'))

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No File Selected')
            return redirect(url_for('home'))

        # if file exists and the format is mp4 then firstly we secure
        # the filename. Then save the file to upload folder
        if file and allowed_file(file.filename):
            # filename = secure_filename(file.filename)

            filename = ''.join(choices(ascii_uppercase + digits, k=15))
            filename = filename + ".mp4"

            file_path = os.path.join(
                UPLOAD_FOLDER, filename).replace("\\", "/")

            file.save(file_path)
            session['output_file_name'] = trim_video(filename)
            return redirect(url_for('complete'))

        flash("The File Format Must be Mp4")
        return redirect(url_for('home'))


@app.route("/download")
def download():
    output_file_name = session.get('output_file_name')
    try:
        return send_from_directory(
            directory="./",
            path=output_file_name,
            as_attachment=False,
        )
    except FileNotFoundError:
        return abort(404)


@app.route('/complete')
def complete():
    return render_template('complete.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
