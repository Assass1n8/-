import RPi.GPIO as GP
import time


def two_binary(value):
    return [int(element) for element in bin(value)[2:].zfill(8)]


def num2dac(value):
    signal = two_binary(value)
    GP.output(dac, signal)
    return signal


def adc():
    raz = [0, 0, 0, 0, 0, 0, 0, 0]    
    for value in range(bits):
        raz[value] = 1
        GP.output(dac, raz)
        time.sleep(0.001)
        compValue = GP.input(comp)
        if compValue == 0:
            raz[value] = 0
        else:
            raz[value] = 1
    return raz[0] * 128 + raz[1] * 64 + raz[2] * 32 + raz[3] * 16 + raz[4] * 8 + raz[5] * 4 + raz[6] * 2 + raz[7] * 1


GP.setmode(GP.BCM)

dac = [26, 19, 13, 6, 5, 11, 9, 10]
leds = [21, 20, 16, 12, 7, 8, 25, 24]
bits = len(dac)
levels = 2**bits
maxVoltage = 3.3
comp = 4
troyka = 17


GP.setup(dac, GP.OUT)
GP.setup(leds, GP.OUT)
GP.setup(troyka, GP.OUT, initial = GP.HIGH)
GP.setup(comp, GP.IN)

try:
    while True:
        voltage = adc()
        print("voltage -> {:.2f}, code -> {}".format(voltage * maxVoltage / levels, voltage))
        number = round(bits/levels * voltage)
        GP.output(leds, two_binary(2**number-1))
        time.sleep(0.00001)

finally:
    GP.output(dac, 0)
    GP.cleanup()