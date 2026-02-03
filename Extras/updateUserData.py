import pyautogui
import keyboard
import os
from datetime import datetime
#import sys
import pystray
from PIL import Image
import webbrowser
from tkinter import messagebox
import platform
import subprocess
import wmi
import itertools
import firebase_admin
from firebase_admin import credentials, firestore
import requests  # Import requests library for network connectivity check
from customtkinter import *
import customtkinter as ctk
from plyer import notification
from dateutil.relativedelta import relativedelta
import asyncio
from concurrent.futures import ThreadPoolExecutor
import threading
import time

pyautogui.PAUSE = 0.000001

windows = []

total_keyStrokes = 0
total_shortcuts = 0
total_runtime = 0
previous_time = time.time() 


def initialize_firestore():
    try:
        cred = credentials.Certificate({
        "type": "service_account",
        "project_id": "kodearrow-server",
        "private_key_id": "12f26b7c63d80d9d0901d9b8644b4f5ad12ebb28",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDGDu+3E6sI34Qw\nqAMOgp0D6fCmNtJmK0ESBFJyUrU38H6ZwtfnSHppnfFvvqbDXiqCCEKvc2dcXBmt\nBndUsXMPNsPv4fLJB30l8EQozr/ai1SsGoHFcZIYXwT0R6Ao5nWy49Ixj+URoBcy\nqfowR60JJMwn+a4KomEEd551f3RIWe/Ik/Oae0Hk3ONTdUGpZpHrN2WxCXSgk3zt\n2FiTZW+HEHyYYAF65XcX94asXpX1UeUMrpf02S8sI2/X/6PUEdGK5YfWhEE35uLH\n4oL62RSIk5b4eoJPC67+rDIDxeBUs3V/LJIn8AoxcW/FWMb1fwdZtZSW/yDqXV4L\nFGYWFwevAgMBAAECggEAFdw5LiJQGuscuogYykW1UeTEyHu9jkRQ6s2qUe76DIIR\nXyRH00HHLRgfOV+4JVEj7PU/cwEQU/vgY54WlrT9R50aVERCmVinwgO6aiyjtVny\njwpf72yBHQqDz/iF323MaOHHZewFcwQR+2gScri+iwdSN0lSId9ZSPZw+XQHYCLG\n/SA+3KXiQlfoHoVi+ZNbzwqJKAwDP5hy0UsvElkULXZLCA31zZZHd9gbhKv8osJa\ngXKbqA/IBF24v+hoO0r3KGj5m+OqEHD7FcGKs5EAxBzLT01dPmPSlDghDkH78HlM\nc6XyHuQaxI6FkBG/FtK/Dy5+fpe3fzAOlxe/vVjYUQKBgQD/2vvNfwEbwggqtweV\n84GAyj7R5x+OYP1Wy5E7fZ4zcoMDxGbm5LUjt3asO8YKxUtB8bSk5HvUcmoLLKfc\nLJy1fu0gv+Xi50lAcDsSrRbpPzy+6feVqh23O5EAZj4ZndhVfyUChALVxK+V1E/a\nfZh4jHqtEOq45Dr/RCApPytckQKBgQDGK5dDtzA4fvKTHfDvidtSILGBYe3jXDX1\nqFIbdLoIcYsQzUjTrepbH4pp55Rx9n+YBHIvs0DhMB2v2kiKCBFPGj7voZbHWfCN\n17qs1gYbmq7dJkm2oPajwqgOuVQZOsjmvVJDAdQNzsMV9hW2Pz7hQ9c8xv8vs+bQ\nsfSLXldAPwKBgDBS0eA8Lp9phFVdAGfH+Bu1FyxZ9NHVa8Pq6uFLloetByW9AJp3\nc+btDdL17y+1l8M6vZ2vMdwsR+8YXhPtsSNud6cJ14eFm4Y6LE4Ytw0SzoxYcFSq\nLrae34ItzWjVMTjkrL7O5CIv5eHsmbBwrE2IatspKMwG/0WbPl/L+IqhAoGAd99I\nadq23YXVAC7dXlh6hYxnM0dkmeJedZHy0M7j9VWRdIFo6zrJh4Nlu7gssF8WQYN2\n+umodk8ftg8JUA2fQsUyisupJD+AZpy3O/Ne0HXaDsYpUsK9TsPh2r46Y+SOQB0H\nVKcXeZ63nWI1Mf/B7ouV+Bq7pERje5wZu/A+QQsCgYAdpDWyLpkSX0SpmUIyL7RC\nUqwhhJ1y1hzh91Gqs9KPz53VzoBHcXT8VmTE4DJG8Nrm3RAxgu0ydmz5n9Fq4BUX\n7E/GIEzKaswgiDUkPHjJzDVF2hs2/5jqopCBK31PxH7jst0r7Xg02AYbSyU/pMqa\ndKmjzfzBS7WlXg06wn0JxA==\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk-9qxya@kodearrow-server.iam.gserviceaccount.com",
        "client_id": "102780777134400554469",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-9qxya%40kodearrow-server.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
        }
        )
    
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        return db
    except Exception as e:
        if 'invalid_grant: Invalid JWT Signature' in str(e):
            messagebox.showinfo("Error", "Please update KodeArrow to the newest version")
            print("Please update KodeArrow to the newest version")
        else:
            messagebox.showinfo("Error", "Please update KodeArrow to the newest version")
            print(f"An error occurred: {e}")
db = initialize_firestore()


def uploadUserData():
    doc_ref_user = db.collection('ControlGroup').document("rp01@kodeArrow.com")
    usage_ref = doc_ref_user.collection('usage').document('usage_data')

    # Fetch the existing usage data
    usage_doc = usage_ref.get()

    if usage_doc.exists:
        # Extract the existing data
        existing_data = usage_doc.to_dict()
        
        # Update the existing data with new values
        existing_data['charactersTyped'] += 50
        existing_data['kodeArrowHotkeys'] += 60
        existing_data['TotalUsageMinutes'] += 10
        
        # Save the updated data back to Firestore
        usage_ref.set(existing_data)
        print("Usage data updated successfully.")
    else:
        print("Usage document does not exist. Initialize it first.")

uploadUserData()