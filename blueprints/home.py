from flask import Blueprint, render_template, redirect, url_for, request, session
import json
from src.Rfid import Rfid

bp = Blueprint("home", __name__, url_prefix="/")

@bp.route("/")
def home():
     insi=Rfid.InsidePgUser()
     outsi=Rfid.OutsidePgUser()
     tot=int(insi)+int(outsi)
     deact=Rfid.DeactivateduserCount()
     countDta=(insi,outsi,tot,deact)
     chatdt=Rfid.GetallData()
     print(chatdt)
     chatdt=chatdt.json
     print(chatdt)
     return render_template('index.html', session=session,data=chatdt,data1=countDta)


