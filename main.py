import moviepy.editor as mv
from flask import Flask, render_template, request, flash, redirect, url_for, abort, send_from_directory, session  # noqa : E501
from werkzeug.exceptions import RequestEntityTooLarge
from random import choices
from string import ascii_uppercase, digits
from zipfile import ZipFile
import os
from math import floor
from flask_session import Session
from flask_apscheduler import APScheduler
from time import time

# TODO 2: Refactor The Code


class Config:
    SCHEDULER_API_ENABLED = True


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
app.secret_key = "hsfvdsbrfgi67548hfjbg478gfbhe"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.config.from_object(Config())
scheduler = APScheduler()


UPLOAD_FOLDER = "uploads"
DOWNLOAD_FOLDER = "downloads"
SESSION_FOLDER = "flask_session"


@scheduler.task('interval', id='do_job_1', seconds=1800,
                misfire_grace_time=3600)
def every_half_an_hour():
    if os.path.isdir(DOWNLOAD_FOLDER) and os.path.isdir(SESSION_FOLDER):
        print("Deletion Performed")
        now = time()
        for f in os.listdir(DOWNLOAD_FOLDER):
            f = os.path.join(DOWNLOAD_FOLDER, f)
            if os.stat(f).st_mtime < now - 1800:
                os.remove(f)

        for f in os.listdir(SESSION_FOLDER):
            f = os.path.join(SESSION_FOLDER, f)
            if os.stat(f).st_mtime < now - 1800:
                os.remove(f)


scheduler.start()


def trim_video(filename):
    try:

        K = 12  # TODO 1: K will be passed with function.
        file_path = os.path.join(
            UPLOAD_FOLDER, filename).replace("\\", "/")
        vedio_clip = mv.VideoFileClip(file_path)

        all_paths = []
        limit = floor(vedio_clip.duration) // K

        for i in range(0, limit):
            sub_clip = vedio_clip.subclip(i, K * (i+1))
            all_paths.append(DOWNLOAD_FOLDER + "/" + f"{i}_" + filename)
            sub_clip.write_videofile(all_paths[-1])

        i += 1

        if floor(vedio_clip.duration) % K > 5:
            sub_clip = vedio_clip.subclip(
                K*i, (K*i) + int(vedio_clip.duration) % K)
            all_paths.append(DOWNLOAD_FOLDER + "/" + f"{i}_" + filename)
            sub_clip.write_videofile(all_paths[-1])

        with ZipFile(DOWNLOAD_FOLDER + "/" +
                     filename.replace(".mp4", ".zip"), 'w') as zip:
            # writing each file one by one
            for file in all_paths:
                zip.write(file)

        for file in all_paths:
            os.remove(file)
        os.remove(file_path)

        session['output_file_name'] = DOWNLOAD_FOLDER + \
            "/" + filename.replace(".mp4", ".zip")

    except OSError:
        flash("There seems to be an error. Please upload the File Again.")
        return


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

        # check if the post request has the file part
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
            trim_video(filename)
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
