from src.Database import Database
from src.Users import Users
from src.Auth import Auth
from src.Xlsheet import Xlsheet
from time import time
from werkzeug.security import generate_password_hash
import arrow
import logging
from flask import jsonify
import datetime


db = Database.get_connection()
rfid = db.rfid_data

class Rfid:

    def Entry(rfidno,device):
        current_datetime = datetime.datetime.now()
        current_date = str(current_datetime.date())
        hours = current_datetime.hour
        minutes = current_datetime.minute

        currentTime = f"{hours}:{minutes}"

        document = rfid.find_one({"rfid": rfidno})
        if document:
            times_data = document.get("logs")
            times_data[current_date] = times_data.get(current_date,[])
            
            # rfid.update_one({"_id": document["_id"]}, {"$set": {"logs": times_data}})

            present="in"
            credit=int(document['creditScore'])
            if device==1:
               if document["present"]=="in":
                  credit=credit+1   
                  present="in"  
               else:
                  present="in"
            else:   
               if document["present"]=="out":
                  credit=credit+1 
                  present="out"
               else:
                 present="out"
            
            Xlsheet.writexl(document['username'],current_date,currentTime)
            times_data[current_date].append({present: currentTime})
            rfid.update_one({"_id": document["_id"]}, {"$set": {"logs": times_data,"present":present,"creditScore":credit}})
            
            print(present,document['username'])
            return f"{present}  {str(document['username'])}"
        else:
            return 0

   
    ALLOWING_TIME_UNTIL_DEFAULT = 22
    ONE_DAY_PERMISSION_DEFAULT = 0
    @staticmethod
    def WriteRfid(rfidNum, username, password, age, phoneNum, roomNum, adharNum, location, first_name, last_name, email, section, allowingTimeUntil=ALLOWING_TIME_UNTIL_DEFAULT, oneDayPermission=ONE_DAY_PERMISSION_DEFAULT):
      try:
         # Check if rfidNum already exists in the collection
         existing_doc = rfid.find_one({"rfidNum": rfidNum})

         if existing_doc:
               # RFID number already exists, return an error message
               return "RFID number already exists", 400

         # Hash the password before storing
         hashed_password = generate_password_hash(password)

         # RFID number is not present, insert the new document
         _id = rfid.insert_one({
               "rfidNum": rfidNum,
               "username": username,
               "roomNum": roomNum,
               "section": section,
               "Card_start": time(),
               "active": 0,
               "present": "in",
               "creditScore": 0,
               "allowedUntill": allowingTimeUntil,
               "oneDayPermission": oneDayPermission,
               "logs": {},
         })

         Users.adduser(rfidNum, username, hashed_password, age, phoneNum, roomNum, adharNum, location, first_name, last_name, email, section)

         return 200
      except Exception as e:
         logging.error(f"Error writing RFID: {e}")
         return "An error occurred while processing the request", 500
       
    @staticmethod
    def ReadRfid(rfidno,device):
       
        existing_doc = rfid.find_one({"rfid": rfidno})
        existing_doc1 = Auth.getALL()
        actTime=existing_doc1.json
        start = actTime[0]['activestart']
        end = actTime[0]['activeEnd']
       
  
        if existing_doc: 
            if existing_doc['active']==0:      
               current_time = datetime.datetime.now().time()
               activetime = datetime.time(int(start), 0)  
               active_end = datetime.time(int(end), 0)  
               # restrictedTime = datetime.time(22, 2)  
               # restrictedEnd = datetime.time(4, 59) 
             

               
               if activetime <= current_time <= active_end:
                
                   attempt=Rfid.Entry(rfidno,device)
                   if attempt==0:
                     return "cardNotAllowed"
                   else:
                     #  return f"{existing_doc['username']} {attempt}"
                     return attempt
                
               else:
                  
                   a=Rfid.DailyextrTimePermission(int(existing_doc['allowedUntill']),device,existing_doc['username'],existing_doc['oneDayPermission'])
                   Rfid.Entry(rfidno,device)
                   return str(a)
               # else:
               #    return "something wrong"
            else:
               return "Deactivated"
 
        else:
           return "you are card is not allowed"
    

    @staticmethod
    def DailyextrTimePermission(time,device,username,daypermission):
        current_time = datetime.datetime.now().time()
        permisTime = datetime.time(time, 0)  
        restrictedTime = datetime.time(22, 0) 
        print("hhh")

        if restrictedTime <= current_time <= permisTime:          
          return "in" if device == 1 else "out"
        elif daypermission==0:
           return "ask permission" 
        elif daypermission >=0:
           permisTime1 = datetime.time(int(daypermission), 0) 
           if restrictedTime <= current_time <= permisTime1:
              return "in" if device == 1 else "out"
              
    

    @staticmethod
    def setOneDayPermission(rfidno,dayPermission):
       existing_doc = rfid.find_one({"rfid": rfidno})
       if existing_doc:
          result = rfid.update_one({"rfid": rfidno}, {"$set": {"oneDayPermission": int(dayPermission)}})
          return f"update success untill {dayPermission}"
       else:
          return "this card is not allowed"

    @staticmethod   
    def SetMoreDaypermission(rfidno):
       pass
    
    @staticmethod
    def removeAlldayPermissions():
       result = rfid.update_many({}, {"$set": {"oneDayPermission": 0}})
       if result.modified_count > 0:
          return "successfully updated"
       else:
          return "already updated"
       
    @staticmethod   
    def removePersononedayPermission(rfidno):
       result = rfid.update_many({"rfid": rfidno}, {"$set": {"oneDayPermission": 0}})
       if result.modified_count > 0:
          return "successfully Removed "
       else:
          return "already removed"

    @staticmethod   
    def changeonedayPermission(rfidno,allowTime):
       result = rfid.update_many({"rfid": rfidno}, {"$set": {"oneDayPermission": int(allowTime)}}) 
       if result.modified_count > 0:
          return "successfully changed"
       else:
          return "already changed"  

    
    @staticmethod
    def updateAlldata(rfidno,username,DailyUntill,age,ondaypermison=0):
       existing_doc = rfid.find_one({"rfid": rfidno})
       if existing_doc:
          result = rfid.update_one({"rfid": rfidno}, {"$set": {
            "username": username,
            "Card_start": time(),
            "active":0,
            "present":"in",
            "creditScore":0,
            "allowedUntill":DailyUntill,
            "oneDayPermission":ondaypermison,
            "logs":{},
            "age":int(age)}})
          return "update success "
       else:
          return "this card is not allowed"
            

    @staticmethod
    def GetallData():
        list1=[]
        result=rfid.find()

        for document in result:
            
            id=str(document['_id'])
            rfidno=document['rfid']
            username=document['username']
            datetime_obj = arrow.get(document['Card_start'])
            human_readable_time = datetime_obj.humanize()
            present=document['present']
            permissionUntill=document['oneDayPermission']
            logs=document['logs']
            active1=document['active']
            creditscr=document['creditScore']
            btnclr=""
            activecheck=""
            if active1==0:
               activecheck="activated"
               btnclr="bg-success"
            else:
               activecheck="deactivated"
               btnclr="bg-danger"


          
            list1.append({
                "rfidno":rfidno,
                "card_time":human_readable_time,
                "username":username,
                "id":id,
                "present":present,
                "permissiontoday":permissionUntill,
                "logs":logs,
                "active":activecheck,
                "btnclr":btnclr,
                "creditscr":creditscr
            })

        return jsonify(list1)
        
    

    @staticmethod
    def getEntryData(rfidno):
      document = rfid.find_one({"rfid": rfidno})
      if document:
         times_data = document.get("logs", {})  # Get the "times" dictionary, default to an empty dictionary if it's not present
         return times_data
      else:
         return "no logs"
        
       

    @staticmethod
    def getEntryDataWITHdate(rfidno,Filterdate):
      document = rfid.find_one({"rfid": rfidno})
      if document:
         times_data = document.get("logs", [])
         if Filterdate in times_data:
            specific_date_times = times_data[Filterdate]
            return jsonify(specific_date_times)
         else:
            specific_date_times = ["nodata"]
            return jsonify(specific_date_times)

      else:
         return "no logs"
        
    @staticmethod
    def InsidePgUser():
       count = rfid.count_documents({"present": "in"})
       return int(count)
    
    @staticmethod
    def OutsidePgUser():
       count = rfid.count_documents({"present": "out"})
       return int(count)
    
    @staticmethod
    def DeactivateduserCount():
       count = rfid.count_documents({"active": 1})
       return int(count)
    
    @staticmethod
    def toggleActivate(rfidno):
      existing_doc = rfid.find_one({"rfid": rfidno})
      toggle=0
  
      if existing_doc:
         if existing_doc['active']==1:
            toggle=0
         else:
            toggle=1
            
         result = rfid.update_one({"rfid": rfidno}, {"$set": {"active": int(toggle)}})
         return str(toggle)   
      else:
         return "deactivated one"
 
    @staticmethod
    def delUser(rfidno):
      result = rfid.delete_one({"rfid": rfidno})
      if result.deleted_count == 1:
         print("Document deleted successfully.")
      else:
         print("Document not found or not deleted.")


    @staticmethod
    def totaluserPg():
      result =rfid.find({"active": 0})
   
      list1=[]
      for document in result:
            
            id=str(document['_id'])
            rfidno=document['rfid']
            username=document['username']
          
          
            list1.append({
                "rfidno":rfidno,
                "username":username,
                "id":id
        
            })

      return jsonify(list1)
      

    @staticmethod
    def InsideUsername():
      result =rfid.find({ "$and": [{"present": "in"},{"active": 0}]})
   
      list1=[]
      for document in result:
            
            id=str(document['_id'])
            rfidno=document['rfid']
            username=document['username']
          
          
            list1.append({
                "rfidno":rfidno,
                "username":username,
                "id":id
        
            })

      return jsonify(list1)

    @staticmethod
    def outsideUsername():
      result =rfid.find({ "$and": [{"present": "out"},{"active": 0}]})
   
      list1=[]
      for document in result:
            
            id=str(document['_id'])
            rfidno=document['rfid']
            username=document['username']
          
          
            list1.append({
                "rfidno":rfidno,
                "username":username,
                "id":id
        
            })

      return jsonify(list1)
    
    @staticmethod
    def deactiveUsernam():
      result =rfid.find({"active": 1})
   
      list1=[]
      for document in result:
            id=str(document['_id'])
            rfidno=document['rfid']
            username=document['username']
          
          
            list1.append({
                "rfidno":rfidno,
                "username":username,
                "id":id
        
            })

      return jsonify(list1)