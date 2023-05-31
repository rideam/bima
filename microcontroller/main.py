import network
import time
import creds
import urequests
import dht11
import soil_moisture
import ujson


def connect_wifi():
    """connect to Wifi"""
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(creds.ssid, creds.pwd)

    timeout = 6
    delay = 0
    if not wifi.isconnected():
        print('connecting ..')
        while not wifi.isconnected() and delay < timeout:
            print(timeout - delay)
            delay = delay + 1
            time.sleep(2)

    if wifi.isconnected():
        print('Wifi Connected')
    else:
        print('Connection Timed Out')
    return wifi


def get_data():
    """Get data from sensors """
    temperature, humidity = dht11.get_temp_hum()
    soil_m = soil_moisture.get_soil_moisture()

    post_data = ujson.dumps({
        'temperature': temperature,
        'humidity': humidity,
        'soil_moisture': soil_m,
        'farm': 'Puma Farm',
        'crop': 'Maize',
        'user': creds.wallet
    })
    request_url = creds.endpoint + '/weather'
    try:
        print('Temperature: %3.1f C' % temperature)
        print('Humidity: %3.1f %%' % humidity)
        print('Soil Moisture: %3.1f %%' % soil_m)
        res = urequests.post(request_url, headers={'content-type': 'application/json'}, data=post_data)
        print(f'\nData posted successfully')
    except Exception as e:
        print(f'\nError posting data {e}')


def main():
    wifi = connect_wifi()
    if wifi.isconnected():
        while True:
            get_data()
            time.sleep(7200)  # sleep for 2 hours


main()

