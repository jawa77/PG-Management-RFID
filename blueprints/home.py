from flask import Blueprint, render_template, redirect, url_for, request, session
import json
from src.Rfid import Rfid

bp = Blueprint("home", __name__, url_prefix="/")

@bp.route("/dashboard")
def dashboard():
     insi=Rfid.InsidePgUser()
     outsi=Rfid.OutsidePgUser()
     tot=int(insi)+int(outsi)
     deact=Rfid.DeactivateduserCount()
     countDta=(insi,outsi,tot,deact)
     chatdt=Rfid.GetallData()
     print(chatdt)
     chatdt=chatdt.json
     print(chatdt)
     return render_template('dashboard.html', session=session,data=chatdt,data1=countDta)

@bp.route("/info")
def info():
     return render_template('info.html', session=session)

@bp.route("/")
def login():
     return render_template('login.html', session=session)