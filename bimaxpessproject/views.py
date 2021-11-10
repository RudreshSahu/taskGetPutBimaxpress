from typing import final
from django.core.mail import message
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django import http
from django.urls import path
from django.shortcuts import redirect, render, HttpResponse
from django.http import HttpResponse, request
from django.core.paginator import Paginator
from fireo.queries import filter_query
# from .decoration import adminuser
from django.core.paginator import Paginator
from pyasn1_modules.rfc2459 import Validity
from .models import *
import os
from .settings import BASE_DIR, EMAIL_BACKEND,EMAIL_PORT, EMAIL_USE_SSL
import fireo

from email.mime.multipart import MIMEMultipart
from email.utils import make_msgid
import smtplib
from django.contrib.auth.forms import UserCreationForm
from django.core.mail.message import MIMEMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import get_connection

import urllib
import imaplib
import email
import json
# from .sendemail_form import EmailForm
from django.core.mail import send_mail, send_mass_mail, EmailMessage
import re
import datetime ,pytz
import os
from datetime import date, datetime, timedelta
from django.http import HttpResponse, HttpResponseRedirect
# from background_task import background
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from email.mime.message import MIMEMessage
from textwrap import dedent
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import make_msgid
import time
from html import escape, unescape
import requests
import rpa as r

# database stuff
import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate(
    os.path.join(BASE_DIR, "serviceAccountKey.json"))
firebase_admin.initialize_app(cred)
db = firestore.client()
databunny = {}
firebaseConfig = {
    "apiKey": "AIzaSyDlZMu8lypZDEhRpMVKlD3JcTuvItFaG2A",
    "authDomain": "bimaxpress-cashless.firebaseapp.com",
    "projectId": "bimaxpress-cashless",
    "storageBucket": "bimaxpress-cashless.appspot.com",
    "messagingSenderId": "577257002368",
    "databaseURL": "https://accounts.google.com/o/oauth2/auth",
    "appId": "1:577257002368:web:489252768c47b398465d65",
    "measurementId": "G-Y8B68GW5YX"
}

mth = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
       "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
week = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']
allpage=0
firebase = pyrebase.initialize_app(firebaseConfig)
authe = firebase.auth()    


last_pop = {}
first_pop = {}
mylist = []
all_cases = 0

def postsignIn(request):
    global mylist
    global last_pop
    global first_pop
    global all_cases
    
    try:
        context={}
        cases_data={}
        values={}
        mydoctor={}
        mylist = []
        list_status = ['draft',  'Unprocessed', 'query', 'Approved', 'Reject',
                    'Enhance', "fci",'Discharge_Approved', 'Settled']        
        if request.method == "POST":
            email = request.POST.get('email')
            pasw = request.POST.get('pass')
            try:
                user = authe.sign_in_with_email_and_password(email, pasw)
                request.session['email'] = user['email']
                
                
                return HttpResponse("THIS WILL BE HOME PAGE")

            except:
                message = "Invalid Credentials!!Please ChecK your Data"
                return render(request, "login.html", {"message": message})
        else:
            return redirect("login")
    except:
        return redirect("login")



selectedhospital = ""


def mainpage(request):
    print("got it")
    global mylist
    global last_pop
    global first_pop
    global all_cases
    
    context = {}
    cases_data = {}
    mylist = []
    list_status = ['draft',  'Unprocessed', 'query', 'Approved', 'Reject',
                   'Enhance', "fci",'Discharge_Approved', 'Settled']
    if request.session['role'] == 'dataentry':
        print("role ",request.session['role'])
        accessdata={}
        context={}
        wholedata=[]
        hospitallist={}
        docs = db.collection(u'hospitals').stream()
        for doc in docs:
            hospitallist[doc.id] = doc.to_dict()['name']
        try:
            lessdata={}
            context["data"] = doc.to_dict()
            case = db.collection(u'hospitals').document("abnew@gmail.com").collection("cases").where(u'RPA', u'==', 'notdone').order_by(u'ageing').get()
            all_cases = len(case)
            doctemp = db.collection(u'hospitals').document("abnew@gmail.com").collection("cases").where(u'RPA', u'==', 'notdone').order_by(u'ageing').limit(3).stream()
            for i in doctemp:
                new_dict = i.to_dict()
                new_dict["hospital_email"] = "abnew@gmail.com"
                a = new_dict['audit_trail']
                lastelement = a[len(a)-1]
                lastelement = lastelement.split("+")
                new_dict["lastaction"] = lastelement[2]
                lessdata[i.id] = new_dict
                mylist.append(i.to_dict())

            if len(lessdata) > 0:        
                wholedata.append(lessdata)

            
            if(len(mylist) == 0):
                last_doc = {}
                last_pop = {}
                print("last pop value is", last_pop)
            else:
                last_doc = mylist[len(mylist)-1]
                last_pop = last_doc[u'ageing']
                print("last pop value is", last_pop)
                
                # context["cases_data"] = cases_data
            accessdata['hospitalLists'] = hospitallist   
            accessdata['list_status'] = list_status
            accessdata['lessdata'] = lessdata
            accessdata['wholedata'] = wholedata
            accessdata['role'] = request.session['role']
            accessdata['all_cases'] = all_cases
            accessdata['mylist'] =  len(mylist)
            return render(request, "index.html", accessdata) 
            
        except Exception as e:
            print(e)

    print("this is role ", request.session['role'])
    print("hospooiiiiiiiiiiiii",request.session['hospital_email'])
    
    cases_draft = db.collection(u'hospitals').document(request.session['hospital_email']).collection('cases').where(u'status', u'==', "done").where("formstatus", "==" , "draft").get()
    
    doc_ref = db.collection(u'counter').document(request.session['hospital_email'])

    doc_counter = doc_ref.get()
    if doc_counter.exists:
        values = doc_counter.to_dict()
    else:
        print(u'No such document!')
        
    if request.session['role'] != 'admin':
        case = db.collection(u'hospitals').document(request.session['hospital_email']).collection('cases').where(u'status', u'==', "done").where("formstatus", "==" , "draft").order_by(u'ageing').get()
        all_cases = len(case)
        cases = db.collection(u'hospitals').document(request.session['hospital_email']).collection('cases').where(u'status', u'==', "done").where("formstatus", "==" , "draft").order_by(u'ageing').limit(3).stream()
        for i in cases:
            new_dict = i.to_dict()
            a = new_dict['audit_trail']
            lastelement = a[len(a)-1]
            lastelement = lastelement.split("+")
            new_dict["lastaction"] = lastelement[2]
            cases_data[i.id] = new_dict
            mylist.append(i.to_dict())

        if(len(mylist) == 0):
            last_doc = {}
            last_pop = {}
            print("last pop value is", last_pop)
        else:
            last_doc = mylist[len(mylist)-1]
            last_pop = last_doc[u'ageing']
            print("last pop value is", last_pop)
            
        print(values)
        context['draft'] = len(cases_draft)
        context["cases_data"] = cases_data
        context['list_status'] = list_status
        context['values'] = values
        context['hospital_email'] = request.session['hospital_email']
        context['role'] = request.session['role']
        context['all_cases'] = all_cases
        context['mylist'] =  len(mylist)
        return render(request, "index.html", context)
            
    else:
        print("this is session",request.session['hospital_email'])
        case = db.collection(u'hospitals').document(request.session['hospital_email']).collection('cases').where(u'status', u'==', "done").where("formstatus", "==" , "draft").order_by(u'ageing').get()
        all_cases = len(case)
        cases = db.collection(u'hospitals').document(request.session['hospital_email']).collection('cases').where(u'status', u'==', "done").where("formstatus", "==" , "draft").order_by(u'ageing').limit(3).stream()

        for i in cases:
            new_dict = i.to_dict()
            
            a = new_dict['audit_trail']
            lastelement = a[len(a)-1]
            lastelement = lastelement.split("+")
            new_dict["lastaction"] = lastelement[2]
            cases_data[i.id] = new_dict
            mylist.append(i.to_dict())

        print("the length of my list is", len(mylist))

        if(len(mylist) == 0):
            last_doc = {}
            last_pop = {}
            print("last pop value is", last_pop)
        else:
            last_doc = mylist[len(mylist)-1]
            last_pop = last_doc[u'ageing']
            print("last pop value is", last_pop)
        
        
            
            
        print(values)
        context['draft'] = len(cases_draft)
        context["cases_data"] = cases_data
        context['list_status'] = list_status
        context['values'] = values
        context['hospital_email'] = request.session['hospital_email']
        context['role'] = request.session['role']
        context['all_cases'] = all_cases
        context['mylist'] =  len(mylist)
        return render(request, "index.html", context)
   



