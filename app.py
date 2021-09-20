# Author      : Ethan Rietz
# Date        : 2021-09-19
# Description : A photo gallery Flask web app 

"""
To run on the local network, set the host to 0.0.0.0 by running
    python app.py /path/to/photos --listen=0.0.0.0

Note that this should be with care if the debugger is enabled
"""

from flask import Flask, render_template, send_from_directory, request, redirect
from pathlib import Path
import argparse
from PIL import Image, ExifTags
from PIL.ExifTags import TAGS

app = Flask("Flask Image Gallery")

#-------------------------------------------------------------------------------
# Route Handling
#-------------------------------------------------------------------------------

@app.route("/", methods=["GET"])
def home():
    if len(request.args) < 2:
        start = 0
        stop = 10
    else:
        start = int(request.args.get("start"))
        stop = int(request.args.get("stop"))

    images = app.config["IMAGE_PATHS"][start:stop]

    image_data = []
    for image in images:
        data = {}
        data['path'] = str(image)
        data['caption'] = image.name
        image_data.append(data)

    return render_template("index.html", image_data=image_data)

@app.route("/photos/<path:filepath>")
def get_photo(filepath):
    dir = Path(filepath).parent
    filename = Path(filepath).name
    return send_from_directory("/" + str(dir), str(filename), as_attachment=False)

@app.route("/preview/<path:filepath>")
def preview_image(filepath):
    file = Path(filepath)
    dir = file.parent
    filename = file.name

    image = Image.open('/' + filepath)
    exifdata = image.getexif()
    metadata = {}
    for tag_id in exifdata:
        # get the tag name, instead of human unreadable tag id
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        # decode bytes 
        if isinstance(data, bytes):
            try:
                data = data.decode()
            except UnicodeDecodeError:
                data = "COULD NOT DECODE THIS"
        metadata[tag] = data

    return render_template("preview.html", path=filepath, caption=filename, metadata=metadata)

@app.route('/next/<path:filepath>')
def next_image(filepath):
    index = app.config['IMAGE_PATHS'].index(Path('/') / filepath)
    if index is None:
        return 'Error: path does not exist'
    else:
        next_path = app.config['IMAGE_PATHS'][index + 1]
        return redirect(f'/preview/{next_path}')

@app.route('/previous/<path:filepath>')
def previous_image(filepath):
    index = app.config['IMAGE_PATHS'].index(Path('/') / filepath)
    if index is None:
        return 'Error: path does not exist'
    else:
        previous_path = app.config['IMAGE_PATHS'][index - 1]
        return redirect(f'/preview/{previous_path}')

#-------------------------------------------------------------------------------
# Main Function
#-------------------------------------------------------------------------------
def parse_arguments():
    parser = argparse.ArgumentParser("Usage: %prog [options]")

    parser.add_argument("root_dir", help="Gallery root directory path")

    parser.add_argument(
            "-l",
            "--listen",
            dest="host",
            default="127.0.0.1",
            help="address to listen on [127.0.0.1]"
            )

    parser.add_argument(
            "-p",
            "--port",
            metavar="PORT",
            dest="port",
            type=int,
            default=5000,
            help="port to listen on [5000]"
            )

    args = parser.parse_args()
    return args

def main():
    args = parse_arguments()

    app.config["IMAGE_EXTS"] = [".png", ".jpg", ".jpeg", ".gif", ".tiff", ".JPG"]
    app.config["ROOT_DIR"] = args.root_dir

    app.config["IMAGE_PATHS"] = []
    root_dir = Path(app.config["ROOT_DIR"])
    for file in root_dir.glob("**/*"):
        if file.suffix in app.config["IMAGE_EXTS"]:
            app.config["IMAGE_PATHS"].append(file)

    app.run(host=args.host, port=args.port, debug=True)

if __name__=="__main__":
    main()
