import argparse
import os

from types import SimpleNamespace

PLUGBOARD_wiring = {
            'PLUGBOARD_A': 'AV BS CG DL FU HZ IN KM OW RX',
            'PLUGBOARD_B': 'AJ BX CH EM FY IS LW OT DV KQ',
            'PLUGBOARD_C': 'AR BD CO EJ FN GT HK IV LM PW',
            'PLUGBOARD_D': 'AE BN CK DQ FU GY HW IJ LO MP'
        }

REFLECTOR_wiring = {
            'REFLECTOR_A': 'EJMZALYXVBWFCRQUONTSPIKHGD',
            'REFLECTOR_B': 'YRUHQSLDPXNGOKMIEBFZCWVJAT',
            'REFLECTOR_C': 'FVPJIAOYEDRZXWGCTKUQSBNMHL',
            'REFLECTOR_D': 'ENKQAUYWJICOPBLMDXZVFTHRGS'
        }

def clear_screen() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

def get_system_vars() -> argparse.Namespace:
    helptext_dict = {
        'help_message': '''Message to be encrypted''',
        'help_rotor_count': '''Number of rotors to be used''',
        'help_rotor_list': '''List of rotors to be used, separated by commas. 
                              Pass the rotors in the order you want them to be used.''',
    }
    
    parser = argparse.ArgumentParser(description = '#TODO', usage=argparse.SUPPRESS,
                formatter_class=lambda prog: argparse.HelpFormatter(
                    prog, max_help_position=80, width=80))
    
    parser.add_argument('-m', '--message', metavar='', type=str, default='default', required=True, help=helptext_dict['help_message'])
    
    eg = parser.add_argument_group('Enigma Setup Options', 'Setup options for the Enigma Machine')
    eg.add_argument('-rc', '--rotor_count', metavar='', type=int, default=3, required=True ,help=helptext_dict['help_rotor_count'])
    eg.add_argument('-rls', '--rotor_list_s', metavar='', type=str, default='ROTOR_I,ROTOR_II,ROTOR_III', required=True, help=helptext_dict['help_rotor_list'])
    eg.add_argument('-rr', '--random_rotor', metavar='', type=int, default=False, required=False, help=helptext_dict['help_rotor_list'])
    
    return parser.parse_args( )
    
    
class ROTOR:
    ROTOR_names = [
        'ROTOR_I',
        'ROTOR_II',
        'ROTOR_III',
        'ROTOR_IV',
        'ROTOR_V',
        'ROTOR_VI',
        'ROTOR_VII',
        'ROTOR_VIII',
        'ROTOR_BETA',
        'ROTOR_GAMMA',
        'ROTOR_B',
        'ROTOR_C',
        'ROTOR_B_THIN'
    ]
    ROTOR_wiring = [     
       #'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        'EKMFLGDQVZNTOWYHXUSPAIBRCJ',
        'AJDKSIRUXBLHWTMCQGZNPYFVOE',
        'BDFHJLCPRTXVZNYEIWGAKMUSQO',
        'ESOVPZJAYQUIRHXLNFTGKDCMWB',
        'VZBRGITYUPSDNHLXAWMJQOFECK',
        'JPGVOUMFYQBENHZRDKASXLICTW',
        'NZJHGRCXMYSWBOUFAIVLPEKQDT',
        'FKQHTLXOCBJSPDZRAMEWNIUYGV',
        'LEYJVCNIXWPBQMDRTAKZGFUHOS',
        'FSOKANUERHMBTIYCWLQPZXVGJD',
        'ENKQAUYWJICOPBLMDXZVFTHRGS',
        'RDOBJNTKVEHMLFCWZAXGYIPSUQ',
        'ALBEVFCYODJWUGNMQTZSKPRHXI'
    ]
    
    def __init__(self, rotor: list[str]):
        self.init_rotor = rotor
        self.rotor_list = []
        self.start_rotor()
    
    def start_rotor(self):
        for i in self.init_rotor:
            self.rotor_list.append(self.ROTOR_wiring[self.ROTOR_names.index(i)])
    
    def rotate(self, settings: SimpleNamespace):
        rotor, rotor_cmp = settings.rotor_list, settings.rotor_list
        


        print(settings.rotor_list)

def process_char(settings: SimpleNamespace, char: str, rotor: ROTOR):
    '''
        Explanation:
            This function takes a single character and passes it through a single rotor.
            The resulting char is the char that would be outputted by the rotor.
        Parameters:
            char: str - The character to be processed
            rotor: str - The rotor to be used
        Returns:
    '''
    abc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    enciphered_char = ''
    
    abc_index = abc.index(char)
    
    return enciphered_char

def machine( settings: SimpleNamespace):
    ROTOR = settings.rotor
    message_arr = settings.message_arr # just used as a backup variable :)
    enciphered_message: str = ''
    
    for char in message_arr:
        for rotor in settings.rotor.rotor_list:
            enciphered_char = process_char(settings, char, rotor)
            enciphered_message += enciphered_char
        ROTOR.rotate(settings)
    
    return enciphered_message

if __name__ == '__main__':
    args = get_system_vars()
    
    settings = SimpleNamespace()
    
    settings.message = args.message
    settings.message_arr = list(settings.message)
    
    settings.rotor_count = args.rotor_count
    settings.rotor_list_s = args.rotor_list_s.split(',')
    
    settings.rotor = ROTOR(settings.rotor_list_s)
    settings.rotor_list = settings.rotor.rotor_list
     
    message = machine( settings )
    print(f'Rotor List: {settings.rotor_list}')
