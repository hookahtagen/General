'''
    Title:      Enigma Machine Simulator
    Author:     Hendrik Siemens
    Date:       2022-02-03
    Version:    1.0
    
    Description:
                This is a simple enigma machine simulator. It can be used to encrypt and decrypt messages.
                The machine uses rotors, which could be chosen from a list of rotors, or randomly selected.
                You can also choose the reflector and the plugboard, and provide an initial rotor offset.
                
                For more information about the enigma machine, see https://en.wikipedia.org/wiki/Enigma_machine
                or visit my github page:
                
    Already implemented:
                General:
                    - Enciphering messages
                    - Choosing rotors from a list
                    - Choosing the number of rotors
                    - Choosing the reflector
                    - Choosing the plugboard
                    - Choosing the initial rotor offset
                    - Choosing the message to be enciphered or deciphered
                    - Getting the notches of the rotors (for the rotor turnover)
                    
                Special:
                    - Creating a set of random rotors and save it to a txt file
                    - 
    Planned:
                General:
                    - Deciphering messages
'''

import argparse
import os
import random
from types import SimpleNamespace



PLUGBOARD_wiring = {
            'PLUGBOARD_A': ['AV','BS','CG','DL','FU','HZ','IN','KM','OW','RX'],
            'PLUGBOARD_B': ['AJ','BX','CH','EM','FY','IS','LW','OT','DV','KQ'],
            'PLUGBOARD_C': ['AR','BD','CO','EJ','FN','GT','HK','IV','LM','PW'],
            'PLUGBOARD_D': ['AE','BN','CK','DQ','FU','GY','HW','IJ','LO','MP']
        }

REFLECTOR_wiring = {
            'REFLECTOR_A': 'EJMZALYXVBWFCRQUONTSPIKHGD',
            'REFLECTOR_B': 'YRUHQSLDPXNGOKMIEBFZCWVJAT',
            'REFLECTOR_C': 'FVPJIAOYEDRZXWGCTKUQSBNMHL',
            'REFLECTOR_D': 'ENKQAUYWJICOPBLMDXZVFTHRGS'
        }

ROTOR_wiring = {
        'ROTOR_I': 'EKMFLGDQVZNTOWYHXUSPAIBRCJ',
        'ROTOR_II': 'AJDKSIRUXBLHWTMCQGZNPYFVOE',
        'ROTOR_III': 'BDFHJLCPRTXVZNYEIWGAKMUSQO',
        'ROTOR_IV': 'ESOVPZJAYQUIRHXLNFTGKDCMWB',
        'ROTOR_V': 'VZBRGITYUPSDNHLXAWMJQOFECK',
        'ROTOR_VI': 'JPGVOUMFYQBENHZRDKASXLICTW',
        'ROTOR_VII': 'NZJHGRCXMYSWBOUFAIVLPEKQDT',
        'ROTOR_VIII': 'FKQHTLXOCBJSPDZRAMEWNIUYGV',
    }   

def get_system_settings():
    helptext_dict = {
     'description': '''This is a simple enigma machine simulator. It can be used to encrypt and decrypt messages.
                       By default, the machine uses 3 rotors, the reflector A, the plugboard A and the rotor offset W,X,C.''',
     
     'rotor_list': 'The rotors used in the machine. The rotors are seperated by a comma. The default value is ROTOR_I,ROTOR_II,ROTOR_III',
     'rotor_count': 'The number of rotors used in the machine. The default value is 3',
     'reflector': 'The reflector used in the machine. The default value is REFLECTOR_A',
     'plugboard': 'The plugboard used in the machine. The default value is PLUGBOARD_A',
     'rotor_offset': 'The initial offset of the rotors. The default value is W,X,C',
     'message': 'The message to be encrypted or decrypted. This is a required argument.'
    }
    ht = helptext_dict
    
    parser = argparse.ArgumentParser(description = ht['description'], usage=argparse.SUPPRESS,
                formatter_class=lambda prog: argparse.HelpFormatter(
                    prog, max_help_position=80, width=120))
    
    parser.usage = 'python3 enigma.py [options]'
    
    eg = parser.add_argument_group('Enigma machine settings')
    eg.add_argument('-rl', '--rotor_list', type=str, help=ht['rotor_list'])
    eg.add_argument('-rc', '--rotor_count', type=int, help=ht['rotor_count'])
    eg.add_argument('-ref', '--reflector', type=str, help=ht['reflector'])
    eg.add_argument('-pb', '--plugboard', type=str, help=ht['plugboard'])
    eg.add_argument('-ro', '--rotor_offset', type=str, help=ht['rotor_offset'])
    eg.add_argument('-m', '--message', type=str, default='HELLOWORLD', required=True, help=ht['message'])
    
    args = parser.parse_args()
    
    settings = SimpleNamespace()
    
    if args.rotor_list:
        settings.rotor_list = args.rotor_list
    else:
        '''Randomly select rotors. The number of rotors to be selected is specified by the rotor_count argument.'''
        rotor_amount = args.rotor_count if args.rotor_count else 3
        
        for i in range(rotor_amount):
            rotor = random.choice(list(ROTOR_wiring.keys()))
            if i == 0:
                settings.rotor_list = rotor
            else:
                settings.rotor_list += ',' + rotor
    
    settings.rotor_count = args.rotor_count
    settings.reflector = args.reflector
    settings.plugboard = args.plugboard
    
    settings.message = args.message.upper()
    settings.original_message_arr = list(settings.message)
    settings.message_arr = settings.original_message_arr.copy()
    if settings.plugboard:
        settings.message_arr = plugboard( settings )
    
    settings.rotor_offset = "W,X,C"
    settings.rotor_list = get_initial_rotors(settings.rotor_list)
    settings.rotor_list_save = settings.rotor_list.copy()
    settings.notch = get_notch(settings.rotor_list)
    
    settings.enciphered_message = ''
    
    return settings

