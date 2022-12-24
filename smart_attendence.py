import cv2
import numpy as np
import dlib
import os
import face_recognition as facerec
import requests
#import pyttsx3 as textspeech

from datetime import datetime

def resize(img, size) :
  width = int(img.shape[1]*size)
  height = int(img.shape[0]*size)
  dimension = (width, height)
  return cv2.resize(img, dimension, interpolation=cv2.INTER_AREA)

path = 'staff_images'
staffimg = []
staffname = []
mylist = os.listdir(path)
#print(mylist)

for cl in mylist :
  curImg = cv2.imread(f'{path}\{cl}')
  staffimg.append(curImg)
  staffname.append(os.path.splitext(cl)[0])
#print(staffname)

def findencoding(images):
  encoding_list = []
  for img in images :
    img = resize(img, 0.50)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    encodeimg = facerec.face_encodings(img)[0]
    encoding_list.append(encodeimg)
  return encoding_list

def markattendence(name):
  with open('attendence.csv', 'r+') as f:
    mydatalist = f.readlines()
    namelist = []
    for line in mydatalist :
      entry = line.split(',')
      namelist.append(entry[0])

    if name not in namelist :
      now = datetime.now()
      timestr = now.strftime('%H: %M')
      f.writelines(f'\n{name}, {timestr}')
      #engine.say('Welcome' + name)
      #enigne.runAndWait()

AIRTABLE_BASEID='appAfgNCoslMU4ehB'
AIRTABLE_TOKEN='keyVMBAulTbdEjLdo'
AIRTABLE_NAME='testbase_1'

endpoint=f'https://api.airtable.com/v0/{AIRTABLE_BASEID}/{AIRTABLE_NAME}'

def add_to_airtable(name="", time=""):
    if name is None:
        return
    headers = {
        "Authorization": f"Bearer {AIRTABLE_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "records": [
            {
                "fields": {
                    "Name": name,
                    "time": time
                }
            }
        ]
    }
    r = requests.post(endpoint, json=data, headers=headers)
    print(r.json())

encode_list = findencoding(staffimg)

vid = cv2.VideoCapture(0)

while True:
  success, frame = vid.read()
  frames = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
  frames = cv2.cvtColor(frames, cv2.COLOR_BGR2RGB)

  faces_in_frame = facerec.face_locations(frame)
  encode_in_frame = facerec.face_encodings(frame, faces_in_frame)

  for encodeface, faceloc in zip(encode_in_frame, faces_in_frame):
      matches = facerec.compare_faces(encode_list, encodeface)
      facedis = facerec.face_distance(encode_list, encodeface)
      print(facedis)
      matchIndex = np.argmin(facedis)

      if matches[matchIndex]:
          name = staffname[matchIndex].upper()
          y1, x2, y2, x1 = faceloc
          y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
          cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
          cv2.rectangle(frame, (x1, y2 - 25), (x2, y2), (0, 255, 0), cv2.FILLED)
          cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
          now = datetime.now()
          time = now.strftime('%H: %M')
          markattendence(name)
          add_to_airtable(name, time)

cv2.imshow('video', frame)
cv2.waitKey(1)
