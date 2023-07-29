from flask import Flask
app = Flask(__name__)

@app.route('/')
def main_page():
    return 'TODO'


@app.route('/debate')
def debate():
    return 'TODO'


@app.route('/save_debate')
def save_debate():
    return 'TODO'
