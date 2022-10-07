import time
import board
import busio
import digitalio
import adafruit_scd4x

# SETUP SENSOR
scl = board.GP9
sda = board.GP8
i2c = busio.I2C(scl, sda)
scd4x = adafruit_scd4x.SCD4X(i2c)
print("Serial number:", [hex(i) for i in scd4x.serial_number])

# SETUP FANS
fan1 = digitalio.DigitalInOut(board.GP27)
fan1.direction = digitalio.Direction.OUTPUT
fan2 = digitalio.DigitalInOut(board.GP26)
fan2.direction = digitalio.Direction.OUTPUT

# SETUP HUMIDIFIER
humid = digitalio.DigitalInOut(board.GP15)
humid.direction = digitalio.Direction.OUTPUT

# SETUP LED
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

humid_target = 85
co2_target = 1000
record_freq = 10

sensor_pm_time = time.time()
print("getting sensor ready")
scd4x.start_periodic_measurement()

while not scd4x.data_ready:
    time.sleep(1)
    
time.sleep(120)

sensor_ready_time = time.time()
print("sensor ready: {} s".format(sensor_ready_time - sensor_pm_time))

humid_on_time = time.time()
humid_off_time = time.time()
fans_on_time = time.time()
fans_off_time = time.time()
humid_on_duration = 0
humid_off_duration = 0
fans_on_duration = 0
fans_off_duration = 0

while True:
    print("CO2: %d ppm" % scd4x.CO2)
    print("Temperature: %0.1f *C" % scd4x.temperature)
    print("Humidity: %0.1f %%" % scd4x.relative_humidity)
    # print("{} s".format(time.time() - sensor_ready_time))

    # humidifier
    if scd4x.relative_humidity <= humid_target:
        if humid.value == False:
            humid.value = True
            humid_on_time = time.time()
            humid_off_duration = time.time() - humid_off_time
        humid_on_duration = time.time() - humid_on_time
        print("Humidity ON: {} s; Last OFF: {} s".format(humid_on_duration, humid_off_duration))
    elif scd4x.relative_humidity > humid_target:
        if humid.value:
            humid.value = False
            humid_off_time = time.time()
            humid_on_duration = time.time() - humid_on_time
        humid_off_duration = time.time() - humid_off_time
        print("Humidity OFF: {} s; Last ON: {} s".format(humid_off_duration, humid_on_duration))
    
    # fan 1
    if scd4x.CO2 < co2_target:
        if fan1.value:
            fan1.value = False
            fans_off_time = time.time()
            fans_on_duration = time.time() - fans_on_time
        fans_off_duration = time.time() - fans_off_time
        print("Fans OFF: {} s; Last ON: {} s".format(fans_off_duration, fans_on_duration))
    elif scd4x.CO2 >= co2_target:
        if fan1.value == False:
            fan1.value = True
            fans_on_time = time.time()
            fans_off_duration = time.time() - fans_off_time
        fans_on_duration = time.time() - fans_on_time
        print("Fans ON: {} s; Last OFF: {} s".format(fans_on_duration, fans_off_duration))
        
    # fan 2 (both C02 and Humidity control)
    if fan1.value or humid.value:
        if fan2.value == False:
            fan2.value = True
    elif fan2.value:
        fan2.value = False
    print("--------------------")
    time.sleep(record_freq)

scd4x.stop_periodic_measurement()        
