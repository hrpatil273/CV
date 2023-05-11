from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

from creating_2d_animation import save_animation
import os

from video_processor import annotate_video

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/'
app.config['PROCESSED_FOLDER'] = 'static/'
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def home():
    return render_template('form.html')


@app.route('/process')
def process():
    return render_template('process.html')


@app.route('/processing', methods=['POST'])
def processing():
    # Handle video file upload
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    filename = ""
    file_path = ""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # code for uploading the files under upload folder
        # file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # file.save(file_path)

    video_name = filename
    output_path = 'labeled_' + video_name

    ## change the video name accordingly to process the file
    labeled_video_path = annotate_video(video_name, app.config['PROCESSED_FOLDER']+output_path)

    return render_template('output.html', file_url=video_name)


@app.route('/submit', methods=['POST'])
def submit():
    gameplay = request.form['gameplay']
    position = request.form['position']
    jersey = request.form['jersey']

    if len(position) == 0:
        position_values = None
    elif position != 'All':
        position_values = position.split(' ')
    else:
        position_values = position

    if len(jersey) == 0:
        jersey_values = None
    elif jersey != 'All':
        jersey_values = jersey.split(' ')
    else:
        jersey_values = jersey

    # Call your function here with the submitted values
    file_url = save_animation(gameplay, position=position_values, jersey=jersey_values)

    return render_template('result.html', gameplay=gameplay, file_url=file_url, position=position_values, jersey=jersey_values)


if __name__ == '__main__':
    app.run(debug=True)
