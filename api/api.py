
from operator import concat
from flask import Flask, jsonify, Response, render_template
from subprocess import Popen, PIPE

app = Flask(__name__)

@app.route('/')
def index():
    # Read menu file to display
    # This method of creating was chosen to keep the code
    # clean an simple
    menu = [ ]
    with open('/home/hendrik/Documents/General/api//menu.txt', 'r') as f:
        for line in f:
            menu.append(line)
            
    return Response(menu, mimetype='text/plain')

@app.route('/status')
def status():
    data = {
        'status': 'running',
        'version': '1.0.1'
        }
    return jsonify(data)

@app.route('/index')
def test_page():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'error': 'page not found! Please try again.'}), 404

if __name__ == '__main__':
    app.run(debug=True)