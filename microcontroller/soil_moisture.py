from machine import ADC, Pin


def get_soil_moisture():
    soil = ADC(Pin(34))
    soil.atten(ADC.ATTN_11DB)
    min_m = 17000
    max_m = 40000
    moisture = (max_m - soil.read_u16()) * 100 / (max_m - min_m)
    return float(moisture)