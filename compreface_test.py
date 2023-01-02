import json
import requests


def send_request( filename: str, mode: str) -> dict:
    '''
        Explanation:
            This function will send a request to the API. The mode of the request
            is determined by the mode parameter.
        Parameters: 
            filename: str - The name of the file to be sent to the API.
            mode: str - The mode of the request.
        Returns:
            dict - The JSON response from the API.
    '''
    api_key_1 = 'd4ea29a3-3c79-40e9-a0e2-2e4728cd88d9'
    api_key_2 = ''
    #url
    
    if mode == 'recognize':
        api_key = 'd4ea29a3-3c79-40e9-a0e2-2e4728cd88d9'
        url = f'http://localhost:8000/api/v1/recognition/recognize'
        headers = { 
                   'x-api-key': api_key,
                   'face_plugins': 'pose'
                   }
        files = { 'file': open( filename, 'rb' ) }
        response = requests.post( url, files = files, headers = headers )
        json_data = json.loads( response.text )
    return json_data

def recognize_face( filename: str ) -> dict:
    '''
        Explanation:
            This function will send a request to the API to recognize a face.
            It then prints the response.
        Parameters: 
            filename: str - The name of the file to be sent to the API.
        Returns:
            response:dict - The JSON response from the API.
            format_response:dict - The formatted JSON response from the API.
            
    '''
    response = send_request( filename, 'recognize' )
    result = response['result']
    subjects = result[0]['subjects']
    subject = subjects[0]['subject']

    if subject == 'Hendrik Siemens':
        print( 'Hello Admin!' )
    
    # Returning the response and the formatted response
    #return response, format_response
    
    return subject
    

recognize_face( 'test.jpg' )

