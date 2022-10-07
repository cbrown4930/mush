import time
import board
import digitalio

fan1 = digitalio.DigitalInOut(board.GP27)
fan1.direction = digitalio.Direction.OUTPUT
fan1.value = True
time.sleep(10)
fan1.value = False