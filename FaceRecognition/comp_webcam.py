import cv2
import argparse
import time
import numpy as np
import os
from numba import jit, njit

from threading import Thread
from compreface import CompreFace
from compreface.service import RecognitionService


FONT = cv2.FONT_HERSHEY_SIMPLEX
factor = 4
div_factor = 0.25

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_help( key ):
    help_dict = {}
    
    return '#TODO #1'

def parseArguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("--api-key", help=get_help( 'api_key' ), type=str, default='d4ea29a3-3c79-40e9-a0e2-2e4728cd88d9')
    parser.add_argument("--host", help=get_help( 'host' ), type=str, default='http://localhost')
    parser.add_argument("--port", help=get_help( 'port' ), type=str, default='8000')
    parser.add_argument("--mode", help=get_help( 'mode' ), type=str, default='0')

    args = parser.parse_args()

    return args

def resize_image( image, mode: str ):  
    if mode == 'up':
        small_image = cv2.resize( image, ( 0, 0 ), fx = factor, fy = factor )
    small_image = cv2.resize( image, ( 0, 0 ), fx = div_factor, fy = div_factor )
    return small_image
    

class ThreadedCamera:
    def __init__(self, api_key, host, port, mode):
        self.active = True
        self.results = []
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 2)

        compre_face: CompreFace = CompreFace(host, port, {
            "limit": 0,
            "det_prob_threshold": 0.8,
            "prediction      _count": 1,
            "face_plugins": "age,gender,landmarks",
            "status": False
        })

        self.recognition: RecognitionService = compre_face.init_face_recognition(api_key)

        self.FPS = 1/30
        
        # Define some facial variables
        self.mouth_open = False
        self.eyes_open = False
        
        # Check variable for processing boxes and showing the video stream
        self.process_box = True
        # if mode == '0':
        #     self.process_box = False
        
        # Define the variables for the angles of the x and y axis relative to the camera.
        # This should mean that the camera is the centre of a 'coordinate system".
        self.angle_vertical = 0.0
        self.angle_horizontal = 0.0
        self.looking_at_camera = False

        # Start frame retrieval thread
        self.thread = Thread(target=self.show_frame, args=())
        self.thread.daemon = True
        self.thread.start()

    def show_frame(self):
        '''
            Explanation:
                This function is used to retrieve frames from the camera and process them.
                It is run in a separate thread to prevent the GUI from freezing.
            Parameters:
                self (ThreadedCamera) - The current ThreadedCamera object.
        '''
        print("Started")
        process_this_frame = True
        while self.capture.isOpened():
            (status, frame_raw) = self.capture.read()
            self.frame = cv2.flip(frame_raw, 1)
            #print(self.results)
            
            if process_this_frame:
                if self.results:
                    results = self.results
                    show_landmarks = True
                    for result in results:
                        box = result.get('box')
                        age = result.get('age')
                        gender = result.get('gender')
                        mask = result.get('mask')
                        subjects = result.get('subjects')
                        if box and self.process_box:
                            cv2.rectangle(img=self.frame, pt1=(box['x_min'], box['y_min']),
                                        pt2=(box['x_max'], box['y_max']), color=(0, 255, 0), thickness=1)
                            if age:
                                age = f"Age: {age['low']} - {age['high']}"
                                cv2.putText(self.frame, age, (box['x_max'], box['y_min'] + 15),
                                            FONT, 0.6, (0, 255, 0), 1)
                            if gender:
                                gender = f"Gender: {gender['value']}"
                                cv2.putText(self.frame, gender, (box['x_max'], box['y_min'] + 35),
                                            FONT, 0.6, (0, 255, 0), 1)
                            if mask:
                                mask = f"Mask: {mask['value']}"
                                cv2.putText(self.frame, mask.replace( '_', ' ' ), (box['x_max'], box['y_min'] + 55),
                                            FONT, 0.6, (0, 255, 0), 1)

                            if subjects:
                                subjects = sorted(subjects, key=lambda k: k['similarity'], reverse=True)
                                name = f"{subjects[0]['subject']}"
                                similarity = f"Similarity: {subjects[0]['similarity']}"
                                cv2.putText(self.frame, f"Name: {name}", (box['x_max'], box['y_min'] + 75),
                                            FONT, 0.6, (0, 255, 0), 1)
                                cv2.putText(self.frame, similarity, (box['x_max'], box['y_min'] + 95),
                                            FONT, 0.6, (0, 255, 0), 1)
                            else:
                                name = f"No known faces"
                                cv2.putText(self.frame, name, (box['x_max'], box['y_min'] + 75),
                                            FONT, 0.6, (0, 255, 0), 1)
                        
                        if not self.process_box and show_landmarks:
                            landmarks = result.get('landmarks')
                            # left_eye = landmarks[0]
                            # right_eye = landmarks[1]
                            # nose_tip = landmarks[2]
                            # left_mouth = landmarks[3]
                            # right_mouth = landmarks[4]
                            clear_screen()
                            print(landmarks)
                            show_landmarks = not show_landmarks

            if self.process_box:
                cv2.imshow('CompreFace demo', self.frame)
                time.sleep(self.FPS)
                #process_this_frame = not process_this_frame
            
                if cv2.waitKey(1) & 0xFF == 27:
                    self.capture.release()
                    cv2.destroyAllWindows()
                    self.active=False

    def is_active(self):
        '''
            Explanation:
                Returns the active state of the camera
            Parameters:
                None
            Returns:
                self.active (bool): True if the camera is active, False otherwise
        '''
        return self.active

    def update(self):
        '''
            Explanation:
                Updates the frame and results. Also calls the recognition service
                for recognizing the faces in the frame.
            Parameters:
                self (ThreadedCamera): The camera object
            Returns:
                None
        '''
        
        if not hasattr(self, 'frame'):

            return

        #Activate the two following lines for sizing down the frame
        #before processing/sending it
        
        #image = resize_image(self.frame, 'down')
        #self.frame = image
        
        _, im_buf_arr = cv2.imencode(".jpg", self.frame)
        byte_im = im_buf_arr.tobytes()
        data = self.recognition.recognize(byte_im)
        self.results = data.get('result')
       
        a=1              
            
if __name__ == '__main__':
    '''
        Explanation:
            Main function. Parses the arguments and starts the camera.
        Parameters:
            None
        Returns:
            None
    '''
    
    args = parseArguments()
    threaded_camera = ThreadedCamera(args.api_key, args.host, args.port, args.mode)
    while threaded_camera.is_active():
        threaded_camera.update()
