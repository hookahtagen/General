import json
import requests
import ssl

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
    
    api_key = '79c3ae75-2b04-4168-93f6-6a09eefccd7e'
    url = f'http://localhost:8000/api/v1/recognition/recognize'
    headers = { 'x-api-key': api_key }
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
            dict - The JSON response from the API.
    '''
    response = send_request( filename, 'recognize' )
    print(json.dumps(response, indent=4))
    

recognize_face( 'test4.jpg' )