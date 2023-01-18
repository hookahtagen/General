from datetime import datetime
import hashlib
import json
import logging
import os
import sqlite3 as s
import time
import threading

from flask import Flask, jsonify, Response, render_template, request

app = Flask( __name__ )
lock = threading.Lock( )

class logger:
    '''
        Explanation:
            This class is used to log messages to a file.
        Parameters:
            name: str - The name of the logger
        Returns:
            None
    '''
    
    def __init__( self, name ):
        self.logger = logging.getLogger( name )
        self.logger.setLevel( logging.DEBUG )
        self.file_handler = logging.FileHandler( '/home/hendrik/Documents/General/api/dist/api/log/server_log.log' )
        self.file_handler.setFormatter( logging.Formatter( '------------------------------------\n%(asctime)s - level: %(levelname)s - %(message)s' ) )
        self.logger.addHandler( self.file_handler )

    def debug( self, message ):
        message = '\n' + message + '\n'
        self.logger.debug( message )

    def info( self, message ):
        message = '\n' + message + '\n'
        self.logger.info( message )

    def warning( self, message ):
        message = '\n' + message + '\n'
        self.logger.warning( message )

    def error( self, message ):
        message = '\n' + message + '\n'
        self.logger.error( message )

    def critical( self, message ):
        message = '\n' + message + '\n'
        self.logger.critical( message )
        
#********************#
log = logger( 'api' )
#********************#

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
    '''
        Explanation:
            This function is used to check if the api key is valid.
            It checks if the api key is in the headers, or in the arguments. If so, it checks if the api key is valid by
            hashing it and comparing it to the hash of the api key stored in the environment variables. If it is valid, it
            returns a boolean value of True, else it returns a boolean value of False.
        Parameters:
            None
        Returns:
            boolean #1: bool - A boolean value that indicates if the api key is valid.
            boolean #2: bool - A boolean value that indicates that something is wrong with the api key.            
    '''
    
    if len( request.headers ) > 0:
        hash_key = os.environ.get( 'API_KEY_FLASK' )
        if request.headers.get( 'api_key' ) != None:
            api_key = request.headers.get( 'api_key' )
        if request.headers.get( 'api-key' ) != None:
            api_key = request.headers.get( 'api-key' )
        if request.args.get( 'api_key' ) != None:
            api_key = request.args.get( 'api_key' )
        if request.args.get( 'api-key' ) != None:
            api_key = request.args.get( 'api-key' )
            
        if api_key == "":
            return False, False
        if api_key in ( "0000" , "1234" ):
            return False, True
        
        print(f'api_key: {api_key}')
        api_key_hash = hashlib.sha256( api_key.encode( 'utf-8' ) ).hexdigest( )
        print( api_key )
        print( "TEST" )
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
    print( '\n****************************\n' )
    print( message )
    print( '\n****************************\n' )

def send_notification( message, DURATION = 5000 ):
    '''
        Explanation:
            Sends a notification to the user, that a new message has been received.
        Parameters:
            message: str - The message to send to the user.
        Returns:
            None
    '''
    
    # send a notiffy-send notification, that a new message has been received
    os.system( f'notify-send -t { DURATION } "New message received ( c2 )" "{ message }"' )

def get_db_connect( ):
    '''
        Explanation:
            This function is used to connect to the database.
        Parameters:
            None
        Returns:
            conn: sqlite3.Connection - The connection to the database.
            cursor: sqlite3.Cursor - The cursor to the database.
    '''
    
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
    '''
        Explanation:
            This function is used to add a message to the database.
        Parameters:
            message: str - The message to add to the database.
            m_hash: str - The hash of the message.
            timestamp: str - The timestamp of the message.
            conn: sqlite3.Connection - The connection to the database.
            cursor: sqlite3.Cursor - The cursor to the database.
        Returns:
            None
    '''
    
    cursor.execute( 'INSERT INTO message (message, m_hash, time_stamp, seen) VALUES (?, ?, ?, ?)', ( message, m_hash, timestamp, 0 ) )
    conn.commit( )
    print_console( 'Message added to database' )
    
    # send a notiffy-send notification, that a new message has been received
    # and log to server_log that a new message arrived
    
    send_notification( message )
    log.info( f'New message received' )
    
    