def logout(request):
    request.session.flush()
    return redirect('login')

def index(request):
    return render(request, 'index.html')


def about(request):
    return HttpResponse("About page bolte")

def login(request):
    return render(request, 'login.html')

def sendmail(request):
    try:
        emailId = request.session['hospital_email']
        data = db.collection(u'hospitals').document(emailId).get()
        user = data.to_dict()['Emailer']
        emailId = user['email']
        # emailId = 'anishshende001@gmail.com'
        smtpVal = user['smtp']
        imapVal = user['imap']
        password = user['password']
        if request.method == 'POST':
            sub = request.POST.get('email_title',"")
            body = request.POST.get('email_content',"")
            print("body",body)
            check = request.POST.get('cc',"")
            Cc = check.split(" ")
            print("cc value is ",Cc)
            consultPapers = request.FILES.getlist('uploadConsultation')
            healthCard = request.FILES.getlist("uploadPatientsHealth")
            aadharCard  = request.FILES.getlist("idproofid")
            preauth = request.FILES.getlist("uploadSigned")
            otherDocument = request.FILES.getlist("otherDocumentsg")
            print(healthCard,consultPapers,preauth,consultPapers,otherDocument)
            
            print('**********************************')
            
            files = healthCard+consultPapers+aadharCard+preauth+otherDocument
            print(sub)
            print(body)
            list = request.POST.get('sendbtn')
            Bcc =""
            data = list.split('+')
            companyName = data[0] 
            case = data[2]
            db.collection(u'hospitals').document(data[1]).collection('cases').document(case).update({
                "formstatus":"Unprocessed",
                "RPA":"notdone",
                'rpastatus':"draft",
            })
            db.collection(u'counter').document(request.session['hospital_email']).update({
                            'draft': firestore.Increment(-1),
                            'Unprocessed': firestore.Increment(1),
            })
            
            print(companyName)
            print(case)
            companyName = companyName.replace(" ","_")
            companyDetails = db.collection(u'InsuranceCompany_or_TPA').document(companyName).get().to_dict()
            print(companyDetails)
            to = companyDetails['email']
            # to = 'cse180001006@iiti.ac.in'
            try:
                print("emailid",emailId)
                print("emailid",to)
                
                print("password",)
                
                sendemail(emailId,to,sub,body,Bcc,Cc,files,smtpVal,imapVal,password)
            except:
                context={}
                message="Emailer has some issue please send mail Manually"
                context['message'] = message
                return render(request,"404.html",context)
            
            return redirect('mainpage')
    except Exception as e:
        return HttpResponse("Exception",e)
    
def resendemail(request):
    if request.method == "POST":
        data = request.POST.dict()
    if data['email'] != "":
        authe.send_password_reset_email(data['email'])
    else:
        return redirect("login")
    
    return redirect("login")
     
def get_name(email):
    try:
        name = ''
        for char in email:
            if char == '@':
                return name
            name = name+char
    except:
        return None




# def savestatus(request):
#     if request.method == "POST":
#         data = request.POST.dict()
#         validity = request.POST.get('situation',"")
#         qry = request.POST.get('qry',"")
#         fci = request.POST.get('fci',"")
        
    
        
    
#     # city_ref = db.collection(u'hospitals').document(request.session['hospital_email']).collection(u'cases').document(data['save'])
#     print('********')
#     list = data['save'].split(',')
#     print(list)
    
#     if request.session['role'] == 'dataentry':
#         caseNumber = list[0]
#         data['save'] = caseNumber
#         insuranceCompany = list[1]
#         currentformstatus = list[2]
#         email = list[3]
#         print("length of list",len(list))
#         newformstatus=data['status']
#         print("casenumber",caseNumber)
#         print(insuranceCompany,currentformstatus,newformstatus)
        
#         if newformstatus == 'query':
#             if qry == 'yes':
#                 db.collection(u'hospitals').document(email).collection(u'cases').document(f'{caseNumber}').update({"audit_trail": firestore.ArrayUnion([data.get(
#                 f'{newformstatus}', f'{newformstatus}')+'+'+datetime.today().strftime('%Y-%m-%d')+'+'+"Query Recieved"+'+'+data.get('fileLink',"")])})
#             else:
#                 db.collection(u'hospitals').document(email).collection(u'cases').document(f'{caseNumber}').update({"audit_trail": firestore.ArrayUnion([data.get(
#                 f'{newformstatus}', f'{newformstatus}')+'+'+datetime.today().strftime('%Y-%m-%d')+'+'+"Query Submitted"+'+'+data.get('fileLink',"")])})
                
