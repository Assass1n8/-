import RPi.GPIO as GP
import time


def two_binary(value):
    return [int(element) for element in bin(value)[2:].zfill(8)]


def num2dac(value):
    signal = two_binary(value)
    GP.output(dac, signal)
    return signal


def adc():
    for value in range(256):
        signal = num2dac(value)
        voltage = value / levels * maxVoltage
        time.sleep(0.05)
        compValue = GP.input(comp)
        if compValue == 0:
            print("Value = {:^3} -> {}, input voltage = {:.2f}".format(value, signal, voltage))
            break


GP.setmode(GP.BCM)

dac = [26, 19, 13, 6, 5, 11, 9, 10]
bits = len(dac)
levels = 2**bits
maxVoltage = 3.3
comp = 4
troyka = 17


GP.setup(dac, GP.OUT)
GP.setup(troyka, GP.OUT, initial = GP.HIGH)
GP.setup(comp, GP.IN)

try:
    while True:
        adc()

finally:
    GP.output(dac, 0)
    GP.cleanup()