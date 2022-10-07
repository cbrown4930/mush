import time
import board
import digitalio

fan2 = digitalio.DigitalInOut(board.GP26)
fan2.direction = digitalio.Direction.OUTPUT
fan2.value = True
time.sleep(10)
fan2.value = False