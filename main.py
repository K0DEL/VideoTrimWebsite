import moviepy.editor as mv
from flask import Flask, render_template, request, flash, redirect, url_for, abort, send_from_directory  # noqa : E501
# from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
# from functools import wraps
from random import choices
from string import ascii_uppercase, digits
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
app.secret_key = "hsfvdsbrfgi67548hfjbg478gfbhe"
UPLOAD_FOLDER = "./uploads"


def trim_video(file_path):
    vedio_clip = mv.VideoFileClip(file_path)
    print(vedio_clip.duration)
    sub_clip = vedio_clip.subclip(0, 15)
    output_file_name = "output_1.mp4"
    sub_clip.write_videofile(UPLOAD_FOLDER + "/" + output_file_name)
    return output_file_name

# def file_uploaded(function):
#     @wraps(function)
#     def decorated_function(*args, **kwargs):
#         if args[0] == False:
#             return abort(403)
#         return function(*args, **kwargs)
#     return decorated_function


def allowed_file(filename):
    file_format = filename.split(".")[1]
    if file_format == "mp4":
        return True
    return False


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/upload", methods=['GET', 'POST'])
def upload():

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

            filename = ''.join(choices(ascii_uppercase + digits, k=10))
            filename = filename + ".mp4"

            file_path = os.path.join(
                UPLOAD_FOLDER, filename).replace("\\", "/")
            file.save(file_path)
            return redirect(url_for('download', file_name=filename))
        flash("The File Format Must be Mp4")
        return redirect(url_for('home'))


@app.route("/download")
def download():
    filename = request.args.get('file_name')
    if filename is None:
        return abort(404)
    file_path = os.path.join(
        UPLOAD_FOLDER, filename).replace("\\", "/")
    output_file_name = trim_video(file_path)
    return send_from_directory(
        directory="uploads",
        path=output_file_name,
        as_attachment=False,
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
