from src.Database import Database
from time import time
import json
import arrow
from flask import  jsonify
import datetime


db = Database.get_connection()
users = db.user

class Rfid:

    def Entry(rfidno,device):
        current_datetime = datetime.datetime.now()
        current_date = str(current_datetime.date())
        hours = current_datetime.hour
        minutes = current_datetime.minute

        currentTime = f"{hours}:{minutes}"

        document = users.find_one({"rfid": rfidno})
        if document:
            
            times_data = document.get("times")
            times_data[current_date] = times_data.get(current_date,[])
            
            # users.update_one({"_id": document["_id"]}, {"$set": {"times": times_data}})

            present="in"
            if device==1:
               # if document["present"]=="in":
               #    return "alreadyIn"
               # else:
               present="in"
            else:
             
               # if document["present"]=="out":
               #    return "alreadyOut"
               # else:
               present="out"
            times_data[current_date].append({present: currentTime})
            users.update_one({"_id": document["_id"]}, {"$set": {"times": times_data,"present":present}})
            
            return present
        else:
            return 0

    
    @staticmethod
    def WriteRfid(rfidno,user,allowingTimeUntil=22,oneDayPermission=0):
    # Check if rfidno already exists in the collection
       existing_doc = users.find_one({"rfid": rfidno})
       
       if existing_doc:
        # RFID number already exists, return an error message or handle it as needed
        return "RFID number already exists"
       else:
        # RFID number is not present, insert the new document
        _id = users.insert_one({
            "rfid": rfidno,
            "username": user,
            "Card_start": time(),
            "active":0,
            "present":"in",
            "allowedUntill":allowingTimeUntil,
            "oneDayPermission":oneDayPermission,
            "times":{}

        })
        return str(_id.inserted_id)
       
    @staticmethod
    def ReadRfid(rfidno,device):
       
        existing_doc = users.find_one({"rfid": rfidno})
    #    print(existing_doc)
        if existing_doc: 
            if existing_doc['active']==0:      
               current_time = datetime.datetime.now().time()
               activetime = datetime.time(5, 0)  
               active_end = datetime.time(22, 0)  
               restrictedTime = datetime.time(22, 0)  
               restrictedEnd = datetime.time(5, 0)  

            
               if activetime <= current_time <= active_end:
                   attempt=Rfid.Entry(rfidno,device)
                   if attempt==0:
                     return "cardNotAllowed"
                   else:
                     #  return f"{existing_doc['username']} {attempt}"
                     return attempt
                
               elif restrictedTime <= current_time <= restrictedEnd:
                   a=Rfid.DailyextrTimePermission(int(existing_doc['allowedUntill']),device,existing_doc['username'],existing_doc['oneDayPermission'])
                   Rfid.Entry(rfidno,device)
                   return str(a)
            else:
               return "Deactivated"
 
        else:
           return "you are card is not allowed"
    

    @staticmethod
    def DailyextrTimePermission(time,device,username,daypermission):
        current_time = datetime.datetime.now().time()
        permisTime = datetime.time(time, 0)  
        restrictedTime = datetime.time(22, 0) 

        if restrictedTime <= current_time <= permisTime:          
          return "in" if device == 1 else "out"
        elif daypermission==0:
           return "ask permission 1234567890" 
        elif daypermission >=0:
           permisTime1 = datetime.time(int(daypermission), 0) 
           if restrictedTime <= current_time <= permisTime1:
              return "in" if device == 1 else "out"
              
    

    @staticmethod
    def setOneDayPermission(rfidno,dayPermission):
       existing_doc = users.find_one({"rfid": rfidno})
       if existing_doc:
          result = users.update_one({"rfid": rfidno}, {"$set": {"oneDayPermission": int(dayPermission)}})
          return f"update success untill {dayPermission}"
       else:
          return "this card is not allowed"

    @staticmethod   
    def SetMoreDaypermission(rfidno):
       pass
    
    @staticmethod
    def removeAlldayPermissions():
       result = users.update_many({}, {"$set": {"oneDayPermission": 0}})
       if result.modified_count > 0:
          return "successfully updated"
       else:
          return "already updated"
       
    @staticmethod   
    def removePersononedayPermission(rfidno):
       result = users.update_many({"rfid": rfidno}, {"$set": {"oneDayPermission": 0}})
       if result.modified_count > 0:
          return "successfully Removed "
       else:
          return "already removed"

    @staticmethod   
    def changeonedayPermission(rfidno,allowTime):
       result = users.update_many({"rfid": rfidno}, {"$set": {"oneDayPermission": int(allowTime)}}) 
       if result.modified_count > 0:
          return "successfully changed"
       else:
          return "already changed"  

    

            

    @staticmethod
    def GetallData():
        list1=[]
        result=users.find()

        for document in result:
            
            id=str(document['_id'])
            rfidno=document['rfid']
            username=document['username']
            datetime_obj = arrow.get(document['Card_start'])
            human_readable_time = datetime_obj.humanize()
            present=document['present']
            permissionUntill=document['oneDayPermission']
            times=document['times']
            active1=document['active']
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
                "times":times,
                "active":activecheck,
                "btnclr":btnclr
            })

        return jsonify(list1)
        
    

    @staticmethod
    def getEntryData(rfidno):
        document = users.find_one({"rfid": rfidno})
        times_data = document.get("times", ["nodata"])   #.get for manage key if key not present the ret []
        return times_data
        
       

    @staticmethod
    def getEntryDataWITHdate(rfidno,Filterdate):
      document = users.find_one({"rfid": rfidno})
      times_data = document.get("times", [])
      
      if Filterdate in times_data:
         specific_date_times = times_data[Filterdate]
         return jsonify(specific_date_times)
      else:
         specific_date_times = ["nodata"]
         return jsonify(specific_date_times)


        
    @staticmethod
    def InsidePgUser():
       count = users.count_documents({"present": "in"})
       return int(count)
    
    @staticmethod
    def OutsidePgUser():
       count = users.count_documents({"present": "out"})
       return int(count)
    
    @staticmethod
    def DeactivateduserCount():
       count = users.count_documents({"active": 1})
       return int(count)
    
    @staticmethod
    def toggleActivate(rfidno):
      existing_doc = users.find_one({"rfid": rfidno})
      toggle=0
  
      if existing_doc:
         if existing_doc['active']==1:
            toggle=0
         else:
            toggle=1
            
         result = users.update_one({"rfid": rfidno}, {"$set": {"active": int(toggle)}})
         return str(toggle)   
      else:
         return "deactivated one"
 
    @staticmethod
    def delUser(rfidno):
      result = users.delete_one({"rfid": rfidno})
      if result.deleted_count == 1:
         print("Document deleted successfully.")
      else:
         print("Document not found or not deleted.")


      