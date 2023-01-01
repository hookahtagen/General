import requests


ip = '192.168.2.95'  # Replace with the IP of your display device
psk = '1234'  # Replace with the PSK of your display device
admin_present: bool = False

def increase_volume(ip, psk):
    url = f'http://{ip}/sony/system'
    headers = {'X-Auth-PSK': psk}
    payload = {
        "method": "getPowerStatus",
        "version": "1.0",
        "id": 1,
        "params": [ ],
    }
    response = requests.post(url, headers=headers, json=payload)
    print(f'Status code: {response.status_code}')
    print(f'Response: {response.text}')
    

if admin_present:
    increase_volume(ip, psk)
