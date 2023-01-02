import cv2
import os
import time
import threading

from types import SimpleNamespace
from compreface import CompreFace
from compreface.service import RecognitionService

def sleep( seconds: int ) -> None:
    '''
        Explanation:
            This function is used to sleep the program for a certain amount of seconds.
        Parameters:
            seconds: int -- The amount of seconds that the program should sleep.
        Returns:
            None
    '''
    
    time.sleep( seconds )

def clear_screen( ) -> None:
    '''
        Explanation:
            This function clears the console.
        Parameters:
            None
        Returns:
            None
    '''
    
    os.system( 'cls' if os.name == 'nt' else 'clear' )

def set_globals( compre_face: CompreFace ) -> SimpleNamespace:
    '''
        Explanation:
            This function sets the global variables.
        Parameters:
            compre_face: CompreFace -- The compreface object that is used to create the recognition service.
        Returns:
            env: SimpleNamespace -- The environmental namespace that contains the webcam object.
    '''
    
    # Create the environmental Namespace
    env = SimpleNamespace( )
    
    # Set the admin present flag
    env.admin_present = False
    
    # Set the admin name
    env.admin_name = 'Hendrik Siemens'
    
    # Create a recognition service using compreface
    env.recognition: RecognitionService = \
    compre_face.init_face_recognition( 'd4ea29a3-3c79-40e9-a0e2-2e4728cd88d9' )
    
    # Set the camera object
    env.cap = cv2.VideoCapture( 0 )
    env.cap.set( cv2.CAP_PROP_BUFFERSIZE, 2 )
    
    # Set the FPS
    env.FPS = 1/30
    
    env.run_check = True
    
    return env

def get_subjects( env ) -> any:
    '''
        Explanation:
            This function gets the subjects from the current frame of the webcam.
            When you call this function, it will get the current frame of the webcam
            and then it will send it to the compreface server to get the subjects from it.
        Parameters:
            cap: The webcam object that is used to get the current frame of the webcam.
        Returns:
            subjects: any -- The subjects from the current frame of the webcam.
    '''
    
    subjects = [ ]
    
    # Get the current frame of the webcam
    _, frame = env.cap.read( )
    
    # Resize the frame
    _, im_buf_arr = cv2.imencode( '.jpg', frame )
    byte_im = im_buf_arr.tobytes( )
    
    # Send the image to the compreface server for recognizing the subjects in the frame
    data_retrieved = env.recognition.recognize( byte_im )
    results = data_retrieved.get('result')
    
    # Checks if the admin is present or not
    if results is None:
        env.admin_present = False       
    else:
        # Get the subjects from the results
        subjects = results[ 0 ].get( 'subjects', [ ] )
    
    return subjects

def search_for_admin( env ) -> None:
    '''
        Explanation:
            This function checks if the admin is present in the current frame of the webcam or not.
        Parameters:
            subjects: any -- The subjects from the current frame of the webcam.
        Returns:
            None
    '''
    
    subjects = get_subjects( env )
    if len( subjects ) > 0:
        name = subjects[0]['subject']
        
        if name == env.admin_name:
            #print( f'Welcome admin!' )
            env.admin_present = True
        else:
            env.admin_present = False

def main( env: SimpleNamespace ) -> None:
    '''
        Explanation:
            This function is the main function of the program.
            It will continuously check if the admin is present in the current frame of the webcam or not.
            If the admin is not present, this program will lock some of the functions of the computer.
        Parameters:
            env: SimpleNamespace -- The environmental namespace that contains the webcam object.
        Returns:
            None
    '''
    threshold = 300
    
    while True:
        if env.run_check:
            search_for_admin( env )
            if env.admin_present:
                print( f'Welcome admin!' )
                sleep( 5 )
                clear_screen( )
                
                env.run_check = False
        else:    
            search_for_admin( env )
            
            if not env.admin_present:
                # Start a timer that counts to 5 minutes until the screen gets locked
                start_time = time.time( )
                
                while True:
                    if env.admin_present:
                        print( f'Welcome back admin!' )
                        sleep( 5 )
                        clear_screen( )
                        
                        break
                    else:
                        if time.time( ) - start_time >= threshold:
                            print( f'Screen locked in 5 seconds!' )
                            sleep( 5 )
                            clear_screen( )
                            
                            # Lock the screen
                            os.system( 'gnome-screensaver-command --lock' )
                            
                            break
                        else:
                            print( f'You have { 300 - int( time.time( ) - start_time ) } seconds left until the screen gets locked!' )
                            threshold -= 1
                            sleep( 1 )
                            clear_screen( )
                  

if __name__ == "__main__":
    
    '''
        Explanation:
            This is part of the program will set the globals and then call the main function.
        Parameters:
            None
        Returns:
            None
    '''
    
    compre_face: CompreFace = CompreFace('http://localhost', '8000', {
            "limit": 0,
            "det_prob_threshold": 0.8,
            "prediction      _count": 1,
            "face_plugins": "age,gender,landmarks",
            "status": False
        })
    
    # Set globals
    env = set_globals( compre_face )
    
    
    main( env )