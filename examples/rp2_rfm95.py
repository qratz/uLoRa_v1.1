# Sample application using the Raspberry Pi Pico with a HopeRF RFM95W module (SX1276)


import utime
from machine import I2C, Pin, deepsleep
import ubinascii
import ujson
from ulora.ulora import TTN, uLoRa

# SPI1 on Raspberry Pi Pico with arbitrary GPIOs for IRQ, RST
LORA_SPIPORT = const(1)
LORA_CS = const(13)
LORA_SCK = const(14)
LORA_MOSI = const(15)
LORA_MISO = const(12)
LORA_IRQ = const(20)
LORA_RST = const(10)
LORA_FPORT = const(1)
# default Data rate for EU868 OTAA
LORA_DATARATE = "SF9BW125"

DEVADDR = "00000000"
NWKEY = "00000000000000000000000000000000"
APPKEY = "00000000000000000000000000000000"

# The Things Network (TTN) device details (available in TTN console)
# TTN device address, 4 Bytes, MSB (REPLACE WITH YOUR OWN!!!)
TTN_DEVADDR = bytearray(ubinascii.unhexlify(DEVADDR))
# TTN network session key, 16 Bytes, MSB (REPLACE WITH YOUR OWN!!!)
TTN_NWKEY = bytearray(ubinascii.unhexlify(NWKEY))
# TTN application session key, 16 Bytes, MSB (REPLACE WITH YOUR OWN!!!)
TTN_APP = bytearray(ubinascii.unhexlify(APPKEY))

TTN_CONFIG = TTN(TTN_DEVADDR, TTN_NWKEY, TTN_APP, country="EU")

# Additional configurations
PROGRAM_LOOP_MS = const(600000)
PROGRAM_WAIT_MS = const(3000)
# Onboard LED
LED_PIN = const(25)

def main():
    start_time = utime.ticks_ms()
    # Turn LED for the duration of the program
    led = Pin(LED_PIN, Pin.OUT, value=1)
    # LoRaWAN / TTN send
    spi = machine.SPI(
        LORA_SPIPORT,
        baudrate=4000000,
        polarity=0,
        phase=0,
        sck=machine.Pin(LORA_SCK),
        mosi=machine.Pin(LORA_MOSI),
        miso=machine.Pin(LORA_MISO)
    )
    lora = uLoRa(
        spi_device = spi,
        cs=LORA_CS,
        irq=LORA_IRQ,
        rst=LORA_RST,
        ttn_config=TTN_CONFIG,
        datarate=LORA_DATARATE,
        fport=LORA_FPORT
    )
    data = ubinascii.hexlify("01")
    print("Sending packet...", lora.frame_counter, ubinascii.hexlify(data))
    lora.send_data(data, len(data), lora.frame_counter)
    print(len(data), "bytes sent!")
    lora.frame_counter += 1
    utime.sleep(3)
    #deepsleep(PROGRAM_LOOP_MS - (utime.ticks_ms() - start_time))

if __name__ == "__main__":
    main()