def get_system_stats( ):
    '''
        Exaplanation:
            This function is used to get the system stats.
            It is used for various tasks, such as checking the status of the system.
        Parameters:
            None
        Returns:
            None
    '''
    os.system( "uptime -p > /home/hendrik/Documents/General/api/dist/api/status/uptime.log" )
    os.system( "vnstat -tr 2 > /home/hendrik/Documents/General/api/dist/api/status/vnstat.log" )
    os.system( "df -h > /home/hendrik/Documents/General/api/dist/api/status/df.log" )
    os.system( "free -h > /home/hendrik/Documents/General/api/dist/api/status/free.log" )
    os.system( "cat /proc/loadavg > /home/hendrik/Documents/General/api/dist/api/status/loadavg.log" )

#
# ************************************** API FUNCTIONS **************************************
#

@app.route( '/docs' )
def docs( ):
    '''
        Explanation :
            This function handles the request for the documentation entry.
        Parameters:
            None
        Returns:
            docs.html: webpage - Webpage for the API-Documentation
    '''
    return render_template( 'docs.html' )

@app.route( '/' )
def start( ):
    '''
        Explanation:
            This function redirects access attempts from '/' to '/index'
        Parameters:
            None
        Returns:
            index( ): func - function index( )
    '''
    
    return index( )

@app.route( '/index' )
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
    return render_template( 'index.html' )

@app.route( '/shutdown' )
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
            
            # server logging
            log.critical('Shutting down server...')
            log.critical(f'shutdown command issued by { request.remote_addr } with api key: { request.args.get( "api_key" ) }')
            
            os.system("shutdown -h now")
            return jsonify({'status': 'shutting down now...'}), 200
        if mal_bool:
            return jsonify({'error': 'Nice try. But nope. Just nope!'}), 403
        else:
            return jsonify({'error': 'Invalid api key. Please correct the key and try again.'}), 403
    return jsonify({'error': 'You must specify a api key!'}), 403

@app.route('/status')
def status( ):
    '''
        Explanation:
            This function is called when the user tries to access the status page.
            It returns a 200 status code and a message.
        Parameters:
            None
        Returns:
            A 200 status code and a message
    '''
    
    if request.args.get( 'api_key' ) or request.headers.get( 'api_key' ) == "E!QLm9cTJY;F":
        val_bool, mal_bool = True, False
    else:
        val_bool, mal_bool = False, True
    #val_bool, mal_bool = check_api_key( )
    if val_bool and not mal_bool:
        with lock:
            # status
            status = open("/home/hendrik/Documents/General/api/dist/api/status/status.log", "r").read()
            
            # uptime
            uptime = open("/home/hendrik/Documents/General/api/dist/api/status/uptime.log", "r").read()
            uptime = uptime.replace("up ", "").replace(",", " |"). replace("\n", "")
            
            # vnstat
            vnstat_a = open("/home/hendrik/Documents/General/api/dist/api/status/vnstat.log", "r").readlines()[3]
            vnstat_b = open("/home/hendrik/Documents/General/api/dist/api/status/vnstat.log", "r").readlines()[4]
            
            
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
    '''
        Explanation:
            This function is called when the user tries to send a message via the page '/message'.
        Parameters:
            None
        Returns:
            A 200 status code and a message
    '''
    
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
    
    return render_template( 'sent_message.html', message = message )

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
    
    log.error( 'user tried to access page {}\nWhich resulted in a Error 404.'.format( request.url ) )
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
    
    # Log started server
    log.info( "Server started" )

    while True:
        clear_screen( )
        print( "Main loop is running..." )
        
        with lock:
            get_system_stats( )
        
        time.sleep( 5 )

def main():
    '''
        Explanation:
            This function starts the main-thread for handling various things
            and the flask-server which handles most of the http-traffic.
        Parameters:
            None
        Returns:
            None
    '''
        
    # t1 = threading.Thread( target = app.run, kwargs = { 'host': '192.168.2.17' } ) ; also include the lock
    t1 = threading.Thread( target = app.run, kwargs = { 'host': '192.168.2.17', 'port': 5000 } )
    t1.start( )
    t2 = threading.Thread( target = main_loop )
    t2.start( )

if __name__ == '__main__':
    '''
        Explanation:
            This function is called when the program is started.
            It just calls the main function.
        Parameters:
            None
        Returns:
            None
    '''
    
    main( )
    

