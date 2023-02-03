import argparse
import os

from types import SimpleNamespace
from pyenigma import enigma
from pyenigma import rotor

def clear_screen() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')
    
def set_help_text() -> SimpleNamespace:
    ht = SimpleNamespace() # helptext namespace
    ht.description = '''This program encrypts a message using the Enigma Machine'''
    ht.message = '''Message to encrypt'''
    
    return ht

def parse_args() -> str:
    ht = set_help_text()
    
    parser = argparse.ArgumentParser(description = ht.description, usage=argparse.SUPPRESS,
                formatter_class=lambda prog: argparse.HelpFormatter(
                    prog, max_help_position=80, width=80))
    parser.usage = 'example: python enigma.py --message <message to encipher>'
    
    parser.add_argument('-m', '--message', metavar='<message>', type=str,required=True, help=ht.message)
    args = parser.parse_args()
    
    message = args.message
    
    return message


def enigma_machine( message: str) -> None:
    engine = enigma.Enigma(rotor.ROTOR_Reflector_C, rotor.ROTOR_I,
                                rotor.ROTOR_II, rotor.ROTOR_III, key="WXC",
                                plugs="AV BS CG DL FU HZ IN KM OW RX")



    print(engine)
    input("Press Enter to continue...")
    clear_screen()
    
    message = engine.encipher( parse_args( ) )
    
    print(f'Enciphered message: {message}')
    

if __name__ == '__main__':
    message = parse_args( )
    
    enigma_machine( message )
    
    
    
    
    