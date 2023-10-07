# login sess set
#otp pin generate

from src.Database import Database
from src.Users import Users
from time import time
import json
import arrow
from flask import jsonify 
import datetime


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
    def register(user,passwd):
        existing_doc = auths.find_one({"username": user})
        if existing_doc:
            return "user already Exists"
       
        else:
            _id = auths.insert_one({
            "password": passwd,
            "username": user,
            "pinNumber":"1234"
            })

            return str(_id.inserted_id)
         

       
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
          
