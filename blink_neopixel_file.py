import time

import board
import digitalio

import lib.neopixel as neopixel  # RGB LED

neopwr: digitalio.DigitalInOut = digitalio.DigitalInOut(board.NEO_PWR)
neopwr.switch_to_output(value=True)
neopixel: neopixel.NeoPixel = neopixel.NeoPixel(
    board.NEOPIX, 1, brightness=0.2, pixel_order=neopixel.GRB
)
neopixel[0] = (0, 0, 255)


for x in range(5):
    neopixel[0] = (0, 0, 0)
    time.sleep(0.5)
    neopixel[0] = (0, 0, 255)
    time.sleep(0.5)
