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
    api_key_1 = '79c3ae75-2b04-4168-93f6-6a09eefccd7e'
    api_key_2 = ''
    #url
    
    if mode == 'recognize':
        api_key = '79c3ae75-2b04-4168-93f6-6a09eefccd7e'
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
    format_response = json.dumps( response, indent = 4 )
    print(json.dumps(response, indent=4))
    
    # Returning the response and the formatted response
    return response, format_response
    

recognize_face( 'test.jpg' )