def get_initial_rotors(rotor_list: str):
    rotors = rotor_list.split(',')
    init = [ROTOR_wiring[rotor] for rotor in rotors]
    return init



def get_notch(rotor_list):
    notch = []
    for rotor in rotor_list:
        notch.append(rotor[0])
        
    return notch



def encipher_char_reverse(settings: SimpleNamespace, char: str):
    abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    abc_index = abc.index(char)
    enciphered_char = ''
    reverse_rotor_list = settings.rotor_list[::-1]
    
    for rotor in reverse_rotor_list:
        enciphered_char = rotor[abc_index]
    
    return enciphered_char



def encipher_char(settings: SimpleNamespace, char: str):
    abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    abc_index = abc.index(char)
    enciphered_char = ''
    
    for rotor in settings.rotor_list:
        enciphered_char = rotor[abc_index]
    
    return enciphered_char



def rotate(settings: SimpleNamespace) -> list[str]:
    '''
        Explanation: 
            This function rotates the rotors by one position.
            The first rotor rotates everytime, the second rotor rotates when the first rotor is at the notch
            and so on. The last rotor rotates when the second rotor is at the notch.
            
            The rotor list isn't a fixed list, it could be any number of rotors.
        Parameters:
            settings: SimpleNamespace
        return:
            rotor_list: list[str]
    '''
    
    rotor_list = settings.rotor_list
    rotor_list[0] = rotor_list[0][-1:] + rotor_list[0][:-1]
    
    for i in range(1, len(rotor_list)):
        if rotor_list[i-1][0] == settings.notch[i-1]:
            rotor_list[i] = rotor_list[i][-1:] + rotor_list[i][:-1]
    
    return rotor_list



def plugboard( settings: SimpleNamespace ):
    message_arr = settings.message_arr
    
    for i in range(len(message_arr)):
        for plug in PLUGBOARD_wiring[settings.plugboard]:
            if message_arr[i] in plug:
                message_arr[i] = message_arr[i].replace(message_arr[i], plug[1])
    
    return message_arr



def reflector( settings: SimpleNamespace, char: str):
    abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    abc_index = abc.index(char)
    
    return REFLECTOR_wiring[settings.reflector][abc_index]



def set_rotor_offset( settings: SimpleNamespace ):
    '''
        Explanation:
            This function turns the rotors until the rotor offset is reached.
            This means that the rotor offset is the first letter that is shown on the rotor.
        Parameters:
            settings: SimpleNamespace
        return:
            settings
    '''
    def rotate_offset(rotor: str, rotor_index: int):
        offset = ord(settings.rotor_offset[i]) - 65
        return rotor[offset:] + rotor[:offset]
    
    i=0
    for rotor in settings.rotor_list:
        settings.rotor_list[i] = rotate_offset(rotor, i)
        
    return settings


if __name__ == '__main__':
    settings = get_system_settings()
    
    for char in settings.message_arr:
        enciphered_char = encipher_char(settings, char)
        enciphered_char = reflector(settings, enciphered_char)    
        enciphered_char = encipher_char_reverse(settings, enciphered_char)
    
        settings.rotor_list = rotate(settings)
        settings.enciphered_message += enciphered_char

    print(f'Original message:\t{"".join(settings.original_message_arr)}')
    print(f'Enciphered message:\t{settings.enciphered_message}')
    
    # Save the rotor list to a txt-file
    # Each rotor is printed to a new line
    file_path = '/home/hendrik/Documents/Github/General/Enigma/rotor_list.txt'
    
    with open(file_path, 'w') as f:
        f.write('Rotor list:\n')
        for rotor in settings.rotor_list_save:
            f.write(rotor+'\n')
        f.write('\n')
        f.write('Rotor offset:\n')
        f.write(settings.rotor_offset)
        f.write('\n')
        f.write('rotor_count:\n')
        f.write(str(settings.rotor_count))