#         elif newformstatus == 'Approved':
#             db.collection(u'hospitals').document(email).collection(u'cases').document(f'{caseNumber}').update({"audit_trail": firestore.ArrayUnion([data.get(
#             f'{newformstatus}', f'{newformstatus}')+'+'+datetime.today().strftime('%Y-%m-%d')+'+'+"Preauth Approved"+'+'+data.get('fileLink',"")])})
        
#         elif newformstatus == 'Discharge_Approved':
#             db.collection(u'hospitals').document(email).collection(u'cases').document(f'{caseNumber}').update({"audit_trail": firestore.ArrayUnion([data.get(
#             f'{newformstatus}', f'{newformstatus}')+'+'+datetime.today().strftime('%Y-%m-%d')+'+'+"Discharge Approved"+'+'+data.get('fileLink',"")])})
        
#         elif newformstatus == 'fci':
#             if fci == 'yes':
#                 db.collection(u'hospitals').document(email).collection(u'cases').document(f'{caseNumber}').update({"audit_trail": firestore.ArrayUnion([data.get(
#             f'{newformstatus}', f'{newformstatus}')+'+'+datetime.today().strftime('%Y-%m-%d')+'+'+"Final claim Requested"+'+'+data.get('fileLink',"")])})
#             else :    
#                 db.collection(u'hospitals').document(email).collection(u'cases').document(f'{caseNumber}').update({"audit_trail": firestore.ArrayUnion([data.get(
#                 f'{newformstatus}', f'{newformstatus}')+'+'+datetime.today().strftime('%Y-%m-%d')+'+'+"Final claim Reject"+'+'+data.get('fileLink',"")])})
            
#         elif newformstatus == 'Enhance':
#             if validity == 'yes':
#                 db.collection(u'hospitals').document(email).collection(u'cases').document(f'{caseNumber}').update({"audit_trail": firestore.ArrayUnion([data.get(
#                 f'{newformstatus}', f'{newformstatus}')+'+'+datetime.today().strftime('%Y-%m-%d')+'+'+"Enhance Approved"+'+'+data.get('fileLink',"")])})
#             else:
#                 db.collection(u'hospitals').document(email).collection(u'cases').document(f'{caseNumber}').update({"audit_trail": firestore.ArrayUnion([data.get(
#                 f'{newformstatus}', f'{newformstatus}')+'+'+datetime.today().strftime('%Y-%m-%d')+'+'+"Enhance Rejected"+'+'+data.get('fileLink',"")])})
                

#         else:
#             db.collection(u'hospitals').document(email).collection(u'cases').document(f'{caseNumber}').update({"audit_trail": firestore.ArrayUnion([data.get(
#             f'{newformstatus}', f'{newformstatus}')+'+'+datetime.today().strftime('%Y-%m-%d')+'+'+"Status Change"+'+'+data.get('fileLink',"")])})

    
#         db.collection(u'hospitals').document(email).collection(u'cases').document(f'{caseNumber}').update({
#             'formstatus': newformstatus,
#             'rpastatus': newformstatus,
#             f'{newformstatus}settledate': data.get('date', ""),
#             f'{newformstatus}settleamount': data.get('amount', ""),
#             'status': "done"
#         })
        
#         if(currentformstatus != newformstatus):
#             db.collection(u'counter').document(email).update({
#                 f'{currentformstatus}': firestore.Increment(-1),
#                 f'{newformstatus}': firestore.Increment(1),              
#         })
    
#         return redirect('mainpage')
    
    
#     if len(list) == 3:
#         caseNumber = list[0]
#         data['save'] = caseNumber
#         insuranceCompany = list[1]
#         currentformstatus = list[2]
#         print("length of list",len(list))
#         newformstatus=data['status']
#         # print(city_ref)
#         files = request.FILES.getlist('files')
#         check = request.POST.get('cc',"")
#         Cc = check.split(" ")
#         sub = data['email_title']
#         msg = data['email_content']
#         toEmail = db.collection(u'InsuranceCompany_or_TPA').document(insuranceCompany).get().to_dict()['email']

#         print('***********************')

#         try:
#             if newformstatus == 'query':
#                 db.collection(u'hospitals').document(request.session['hospital_email']).collection(u'cases').document(f'{caseNumber}').update({"audit_trail": firestore.ArrayUnion([data.get(
#                 f'{newformstatus}', f'{newformstatus}')+'+'+datetime.today().strftime('%Y-%m-%d')+'+'+"Query Responded"+'+'+data.get('fileLink',"")])})

#             elif newformstatus == 'Discharge_Approved':
#                 db.collection(u'hospitals').document(request.session['hospital_email']).collection(u'cases').document(f'{caseNumber}').update({"audit_trail": firestore.ArrayUnion([data.get(
#                 f'{newformstatus}', f'{newformstatus}')+'+'+datetime.today().strftime('%Y-%m-%d')+'+'+"Discharge Approval Requested"+'+'+data.get('fileLink',"")])})

#             elif newformstatus == 'Enhance':
#                 db.collection(u'hospitals').document(request.session['hospital_email']).collection(u'cases').document(f'{caseNumber}').update({"audit_trail": firestore.ArrayUnion([data.get(
#                 f'{newformstatus}', f'{newformstatus}')+'+'+datetime.today().strftime('%Y-%m-%d')+'+'+"Enhance Requested"+'+'+data.get('fileLink',"")])})
            
#             elif newformstatus == 'fci':
#                 db.collection(u'hospitals').document(request.session['hospital_email']).collection(u'cases').document(f'{caseNumber}').update({"audit_trail": firestore.ArrayUnion([data.get(
#             f'{newformstatus}', f'{newformstatus}')+'+'+datetime.today().strftime('%Y-%m-%d')+'+'+"final claim Initiated"+'+'+data.get('fileLink',"")])})
            
