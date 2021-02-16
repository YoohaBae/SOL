import pyzbar.pyzbar as pyzbar
import cv2
import sqlite3
import pandas as pd
import numpy as np
import datetime

'''컨베이어 벨트에서 수하물이 돌아갈때 qr스캐너가 코드를 찍는 프로그램'''

def isCaptured(img):
  if pyzbar.decode(img) != []:
      return True
    
def stopwatch(array):   #틀렸음
    if array != []:
      return (array[len(array) - 1] - array[0])
    
# def loop_count(num_scan):  #기준이 애매함


# Database part
# DB 연결
# conn = sqlite3.connect('C:\sql_output\example.db')
# cur = conn.cursor()

cap = cv2.VideoCapture(0)

i = 0
num_scan = 0
start = 0
sample = []
scans = [0]

while(cap.isOpened()):
  ret, img = cap.read()
  
  if not ret:
    continue

  # 카메라로 찍은 이미지 색변환
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  if isCaptured(gray):
      stop = datetime.datetime.now()
      sample.append(stop)
      num_scan += 1
  
  if num_scan == scans[len(scans) - 1]:
        pass
  else:
        scans.append(num_scan)
  
  # gray로 변환한 이미지 decode
  decoded = pyzbar.decode(gray)

  for d in decoded:
        # 이미지에서의 좌표 계산
    x, y, w, h = d.rect

    # 좌표의 데이터 utf-8 형식으로 변환
    barcode_data = d.data.decode("utf-8")
    barcode_type = d.type

    # qr코드에 바운딩박스 치기
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # qr코드의 데이터 텍스트화 
    text = '%s (%s)' % (barcode_data, barcode_type)
    
    # DB에서 수하물 정보 받아와서 pandas 표에 시간 정보 추가
    # query = cur.execute("SELECT * From Luggage_Database")
    # cols = [column[0] for column in query.description]
    
    # luggage_info = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)
    
    # # 시간정보, 측정 횟수 추가
      
    # conn.close()
      
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
  
  # luggage_info['Time'] = stopwatch(sample)
  # luggage_info['Num_Scan'] = num_scan
  cv2.imshow('cam', img)
  print(scans)
  print(stopwatch(sample))

  key = cv2.waitKey(1)
  # ESC 누르면 종료
  if key == 27:
    cv2.destroyWindow('cam')
    break

cap.release()
cv2.waitKey(0)
cv2.destroyAllWindows()
