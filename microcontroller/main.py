import network
import time
import creds
import urequests
import dht11
import soil_moisture
import ujson


def connect_wifi():
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
            time.sleep(1)

    if wifi.isconnected():
        print('Connected')
    else:
        print('Timed Out')

    return wifi


def get_data():
    temperature, humidity = dht11.get_temp_hum()
    #soil_m = soil_moisture.get_soil_moisture()

    post_data = ujson.dumps({'temperature': temperature, 'humidity': humidity, 'soil_moisture': 50 , 'farm': 'Puma Farm', 'crop': 'Maize'})
    request_url = creds.endpoint + '/weather'
    print(request_url)
    try:
        res = urequests.post(request_url, headers={'content-type': 'application/json'}, data=post_data)
        print(res.json)
    except Exception as e:
        print(e)


def main():
    wifi = connect_wifi()
    if wifi.isconnected():
        while True:
            get_data()
            time.sleep(20)


main()