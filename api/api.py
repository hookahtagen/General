import hashlib
import json
import os
import threading
import time
from flask import Flask, jsonify, Response, render_template, request

app = Flask(__name__)

def check_api_key( ) -> bool:
    if len(request.args) > 0:
        hash_key = os.environ.get('API_KEY_FLASK')
        try:
            api_key = request.args.get('api_key')
        except:
            api_key = request.args.get('api-key')
            
        if api_key == "":
            return False, False
        if api_key in ( "0000" , "1234" ):
            return False, True
        
        api_key_hash = hashlib.sha256( api_key.encode( 'utf-8' ) ).hexdigest( )
        print(api_key)
        if api_key_hash != hash_key:
            return False, False
        
        return True, False
    return False, False

@app.route('/docs')
def docs():
    return jsonify({'message': 'This is the documentation for the api.'})

@app.route('/')
def start():
   return index( )

@app.route('/status')
def status():
    val_bool, mal_bool = check_api_key( )
    if val_bool and not mal_bool:
        uptime = open("/home/hendrik/Documents/General/api/status/uptime.log", "r").read()
        uptime = uptime.replace("up ", "").replace(",", " |"). replace("\n", "")
        
        data = {
            'status': 'gestartet / running',
            'uptime': uptime,
            'version': '1.0.1'
            }
        
        json_data = json.dumps(data, indent = 4)
        return json_data
    else:
        if mal_bool:
            return jsonify({'error': 'Nice try. But nope. Just nope!'}), 403
        return jsonify({'error': 'Invalid api key. Please correct the key and try again.'}), 403

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
    if len(request.args) > 0:
        val_bool, mal_bool = check_api_key( )
        if val_bool:
            time.sleep(5)
            os.system("shutdown -h now")
            os.shutdown(0)
            return jsonify({'status': 'shutting down now...'}), 200
        if mal_bool:
            return jsonify({'error': 'Nice try. But nope. Just nope!'}), 403
        else:
            return jsonify({'error': 'Invalid api key. Please correct the key and try again.'}), 403
    return jsonify({'error': 'You must specify a api key!'}), 403

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
    os.system("vnstat -tr 2 > /home/hendrik/Documents/General/api/status/vnstat.log")
    os.system("uptime -p > /home/hendrik/Documents/General/api/status/uptime.log")
    os.system("df -h > /home/hendrik/Documents/General/api/status/df.log")
    os.system("free -h > /home/hendrik/Documents/General/api/status/free.log")
    os.system("cat /proc/loadavg > /home/hendrik/Documents/General/api/status/loadavg.log")

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
        if i % 2 == 0:
            i = 0
            print("Main loop is running...")
        i += 1
        
        get_system_stats( )
        
        time.sleep(5)

def main():
    # Create two threads
    # Thread 1: Running the flask server
    # Thread 2: Running the main loop
    
    
    
    
    t1 = threading.Thread( target = app.run, kwargs = { 'host': '192.168.2.17' } )
    t1.start( )
    t2 = threading.Thread( target = main_loop )
    t2.start( )
    #app.run(host = "192.168.2.43")


if __name__ == '__main__':
    main( )
    
