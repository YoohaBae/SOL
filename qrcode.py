# Require python version : python 3.7.2

# install pyzbar:
#  - open cmd, type following commands
#   pip install pyzbar

# install cv2 in cmd
# - pip install opencv-python
# - pip install opencv-contrib-python
# - pip install numpy
# - pip install matplotlib

import pyzbar.pyzbar as pyzbar
import cv2

cap = cv2.VideoCapture(0)

i = 0
while(cap.isOpened()):
  ret, img = cap.read()

  if not ret:
    continue

  # 카메라로 찍은 이미지
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

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
    print(text)
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

  cv2.imshow('cam', img)

  key = cv2.waitKey(1)
  # ESC 누르면 종료
  if key == 27:
    cv2.destroyWindow('cam')
    break

cap.release()
cv2.waitKey(0)
cv2.destroyAllWindows()