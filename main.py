import moviepy.editor as mv
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
app.secret_key = "hsfvdsbrfgi67548hfjbg478gfbhe"
UPLOAD_FOLDER = "C:\\Users\\Keshav\\Documents\\CP\\python\\trim\\uploads"

# loading video dsa gfg intro video
vedio_clip = mv.VideoFileClip("1.mp4")

# cutting out some part from the clip
# sub_clip = vedio_clip.subclip(0, 15)

# showing  clip
# sub_clip.write_videofile("output_1.mp4")


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
            print("Too Large")
            return redirect(url_for('home'))
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('home'))

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for('home'))
        print('NO')
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
