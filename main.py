
import board
import neopixel

# STRAND controls a 30 pixel NeoPixel array attached by gator clips
# to ground, VIN, and STRAND_CONTROL_PIN
# Setting this up before cpx makes STRAND_CONTROL_PIN a capacative touch pin
STRAND_CONTROL_PIN = board.D9
STRAND_LENGTH = 30
STRAND = neopixel.NeoPixel(STRAND_CONTROL_PIN, STRAND_LENGTH, brightness=0.2, auto_write=False)

from adafruit_circuitplayground.express import cpx

# Configure the cpx

# Not too bright!
cpx.pixels.brightness = 0.3

# Set up the accelerometer to detect tapping
cpx.detect_taps = 1  # detect single tap only

cpx.red_led = True  # Turns the little LED next to USB on

cpx.play_file("Coin.wav")  # Play a coin sound on boot

# Values to impact colors displayed on NeoPixels
pixeln = 0  # Our counter for all 10 pixels
last_switch = cpx.switch  # Initial switch position



def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    max_value= 255
    if not (0 <= pos <= max_value):
        return PIXEL_OFF

    shift_at = 85
    secondary = int(3 * (pos % shift_at))
    primary = max_value - secondary

    if pos < shift_at:
        return (primary, secondary, 0)
    elif pos < (max_value - shift_at):
        return (0, primary, secondary)
    else:
        return (secondary, 0, primary)


while True:

    if cpx.tapped:     # Look for a single tap
        cpx.play_file("Coin.wav")
        cpx.red_led = not cpx.red_led

    # This math makes a 'comet' of swirling rainbow colors!
    for p in range(10):
        step = int((pixeln + p) % 10)
        color = wheel(25 * step)
        conf = [int(c * ((10 - step) / 10.0)) for c in color]
        cpx.pixels[p] = conf
        STRAND[p] = conf
        STRAND[p + 10] = conf
        STRAND[p + 20] = conf

    STRAND.show()

    # Each time 'round we tick off one pixel at a time
    if cpx.switch:      # depending on the switch we'll go clockwise
        pixeln += 1
        if pixeln > 9:
            pixeln = 0
    else:               # or counter clockwise
        pixeln -= 1
        if pixeln < 0:
            pixeln = 9

    # Depending on the buttons, make it dimmer
    if cpx.button_a:
        print("Button A pressed")
        cpx.pixels.brightness = 0.1
    # or brighter!
    if cpx.button_b:
        print("Button B pressed")
        cpx.pixels.brightness = 0.5
    # neither buttons pressed
    if not cpx.button_a and not cpx.button_b:
        cpx.pixels.brightness = 0.3

    # Check the switch
    if cpx.switch:
        if last_switch != cpx.switch: # if it moved, print it out
            print("Switch moved left")
    else:
        if last_switch != cpx.switch:
            print("Switch moved right")
    last_switch = cpx.switch


    # loop to the beginning!