def enigma( char: str):
    '''
        Explanation:
            This function takes a single character as input and passes
            it through the three rotors and the reflector.
        Parameters:
            char: str - The character to be enciphered
        Returns:
            enciphered_char: str - The enciphered character
    '''
    machine = {
        'ABC':       'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
        'ROTOR_I':   'EKMFLGDQVZNTOWYHXUSPAIBRCJ',
        'ROTOR_II':  'AJDKSIRUXBLHWTMCQGZNPYFVOE',
        'ROTOR_III': 'BDFHJLCPRTXVZNYEIWGAKMUSQO',
        'REFLECTOR': 'YRUHQSLDPXNGOKMIEBFZCWVJAT',
    }
    enciphered_char = ''
    
    abc_index = machine['ABC'].index(char)
    rotor_i_index = machine['ROTOR_I'].index()
    
    return rotor_i_index
    
enciphered_char = enigma( 'A' )
print(f'Enciphered char: {enciphered_char}')