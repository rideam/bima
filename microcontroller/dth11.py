from machine import Pin
import dht


def get_temp_hum():
    sensor = dht.DHT11(Pin(5))
    try:
        sensor.measure()
        t = sensor.temperature()
        h = sensor.humidity()
        return t, h
    except OSError as e:
        print('Sensor Reading Failed')

