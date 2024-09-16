import cv2
import time

from emailing import send_email

# 0 for intergrated camera
video = cv2.VideoCapture(0)
# wait 1 second for camera to load
time.sleep(1)

first_frame = None
status_list =[]
while True:
    status = 0
    check, frame = video.read()
    gray_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame,(21,21), 0)


    if first_frame is None:
        first_frame = gray_frame_gau


    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)


    thresh_frame = cv2.threshold(delta_frame,60,255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations = 2)
    cv2.imshow('my video', dil_frame)

    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour)<5000:
            continue
        x, y, w, h =cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 3)
        if rectangle.any():
            status = 1


    status_list.append(status)
    status_lists = status_list[-2:]

    # if enters and exit essentiall, enter will have status 1 if exit status will be 0. This point is when we send the email
    if status_lists[0]==1 and stauts_list[1] == 0:
        send_email()

    cv2.imshow('Video', frame)

    # creates keyboard object
    key = cv2.waitKey(1) # has to be in a while loop
    # if we press the q key here wee clsoe the video
    if key == ord('q'):
        break

video.release()