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

if __name__ == "__main__":
    number = 3549
    getRoman(number)
    
    print(f'The roman value of {number} is: {getRoman(number)}')