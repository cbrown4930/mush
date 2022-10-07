import time
import logging
from logging.handlers import RotatingFileHandler

import smbus
from gpiozero import LED

import adafruit_sht31d
import board

# SETUP SENSOR
i2c = board.I2C()
sens = adafruit_sht31d.SHT31D(i2c)

# SETUP FAN
fan1 = LED(25)
fan = False

# SETUP HUMIDIFIER
humid = LED(24)

humid_target = 85
fan_on_target = 60
fan_off_target = 600
record_freq = 60

humid_on_time = time.time()
humid_off_time = time.time()
fans_on_time = time.time()
fans_off_time = time.time()
humid_on_duration = 0
humid_off_duration = 0
fans_on_duration = 0
fans_off_duration = 0
humid_last_on = 0
humid_last_off = 0
fans_last_on = 0
fans_last_off = 0

log_handler = RotatingFileHandler("fruit.log", mode="W", maxBytes=1*1024*1024)
logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.DEBUG,
    handlers=[log_handler],
)

while True:

    logging.info(sens.temperature)
    logging.info(sens.relative_humidity)
    # humidifier
    if sens.relative_humidity <= humid_target:
        if not humid.value:
            humid.on()
            humid_on_time = time.time()
            humid_last_off = time.time() - humid_off_time
        humid_on_duration = time.time() - humid_on_time
        logging.info(
            "Humidity ON: {} s; Last OFF: {} s".format(
                humid_on_duration, humid_last_off
            )
        )
    elif sens.relative_humidity > humid_target:
        if humid.value:
            humid.off()
            humid_off_time = time.time()
            humid_last_on = time.time() - humid_on_time
        humid_off_duration = time.time() - humid_off_time
        logging.info(
            "Humidity OFF: {} s; Last ON: {} s".format(
                humid_off_duration, humid_last_on
            )
        )

    # fan 1
    if fan:
        fans_on_duration = time.time() - fans_on_time
        # do I need to turn off?
        if fans_on_duration >= fan_on_target and not humid.value:
            fan1.off()
            fans_off_time = time.time()
            fans_last_on = fans_on_duration
            fans_on_duration = 0
            fan = False
    else:
        fans_off_duration = time.time() - fans_off_time
        # do I need to turn on?
        if fans_off_duration >= fan_off_target or humid.value:
            fan1.on()
            fans_on_time = time.time()
            fans_last_off = fans_off_duration
            fans_off_duration = 0
            fan = True
    logging.info(
        "Fans {}: time on {:.1f}; time off {:.1f}; last on {:.1f}; last off: {:.1f}".format(
            fan,
            fans_on_duration,
            fans_off_duration,
            fans_last_on,
            fans_last_off,
        )
    )

    time.sleep(record_freq)
