import moviepy.editor as mv
from zipfile import ZipFile
import os
from math import floor

UPLOAD_FOLDER = "uploads"
DOWNLOAD_FOLDER = "downloads"
TEMPORARY_FOLDER = "temp"


def trim_video(filename):
    try:
        K = 12  # K will be passed with function in the original program
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

        return DOWNLOAD_FOLDER + "/" + filename

    except OSError:
        print("There seems to be an error. Please upload the File Again.")
        return ""


output = trim_video("1.mp4").replace(".mp4", ".zip")
os.rename(output,
          output.replace(
              DOWNLOAD_FOLDER, TEMPORARY_FOLDER))
# shutil.move(output,
#             output.replace(
#                 DOWNLOAD_FOLDER, TEMPORARY_FOLDER))
