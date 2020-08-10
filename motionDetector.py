import cv2 as cv, time, pandas
from datetime import datetime

video = cv.VideoCapture(0)
firstFrame = None
statusList = [None, None]
times = []
df = pandas.DataFrame(columns = ["Start", "End"])

while true:
    check, frame =  video.read()

    status = 0

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray, (21, 21), 0)

    if firstFrame is None:
        firstFrame = gray
        continue
    
    deltaFrame = cv.absdiff(firstFrame, gray)
    threshFrame = cv.threshold(deltaFrame, 30, 255, cv.THRESH_BINARY)[1]
    threshFrame = cv.dilate(threshFrame, None, iterations = 2)
    

    (cnts, _ ) = cv.findContours(threshFrame.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv.contourArea(countour) < 10000:
            pass
        (x, y, w, h) = cv.boundingRect(contour)
        cv.rectangle(frame, (x, y), (x + w, y + h), (255,255,255), 3)
        
        status = 1
        statusList.append(status)
        
        if statusList[-1] == 1 and statusList[-2] == 0:
            times.append(datetime.now())
        if statusList[-1] == 0 and statusList[-2] == 1:
            times.append(datetime.now())

    cv.imshow("Gray Frame", gray)
    cv.imshow("Delta Frame", deltaFrame)
    cv.imshow("Threshold Frame", threshFrame)
    cv.imshow("Countour Frame", frame)

    key = cv.waitKey(1)

    if key == ord('q'):
        if status == 1:
            times.append(datetime.now())
        break

for i in range(0, len(times), 2):
    df = df.append({"Start": times[i], "End": times[i + 1]}, ignore_index = True)

df.to_csv("Times.csv")

video.release()
cv.destroyAllWindows()
    

