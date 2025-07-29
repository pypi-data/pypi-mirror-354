import json 
import smtplib
import time 
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#Append to the end of your recipient phone number if sending email to sms
#Specifices the mobile carrier's 
#domain name. Must be appended to phone number
#in -> sendmail(sender, recievernumber@carrierdomain.com, message)
carrier = {
  "tmobile": "@tmomail.net",
  "at&t":"@txt.att.net",
  "verizon": "@vtext.com",
  "sprint": "@messaging.sprintpcs.com"}

with open("info.json", "r") as file:
  data = json.load(file)

#Message mime
def message(data: json, subject: str, body: str):
  """
  Creates a MIME message object
  json data must have the fields below
  """
  msg = MIMEMultipart()
  msg['From'] = data['email']
  msg['To'] = data['recipient']
  msg['Subject'] = subject
  msg.attach(MIMEText(body, 'plain'))
  return msg



def sendmail(data: json, msg: MIMEMultipart):
  """
  Sends messages through mail via SMTP 
  using googles smtp server.

  Password must be an app password can be created
  in google settings. 
  """
  s = smtplib.SMTP('smtp.gmail.com', 587)
  # Displays debug messages with timestamp as message is sent
  s.set_debuglevel(2)
  s.starttls()

  s.login(data["email"], data["password"])

  s.sendmail(data["email"], f'{data["number"] + carrier["tmobile"]}', msg.as_string())

  s.quit()

def api(url: str, API_KEY: str):
  """
  A simple starter api for accessing data for use with 
  notified message features
  """
  params = {
    'country': 'us',
    'apiKey': API_KEY,
    'pageSize': 1
  }

  response = requests.get(url, params=params)
  if response.status_code == 200:
    pagedata = response.json()
    #test
    print(pagedata)
  else:
    print(f'Error: {response.status_code}')

def timer(typeoftime: str, minsec: float):
  """
  sleeps typeoftime for unit's long

  typeoftime can be min or sec

  must be used prior to smtp connection or 
  will disconnect abruptley 
  """
  if (((typeoftime != "min") & (typeoftime != "sec")) | (minsec <= 0)):
    print("invalid input, or no time added skipping timer")
    return
  elif (typeoftime == "min"):
    time.sleep(minsec * 60)
  elif (typeoftime == "sec"):
    time.sleep(minsec)

