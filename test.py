
def double_string_chars(string):
    return ''.join([char * 2 for char in string])

result = double_string_chars('hello')

print(result)
