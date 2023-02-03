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
    ROTOR_dict = {
        'ROTOR_I': 'EKMFLGDQVZNTOWYHXUSPAIBRCJ',
        'ROTOR_II': 'AJDKSIRUXBLHWTMCQGZNPYFVOE',
        'ROTOR_III': 'BDFHJLCPRTXVZNYEIWGAKMUSQO',
        'ROTOR_IV': 'ESOVPZJAYQUIRHXLNFTGKDCMWB',
        'ROTOR_V': 'VZBRGITYUPSDNHLXAWMJQOFECK',
        'ROTOR_VI': 'JPGVOUMFYQBENHZRDKASXLICTW',
        'ROTOR_VII': 'NZJHGRCXMYSWBOUFAIVLPEKQDT',
        'ROTOR_VIII': 'FKQHTLXOCBJSPDZRAMEWNIUYGV',
    }

    def __init__(self, rotors: str ) -> None:
        self.rotors = rotors
        self.rotor_list = self.get_rotor_list()

    def get_rotor_list(self):
        tmp = self.rotors.split(',')
        return [self.ROTOR_dict[x] for x in tmp]
    
    def at_notch(self, rotor: list) -> bool:
        if rotor[1].index(0) == rotor[1]:
            return True
        return False
    
    def step_rotors(self, rotor: list) -> None:
        pass
    
    def encipher(self, rotor_list_u: list, char: str) -> str:
        rotor_list = [x for x in rotor_list_u]
        enciphered_char = ''
        abc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        char_index = abc.index(char)
        
        for rotor in rotor_list:
            enciphered_char = rotor[char_index]
            print(f'enciphered_char: {enciphered_char}')
        
        
        return enciphered_char

def machine( rotor_list: str, message: str ) -> None:
    machine = ROTOR(rotor_list)
    message_arr = [char for char in message]
    
    m = ROTOR.encipher(machine, machine.rotor_list, 'A')
    
    
    

if __name__ == '__main__':
    rot_list = 'ROTOR_I,ROTOR_II,ROTOR_III'
    message = "HELLOXWORLD"
    
    machine(rot_list, message)
    