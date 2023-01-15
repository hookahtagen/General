import hashlib
import os
import threading
import time
from flask import Flask, jsonify, Response, render_template, request


app = Flask(__name__)

@app.route('/')
def start():
   return index( )

@app.route('/status')
def status():
    data = {
        'status': 'gestartet / running',
        'version': '1.0.1'
        }
    return jsonify(data)

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/shutdown')
def shutdown_server():
    hash_key = os.environ.get('API_KEY_FLASK')
    if len(request.args) > 0:
        if request.args.get('api-key') == "" or request.args.get('api_key') == "":
            return jsonify({'error': 'API Key is missing! Please try again.'}), 401
        if ( request.args.get( 'api-key' ) or request.args.get( 'api_key' ) ) in ( "0000" , "1234" ):
            return jsonify({'error': 'Nice try. But nope. Just nope.'}), 401
        
        try:
            api_key_hash = hashlib.sha256(request.args.get('api_key').encode()).hexdigest()
        except:
            api_key_hash = hashlib.sha256(request.args.get('api-key').encode()).hexdigest()
            
        if api_key_hash != hash_key:
            print(api_key_hash)
            return jsonify({'error': 'invalid API Key! Please try again.'}), 401
        
        time.sleep(5)
        os.system("shutdown -h now")
        os.shutdown(0)
        return jsonify({'status': 'shutting down now...'}), 200
    else:
        return jsonify({'error': 'API Key is missing! Please try again.'}), 401

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'error': 'page not found! Please try again.'}), 404



def main():
    # Create two threads
    # Thread 1: Running the flask server
    # Thread 2: Running the main loop
    
    
    # Start the flask server
    app.run(host = "192.168.2.43", debug=True)


if __name__ == '__main__':
    main()
    