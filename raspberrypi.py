import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
import requests
import threading
from RPLCD.i2c import CharLCD
from pad4pi import rpi_gpio
import subprocess
import multiprocessing
import os

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

url='http://192.168.83.95:7000'

KEYPAD = [
    [1, 2, 3, "A"],
    [4, 5, 6, "B"],
    [7, 8, 9, "C"],
    ["*", 0, "#", "D"]
]

ROW_PINS = [5, 6, 13, 19] # BCM numbering
COL_PINS = [26, 17, 27, 22] # BCM numbering
TRIG_PIN = 15
ECHO_PIN = 14

GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

greenPin = 21
redpin=20
relaypin=16

def distance():
    # Send a trigger pulse
    GPIO.output(TRIG_PIN, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, GPIO.LOW)

    # Initialize variables
    pulse_start = time.time()
    pulse_end = time.time()

    # Wait for the echo to start
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()

    # Wait for the echo to end
    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    # Calculate the distance in centimeters
    pulse_duration = pulse_end - pulse_start
    distance_cm = pulse_duration * 17150

    return distance_cm

def printdisplay(data):
    try:
        lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=2, dotsize=8)
        lcd.clear()
        lcd.write_string(str(data))
        time.sleep(1)
      
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

def relayof():
    GPIO.setup(relaypin, GPIO.OUT)
    GPIO.output(relaypin,0)
    time.sleep(2)
    GPIO.cleanup(relaypin)
    time.sleep(5)


def relayon():
    GPIO.setup(relaypin, GPIO.OUT)
    GPIO.output(relaypin,1)



def writerr_api(rfid,user,age,phoneNum,roomNum,adharNum,location):
    API_URL = url+'/api/v1/writeRfid'
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
    API_URL = url+'/api/v1/readRfid'
    form_data = {
        'rfidno': rfid,
        'device': device,
    }
    response = requests.post(API_URL, data=form_data)
    print(response.text)
    if response.text.startswith("in") or response.text.startswith("out"):
        green()
        printdisplay(str(response.text))
        relayof()
        relayon()
    else:
        red()
        printdisplay(str(response.text))

def pin_verify(pin):
    API_URL = url+'/api/v1/pinverify'
    form_data = {
        'pin': pin,
        
    }
    response = requests.post(API_URL, data=form_data)
    print(response.text)
    if response.text=="success":
        green()
        printdisplay(str(response.text))
        relayof()
        relayon()
       
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
    dist = distance()
    print("Distance:", dist, "cm")

    if dist <= 30:

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
            time.sleep(1)
            #read_db_write()
           
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



def check_wifi_connection():
    try:
        # Run the 'iwconfig' command to check the wireless interface status
        result = subprocess.check_output(["iwconfig"], stderr=subprocess.STDOUT, universal_newlines=True)
        
        # Check if the output contains the name of your wireless interface (e.g., "wlan0")
        if "wlan0" in result:
            return True  # Connected to Wi-Fi
        else:
            return False  # Not connected to Wi-Fi
    except subprocess.CalledProcessError:
        return False  # An error occurred or the command failed



def check_url_availability(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        
        # Check the response status code
        if response.status_code == 200:
            return True  # URL is reachable and active
        else:
            return False  # URL is not reachable or returned an error status
    except requests.ConnectionError:
        return False  # Unable to connect to the URL

def main():
    relayon()
    # while True:
    if check_wifi_connection():
        printdisplay("connected to Wi-Fi.")
        time.sleep(2)

        # Check URL availability
        if check_url_availability(url):
            printdisplay("server is active.")
          
          
            process1 = multiprocessing.Process(target=tt1)
            process2 = multiprocessing.Process(target=tt2)

            process1.start()
            process2.start()
            # process1.join()
            # process2.join()
            
            # break
        else:
            printdisplay("server is not active")
            time.sleep(6)

    else:
        printdisplay("Not connected to Wi-Fi.")
        time.sleep(6)

            # if thread1.is_alive() and thread2.is_alive():
            #     print("Thread 1 is running.")

if __name__ == "__main__":
    main()

    #sudo systemctl restart myscript.service