#             else:
#                 db.collection(u'hospitals').document(request.session['hospital_email']).collection(u'cases').document(f'{caseNumber}').update({"audit_trail": firestore.ArrayUnion([data.get(
#                     f'{newformstatus}', f'{newformstatus}')+'+'+datetime.today().strftime('%Y-%m-%d')+'+'+data['email_title']+'+'+data.get('fileLink',"")])})

            
#             db.collection(u'hospitals').document(request.session['hospital_email']).collection(u'cases').document(f'{caseNumber}').update({
#                 'formstatus': data['status'],
#                 f'{newformstatus}settledate': data.get('date', ""),
#                 f'{newformstatus}settleamount': data.get('amount', ""),
#                 'status': "done"
#             })

#             if(currentformstatus != newformstatus):
#                 db.collection(u'counter').document(request.session['hospital_email']).update({
#                                 f'{currentformstatus}': firestore.Increment(-1),
#                                 f'{newformstatus}': firestore.Increment(1),              
#             })
                
#         except Exception as e:
#             print("Exception aarh h ")
#             return HttpResponse("Exception",e)

#         fromEmail = request.session['hospital_email'] 
        
#         details = db.collection(u'hospitals').document(fromEmail).get().to_dict()['Emailer']	
#         fromEmail = details['email']
#         smtpVal = details['smtp']
#         imapVal = details['imap']
#         password = details['password']
#         Bcc = ""
        
        
#         sendemail(fromEmail,toEmail,sub,msg,Bcc,Cc,files,smtpVal,imapVal,password)
            
#         return redirect("mainpage")
#     else:
#         caseNumber = list[0]
#         data['save'] = caseNumber
#         insuranceCompany = list[1]
#         currentformstatus = list[2]
#         print("length of list",len(list))
#         newformstatus=data['status']
        
        
#         print("check statement",caseNumber,newformstatus,currentformstatus)
#         try:
#             if newformstatus == 'query':
#                 db.collection(u'hospitals').document(request.session['hospital_email']).collection(u'cases').document(f'{caseNumber}').update({"audit_trail": firestore.ArrayUnion([data.get(
#                 f'{newformstatus}', f'{newformstatus}')+'+'+datetime.today().strftime('%Y-%m-%d')+'+'+"Query Responded"+'+'+data.get('fileLink',"")])})

#             elif newformstatus == 'Discharge_Approved':
#                 db.collection(u'hospitals').document(request.session['hospital_email']).collection(u'cases').document(f'{caseNumber}').update({"audit_trail": firestore.ArrayUnion([data.get(
#                 f'{newformstatus}', f'{newformstatus}')+'+'+datetime.today().strftime('%Y-%m-%d')+'+'+"Discharge Approval Requested"+'+'+data.get('fileLink',"")])})

#             elif newformstatus == 'Enhance':
#                 db.collection(u'hospitals').document(request.session['hospital_email']).collection(u'cases').document(f'{caseNumber}').update({"audit_trail": firestore.ArrayUnion([data.get(
#                 f'{newformstatus}', f'{newformstatus}')+'+'+datetime.today().strftime('%Y-%m-%d')+'+'+"Enhance Requested"+'+'+data.get('fileLink',"")])})
            
#             elif newformstatus == 'fci':
#                 db.collection(u'hospitals').document(request.session['hospital_email']).collection(u'cases').document(f'{caseNumber}').update({"audit_trail": firestore.ArrayUnion([data.get(
#             f'{newformstatus}', f'{newformstatus}')+'+'+datetime.today().strftime('%Y-%m-%d')+'+'+"final claim Initiated"+'+'+data.get('fileLink',"")])})
            
#             else:
#                 db.collection(u'hospitals').document(request.session['hospital_email']).collection(u'cases').document(f'{caseNumber}').update({"audit_trail": firestore.ArrayUnion([data.get(
#                     f'{newformstatus}', f'{newformstatus}')+'+'+datetime.today().strftime('%Y-%m-%d')+'+'+data['email_title']+'+'+data.get('fileLink',"")])})
            
#             db.collection(u'hospitals').document(request.session['hospital_email']).collection(u'cases').document(f'{caseNumber}').update({
#                 'formstatus': data['status'],
#                 f'{newformstatus}settledate': data.get('date', ""),
#                 f'{newformstatus}settleamount': data.get('amount', ""),
#                 'status': "done"
#             })
            
#             if(currentformstatus != newformstatus):
#                 db.collection(u'counter').document(request.session['hospital_email']).update({
#                                 f'{currentformstatus}': firestore.Increment(-1),
#                                 f'{newformstatus}': firestore.Increment(1),              
#                 })
#         except:
#             print("Exception aarh h")
#             return redirect("error_404")        
#         return redirect("mainpage")

       
def error_404(request,exception):
    return render(request,"404.html");

def error_500(request):
        return render(request,"404.html")

def error_403(request,  exception):
        return render(request,"404.html")

def error_400(request,  exception):
        return render(request,"404.html")

def newAction(request):
    return render(request, 'newAction.html')


def loginPage(request):
    return render(request, 'loginPage.html')


def companyDetails(request):
    return render(request, 'companyDetails.html')

# Emailer Anish
def optimiser(s):
    if(s[0] == '"' and s[len(s)-1] == '"'):
        return s[1:-1]
    else:
        return s


def helper(s):
    s = str(s)
    if(s[0] == '0'):
        return s[1:]
    else:
        return s

def spliteremail(s):
    if(s == None):
        return "", ""
    idx = s.find('<')
    if(idx == -1):
        return s, s
    lgth = len(s)
    # print(s)
    x_name = s[:idx-1]
    if s[:-1].isalpha():
        y_email = s[idx+1:]

    else:
        y_email = s[idx+1:-1]
    # print (y_email)
    # print("-"*50)
    return x_name, y_email

def func(s):
    if(s[:2].isdigit()):
        x = s[:2]
        y = s[2:]
    else:
        x = s[:1]
        y = s[1:]

    # print(x)
    # print(y)
    return x, y


def spliterdate(s):
    if s == None:
        return "0"
    if(s[0:3] in week):
        day = s[5:11]
    else:
        day = s[0:6]
    # print(day)
    # print("xxxxxx")

    final = day
    monthdate = day.replace(" ", "")
    curr = datetime.today()
    date, day = func(monthdate)
    date = helper(date)
    day = mth.index(day) + 1
    tdate = helper(curr.day)
    tmonth = helper(curr.month)

    if(date == tdate and day == tmonth):
        return "today"
    else:
        s = date + " " + mth[day-1]
        return s
    
