
from operator import concat
from flask import Flask, jsonify, Response, render_template
from subprocess import Popen, PIPE

app = Flask(__name__)

@app.route('/')
def start():
   return index( )

@app.route('/status')
def status():
    data = {
        'status': 'running',
        'version': '1.0.1'
        }
    return jsonify(data)

@app.route('/index')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'error': 'page not found! Please try again.'}), 404

if __name__ == '__main__':
    app.run(host = "192.168.2.43", debug=True)