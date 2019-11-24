import numpy as np
import cv2
import winsound

frequency = 2500  # Set Frequency To 2500 Hertz
duration = 1000   # Set Duration To 1000 ms == 1 second

scale = 1.1

x1, x2 = 250, 400
y1, y2 = 100, 250

mask = np.zeros((480, 640), np.uint8)
mask[y1:y2, x1:x2] = 255
text_control = "SU TAHLIYE TIKANIKLIK KONTROL"
text_result = "OK"
font = cv2.FONT_HERSHEY_COMPLEX

# threshold values for edge detection
lower = 45 
upper = 90 

cap = cv2.VideoCapture(1)

# capturing frames to adapt to ambience lighting.
for i in range(1, 6):
    ret, frame = cap.read()

grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
maskedGrayFrame = cv2.bitwise_and(grayFrame, grayFrame, mask=mask)

filtered = cv2.bilateralFilter(maskedGrayFrame, 7, 50, 50)
edges = cv2.Canny(filtered, threshold1=lower, threshold2=upper)

limit = edges.mean() * scale   # for comparison value

while True:
    ret, frame = cap.read()
    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    maskedGrayFrame = cv2.bitwise_and(grayFrame, grayFrame, mask=mask)

    filtered = cv2.bilateralFilter(maskedGrayFrame, 7, 50, 50)
    edges = cv2.Canny(filtered, threshold1=lower, threshold2=upper)

    value = edges.mean()

    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

    if value > limit:

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, text_result, (290, 300), font, 1.5, (0, 255, 0), 2)
        cv2.putText(frame, str(value)[:4], (290, 340), font, 1, (0, 255, 0), 2)

        winsound.Beep(frequency, duration)

    cv2.putText(frame, text_control, (50, 450), font, 1, (255, 0, 0), 2)
    cv2.putText(frame, str(limit)[:4], (5, 30), font, 1, (0, 0, 255), 2)

    cv2.imshow("control", frame)

    k = cv2.waitKey(30) & 0xFF
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()
