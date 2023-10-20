from flask import Blueprint,redirect, url_for, request, session,flash
import re
from datetime import datetime
from src.Database import Database
from src.Rfid import Rfid
from src.Auth import Auth
from src.UserController import Users
db = Database.get_connection()
users = db.users

def verify_input(password, dob, phoneNum, roomNum, adharNum, location, first_name, last_name, email, section):
    # Implement verification logic here.
    # You can add more checks depending on your specific requirements.

    # Check password strength (at least 8 characters)
    if len(password) < 8: 
        flash("Password must be at least 8 characters long.")
        return False, "Password must be at least 8 characters long."

    # Check DOB format (assuming YYYY-MM-DD)
    dob_pattern = r'^\d{4}-\d{2}-\d{2}$'
    if not re.match(dob_pattern, dob):
        flash("Invalid date of birth format. Please use YYYY-MM-DD.")
        return False, "Invalid date of birth format. Please use YYYY-MM-DD."

    # Check phone number format (assuming 10 digits)
    phone_pattern = r'^\d{10}$'
    if not re.match(phone_pattern, phoneNum):
        flash("Invalid phone number format. Please use 10 digits.")   
        return False, "Invalid phone number format. Please use 10 digits."

    # Check room number (assuming it should be a positive integer)
    try:
        roomNum = int(roomNum)
        if roomNum <= 0:
            raise ValueError
    except ValueError:
        flash("Invalid room number.")
        return False, "Invalid room number. Please use a positive integer."

    # Check Aadhar number format (assuming 12 digits)
    aadhar_pattern = r'^\d{12}$'
    if not re.match(aadhar_pattern, adharNum):
        flash("Invalid Aadhar number format. Please use 12 digits.")
        return False, "Invalid Aadhar number format. Please use 12 digits."

    # Check email format using a simple regex pattern
    email_pattern = r'^\S+@\S+\.\S+$'
    if not re.match(email_pattern, email):
        flash("Invalid email address format.")
        return False, "Invalid email address format."

    # Add more verification checks as needed.

    return True, "Data is verified."


def remove_special_characters(input_string):
    pattern = r'[~!#$%^&*()+{}\[\]:,;"\'<>/\|\\]'
    return re.sub(pattern, '', input_string)



def write(rfidNum, username, password, dob, phoneNum, roomNum, adharNum, location, first_name, last_name, email, section):
          sanitized_rfidNum = remove_special_characters(rfidNum)
          sanitized_username = remove_special_characters(username)
          sanitized_password = remove_special_characters(password)
          sanitized_dob = remove_special_characters(dob)
          sanitized_phoneNum = remove_special_characters(phoneNum)
          sanitized_roomNum = remove_special_characters(roomNum)
          sanitized_adharNum = remove_special_characters(adharNum)
          sanitized_location = remove_special_characters(location)
          sanitized_first_name = remove_special_characters(first_name)
          sanitized_last_name = remove_special_characters(last_name)
          sanitized_email = remove_special_characters(email)
          sanitized_section = remove_special_characters(section)

          is_verified = verify_input(rfidNum, username, password, dob, phoneNum, roomNum, adharNum, location, first_name, last_name, email, section)

          if is_verified:
               # Add the sanitized data to another function
               data_to_add = {
                    "rfidNum": sanitized_rfidNum,
                    "username": sanitized_username,
                    "password": sanitized_password,
                    "dob": sanitized_dob,
                    "phoneNum": sanitized_phoneNum,
                    "roomNum": sanitized_roomNum,
                    "adharNum": sanitized_adharNum,
                    "location": sanitized_location,
                    "first_name": sanitized_first_name,
                    "last_name": sanitized_last_name,
                    "email": sanitized_email,
                    "section": sanitized_section,
               }
               Users.add_user(data_to_add)
               flash("User added successfully.")
          else:
               flash("Input data verification failed:")


# @bp.route("/readRfid", methods=['POST'])
def read():
     if 'rfidno' in request.form and 'device' in request.form:
         rfidNo = request.form['rfidno']
         device=request.form['device']
      
         pattern = r'[~!#$%^&*()+{}\[\]:,;"\'<>/\|\\]'
         rfidNo=re.sub(pattern, '', rfidNo)
         
  
         a=Rfid.ReadRfid(rfidNo,int(device))
         return str(a)      

