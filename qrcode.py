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

  cv2.imshow('img', img)

  key = cv2.waitKey(1)
  if key == ord('q'):
    break
  elif key == ord('s'):
    i += 1
    cv2.imwrite('c_%03d.jpg' % i, img)

cap.release()
cv2.destroyAllWindows()