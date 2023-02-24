from machine import ADC, Pin


def get_soil_moisture():
    soil = ADC(Pin(15))

    min_m = 0
    max_m = 65535

    moisture = (max_m - soil.read_u16()) * 100 / (max_m - min_m)
    print(" moisture : " + "%.2f" % moisture + " % (adc : " + str(soil.read_u16()) + ")")
    return moisture
