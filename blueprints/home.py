from flask import Blueprint, render_template, redirect, url_for, request, session
import json
from src.Rfid import Rfid
from src.Auth import Auth

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

@bp.route("/")
def login():
     return render_template('login.html', session=session)


@bp.route("/logs")
def loggs():
     return render_template('logview.html', session=session)