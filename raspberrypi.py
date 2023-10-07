import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
import requests
import threading
from RPLCD.i2c import CharLCD
from pad4pi import rpi_gpio

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)



KEYPAD = [
    [1, 2, 3, "A"],
    [4, 5, 6, "B"],
    [7, 8, 9, "C"],
    ["*", 0, "#", "D"]
]

ROW_PINS = [5, 6, 13, 19] # BCM numbering
COL_PINS = [26, 17, 27, 22] # BCM numbering

greenPin = 21
redpin=20
relaypin=16







def printdisplay(data):
    try:
        lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=2, dotsize=8)
        lcd.clear()
        lcd.write_string(str(data))
        time.sleep(1)
        lcd.clear()
    except:
        pass

def displayInitial(data):
    try:
        lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=2, dotsize=8)
        lcd.clear()
        lcd.write_string(str(data))
    except:
        pass
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

def relay():
    GPIO.setup(relaypin, GPIO.OUT)
    GPIO.output(relaypin,1)
    time.sleep(1)
    GPIO.output(relaypin,0)





def writerr_api(rfid,user,age,phoneNum,roomNum,adharNum,location):
    API_URL = 'http://192.168.50.95:7000/api/v1/writeRfid'
    form_data = {
        'rfidno': rfid,
        'user': user,
        'age':age,
        'phoneNum':phoneNum,
        'roomnum':roomNum,
        'adharNum':adharNum,
        'location':location,
    }
    response = requests.post(API_URL, data=form_data)
    print(response.text)

def readerr_api(rfid, device):
    API_URL = 'http://192.168.50.95:7000/api/v1/readRfid'
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

        
    else:
        red()
        printdisplay(str(response.text))

def pin_verify(pin):
    API_URL = 'http://192.168.50.95:7000/api/v1/pinverify'
    form_data = {
        'pin': pin,
        
    }
    response = requests.post(API_URL, data=form_data)
    print(response.text)
    if response.text=="success":
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
        user=input("enter the name > ")
        age=int(input("enter the age > "))
        phoneNum=input("enter the phonenum > ")
        roomNum=input("enter the roomNum > ")
        adharNum=input("enter the adharNum > ")
        location=input("enter the location > ")

        writerr_api(id,user,age,phoneNum,roomNum,adharNum,location)
       
    finally:
        # GPIO.cleanup()
        pass


def read_card_and_process():
    reader = SimpleMFRC522()
    try:
        displayInitial("RFID card here")
        id, text = reader.read()
        print("Card ID:", id)
        print("Data:", text)
        readerr_api(id, 2)
    except KeyboardInterrupt:
        pass
    finally:
        # GPIO.cleanup()
        pass


    
str_list = []

def print_key(key):
    global str_list
    if key=='C':
        result = "".join(str_list)
        printdisplay(result+"  verify")
        
        pin_verify(result)
        displayInitial("hold rfid here")
        str_list=[]
    else:  
        print(f"Received key from interrupt:: {key}")
        str_list.append(str(key))
        result = "".join(str_list)
        printdisplay(result)
        
        




def tt1():
    try:
        while True:
            read_card_and_process()
            #read_db_write()
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
      GPIO.cleanup()

def tt2():

    try:
        factory = rpi_gpio.KeypadFactory()
        keypad = factory.create_keypad(keypad=KEYPAD,row_pins=ROW_PINS, col_pins=COL_PINS) # makes assumptions about keypad layout and GPIO pin numbers

        keypad.registerKeyPressHandler(print_key)

        print("Press buttons on your keypad. Ctrl+C to exit.")
        while True:
           time.sleep(1)
    except KeyboardInterrupt:
        print("Goodbye")
    finally:
        keypad.cleanup()


thread1 = threading.Thread(target=tt1)
thread2 = threading.Thread(target=tt2)

# Start the threads
thread1.start()
thread2.start()

# if thread1.is_alive() and thread2.is_alive():
#     print("Thread 1 is running.")