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
    settings = SimpleNamespace()

    settings.rotor_list = "ROTOR_I,ROTOR_II,ROTOR_III"
    settings.reflector = "REFLECTOR_A"
    settings.plugboard = "PLUGBOARD_A"
    
    settings.message = "THERUSSIANSARECOMING"
    settings.original_message_arr = list(settings.message)
    settings.message_arr = settings.original_message_arr.copy()
    if settings.plugboard:
        settings.message_arr = plugboard( settings )
    
    settings.rotor_offset = "W,X,C"
    settings.rotor_list = get_initial_rotors(settings.rotor_list)
    settings.notch = get_notch(settings.rotor_list)
    
    settings.enciphered_message = ''

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
    def rotate_offset(rotor: str, rotor_index: int):
        offset = ord(settings.rotor_offset[i]) - 65
        return rotor[offset:] + rotor[:offset]
    
    i=0
    for rotor in settings.rotor_list:
        rotate_offset(rotor, i)
        i += 1
    
    pass

if __name__ == '__main__':
    settings = SimpleNamespace()

    settings.rotor_list = "ROTOR_I,ROTOR_II,ROTOR_III"
    settings.reflector = "REFLECTOR_A"
    settings.plugboard = "PLUGBOARD_A"
    
    settings.message = "THERUSSIANSARECOMING"
    settings.original_message_arr = list(settings.message)
    settings.message_arr = settings.original_message_arr.copy()
    if settings.plugboard:
        settings.message_arr = plugboard( settings )
    
    settings.rotor_offset = "W,X,C"
    settings.rotor_list = get_initial_rotors(settings.rotor_list)
    settings.notch = get_notch(settings.rotor_list)
    
    settings.enciphered_message = ''
    
    for char in settings.message_arr:
        #print(f'Enciphered char1: {char}')
        enciphered_char = encipher_char(settings, char)
        #print(f'Enciphered char2: {enciphered_char}')
        enciphered_char = encipher_char_reverse(settings, enciphered_char)
        #print(f'Enciphered char3: {enciphered_char}\n')
        settings.rotor_list = rotate(settings)
        settings.enciphered_message += enciphered_char

    print(f'Original message:\t{"".join(settings.original_message_arr)}')
    print(f'Enciphered message:\t{settings.enciphered_message}')