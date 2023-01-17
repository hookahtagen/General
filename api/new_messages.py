import os
import time as t
import datetime as dt
import sqlite3 as s

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


if __name__ == '__main__':
    '''
        Explanation:
            The main function of the program is to check for unread messages in the database.
            If any are found, the user is notified via a notify-send notification.
        Parameters:
            None
        Returns:
            None
    '''
    DURATION = 900_000
    conn, cursor = get_db_connect( )
    
    # The program needs a valid 
    # connection for it to run
    if not conn or not cursor:
        print_console( 'Failed to connect to database\nExiting now!!!' )
        exit( 1 )
    
    sql_query = 'SELECT * FROM message WHERE seen = 0'
    cursor.execute( sql_query )
    
        # Database structure:
        # tables
        #   |
        #   |--> message -> fields
        #                       |--> id (Primary Key, Integer, Not Null)
        #                       |--> message (Text, Not Null)
        #                       |--> m_hash (Text, Not Null)
        #                       |--> time_stamp (Text, Not Null)
        #                       |--> seen (Integer, Not Null)
        
    rows = cursor.fetchall()
    num_messages = len( rows )
    
    os.system( f'notify-send -t { DURATION } "New messages received" "You have { num_messages } unread messages"' )
    os.system( f'paplay /home/hendrik/Documents/General/api/sounds/notification.wav' )