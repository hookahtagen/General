import requests

def play_pause(ip, psk):
    # Set up the IRCC code for the play/pause button
    ircc_code = 'AAAAAgAAAJcAAAAaAw=='
    
    url = "http://192.168.2.95/sony/IRCC"
    headers = {
        "HOST": "192.168.2.95",
        "Accept": "*/*",
        "Content-Type": "application/xml; charset=UTF-8",
        "SOAPACTION": "urn:schemas-sony-com:service:IRCC:1#X_SendIRCC",
        "X-Auth-PSK": "1234",
        "Connection": "Keep-Alive",
        "Content-Length": "313",
    }

    body = """
    <s:Envelope
        xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"
        s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
        <s:Body>
            <u:X_SendIRCC xmlns:u="urn:schemas-sony-com:service:IRCC:1">
                <IRCCCode>AAAAAQAAAAEAAAAUAw==</IRCCCode>
            </u:X_SendIRCC>
        </s:Body>
    </s:Envelope>
    """

    response = requests.post(url, headers=headers, data=body)
    
    # Check if the operation was successful
    return response.status_code == 200

def mute(ip, psk):
# Send a request to get the current audio mute status
    url = f'http://{ip}/sony/audio'
    headers = {'X-Auth-PSK': psk}
    payload = {
        "method": "getVolumeInformation",
        "version": "1.0",
        "id": 1,
        "params": [],
    }
    response = requests.post(url, headers=headers, json=payload)

    # Parse the response to get the current audio mute status
    response_json = response.json()
    
    current_status = response_json['result'][0][0]['mute']

    # Send a request to set the opposite audio mute status
    payload = {
        "method": "setAudioMute",
        "version": "1.0",
        "id": 1,
        "params": [{"status": not current_status}],
    }
    response = requests.post(url, headers=headers, json=payload)
    #print(f'Status code: {response.status_code}')
    #print(f'Response: {response.text}')

def increase_volume(ip, psk):
    url = f'http://{ip}/sony/audio'
    headers = {'X-Auth-PSK': psk}
    payload = {
        "method": "setAudioVolume",
        "version": "1.2",
        "id": 1,
        "params": [{
            "target": "speaker", 
            "volume": "+1",
            "ui": "off"
        }],
    }
    response = requests.post(url, headers=headers, json=payload)
    #print(f'Status code: {response.status_code}')
    #print(f'Response: {response.text}')

def decrease_volume(ip, psk):
    url = f'http://{ip}/sony/audio'
    headers = {'X-Auth-PSK': psk}
    payload = {
        "method": "setAudioVolume",
        "version": "1.0",
        "id": 1,
        "params": [{"target": "speaker", "volume": "-1"}],
    }
    response = requests.post(url, headers=headers, json=payload)
    #print(f'Status code: {response.status_code}')
    #print(f'Response: {response.text}')

def main(argv):
    ip = '192.168.2.95'  # Replace with the IP of your display device
    psk = '1234'  # Replace with the PSK of your display device
    if len(argv) < 2:
        print('Please specify "increase" or "decrease" as an argument.')
        return
    if argv[1] == 'increase':
        increase_volume(ip, psk)
    elif argv[1] == 'decrease':
        decrease_volume(ip, psk)
    elif argv[1] == 'mute':
        mute(ip, psk)
    elif argv[1] == 'play_pause':
        play_pause(ip, psk)
    else:
        print('Invalid argument. Please specify "increase" or "decrease".')

if __name__ == '__main__':
    import sys
    main(sys.argv)


