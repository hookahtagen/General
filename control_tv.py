#!/usr/bin/python3

import requests

ircc_codes = {
    'Power': 'AAAAAQAAAAEAAAAVAw==',
    'Input': 'AAAAAQAAAAEAAAAlAw==',
    'SyncMenu': 'AAAAAgAAABoAAABYAw==',
    'Hdmi1': 'AAAAAgAAABoAAABaAw==',
    'Hdmi2': 'AAAAAgAAABoAAABbAw==',
    'Hdmi3': 'AAAAAgAAABoAAABcAw==',
    'Hdmi4': 'AAAAAgAAABoAAABdAw==',
    'Num1': 'AAAAAQAAAAEAAAAAAw==',
    'Num2': 'AAAAAQAAAAEAAAABAw==',
    'Num3': 'AAAAAQAAAAEAAAACAw==',
    'Num4': 'AAAAAQAAAAEAAAADAw==',
    'Num5': 'AAAAAQAAAAEAAAAEAw==',
    'Num6': 'AAAAAQAAAAEAAAAFAw==',
    'Num7': 'AAAAAQAAAAEAAAAGAw==',
    'Num8': 'AAAAAQAAAAEAAAAHAw==',
    'Num9': 'AAAAAQAAAAEAAAAIAw==',
    'Num0': 'AAAAAQAAAAEAAAAJAw==',
    'Dot': 'AAAAAgAAAJcAAAAdAw==',
    'CC': 'AAAAAgAAAJcAAAAoAw==',
    'Red': 'AAAAAgAAAJcAAAAlAw==',
    'Green': 'AAAAAgAAAJcAAAAmAw==',
    'Yellow': 'AAAAAgAAAJcAAAAnAw==',
    'Blue': 'AAAAAgAAAJcAAAAkAw==',
    'Up': 'AAAAAQAAAAEAAAB0Aw==',
    'Down': 'AAAAAQAAAAEAAAB1Aw==',
    'Right': 'AAAAAQAAAAEAAAAzAw==',
    'Left': 'AAAAAQAAAAEAAAA0Aw==',
    'Confirm': 'AAAAAQAAAAEAAABlAw==',
    'Help': 'AAAAAgAAAMQAAABNAw==',
    'Display': 'AAAAAQAAAAEAAAA6Aw==',
    'Options': 'AAAAAgAAAJcAAAA2Aw==',
    'Back': 'AAAAAgAAAJcAAAAjAw==',
    'Home': 'AAAAAQAAAAEAAABgAw==',
    'VolumeUp': 'AAAAAQAAAAEAAAASAw==',
    'VolumeDown': 'AAAAAQAAAAEAAAATAw==',
    'Mute': 'AAAAAQAAAAEAAAAUAw==',
    'Audio': 'AAAAAQAAAAEAAAAXAw==',
    'ChannelUp': 'AAAAAQAAAAEAAAAQAw==',
    'ChannelDown': 'AAAAAQAAAAEAAAARAw==',
    'Play': 'AAAAAgAAAJcAAAAaAw==',             # Play
    'Pause': 'AAAAAgAAAJcAAAAZAw==',            # Play/Pause
    'Stop': 'AAAAAgAAAJcAAAAYAw==',
    'FlashPlus': 'AAAAAgAAAJcAAAB4Aw==',
    'FlashMinus': 'AAAAAgAAAJcAAAB5Aw==',
    'Prev': 'AAAAAgAAAJcAAAA8Aw==',
    'Next': 'AAAAAgAAAJcAAAA9Aw=='
}

if __name__ == '__main__':

  import sys

  if len( sys.argv ) < 2 or len( sys.argv ) > 2 or sys.argv[ 1 ] not in ircc_codes.keys():
    print ("Usage: %s <TV_IP> <IRCC_COMMAND>" % sys.argv[ 0 ] )
    sys.exit( 1 )

  tv_ip = '192.168.2.95'
  code = ircc_codes[ sys.argv[ 1 ] ]

  cmd = "<?xml version=\"1.0\"?><s:Envelope xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\" s:encodingStyle=\"http://schemas.xmlsoap.org/soap/encoding/\"><s:Body><u:X_SendIRCC xmlns:u=\"urn:schemas-sony-com:service:IRCC:1\"><IRCCCode>" + code + "</IRCCCode></u:X_SendIRCC></s:Body></s:Envelope>"

  headers = {
    'Content-Type': 'text/xml; charset=UTF-8',
    'SOAPACTION': '"urn:schemas-sony-com:service:IRCC:1#X_SendIRCC"',
    'X-Auth-PSK': '1234'
  }

  r = requests.post( 'http://%s/sony/IRCC' % tv_ip, data=cmd, headers=headers )

  if r.status_code == 200:
    print ( '✓' )
  else:
    print ( 'Command failed (HTTP_CODE: %d, try running it in a console)' % r.status_code )
    sys.exit( 1 )
