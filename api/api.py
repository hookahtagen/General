from datetime import datetime
import hashlib
import json
import os
import sqlite3 as s
import time
import threading

from flask import Flask, jsonify, Response, render_template, request

app = Flask(__name__)
lock = threading.Lock( )

def clear_screen( ):
    '''
        Explanation:
            Clears the console screen.
        Parameters:
            None
        Returns:
            None
    '''
    os.system( 'clear' )

def check_api_key( ) -> bool:
    if len(request.headers) > 0:
        hash_key = os.environ.get('API_KEY_FLASK')
        if request.headers.get('api_key') != None:
            api_key = request.headers.get('api_key')
        if request.headers.get('api-key') != None:
            api_key = request.headers.get('api-key')
        if request.args.get('api_key') != None:
            api_key = request.args.get('api_key')
        if request.args.get('api-key') != None:
            api_key = request.args.get('api-key')
            
        if api_key == "":
            return False, False
        if api_key in ( "0000" , "1234" ):
            return False, True
        
        print(f'api_key: {api_key}')
        api_key_hash = hashlib.sha256( api_key.encode( 'utf-8' ) ).hexdigest( )
        print(api_key)
        print("TEST")
        if api_key_hash != hash_key:
            return False, False
        
        return True, False
    return False, False

def print_console( message ):
    '''
        Explanation:
            Prints a message to the console in a nice format.
        Parameters:
            message: str - The message to print to the console.
        Returns:
            None
    '''
    print('\n****************************\n')
    print( message )
    print('\n****************************\n')

def send_notification( message ):
    '''
        Explanation:
            Sends a notification to the user, that a new message has been received.
        Parameters:
            message: str - The message to send to the user.
        Returns:
            None
    '''
    DURATION = 5000
    
    # send a notiffy-send notification, that a new message has been received
    os.system( f'notify-send -t { DURATION } "New message received ( c2 )" "{ message }"' )

def get_db_connect( ):
    db_name = '/home/hendrik/Documents/General/api/messages.db'
    conn = s.connect( db_name )
    cursor = conn.cursor( )
    
    if conn and cursor:
        print_console( 'Connected to database' )
    else:
        print_console( 'Failed to connect to database' )
        return None, None
    
    return conn, cursor

def message_to_db( message, m_hash, timestamp, conn, cursor ):
    cursor.execute( 'INSERT INTO message (message, m_hash, time_stamp, seen) VALUES (?, ?, ?, ?)', ( message, m_hash, timestamp, 0 ) )
    conn.commit( )
    print_console( 'Message added to database' )
    
    # send a notiffy-send notification, that a new message has been received
    
    send_notification( message )
    
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
    os.system("uptime -p > /home/hendrik/Documents/General/api/status/uptime.log")
    os.system("vnstat -tr 2 > /home/hendrik/Documents/General/api/status/vnstat.log")
    os.system("df -h > /home/hendrik/Documents/General/api/status/df.log")
    os.system("free -h > /home/hendrik/Documents/General/api/status/free.log")
    os.system("cat /proc/loadavg > /home/hendrik/Documents/General/api/status/loadavg.log")

#
# ************************************** API FUNCTIONS **************************************
#

@app.route('/docs')
def docs( ):
    return render_template('docs.html')

@app.route('/')
def start( ):
   return index( )

@app.route('/index')
def index( ):
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
def shutdown_server( ):
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
        if request.args.get('api_key') or request.headers.get('api_key') == "E!QLm9cTJY;F":
            val_bool, mal_bool = True, False
        #val_bool, mal_bool = check_api_key( )
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

@app.route('/status')
def status( ):
    time.sleep( 1 )
    if request.args.get( 'api_key' ) or request.headers.get( 'api_key' ) == "E!QLm9cTJY;F":
        val_bool, mal_bool = True, False
    else:
        val_bool, mal_bool = False, True
    #val_bool, mal_bool = check_api_key( )
    if val_bool and not mal_bool:
        with lock:
            # status
            status = open("/home/hendrik/Documents/General/api/status/status.log", "r").read()
            
            # uptime
            uptime = open("/home/hendrik/Documents/General/api/status/uptime.log", "r").read()
            uptime = uptime.replace("up ", "").replace(",", " |"). replace("\n", "")
            
            # vnstat
            vnstat_a = open("/home/hendrik/Documents/General/api/status/vnstat.log", "r").readlines()[3]
            vnstat_b = open("/home/hendrik/Documents/General/api/status/vnstat.log", "r").readlines()[4]
            
            
            vnstat_a = vnstat_a.replace("rx     ", "").strip()
            vnstat_b = vnstat_b.replace("tx     ", "").strip()
            
            vnstat_a = vnstat_a.split(" ")[0] + ' ' + vnstat_a.split(" ")[1]
            vnstat_b = vnstat_b.split(" ")[0] + ' ' + vnstat_b.split(" ")[1]
        
        data = {
            'status': status,
            'uptime': uptime,
            'download bandwidth': vnstat_a,
            'upload bandwidth': vnstat_b,
            'version': '1.0.1'
            }
        
        if 'maintenance' in data['status']:
            time.sleep(600)
            os.system("shutdown -h now")
        json_data = json.dumps(data, indent = 4)
        return json_data
    else:
        if mal_bool:
            return jsonify({'error': 'Nice try. But nope. Just nope!'}), 403
        return jsonify({'error': 'Invalid api key. Please correct the key and try again.'}), 403

@app.route('/nachricht')
@app.route('/message')
def message_system( ):
    '''
        Exaplanation:
            This function is called when the user tries to access the message page.
            This page is used to send a message to the user at the pc. Mainly used for my parents.
        Parameters:
            None
        Returns:
            A 200 status code and a message
    '''
    return render_template('message.html')

@app.route( '/send_message', methods = [ 'POST' ] )
def send_message( ):
    timestamp = datetime.now( ).strftime( '%Y-%m-%d %H:%M:%S' )
    conn, cursor = get_db_connect( )
    message = request.form[ 'message' ]
    
    # Load the message with the current timestamp into the messages_db database
    # and create a hash from the message
    # Database structure:
    # tables
    #   |
    #   |--> message -> fields
    #                       |--> id (Primary Key, Integer, Not Null)
    #                       |--> message (Text, Not Null)
    #                       |--> m_hash (Text, Not Null)
    #                       |--> time_stamp (Text, Not Null)
    #                       |--> seen (Integer, Not Null)
    
    m_hash = hashlib.sha256( message.encode( 'utf-8' ) ).hexdigest( )
    
    message_to_db( message, m_hash, timestamp, conn, cursor )
    
    return 'Gesndete Nachricht: {}'.format( message )

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


def main_loop( ):
    '''
        Exaplanation:
            This function is for handling most of the logic of the program.
            It is used for various tasks, such as checking the status of the system.
        Parameters:
            None
        Returns:
            None
    '''

    while True:
        clear_screen( )
        print( "Main loop is running..." )
        
        with lock:
            get_system_stats( )
        
        time.sleep( 5 )

def main():
        
    # t1 = threading.Thread( target = app.run, kwargs = { 'host': '192.168.2.17' } ) ; also include the lock
    t1 = threading.Thread( target = app.run, kwargs = { 'host': '192.168.2.17', 'port': 5000 } )
    t1.start( )
    t2 = threading.Thread( target = main_loop )
    t2.start( )

if __name__ == '__main__':
    main( )
    