def bunny(request):
    context = {}
    # sender = "anish@bimaxpress.com"
    sender = request.session['hospital_email']
    # sender = "harshyadav24@yahoo.com"
    print(sender)
        # sender = 'newuser@gmail.com'

    data = db.collection(u'hospitals').document(sender).get()
        
    user = data.to_dict()['Emailer']

    imapVal = user['imap']
    smtpVal = user['smtp']
    emailID = user['email']
    password = user['password']
    # print(emailID)
    # print(password)


    if request.method == "POST":
        
        file = request.FILES.getlist("filenameupload")
       
        sender_msg = request.POST.get('smsg')
        reciever = request.POST.get('recv')
        Bcc = request.POST.get('recvBcc')
        Cc = request.POST.get('recvCc')
        sub = request.POST.get('ssub')
        # att = request.POST.get('filenameupload')
        
        print('_'*50)
        print(os.environ)
        print('_'*50)
        # print(len(file))

        sendemail(emailID, reciever, sub, sender_msg, Bcc, Cc,file,smtpVal,imapVal,password)


    imap_server = imaplib.IMAP4_SSL(host=imapVal)
    print("this is imap",imap_server)
    
    imap_server.login(emailID, password)
    
    imap_server.select()  # Default is `INBOX`

    # status, resp = imap_server.status('INBOX')
    # print(status)
    # print(resp)

    count = 0
    # Find all emails in inbox
    _, message_numbers_raw = imap_server.search(None, 'ALL')
    # search_criteria = 'REVERSE DATE'
    # _, message_numbers_raw = imap_server.sort(search_criteria, 'UTF-8', 'ALL')
    message = []
    count = 1
    flag = 0

    arr = list(reversed(message_numbers_raw[0].split()))
    # print(arr)
    totalmsgs = int(len(arr)/10) + 1
    page_id = 8
    n = 10
    leftind = (page_id-1)*n
    rightind = min((page_id*n),len(arr))
    searchArr = arr[leftind:rightind]

    # for message_number in reversed(message_numbers_raw[0].split()):
    for message_number in searchArr:
    # for ct in range(count, count+10):
    #     if(count == 11):
    #         break
        # message_number = "b'"+str(ct)+"'"
        
        print(message_number)
        print('_____________________')
        _, msg = imap_server.fetch(message_number, '(RFC822)')

        # Parse the raw email message in to a convenient object
        x = email.message_from_bytes(msg[0][1])
        nameid, emailid = spliteremail(x['from'])
        print(x['from'])
        print(x['date'])
        print('_' * 50)
        time = spliterdate(x['date'])
        if (x['to'] == None):
            continue;
        


        # nameid = emailID = time = ""

        # print("========email start===========")
        # print(x)
        # print("========email end===========")
        print("to message",x["to"])
        
        newtext = ""
        for part in x.walk():
            if (part.get('Content-Disposition') and part.get('Content-Disposition').startswith("attachment")):

                part.set_type("text/plain")
                part.set_payload('Attachment removed: %s (%s, %d bytes)'
                                 % (part.get_filename(),
                                    part.get_content_type(),
                                    len(part.get_payload(decode=True))))
                del part["Content-Disposition"]
                del part["Content-Transfer-Encoding"]
            # print("part print")
            # print(part)
            if part.get_content_type().startswith("text/plain"):
                newtext += "\n"
                newtext += part.get_payload(decode=False)

        msg_json = {
            # "from" : x['from'],
            "from": escape(emailid),
            "name": escape(optimiser(nameid)),
            "to": escape(x['to']),
            "subject": escape(x['subject']),
            
            "message": escape(newtext),
            "date": escape(time),
            "id": count,
        }
        # print(newtext)
        count += 1
        message.append(msg_json)

    email_message = json.dumps(message)
    # print(email_message)s
    a = eval(email_message)
    # print(a)
    from_list = []
    to_list = []
    sub_list = []
    date_list = []
    l = []
    totalmsgList = []
    time_list = []

    # for i in reversed(range(len(a))):
    for i in range(1,totalmsgs+1):
        totalmsgList.append(str(i))

    for i in range(len(a)):
        print("+++++++++++")
        l.append(a[i])
        from_list.append(a[i]['from'])
        to_list.append(a[i]['to'])
        sub_list.append(a[i]['subject'])
        date_list.append(a[i]['date'])

    # print(l)
    context['data_from'] = from_list
    context['data_to'] = to_list
    context['data_sub'] = sub_list
    context['data_date'] = date_list
    context['data'] = l
    context['pageidlist'] = totalmsgList
    context['pagecount'] = len(totalmsgList)
    
    return render(request, "baseemail.html", context)

def replymail(request):
    context = {}
    # print(request.method)
    if request.method == "POST":
        file = request.FILES.getlist("filenameupload")
        sender = request.session['hospital_email']
        data = db.collection(u'hospitals').document(sender).get()
        user = data.to_dict()['Emailer']
        imapVal = user['imap']
        emailID = user['email']
        password = user['password']

        # file = request.FILES['filenameupload']

        sender_msg = request.POST.get('rep_smsg')
        reciever = request.POST.get('rep_recv')

        Bcc = request.POST.get('rep_recvBcc')
        Cc = request.POST.get('rep_recvCc')
        sub = request.POST.get('rep_ssub')
        m_id = request.POST.get('rep_id')
        # att = request.POST.get('filenameupload')
        # sender = "anish@bimaxpress.com"

        imap_server = imaplib.IMAP4_SSL(host=imapVal)
        imap_server.login(emailID, password)
        imap_server.select()

        _, msg = imap_server.fetch(m_id, '(RFC822)')
        email_msg = email.message_from_bytes(msg[0][1])

        newtext = ""

        new = EmailMultiAlternatives("Re: "+email_msg["Subject"],
                                     sender_msg,
                                     sender,  # from
                                     [email_msg["Reply-To"]
                                         or email_msg["From"]],  # to
                                     headers={'Reply-To': sender,
                                              "In-Reply-To": email_msg["Message-ID"],
                                              "References": email_msg["Message-ID"]})
        # new.attach_alternative(sender_msg, "text/plain")
        new.attach(MIMEMessage(email_msg))
        # print(new.body) # attach original message
        for f in file:
            new.attach(f.name, f.read(),f.content_type)

        new.send()
        next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)
    # return render(request,"baseemail.html",context)





