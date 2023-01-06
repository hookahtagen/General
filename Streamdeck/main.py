import logging
from PIL import Image
from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper

ASSETS_PATH = '/home/hendrik/Document/General/Streamdeck/'
image_filename = 'test.png'

# Create a logger for....logging to the console
logger = logging.getLogger( __name__ )
logger.setLevel( logging.DEBUG )
handler = logging.StreamHandler( )
handler.setLevel( logging.DEBUG )
formatter = logging.Formatter( '%(asctime)s - %(name)s - %(levelname)s - %(message)s' )
handler.setFormatter( formatter )
logger.addHandler( handler )

deck = DeviceManager( ).enumerate( )

print( "Found {} Stream Deck(s).\n".format( len( deck ) ) )


for index, deck in enumerate( deck ):
    if not deck.is_visual( ):
        continue
    deck.open( )
    deck.reset( )

    print("Opened '{}' device ( serial number: '{}' )".format( deck.deck_type( ), deck.get_serial_number( ) ) )

    # Set initial screen brightness to 50%.
    deck.set_brightness( 100 )

    icon = Image.open( '/home/hendrik/Documents/General/Streamdeck/Assets/Red_Alert.gif' )
    icon = PILHelper.create_scaled_image(deck, icon)
    native_frame_image = PILHelper.to_native_format(deck, icon)
    icon = native_frame_image.tobytes( )

    deck.set_key_image( 1, icon )

is_running = True

def key_change_callback( deck, key, state ):
    global is_running
    print( f'key_change_callback: key={key}, state={state}' )
    with deck:
        # Reset deck, clearing all button images.
        deck.reset( )
        # Close deck handle, terminating internal worker threads.
        deck.close( )
        is_running = False

deck.set_key_callback( key_change_callback )

while is_running:
    pass