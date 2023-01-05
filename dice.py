import sys
import os
import random

def roll_dice( ) -> None:
    dice = random.randint( 1, 6 )
    print( f'You rolled a { dice }' )
    return

def get_num() -> None:
    random_num = random.randint( 1, 6 )
    print( f'Your number is { random_num }' )
    print(sys.argv)
    print(len(sys.argv))
    return


if sys.argv == 1:
    a=1
else:
    roll_dice()
    get_num( )