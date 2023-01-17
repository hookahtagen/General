import hashlib
import os
import sqlite3 as s

from datetime import datetime
from flask import Flask, render_template, request

app = Flask( __name__ )

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
    os.system( f'notify-send -t { DURATION } "New message received" "{ message }"' )

def find_new_messages( ):
    timestamp = datetime.now( ).strftime( '%Y-%m-%d %H:%M:%S' )
    
    conn, cursor = get_db_connect( )
    return [ 'Message 1', 'Message 2' ]

def message_to_db( message, m_hash, timestamp, conn, cursor ):
    cursor.execute( 'INSERT INTO message (message, m_hash, time_stamp, seen) VALUES (?, ?, ?, ?)', ( message, m_hash, timestamp, 0 ) )
    conn.commit( )
    print_console( 'Message added to database' )
    
    # send a notiffy-send notification, that a new message has been received
    
    send_notification( message )

@app.route( '/' )
def index( ):
    return render_template( 'message.html' )

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
    
    return 'Message sent: {}'.format( message )

if __name__ == '__main__':
    app.run( host = "192.168.2.17", debug = True )