# @bp.route("/SetOneDayPermission", methods=['POST'])
def setPermission():
      if 'rfidno' in request.form and 'timeuntill' in request.form:
         rfidNo = request.form['rfidno']
         timeuntil=request.form['timeuntill']
         a=Rfid.setOneDayPermission(rfidNo,timeuntil)
         return str(a)

# @bp.route("/removeAlldayPermissions", methods=['POST'])
def removePermiss():
         a=Rfid.removeAlldayPermissions()
         return str(a)

# @bp.route("/RemovePersononedayPermission", methods=['POST'])
def removeOnePermiss():
      if 'rfidno' in request.form:
         rfidNo = request.form['rfidno']
         a=Rfid.removePersononedayPermission(rfidNo)
         return str(a)
    

# @bp.route("/ChangeonedayPermission", methods=['POST'])
def change1DAyPermis():
      if 'rfidno' in request.form and 'allowtime' in request.form:
         rfidNo = request.form['rfidno']
         allowtimw=request.form['allowtime']
         a=Rfid.changeonedayPermission(rfidNo,allowtimw)
         return str(a)

# @bp.route("/getAllDATA", methods=['GET'])
def getAllUserDta():
        lists=Rfid.GetallData()
        
        return lists


# @bp.route("/getEntryData", methods=['POST'])
def entryData():
      if 'rfidno' in request.form:
        rfidNo = request.form['rfidno']
        lists=Rfid.getEntryData(rfidNo)
        return lists

# @bp.route("/getEntryDataWITHdate", methods=['POST'])
def getentrywitdate():
      if 'rfidno' in request.form and 'DatePick' in request.form:
        rfidNo = request.form['rfidno']
        datepic=request.form['DatePick']
        lists=Rfid.getEntryDataWITHdate(rfidNo,datepic)
        return lists
      
# @bp.route("/UserinsidePg", methods=['POST'])
def inside():
     return str(Rfid.InsidePgUser())    

# @bp.route("/UseroutsidePg", methods=['POST'])
def outside():
     return str(Rfid.OutsidePgUser())   

# @bp.route("/deacticedUserCount", methods=['POST'])
def deactivated():
     return str(Rfid.DeactivateduserCount())   

# @bp.route("/toggleactive", methods=['POST'])
def toggle():
     if 'rfidno' in request.form:
         rfidNo = request.form['rfidno']
         return Rfid.toggleActivate(rfidNo) 
     else:
          return "Not enough params"

# @bp.route("/pinverify", methods=['POST'])
def piv():
     if 'pin' in request.form:
         pinNo = request.form['pin']
         a=Auth.checkPin(str(pinNo))
        
         
         return str(a)
     else:
          return "Not enough params"
     
# @bp.route("/register", methods=['POST'])
def registr():
     if 'user' in request.form and 'pass' in request.form:
         user = request.form['user']
         passwd = request.form['pass']

         a=Auth.register(user,passwd)
         return str(a)
     else:
          return "Not enough params"

# @bp.route("/login", methods=['POST'])
def logn():
     if 'user' in request.form and 'pass' in request.form:
         user = request.form['user']
         passwd = request.form['pass']

         a=Auth.login(user,passwd)
         if a==200:
              session['authenticated']=True
              return redirect(url_for('route.dashboard'))
         elif a==400:
              return "authentication failure"
     else:
          return "Not enough params"
     

# @bp.route("/updateResTime",methods=['POST'])
def updtRes():
     if 'username' in request.form and 'actTmStart' in request.form and 'actTmEnd' in request.form and 'pin' in request.form:
          user = request.form['username']
          startTime = request.form['actTmStart']
          endTime=request.form['actTmEnd']
          pin=request.form['pin']

          Auth.updateAll(user,startTime,endTime,pin)
          return "success"
     else:
          return "not enough paramss"

# @bp.route("/availuser",methods=['POST'])
def availuser():
     a=Rfid.totaluserPg()
     return a

# @bp.route("/insidePGUsername",methods=['POST'])
def insiderName():
     a=Rfid.InsideUsername()
     return a
   
# @bp.route("/outsidePGUsername",methods=['POST'])
def outsiderName():
     a=Rfid.outsideUsername()
     return a

# @bp.route("/deactiveUser",methods=['POST'])
def deactUsernme():
     a=Rfid.deactiveUsernam()
     return a