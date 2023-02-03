'''
    Author:     Hendrik Siemens
    Date:       2023-02-02
    Version:    0.1
    
    Description:
        This program is a simple generator for enigma rotors.
        It generates a random rotor and checks if it is a valid rotor.
        A valid rotor is a rotor that has no duplicate letters.   
        The program also checks that no rotor is the same as another rotor. 
'''

import random as rnd
import string

def getRoman(number):
    num = [1, 4, 5, 9, 10, 40, 50, 90,
        100, 400, 500, 900, 1000]
    sym = ["I", "IV", "V", "IX", "X", "XL",
        "L", "XC", "C", "CD", "D", "CM", "M"]
    i = 12
    roman_number = ''
      
    while number:
        div = number // num[i]
        number %= num[i]
  
        while div:
            roman_number += sym[i]
            #;print(sym[i], end = " ")
            #print('\n')
            div -= 1
        i -= 1
        
    return roman_number

def generate_rotor() -> str:
    '''
        Explanation:
            This function generates a random rotor.
        Parameters:
            None
        Return:
            rotor: str
    '''
    rotor = list(string.ascii_uppercase)
    rnd.shuffle(rotor)
    rotor = ''.join(rotor)
    
    return rotor

def validate_rotor(rotor: str) -> bool:
    '''
        Explanation:
            This function checks if a rotor is valid.
            A valid rotor is a rotor that has no duplicate letters.
        Parameters:
            rotor: str
        Return:
            valid: bool
    '''
    valid = True
    for letter in rotor:
        if rotor.count(letter) > 1:
            valid = False
    
    return valid

def validate_rotor_list(rotor_list: str) -> list[str]:
    '''
        Explanation:
            This function checks if a rotor list is valid.
            A valid rotor list is a list of rotors that has no duplicate rotors.
        Parameters:
            rotor_list: str
        Return:
            valid_rotors: list[str]
    '''
    valid_rotors = []
    for rotor in rotor_list.split('\n'):
        if rotor not in valid_rotors:
            valid_rotors.append(rotor)
    
    return valid_rotors


if __name__ == '__main__':
    rotor_amount = int(input("How many rotors do you want to generate? "))
    rotor_list = ''
    
    for i in range(rotor_amount):
        rotor = generate_rotor()
        while not validate_rotor(rotor):
            rotor = generate_rotor()
        
        rotor_list += rotor + '\n'
    
    valid_rotors = validate_rotor_list(rotor_list)
    print(f'Generated rotors:\n')
    for rotor in valid_rotors:
        print(rotor)
    print('\n\n')
    save_file: bool = input("Do you want to save the rotors to a file? (y/n) ").lower() == 'y'
    
    if save_file:
        file_name = input("Enter file name: ")
        with open('/home/hendrik/Documents/Github/General/Enigma/'+file_name, 'w') as file:
            i = 0
            for rotor in valid_rotors:
                n = getRoman(i+1)
                file.write(f'Rotor_{n}:'+rotor+'\n')
                i += 1
                
    