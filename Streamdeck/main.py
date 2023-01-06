from PIL import Image, ImageSequence
from StreamDeck.DeviceManager import DeviceManager

import cv2

deck = DeviceManager( ).enumerate( )

print( "Found {} Stream Deck(s).\n".format( len( deck ) ) )

for index, deck in enumerate( deck ):
    if not deck.is_visual( ):
        continue
    deck.open( )
    deck.reset( )

    print("Opened '{}' device ( serial number: '{}' )".format( deck.deck_type( ), deck.get_serial_number( ) ) )

# Set initial screen brightness to 50%.
deck.set_brightness( 50 )


deck.set_key_image( 0, cv2.imread( "Exit.png" ) )

while True:
    pass