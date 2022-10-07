import time
import board
import busio
import adafruit_scd4x

start_time = time.time()

# SETUP SENSOR
scl = board.GP9
sda = board.GP8
i2c = busio.I2C(scl, sda)
scd4x = adafruit_scd4x.SCD4X(i2c)
print("Serial number:", [hex(i) for i in scd4x.serial_number])

sensor_pm_time = time.time()
print("getting sensor ready")
scd4x.start_periodic_measurement()

while not scd4x.data_ready:
    time.sleep(1)
    
time.sleep(120)

sensor_ready_time = time.time()
print("sensor ready: {} s".format(sensor_ready_time - sensor_pm_time))

while True:
    print("CO2: %d ppm" % scd4x.CO2)
    print("Temperature: %0.1f *C" % scd4x.temperature)
    print("Humidity: %0.1f %%" % scd4x.relative_humidity)
    print("{} s".format(time.time() - sensor_ready_time))
    time.sleep(10)
    
    