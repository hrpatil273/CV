from flask import Flask, render_template, request

from creating_2d_animation import save_animation

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('form.html')


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
