from flask import Blueprint, render_template, redirect, url_for, request, session
import requests
from src.Rfid import Rfid
from src.Auth import Auth
from src.pg_manager import PGManager

bp = Blueprint("home", __name__, url_prefix="/")

@bp.route("/dashboard")
def dashboard():
     insi=Rfid.InsidePgUser()
     outsi=Rfid.OutsidePgUser()
     tot=int(insi)+int(outsi)
     deact=Rfid.DeactivateduserCount()
     data1=(insi,outsi,tot,deact)

     data=Rfid.GetallData().json
     data2=Rfid.totaluserPg().json
     data3=Rfid.InsideUsername().json
     data4=Rfid.outsideUsername().json
     data5=Rfid.deactiveUsernam().json
     return render_template('dashboard.html', session=session,data=data,data1=data1,data2=data2,data3=data3,data4=data4,data5=data5)

#admin info and restriction time
@bp.route("/info")
def info():
     existing_doc1 = Auth.getALL()
     datas=existing_doc1.json
     return render_template('info.html', session=session, data=datas)

@bp.route("/logs")
def loggs():
     return render_template('logview.html', session=session)


@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Extract data from the form
        data = {
            'first_name': request.form.get('first_name'),
            'last_name': request.form.get('last_name'),
            'email': request.form.get('email'),
            'roomNum': request.form.get('roomNum'),
            'section': request.form.get('section'),
            'location': request.form.get('location'),
            'dob': request.form.get('dob'),
            'phoneNum': request.form.get('phone'),
            'adharNum': request.form.get('adharNum'),
            'rfidNum': request.form.get('rfid')
        }
        data['username'], data['password'] = PGManager().create_pg_credentials()


        # Make the API request
        try:
            response = requests.post("http://127.0.0.1:7000/api/v1/writeRfid", data=data)
            
            if response.status_code == 200:
                # Handle successful API response if necessary
                pass
            else:
                # Handle errors returned by the API if necessary
                pass

        except requests.RequestException as e:
            # Handle request exceptions if necessary
            pass

        # Render the data.html template with the form data
        return render_template('data.html', **data)

    return render_template('register.html', session=session)