def sentmail(request):
    context = {}

    sender = request.session['hospital_email']
    data = db.collection(u'hospitals').document(sender).get()
    user = data.to_dict()['Emailer']
    imapVal = user['imap']
    smtpVal = user['smtp']
    emailID = user['email']
    password = user['password']

    # emailID = sender = 'anishshende001@gmail.com'
    # password = 'Anish@123'

    if request.method == "POST":
        file = request.FILES.getlist("filenameupload")
        # file = request.FILES['filenameupload']
        sender_msg = request.POST.get('smsg')
        reciever = request.POST.get('recv')
        Bcc = request.POST.get('recvBcc')
        Cc = request.POST.get('recvCc')
        sub = request.POST.get('ssub')
        # att = request.POST.get('filenameupload')
        # sender = "anish@bimaxpress.com"
        # print(len(file))
        sendemail(sender, reciever, sub, sender_msg, Bcc, Cc,file,smtpVal,imapVal,password)
    # print(data)

    imap_server = imaplib.IMAP4_SSL(host=imapVal)
    imap_server.login(emailID, password)
    print(imap_server.list())

    # sent folder selected
    if imapVal == 'imap.gmail.com':
        imap_server.select('"[Gmail]/Sent Mail"')
        
    else:
        imap_server.select('Sent')

    count = 0
    # Find all emails in inbox
    _, message_numbers_raw = imap_server.search('',None, 'ALL')

    message = []
    count = 0
    for message_number in message_numbers_raw[0].split():
        _, msg = imap_server.fetch(message_number, '(RFC822)')

        # Parse the raw email message in to a convenient object
        x = email.message_from_bytes(msg[0][1])
        # print(x['from'])
        nameid, emailid = spliteremail(x['from'])
        time = spliterdate(x['date'])
        to = ""
        ssub = ""
        mssg = ""
        if(x['to'] != None):
            to = x['to']

        if(x['subject'] != None):
            ssub = x['subject']

        if(x['message'] != None):
            mssg = x['message']

        newtext = ""
        for part in x.walk():
            if (part.get('Content-Disposition') and part.get('Content-Disposition').startswith("attachment")):

                part.set_type("text/plain")
                part.set_payload('Attachment removed: %s (%s, %d bytes)'
                                 % (part.get_filename(),
                                    part.get_content_type(),
                                    len(part.get_payload(decode=True))))
                del part["Content-Disposition"]
                del part["Content-Transfer-Encoding"]

            if part.get_content_type().startswith("text/plain"):
                newtext += "\n"
                newtext += part.get_payload(decode=False)

        msg_json = {
            "from": emailid,
            "name": nameid,
            "to": to,
            "subject": ssub,
            "date": time,
            "id": count,
            "message": newtext,
        }

        if(emailid):
            count += 1
            message.append(msg_json)

    imap_server.close()
    imap_server.logout()

    email_message = json.dumps(message)
    print(email_message)

    a = eval(email_message)
    from_list = []
    to_list = []
    sub_list = []
    date_list = []
    l = []
    time_list = []

    for i in reversed(range(len(a))):
        # print(a[i]['from'])
        # print(a[i]['message'])
        l.append(a[i])
        from_list.append(a[i]['from'])
        to_list.append(a[i]['to'])
        sub_list.append(a[i]['subject'])
        date_list.append(a[i]['date'])

    # print(l)
    context['data_from'] = from_list
    context['data_to'] = to_list
    context['data_sub'] = sub_list
    context['data_date'] = date_list
    context['data'] = l

    return render(request, "sentemail.html", context)


# TRASH Folder



# def trashmail(request):
#     context = {}
#     if request.method == "POST":
#         file = request.FILES.getlist("filenameupload")
#         sender = request.session['hospital_email']
#         data = db.collection(u'hospitals').document(sender).get()
#         user = data.to_dict()['Emailer']
#         imapVal = user['imap']
#         smtpVal = user['smtp']
#         emailID = user['email']
#         password = user['password']
#         # file = request.FILES['filenameupload']
#         sender_msg = request.POST.get('smsg')
#         reciever = request.POST.get('recv')
#         Bcc = request.POST.get('recvBcc')
#         Cc = request.POST.get('recvCc')
#         sub = request.POST.get('ssub')
#         # att = request.POST.get('filenameupload')
#         # sender = "anish@bimaxpress.com"
#         # print(len(file))
#         sendemail(sender, reciever, sub, sender_msg, Bcc, Cc,file,smtpVal,imapVal,password)
#     # print(data)

#     imap_server = imaplib.IMAP4_SSL(host=imapVal)
#     imap_server.login(emailID, password)
#     imap_server.select('INBOX.Trash')  # Default is `INBOX`
#     count = 0
#     # Find all emails in inbox
#     _, message_numbers_raw = imap_server.search(None, 'ALL')

#     message = []
#     count = 0
#     for message_number in message_numbers_raw[0].split():
#         _, msg = imap_server.fetch(message_number, '(RFC822)')

#         # Parse the raw email message in to a convenient object
#         x = email.message_from_bytes(msg[0][1])
#         nameid, emailid = spliteremail(x['from'])
#         time = spliterdate(x['date'])

#         newtext = ""
#         for part in x.walk():
#             if (part.get('Content-Disposition') and part.get('Content-Disposition').startswith("attachment")):

#                 part.set_type("text/plain")
#                 part.set_payload('Attachment removed: %s (%s, %d bytes)'
#                                  % (part.get_filename(),
#                                     part.get_content_type(),
#                                     len(part.get_payload(decode=True))))
#                 del part["Content-Disposition"]
#                 del part["Content-Transfer-Encoding"]

#             if part.get_content_type().startswith("text/plain"):
#                 newtext += "\n"
#                 newtext += part.get_payload(decode=False)

#         msg_json = {
#             "from": emailid,
#             "name": nameid,
#             "to": x['to'],
#             "subject": x['subject'],
#             "date": time,
#             "id": count,
#             "message": newtext,
#         }
#         count += 1
#         message.append(msg_json)

#     email_message = json.dumps(message)
#     # print(email_message)s
#     a = eval(email_message)
#     from_list = []
#     to_list = []
#     sub_list = []
#     date_list = []
#     l = []
#     time_list = []

#     for i in reversed(range(len(a))):
#         # print(a[i]['from'])
#         l.append(a[i])
#         from_list.append(a[i]['from'])
#         to_list.append(a[i]['to'])
#         sub_list.append(a[i]['subject'])
#         date_list.append(a[i]['date'])

#     # print(l)
#     context['data_from'] = from_list
#     context['data_to'] = to_list
#     context['data_sub'] = sub_list
#     context['data_date'] = date_list
#     context['data'] = l

#     return render(request, "trash.html", context)

# # DRAFTS Folder



