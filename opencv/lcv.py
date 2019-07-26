import cv2

cap = cv2.VideoCapture()
f, frame = cap.read()
cv2.imwrite("a.png", frame)
cap.release()
