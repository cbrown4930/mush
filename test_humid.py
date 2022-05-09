import time
import board
import digitalio

humid = digitalio.DigitalInOut(board.GP15)
humid.direction = digitalio.Direction.OUTPUT
fan2 = digitalio.DigitalInOut(board.GP26)
fan2.direction = digitalio.Direction.OUTPUT
fan2.value = True
humid.value = True
time.sleep(10)
humid.value = False
fan2.value = False