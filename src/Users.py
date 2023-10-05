from src.Database import Database

from flask import jsonify

db = Database.get_connection()
users = db.users

class Users:

    @staticmethod
    def adduser(rfidNum,username,age,phoneNum,roomNum,adharNum,location):  
        _id = users.insert_one({
            "rfid": rfidNum,
            "username": username,
            "age": int(age),
            "phone":phoneNum,
            "roomNum":roomNum,
            "adharNum":adharNum,
            "location":location
        })
        return str(_id.inserted_id)
    
    @staticmethod
    def updateData(rfidNum,username,age,phoneNum,roomNum,adharNum,location):  
        existing_doc = users.find_one({"rfid": rfidNum})
        if existing_doc:
            result = users.update_one({"rfid": rfidNum}, 
                                    {"$set": {"username": username,"age": int(age),"phone":phoneNum,"roomNum":roomNum,"adharNum":adharNum,"location":location}})
            return "update success"
        else:
            return "this card is not present"
      
    
    
    @staticmethod
    def GetallData():
        list1=[]
        result=users.find()

        for document in result:
            
            id=str(document['_id'])
            rfidno=document['rfid']
            username=document['username']
            age=int(document['age'])
            phonenum=document['phone']
            roomNum=document['roomNum']
            adharNum=document['adharNum']
            location=document['location']
          
            list1.append({
                "id":id,
                "rfidno":rfidno,
                "username":username,
                "age":age,
                "phonenum":phonenum,
                "roomNum":roomNum,
                "adharNum":adharNum,
                "location":location
              
            })

        return jsonify(list1)

    
    
    # this function set in rfid class
    # @staticmethod
    # def updateDataToAnotherPerson(rfidNum,username,age,phoneNum,roomNum,adharNum,location,aloowedtime=22,creditscor=0,logs={}):  
    #     existing_doc = users.find_one({"rfid": rfidNum})
    #     if existing_doc:
    #         result = users.update_one({"rfid": rfidNum}, 
    #                                 {"$set": {"username": username,"age": int(age),"phone":phoneNum,"roomNum":roomNum,"adharNum":adharNum,"location":location}})
            
    #         Rfid.updateAlldata(rfidNum,username,aloowedtime,age)
    #         return "update success"
    #     else:
    #         return "this card is not present"
      
    