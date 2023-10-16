from src.Database import Database
from flask import jsonify 
from .pg_manager import PGManager

db = Database.get_connection()
auths = db.auth

class Auth:

    @staticmethod
    def checkPin(pin):
        doc=auths.find_one()
        if doc:
            if pin==doc['pinNumber']:
                return "success"
            else:
                return "wrong"
        else:
            return "contact tech team"
    
    
    @staticmethod
    def register():
        user, passwd = PGManager().create_pg_credentials()
        existing_doc = auths.find_one({"username": user})
        if existing_doc:
            return "user already Exists"
       
        else:
            _id = auths.insert_one({
            "password": passwd,
            "username": user
            })

            # return str(_id.inserted_id)
            return user, passwd

         

       
    @staticmethod
    def login(user,passwd):
        existing_doc = auths.find_one({"username": user})
        if existing_doc:
            if existing_doc['username']==user and existing_doc['password']==passwd:
                return True
            else:
                return False
       
        else:
            return "do register"
          

    @staticmethod
    def getALL():
        result=auths.find()
        list1=[]
        for document in result:
            id=str(document['_id'])
            pin=document['pinNumber']
            username=document['username']
            activeStart = document['activetime']
            activeEnd = document['activeEnd']

            list1.append({
                "activestart":activeStart,
                "activeEnd":activeEnd,
                "pin":pin,
                "username":username,
                "id":id
               
            })

        return jsonify(list1)
    

            
    @staticmethod
    def updateAll(username,actiStart,ActiveEnd,pin):
        document = auths.find_one({"username": username})
        if document:
            auths.update_one({"_id": document["_id"]}, {"$set": {"activetime":int(actiStart),"activeEnd":int(ActiveEnd),"pinNumber":str(pin)}})
           
        else:
            return "username Not allowed"



       