import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
import requests
from RPLCD.i2c import CharLCD

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

greenPin = 21
redpin=20
relaypin=16

def printdisplay(data):
    lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=2, dotsize=8)
    lcd.clear()
    lcd.write_string(str(data))
    time.sleep(2)
    lcd.clear()


def relay():
    GPIO.setup(relaypin, GPIO.OUT)
    GPIO.output(relaypin,1)
    time.sleep(1)
    GPIO.output(relaypin,0)



def green():
    GPIO.setup(greenPin, GPIO.OUT)
    print("LED on")
    GPIO.output(greenPin, 1)
    time.sleep(1)
    print("LED off")
    GPIO.output(greenPin, 0)
    

def red():
    GPIO.setup(redpin, GPIO.OUT)
    print("LED on")
    GPIO.output(redpin, 1)
    time.sleep(1)
    print("LED off")
    GPIO.output(redpin, 0)

def writerr_api(rfid, user):
    API_URL = 'http://192.168.97.26:7000/api/v1/writeRfid'
    form_data = {
        'rfidno': rfid,
        'user': user,
    }
    response = requests.post(API_URL, data=form_data)
    print(response.text)

def readerr_api(rfid, device):
    API_URL = 'http://192.168.97.26:7000/api/v1/readRfid'
    form_data = {
        'rfidno': rfid,
        'device': device,
    }
    response = requests.post(API_URL, data=form_data)
    print(response.text)
    if response.text.startswith("in") or response.text.startswith("out"):
        green()
        printdisplay(str(response.text))
        relay()
        GPIO.cleanup(relaypin)

        # GPIO.output(relaypin, 0)
    else:
        red()
        printdisplay(str(response.text))
        


def read_db_write():
    reader = SimpleMFRC522()
    try:
        print("Hold an RFID card near the reader...")
        id, text = reader.read()
        print("Card ID:", id)  
        # print("Data:", text)
        name=input("enter the name >")

        writerr_api(id,name)
       
       
    finally:
        # GPIO.cleanup()
        pass


def read_card_and_process():
    reader = SimpleMFRC522()
    try:
        print("Hold an RFID card near the reader...")
        id, text = reader.read()
        print("Card ID:", id)
        print("Data:", text)
        readerr_api(id, 2)
    except KeyboardInterrupt:
        pass
    finally:
        # GPIO.cleanup()
        pass


# def write_rfid(data):
#     reader = SimpleMFRC522()
#     try:
#         print("Hold an RFID card near the reader to write data...")
#         reader.write(data)
#         print("Data written successfully.")
#     finally:
#         GPIO.cleanup()

try:
    while True:
        read_card_and_process()
        # read_db_write()
        time.sleep(2)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()