def draftmail(request):
    context = {}
    if request.method == "POST":
        file = request.FILES.getlist("filenameupload")
        sender = request.session['hospital_email']
        data = db.collection(u'hospitals').document(sender).get()
        user = data.to_dict()['Emailer']
        imapVal = user['imap']
        smtpVal = user['smtp']
        emailID = user['email']
        password = user['password']

        # file = request.FILES['filenameupload']
        sender_msg = request.POST.get('smsg')
        reciever = request.POST.get('recv')
        Bcc = request.POST.get('recvBcc')
        Cc = request.POST.get('recvCc')
        sub = request.POST.get('ssub')
        # att = request.POST.get('filenameupload')
        # sender = "anish@bimaxpress.com"
        # print(len(file))
        sendemail(sender, reciever, sub, sender_msg, Bcc, Cc,file,smtpVal,imapVal,password)
    # print(data)

    imap_server = imaplib.IMAP4_SSL(host=imapVal)
    imap_server.login(emailID, password)
    imap_server.select('INBOX.Sent')  # Default is `INBOX`
    count = 0
    # Find all emails in inbox
    _, message_numbers_raw = imap_server.search(None, 'ALL')

    message = []
    count = 0
    for message_number in message_numbers_raw[0].split():
        _, msg = imap_server.fetch(message_number, '(RFC822)')

        # Parse the raw email message in to a convenient object
        x = email.message_from_bytes(msg[0][1])
        nameid, emailid = spliteremail(x['from'])
        time = spliterdate(x['date'])

        newtext = ""
        for part in x.walk():
            if (part.get('Content-Disposition') and part.get('Content-Disposition').startswith("attachment")):

                part.set_type("text/plain")
                part.set_payload('Attachment removed: %s (%s, %d bytes)'
                                 % (part.get_filename(),
                                    part.get_content_type(),
                                    len(part.get_payload(decode=True))))
                del part["Content-Disposition"]
                del part["Content-Transfer-Encoding"]

            if part.get_content_type().startswith("text/plain"):
                newtext += "\n"
                newtext += part.get_payload(decode=False)

        msg_json = {
            "from": emailid,
            "name": nameid,
            "to": x['to'],
            "subject": x['subject'],
            "date": time,
            "id": count,
            "message": newtext,
        }
        count += 1
        message.append(msg_json)

    email_message = json.dumps(message)
    # print(email_message)s
    a = eval(email_message)
    from_list = []
    to_list = []
    sub_list = []
    date_list = []
    l = []
    time_list = []

    for i in reversed(range(len(a))):
        # print(a[i]['from'])
        l.append(a[i])
        from_list.append(a[i]['from'])
        to_list.append(a[i]['to'])
        sub_list.append(a[i]['subject'])
        date_list.append(a[i]['date'])

    # print(l)
    context['data_from'] = from_list
    context['data_to'] = to_list
    context['data_sub'] = sub_list
    context['data_date'] = date_list
    context['data'] = l

    return render(request, "drafts.html", context)

# Starred Folder

def starredemail(request):
    context = {}
    if request.method == "POST":
        file = request.FILES.getlist("filenameupload")
        sender = request.session['hospital_email']
        data = db.collection(u'hospitals').document(sender).get()
        user = data.to_dict()['Emailer']
        imapVal = user['imap']
        smtpVal = user['smtp']
        emailID = user['email']
        password = user['password']
        # file = request.FILES['filenameupload']
        sender_msg = request.POST.get('smsg')
        reciever = request.POST.get('recv')
        Bcc = request.POST.get('recvBcc')
        Cc = request.POST.get('recvCc')
        sub = request.POST.get('ssub')
        # att = request.POST.get('filenameupload')
        # sender = "anish@bimaxpress.com"
        # print(len(file))
        sendemail(sender, reciever, sub, sender_msg, Bcc, Cc,file,smtpVal,imapVal,password)
    # print(data)

    imap_server = imaplib.IMAP4_SSL(host=imapVal)
    imap_server.login(emailID, password)
    imap_server.select('INBOX')  # Default is `INBOX`
    count = 0
    # Find all emails in inbox
    _, message_numbers_raw = imap_server.search(None, 'ALL')

    message = []
    count = 0
    for message_number in message_numbers_raw[0].split():
        _, msg = imap_server.fetch(message_number, '(RFC822)')

        # Parse the raw email message in to a convenient object
        x = email.message_from_bytes(msg[0][1])
        nameid, emailid = spliteremail(x['from'])
        time = spliterdate(x['date'])

        newtext = ""
        for part in x.walk():
            if (part.get('Content-Disposition') and part.get('Content-Disposition').startswith("attachment")):

                part.set_type("text/plain")
                part.set_payload('Attachment removed: %s (%s, %d bytes)'
                                 % (part.get_filename(),
                                    part.get_content_type(),
                                    len(part.get_payload(decode=True))))
                del part["Content-Disposition"]
                del part["Content-Transfer-Encoding"]

            if part.get_content_type().startswith("text/plain"):
                newtext += "\n"
                newtext += part.get_payload(decode=False)

        msg_json = {
            "from": emailid,
            "name": nameid,
            "to": x['to'],
            "subject": x['subject'],
            "date": time,
            "id": count,
            "message": newtext,
        }
        count += 1
        message.append(msg_json)

    email_message = json.dumps(message)
    # print(email_message)s
    a = eval(email_message)
    from_list = []
    to_list = []
    sub_list = []
    date_list = []
    l = []
    time_list = []

    for i in reversed(range(len(a))):
        # print(a[i]['from'])
        l.append(a[i])
        from_list.append(a[i]['from'])
        to_list.append(a[i]['to'])
        sub_list.append(a[i]['subject'])
        date_list.append(a[i]['date'])

    # print(l)
    context['data_from'] = from_list
    context['data_to'] = to_list
    context['data_sub'] = sub_list
    context['data_date'] = date_list
    context['data'] = l
    
    return render(request, "starred.html", context)