'''
    1. Overview of the program:
        1. Purpose of the program:
            The purpose of this program is to create a webserver that can be used to control the pc. This could vary from shutting down the pc to sending a message to the user.
            In future versions, I want to add more features to the program, such as a web-based file explorer, a web-based terminal, or even a web-based IDE.
            
            For now, the program is just a simple webserver that can be used to send messages to the admin at the server, getting the status of the system, and shutting down the pc.
            The purpose of the messaging system is mainly for my parents, so they can send me a message when they need something in case I don't hear my phone or so.
        
        2. Audience of the program:
            The audience of this program is mainly for me, but it could also be used by other people who want to create a webserver that can be used to control their pc.
        
        3. System requirements:
            The system requirements for this program are:
                - A computer running Linux
                - A web browser
                or
                - A command line interface
                - Python 3.6 or higher
                - hashlib
                - json
                - logging
                - os
                - sqlite3
                - time
                - threading
                - flask
                - uptime
                - vnstat
                - df
                - free
                - cat
                - ps
                - shutdown
                - clear
                - curl
                - wget
                optional:
                    - ping
                    - traceroute
        
        4. Dependencies:
            The dependencies for this program are:
                - hashlib
                - json
                - logging
                - os
                - sqlite3
                - time
                - threading
                - flask
                - uptime
                - vnstat
                - df
                - free
                - cat
                - ps
                - shutdown
                - clear
                - curl
                or 
                - wget
        
        5. Compatibility:
            The program is compatible with Linux, but it should also work on other operating systems with minor changes like the shutdown command, the clear command, and the uptime command.
            Also the file paths might need to be changed when switching to another operating system.
            
            The program / server was built with VSCode, Python 3.10.7 and Ubuntu 22.10.
        
        6. Version history:
            - v0.0.1: Initial version   |   2023-01-18 22:49:00  |   api.py
     
    2. Installation:
        1. System requirements:
            For the system requirements, see section 1.3.
        
        2. Pre-installation tasks:
            For the pre-installation tasks, see section 1.4.
        
        3. Installation process:
            The installation of the server is very simple.
            For now there are two possible ways to get the server up and running.
            
            Way 1:
            - Unpack the files in the folder of your choice.
            - Open a terminal in the folder where the files are located.
            - Run the command 'python3 api.py' to start the server.
            
            or 
            
            Way 2:
            - Unpak the files in the folder of your choice.
            - Open the folder in your file manager.
            - Open a terminal window.
            - Drag and drop the api.py file into the terminal window.
            - Hit enter to start the server.
        
        4. Post-installation tasks:
            For some api tasks, you will need a valid api key.
                For users running the server on linux:
                    - Create a strong password of your choice.
                    - Open a terminal window.
                    - Run the command 'echo -n "your_password" | sha256sum' to get the hash of your password.
                    - Copy the hash.
                    - Export the hash as an environment variable by running the command 'export API_KEY_FLASK="your_hash"'.
                    - Run the command 'echo $API_KEY_FLASK' to check if the hash was exported correctly.
                    - Run the command 'source ~/.bashrc' to make the environment variable permanent.
                    - Then you can start the server and use the api.
                    -
                    - For more details about the api key, see section 'Security'.
        
        5. Upgrading from a previous version:
            Upgrading from a previous version is very simple:
                For now it's just replacing the old files with the new files.
                
        6. Troubleshooting:
            Many errors can be fixed by just restarting the server.
            If that doesn't work, you can try to reinstall the server after backing up your data.
            
            Some common mistakes are forgetting to export the api key as an environment variable or forgetting to start the server.
            Some other common mistakes are missinf folders ore files, or wrong file permissions. Please check also if the files might be corrupted.
            
        7. Uninstalling:
            Uninstalling the server is very simple:
                Just delete the files and folders, or just delete the parent folder.
                If you wish you can also delete the api key from your environment variables by running the command 'unset API_KEY_FLASK'.
        
    3. User Guide:
        1. Getting started:
            Getting the server up and running is very simple.
            
            For now there are two possible ways to get the server up and running.
            
            Way 1:
            - Unpack the files in the folder of your choice.
            - Open a terminal in the folder where the files are located.
            - Run the command 'python3 api.py' to start the server.
            
            or 
            
            Way 2:
            - Unpak the files in the folder of your choice.
            - Open the folder in your file manager.
            - Open a terminal window.
            - Drag and drop the api.py file into the terminal window.
            - Hit enter to start the server.
            
            After the server is started, you can use the api.
            
        2. Interface:
            
            
                
            
'''