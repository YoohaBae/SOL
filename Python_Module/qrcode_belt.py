import pyzbar.pyzbar as pyzbar
import cv2
import sqlite3 as sq
import pandas as pd
import numpy as np
import datetime

'''컨베이어 벨트에서 수하물이 돌아갈때 qr스캐너가 코드를 찍고 DB에서 확인하는 프로그램'''

def isCaptured(img):
  if pyzbar.decode(img) != []:
    return True
  
def stopwatch(array):
  if array != []:
    return (array[len(array) - 1] - array[0])

def loop_count(num_scan):
  loop = 0
  while num_scan > 0:
    if num_scan / 10 >= 1:
      loop += 1
    num_scan = num_scan - 10
  return loop


# DB part
# DB connect
# conn = sq.connect('C:\sql_output\example.db')
# cur = conn.cursor()

cap = cv2.VideoCapture(0)

i = 0
num_scan = 0
start = 0
sample = []
scans = [0]

while (cap.isOpened()):
  ret, img = cap.read()
  
  if not ret:
    continue
  
  # convert color of the image captured with webcam
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  
  if isCaptured(gray):
    stop = datetime.datetime.now()
    sample.append(stop)
    num_scan += 1
    
  if num_scan == scans[len(scans) - 1]:
    pass
  else:
    scans.append(num_scan)
    
  # decode img converted to gray
  decoded = pyzbar.decode(gray)
  
  for d in decoded:
    # calculate position in img
    x, y, w, h = d.rect
    
    # decode data in position to utf-8
    qrcode_data = d.data.decode("utf-8")
    qrcode_type = d.type
    
    # draw bounding box to qrcode
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
    
    # convert data to string
    text = '%s (%s)' % (qrcode_data, qrcode_type)
    
    # Get info from DB and create pandas table
    # query = cur.execute("SELECT * From Luggage_Database")
    # cols = [column[0] for column in query.description]
    
    # luggage_info = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)
    # conn.close()
    
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)    
  
  # Add time info and num_scan info to padas table
  # luggage_info['Time'] = stopwatch(sample)
  # luggage_info['Num_Scan'] = num_scan
  
  cv2.imshow('cam', img)
  print(loop_count(scans[len(scans) - 1]))
  print(stopwatch(sample))
  
  key = cv2.waitKey(1)
  # press ESC to terminate
  if key == 27:
        cv2.destroyWindow('cam')
        break

cap.release()
cv2.waitKey(0)
cv2.destroyAllWindows()
    
    