def sendemail(sender, reciever, sub, sender_msg, Bcc, Cc,files,smtpVal,imapVal,password):

    connection = get_connection(
        host = smtpVal,
        port = EMAIL_PORT,
        username = sender,
        password = password ,
        use_ssl = EMAIL_USE_SSL,
        backend=EMAIL_BACKEND
    )
    
    if(len(Cc)>=5):
        email = EmailMultiAlternatives(sub, body = "%s \r\n" % sender_msg,from_email= sender, to=[reciever, ], bcc=[
                                   Bcc, ], cc=[Cc[0],Cc[1],Cc[2],Cc[3],Cc[4],],connection=connection)
    if(len(Cc)==4):
        email = EmailMultiAlternatives(sub, body = "%s \r\n" % sender_msg,from_email= sender, to=[reciever, ], bcc=[
                                   Bcc, ], cc=[Cc[0],Cc[1],Cc[2],Cc[3],],connection=connection)
    if(len(Cc)==3):
        email = EmailMultiAlternatives(sub, body = "%s \r\n" % sender_msg,from_email= sender, to=[reciever, ], bcc=[
                                   Bcc, ], cc=[Cc[0],Cc[1],Cc[2],],connection=connection)
    if(len(Cc)==2):
        email = EmailMultiAlternatives(sub, body = "%s \r\n" % sender_msg,from_email= sender, to=[reciever, ], bcc=[
                                   Bcc, ], cc=[Cc[0],Cc[1],],connection=connection)
    if(len(Cc)==1):
        email = EmailMultiAlternatives(sub, body = "%s \r\n" % sender_msg,from_email= sender, to=[reciever, ], bcc=[
                                   Bcc, ], cc=[Cc[0],],connection=connection)
    if(len(Cc)<1):
        email = EmailMultiAlternatives(sub, body = "%s \r\n" % sender_msg,from_email= sender, to=[reciever, ], bcc=[
                                   Bcc, ], cc=["",],connection=connection)
    
    
    # print(email.message())
    text = str(email.message())
    imap_server = imaplib.IMAP4_SSL(host=imapVal, port=993)

    
    imap_server.login(sender, password)
    imap_server.append('Sent', '\\Seen', imaplib.Time2Internaldate(
        time.time()), text.encode('utf8'))

    for f in files:
        email.attach(f.name, f.read(), f.content_type)

    email.send()
    connection.close()

def pageload(request):
    page_id = int(request.GET.get('data'))
    context = {}
    sender = request.session['hospital_email']
    print(sender)
    data = db.collection(u'hospitals').document(sender).get()
    user = data.to_dict()['Emailer']
    imapVal = user['imap']
    smtpVal = user['smtp']
    emailID = user['email']
    password = user['password']
# print(emailID)
# print(password)
    if request.method == "POST":
        page_id = request.POST.get("pageid")
        page_id = int(page_id)
# print(data)
    imap_server = imaplib.IMAP4_SSL(host=imapVal)
    print("this is imap", imap_server)
    imap_server.login(emailID, password)
    imap_server.select()  # Default is `INBOX`
# status, resp = imap_server.status('INBOX')
# print(status)
# print(resp)
    count = 0
# Find all emails in inbox
    _, message_numbers_raw = imap_server.search(None, 'ALL')
# search_criteria = 'REVERSE DATE'
# _, message_numbers_raw = imap_server.sort(search_criteria, 'UTF-8', 'ALL')
    message = []
    count = 1
    flag = 0
    arr = list(reversed(message_numbers_raw[0].split()))
    # print(arr)
    totalmsgs = int(len(arr) / 10) + 1
    n = 10
    leftind = (page_id - 1) * n
    rightind = min((page_id * n), len(arr))
    searchArr = arr[leftind:rightind]
# for message_number in reversed(message_numbers_raw[0].split()):
    for message_number in searchArr:
    # for ct in range(count, count+10):
    #     if(count == 11):
    #         break
    # message_number = "b'"+str(ct)+"'"
        print(message_number)
        print('_____________________')
        _, msg = imap_server.fetch(message_number, '(RFC822)')
    # Parse the raw email message in to a convenient object
        x = email.message_from_bytes(msg[0][1])
        nameid, emailid = spliteremail(x['from'])
        print(x['from'])
        print(x['date'])
        print('_' * 50)
        time = spliterdate(x['date'])
    # nameid = emailID = time = ""
    # print("========email start===========")
    # print(x)
    # print("========email end===========")
        newtext = ""
        for part in x.walk():
            if (part.get('Content-Disposition') and part.get('Content-Disposition').startswith("attachment")):
                part.set_type("text/plain")
                part.set_payload('Attachment removed: %s (%s, %d bytes)'
                             % (part.get_filename(),
                                part.get_content_type(),
                                len(part.get_payload(decode=True))))
                del part["Content-Disposition"]
                del part["Content-Transfer-Encoding"]
        # print("part print")
        # print(part)
            if part.get_content_type().startswith("text/plain"):
                newtext += "\n"
                newtext += part.get_payload(decode=False)
        msg_json = {
        # "from" : x['from'],
        "from": escape(emailid),
        "name": escape(optimiser(nameid)),
        "to": escape(x['to']),
        "subject": escape(x['subject']),
        "message": escape(newtext),
        "date": escape(time),
        "id": count,
        }
    # print(newtext)
        count += 1
        print(msg_json)
        message.append(msg_json)
    email_message = json.dumps(message)
    # print(email_message)s
    a = eval(email_message)
    # print(a)
    from_list = []
    to_list = []
    sub_list = []
    date_list = []
    l = []
    totalmsgList = []
    time_list = []
    print(len(a))
    # for i in reversed(range(len(a))):
    for k in range(1, totalmsgs + 1):
        totalmsgList.append(str(k))
    for i in range(len(a)):
        print("+++++++++++")
        l.append(a[i])
        from_list.append(a[i]['from'])
        to_list.append(a[i]['to'])
        sub_list.append(a[i]['subject'])
        date_list.append(a[i]['date'])
    # print(l)
    context['data_from'] = from_list
    context['data_to'] = to_list
    context['data_sub'] = sub_list
    context['data_date'] = date_list
    context['data'] = l
    context['pageidlist'] = totalmsgList
    context['pagecount'] = len(totalmsgList)
    context["role"] = request.session['role'] 
    return render(request, "baseemail.html", context)

def changestatus(request):
    system = request.POST.dict()
    claimno = system.get('claimno',"")
    system = system.get('finalvalue',"")
    
    flag = 0
    email = ''
    case = ''
    for char in system:
        if char == "+":
            flag = 1
        if flag == 0 and char != '+':
            email = email+char
        if flag == 1 and char != '+':
            case = case+char
    print(email)
    print(case)
    
    db.collection(u'hospitals').document(email).collection(u'cases').document(case).update({
            'rpastatus': "Unprocessed",
            'claimno': f"{claimno}",
    })
    
    return redirect('listData',p='Unprocessed')