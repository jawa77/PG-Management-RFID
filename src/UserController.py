from src.Database import Database

db = Database.get_connection()
users = db.users

class Users:

    @staticmethod
    def add_user(rfidNum, username, password, age, phoneNum, roomNum, adharNum, location, first_name, last_name, email, section):
        try:
            _id = users.insert_one({
                "rfidNum": rfidNum,
                "username": username,
                "password": password,
                "age": int(age),
                "phoneNum": phoneNum,
                "roomNum": roomNum,
                "adharNum": adharNum,
                "location": location,
                "first_name": first_name, 
                "last_name": last_name,
                "email": email,
                "section": section
            })

            if _id:
                return 201  # Created
            else:
                return 500  # Internal Server Error
        except Exception as e:
            # Properly handle the exception (e.g., log it, return an appropriate error code)
            return 500  # Internal Server Error

    @staticmethod
    def read_user(username):
        try:
            user = users.find_one({"username": username})
            if user:
                return {"status": 200, "message": "User found.", "user": user}
            else:
                return {"status": 404, "message": "User not found."}
        except Exception as e:
            # Properly handle the exception (e.g., log it, return an appropriate error code)
            return {"status": 500, "message": f"Internal Server Error: {str(e)}"}
        

    @staticmethod
    def update_user(username, data):
        try:
            result = users.update_one({"_id": username}, {"$set": data})
            if result.modified_count > 0:
                return {"status": 200, "message": "User updated successfully."}
            else:
                return {"status": 404, "message": "User not found."}
        except Exception as e:
            # Properly handle the exception (e.g., log it, return an appropriate error code)
            return {"status": 500, "message": f"Internal Server Error: {str(e)}"}
        

    @staticmethod
    def delete_user(username):
        try:
            result = users.delete_one({"username": username})
            if result.deleted_count > 0:
                return {"status": 200, "message": "User deleted successfully."}
            else:
                return {"status": 404, "message": "User not found."}
        except Exception as e:

            # Properly handle the exception (e.g., log it, return an appropriate error code)
            return {"status": 500, "message": f"Internal Server Error: {str(e)}"}