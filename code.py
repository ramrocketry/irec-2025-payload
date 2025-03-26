# Importing Libraries
import time
import board
import busio
import analogio
import adafruit_bmp3xx
import adafruit_sgp40
import adafruit_hts221
import adafruit_register
import sys

# I2C Bus setup
i2c_bus = busio.I2C(board.SCL, board.SDA)

# Initialize BMP390 sensor
try:
    bmp390 = adafruit_bmp3xx.BMP3XX_I2C(i2c_bus)
    print("BMP390 sensor initialized successfully.")
except ValueError as e:
    bmp390 = None
    print("BMP390 initialization failed:", e)

# Initialize SGP40 sensor
try:
    sgp40 = adafruit_sgp40.SGP40(i2c_bus)
    print("SGP40 sensor initialized successfully.")
except ValueError as e:
    sgp40 = None
    print("SGP40 initialization failed:", e)

# Initialize HTS221 sensor
try:
    hts221 = adafruit_hts221.HTS221(i2c_bus)
    print("HTS221 sensor initialized successfully.")
except ValueError as e:
    hts221 = None
    print("HTS221 initialization failed:", e)


def read_bmp390():
    """
    Read BMP390 sensor data
    Returns temperature in Celsius and pressure in hPa
    """
    if bmp390:
        temperature = bmp390.temperature
        pressure = bmp390.pressure
        return temperature, pressure
    else:
        return None, None


def read_sgp40():
    """
    Read SGP40 sensor data (Air Quality Index - Raw)
    Returns air quality index (AQI)
    """
    if sgp40:
        aqi = sgp40.raw
        return aqi
    else:
        return None


def read_hts221():
    """
    Read HTS221 sensor data
    Returns humidity in % and temperature in Celsius
    """
    if hts221:
        humidity = hts221.relative_humidity
        temperature = hts221.temperature
        return humidity, temperature
    else:
        return None, None


def startup():
    print("Starting in 5", end="")
    time.sleep(1)
    write = sys.stdout.write
    write("\b \b")
    print("4", end="")
    time.sleep(1)
    write = sys.stdout.write
    write("\b \b")
    print("3", end="")
    time.sleep(1)
    write = sys.stdout.write
    write("\b \b")
    print("2", end="")
    time.sleep(1)
    write = sys.stdout.write
    write("\b \b")
    print("1", end="")
    time.sleep(1)
    write = sys.stdout.write
    write("\b \b")
    for i in range(1, 6):
        print("")


def main():
    print(board.board_id)
    startup()
    while True:
        # Read BMP390 data
        temp_bmp, pressure = read_bmp390()
        # Read SGP40 data
        aqi = read_sgp40()
        # Read HTS221 data
        humidity, temp_hts = read_hts221()
        if temp_bmp is not None and temp_hts is not None:
            temp_final = (9 / 5) * (
                temp_bmp + temp_hts
            ) / 2 + 32  # take average of the two measurements

        if temp_final is not None and pressure is not None:
            print(f"Temperature             = {temp_final:.2f} Fahrenheit")
            print(f"Pressure                = {pressure:.2f} hPa")
        else:
            print("BMP390: Sensor not initialized")

        if aqi is not None:
            print(f"Air Quality Index (RAW) = {aqi}")
        else:
            print("SGP40: Sensor not initialized")

        if humidity is not None and temp_hts is not None:
            print(f"Humidity                = {humidity:.2f}%")
        else:
            print("HTS221: Sensor not initialized")

        print("-" * 45)
        time.sleep(0.1)


# Run the main loop
if __name__ == "__main__":
    main()
