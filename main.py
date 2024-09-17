import cv2
import time
import glob
from emailing import send_email
import os
from threading import Thread

# 0 for intergrated camera
video = cv2.VideoCapture(0)
# wait 1 second for camera to load
time.sleep(1)

first_frame = None
status_list =[]

count = 1

def clean_folder():
    print('Clean folder function started')
    images = glob.glob('images/*.png')
    for image in images:
        os.remove(image)
    print('Clean folder function ended')

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
            cv2.imwrite(f'images/{count}.png', frame)
            count = count + 1
            all_images = glob.glob('images/*.png')
            index =int(len(all_images)/2)
            images_with_object = all_images[index]


    status_list.append(status)
    status_lists = status_list[-2:]

    # if enters and exit essentiall, enter will have status 1 if exit status will be 0. This point is when we send the email
    if status_lists[0]==1 and status_list[1] == 0:
        # we let the email function to run in the background as otherwise frame freezes
        email_thread = Thread(target=send_email, args = (images_with_object, ))# add a coma to make it turple, otherwise error pops up as think its one string
        email_thread.daemon = True
        # we thread also for the clean_folder
        clean_thread = Thread(target=clean_folder)
        clean_thread.daemon = True
        # then we execute the function through thread
        email_thread.start()



    cv2.imshow('Video', frame)

    # creates keyboard object
    key = cv2.waitKey(1) # has to be in a while loop
    # if we press the q key here wee clsoe the video
    if key == ord('q'):
        break

clean_thread.start()
video.release()

 # only want to delete images once the user quit the programe
# as otherwise this may delete the file that wants to be emailed