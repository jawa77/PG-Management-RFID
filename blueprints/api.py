from flask import Blueprint, render_template, redirect, url_for, request, session
import re
from src.Database import Database
from src.Rfid import Rfid
bp = Blueprint("apiv1", __name__, url_prefix="/api/v1/")
import json
db = Database.get_connection()

@bp.route("/writeRfid", methods=['POST'])
def write():
      if 'rfidno' in request.form and 'user' in request.form:
         rfidNo = request.form['rfidno']
         user = request.form['user']
         

         pattern = r'[~!#$%^&*()+{}\[\]:,;"\'<>/\|\\]'
         rfidNo=re.sub(pattern, '', rfidNo)
         user=re.sub(pattern, '', user)
  
         a=Rfid.WriteRfid(rfidNo,user)
         return str(a)
      else:
          return "not enough params"

@bp.route("/readRfid", methods=['POST'])
def read():
      if 'rfidno' in request.form:
         rfidNo = request.form['rfidno']
      
         pattern = r'[~!#$%^&*()+{}\[\]:,;"\'<>/\|\\]'
         rfidNo=re.sub(pattern, '', rfidNo)
         
  
         a=Rfid.ReadRfid(rfidNo,2)
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