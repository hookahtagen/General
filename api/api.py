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
    '''
        Exaplanation:
            This function is called when the user tries to access the index page.
            It returns a 200 status code and a message.
        Parameters:
            None
        Returns:
            A 200 status code and a message
    '''
    return render_template('index.html')

@app.route('/shutdown')
def shutdown_server():
    '''
        Exaplanation:
            This function is called when the user tries to access the shutdown page.
            It returns a 200 status code and a message.
        Parameters:
            None
        Returns:
            A 200 status code and a message
    '''
    hash_key = os.environ.get('API_KEY_FLASK')
    if len(request.args) > 0:
        if request.args.get('api-key') == "" or request.args.get('api_key') == "":
            return jsonify({'error': 'API Key is missing! Please try again.'}), 401
        if ( request.args.get( 'api-key' ) or request.args.get( 'api_key' ) ) in ( "0000" , "1234" ):
            return jsonify({'error': 'Nice try. But nope. Just nope.'}), 401
        
        try:
            api_key_hash = get_hash(request.args.get('api_key'))
        except:
            api_key_hash = get_hash(request.args.get('api-key'))
            
        if api_key_hash != hash_key:
            print(api_key_hash)
            return jsonify({'error': 'invalid API Key! Please try again.'}), 401
        
        time.sleep(5)
        os.system("shutdown -h now")
        os.shutdown(0)
        return jsonify({'status': 'shutting down now...'}), 200
    else:
        return jsonify({'error': 'API Key is missing! Please try again.'}), 401

@app.route('/message')
def message_system():
    '''
        Exaplanation:
            This function is called when the user tries to access the message page.
            This page is used to send a message to the user at the pc. Mainly used for my parents.
        Parameters:
            None
        Returns:
            A 200 status code and a message
    '''
    a=1

@app.errorhandler(404)
def page_not_found(e):
    '''
        Exaplanation:
            This function is called when the user tries to access a page that does not exist.
            It returns a 404 error code and a message.
        Parameters:
            e: The error message
        Returns:
            A 404 error code and a message
    '''
    return jsonify({'error': 'page not found! Please try again.'}), 404

def get_hash( api_key: str ) -> str:
    '''
        Explanation:
            This function is used to hash the api key.
        Parameters:
            api_key: The api key that needs to be hashed.
        Returns:
            The hashed api key.
    '''
    return hashlib.sha256( api_key.encode( 'utf-8' ) ).hexdigest( )

def get_system_stats():
    '''
        Exaplanation:
            This function is used to get the system stats.
            It is used for various tasks, such as checking the status of the system.
        Parameters:
            None
        Returns:
            None
    '''
    pass

def main_loop():
    '''
        Exaplanation:
            This function is for handling most of the logic of the program.
            It is used for various tasks, such as checking the status of the system.
        Parameters:
            None
        Returns:
            None
    '''
    i=0
    while True:
        if i % 8 == 0:
            i = 0
            print("Main loop is running...")
        i += 1
        
        get_system_stats( )
        
        time.sleep(1.25)

def main():
    # Create two threads
    # Thread 1: Running the flask server
    # Thread 2: Running the main loop
    
    
    # Start the flask server
    t1 = threading.Thread( target = app.run, kwargs = { 'host': '192.168.2.43' } )
    t1.start( )
    t2 = threading.Thread( target = main_loop )
    t2.start( )
    #app.run(host = "192.168.2.43")


if __name__ == '__main__':
    main( )
    
