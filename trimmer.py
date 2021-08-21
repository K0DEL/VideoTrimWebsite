import moviepy.editor as mv
from flask import flash
from zipfile import ZipFile
import os
from math import floor
from pathlib import Path
from constants import DOWNLOAD_FOLDER, UPLOAD_FOLDER


def trim_video(filename):
    try:

        Path(DOWNLOAD_FOLDER).mkdir(parents=True, exist_ok=True)
        K = 12  # TODO 1: K will be passed with function.
        file_path = os.path.join(
            UPLOAD_FOLDER, filename).replace("\\", "/")
        video_clip = mv.VideoFileClip(file_path)

        all_paths = []
        limit = floor(video_clip.duration) // K

        for i in range(0, limit):
            sub_clip = video_clip.subclip(i, K * (i+1))
            all_paths.append(DOWNLOAD_FOLDER + "/" + f"{i}_" + filename)
            sub_clip.write_videofile(all_paths[-1])

        i += 1

        if floor(video_clip.duration) % K > 5:
            sub_clip = video_clip.subclip(
                K*i, (K*i) + int(video_clip.duration) % K)
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

        return DOWNLOAD_FOLDER + \
            "/" + filename.replace(".mp4", ".zip")

    except OSError:
        flash("There seems to be an error. Please upload the File Again.")
        return
