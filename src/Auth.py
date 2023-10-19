from src.Database import Database
from flask import jsonify 
from werkzeug.security import check_password_hash


db = Database.get_connection()
users = db.users

class Auth:

    # @staticmethod
    # def checkPin(pin):
    #     doc=users.find_one()
    #     if doc:
    #         if pin==doc['pinNumber']:
                
    #             return "success"
    #         else:
    #             return "wrong"
    #     else:
    #         return "contact tech team"
    
       
    @staticmethod
    def login(user, passwd):
        try:
            existing_doc = users.find_one({"username": user})
            print(existing_doc)
            print(existing_doc['password'])

            if existing_doc:
                if check_password_hash(existing_doc['password'], passwd):
                    print("Login successful")
                    return 200
                else:
                    print("Incorrect password", passwd)
                    return 400
            else:
                return 404

        except Exception as e:
            # Handle potential database or other exceptions
            print(f"Error during login: {e}")
            return False, "An error occurred during login"
          

    @staticmethod
    def getALL():
        result=users.find()
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
        document = users.find_one({"username": username})
        if document:
            users.update_one({"_id": document["_id"]}, {"$set": {"activetime":int(actiStart),"activeEnd":int(ActiveEnd),"pinNumber":str(pin)}})
           
        else:
            return "username Not allowed"



       