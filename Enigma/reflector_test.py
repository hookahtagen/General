arepl_filter = "reflector", "text", "result"

class test:
    def __init__(self, text: str):
        self.text = self.rotate(text)
        
    def rotate(self, rotor: str):
        print("unrotated:\t"+rotor)
        rotor = rotor[-1:] + rotor[:-1]
        print("rotated:\t"+rotor)
        return rotor

text = 'EKMFLGDQVZNTOWYHXUSPAIBRCJ'

t = test(text)

#print(f'rotated:\t{result}')