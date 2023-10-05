from flask import Blueprint, render_template, redirect, url_for, request, session
import re
from src.Database import Database
from src.Rfid import Rfid
bp = Blueprint("apiv1", __name__, url_prefix="/api/v1/")
import json
db = Database.get_connection()

@staticmethod
def remove_special_characters(input_string):
    pattern = r'[~!#$%^&*()+{}\[\]:,;"\'<>/\|\\]'
    return re.sub(pattern, '', input_string)


 
@bp.route("/writeRfid", methods=['POST'])
def write():
     if 'rfidno' in request.form and 'user' in request.form and 'age' in request.form and 'roomnum' in request.form and 'adharNum' in request.form and 'phoneNum' in request.form and 'location' in request.form:
         rfidNo = remove_special_characters(request.form['rfidno'])
         user = remove_special_characters(request.form['user'])
         age=remove_special_characters(request.form['age'])
         roomnum = remove_special_characters(request.form['roomnum'])
         adhar = remove_special_characters(request.form['adharNum'])
         phone=remove_special_characters(request.form['phoneNum'])
         location=remove_special_characters(request.form['location'])

         
  
         a=Rfid.WriteRfid(rfidNo,user,age,phone,roomnum,adhar,location)
         return str(a)
     else:
          return "not enough params"

@bp.route("/readRfid", methods=['POST'])
def read():
      if 'rfidno' in request.form and 'device' in request.form :
         rfidNo = request.form['rfidno']
         device=request.form['device']
      
         pattern = r'[~!#$%^&*()+{}\[\]:,;"\'<>/\|\\]'
         rfidNo=re.sub(pattern, '', rfidNo)
         
  
         a=Rfid.ReadRfid(rfidNo,int(device))
         return str(a)      

@bp.route("/SetOneDayPermission", methods=['POST'])
def setPermission():
      if 'rfidno' in request.form and 'timeuntill' in request.form:
         rfidNo = request.form['rfidno']
         timeuntil=request.form['timeuntill']
         a=Rfid.setOneDayPermission(rfidNo,timeuntil)
         return str(a)

@bp.route("/removeAlldayPermissions", methods=['POST'])
def removePermiss():
         a=Rfid.removeAlldayPermissions()
         return str(a)

@bp.route("/RemovePersononedayPermission", methods=['POST'])
def removeOnePermiss():
      if 'rfidno' in request.form:
         rfidNo = request.form['rfidno']
         a=Rfid.removePersononedayPermission(rfidNo)
         return str(a)
    

@bp.route("/ChangeonedayPermission", methods=['POST'])
def change1DAyPermis():
      if 'rfidno' in request.form and 'allowtime' in request.form:
         rfidNo = request.form['rfidno']
         allowtimw=request.form['allowtime']
         a=Rfid.changeonedayPermission(rfidNo,allowtimw)
         return str(a)

@bp.route("/getAllDATA", methods=['GET'])
def getAllUserDta():
        lists=Rfid.GetallData()
        
        return lists


@bp.route("/getEntryData", methods=['POST'])
def entryData():
      if 'rfidno' in request.form:
        rfidNo = request.form['rfidno']
        lists=Rfid.getEntryData(rfidNo)
        return lists

@bp.route("/getEntryDataWITHdate", methods=['POST'])
def getentrywitdate():
      if 'rfidno' in request.form and 'DatePick' in request.form:
        rfidNo = request.form['rfidno']
        datepic=request.form['DatePick']
        lists=Rfid.getEntryDataWITHdate(rfidNo,datepic)
        return lists
      
@bp.route("/UserinsidePg", methods=['POST'])
def inside():
     return str(Rfid.InsidePgUser())    

@bp.route("/UseroutsidePg", methods=['POST'])
def outside():
     return str(Rfid.OutsidePgUser())   

@bp.route("/deacticedUserCount", methods=['POST'])
def deactivated():
     return str(Rfid.DeactivateduserCount())   

@bp.route("/toggleactive", methods=['POST'])
def toggle():
     if 'rfidno' in request.form:
         rfidNo = request.form['rfidno']
         return Rfid.toggleActivate(rfidNo) 
     else:
          return "Not enough params"