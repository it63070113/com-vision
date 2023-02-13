import cv2
import mediapipe as mp
import time
from tkinter import *

# It's creating a GUI for user to input the time to work and time to rest.
root = Tk()
root.title("Rest Detection")
root.geometry("300x200")
header = Label(root, text="3 sa-hai-pa-gun-nonn", font=("Courier", 15)).pack()
L1 = Label(root, text="Time to WORK (mins)", font=("Courier", 10)).pack()
txt1 = StringVar()
E1 = Entry(root,textvariable=txt1, bd = 3).pack()
L2 = Label(root, text="Time to REST (mins)", font=("Courier", 10)).pack()
txt2 = StringVar()
E2 = Entry(root,textvariable=txt2, bd = 3).pack()

def detect(input_alltime, input_rest):
    '''main function'''
    #cap = cv2.VideoCapture('video.mp4')
    cap = cv2.VideoCapture(1)
    # cap.set(3, 1280)
    # cap.set(4, 720)
    mpFaceDetection = mp.solutions.face_detection
    faceDetection = mpFaceDetection.FaceDetection(0.75)

    check_con = 0
    online_firsttime = 0
    online_lasttime = 0
    rest_time = []

    start_time = time.time()
    all_time = input_alltime

    # log check
    detected = '0'
    value_before = 0
    interrupt = False

    print('Program started!')
    while (1):

        # Calculating the time that has passed since the program started.
        current_time = time.time()
        elapsed_time = current_time - start_time

        # detect varible
        # Reading the video from the camera and converting it to RGB.
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = faceDetection.process(imgRGB)
        width = img.shape[1]
        height = img.shape[0]

        if elapsed_time > all_time:
            # print('You need a rest!!!!')
            cv2.putText(img, f"You need a rest!!!!", (5, 100),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255), 3)
            # break

        if results.detections:
            for id, detection in enumerate(results.detections):
                bounding_box = detection.location_data.relative_bounding_box
                landmark = detection.location_data.relative_keypoints
                if id == 0:
                    x = int(bounding_box.xmin * width)
                    w = int(bounding_box.width * width)
                    y = int(bounding_box.ymin * height)
                    h = int(bounding_box.height * height)

                    # face = x, w, y, h
                    # right_ear = (
                    #     int(landmark[4].x * width), int(landmark[4].y * height))
                    # left_ear = (int(landmark[5].x * width),
                    #           int(landmark[5].y * height))

                    right_ear_x = int(landmark[4].x * width)
                    left_ear_x = int(landmark[5].x * width)

                    cv2.rectangle(img, (x, y), (x+w+10, y+h+10),
                                  color=(255, 255, 255), thickness=2)
                    # cv2.circle(img , right_ear, 5, (0,0,255), -1)
                    # cv2.circle(img , left_ear, 5, (0,0,255), -1)
                    cv2.putText(img, f'{int(detection.score[0] * 100)}%',
                                (x, y-20), cv2.FONT_HERSHEY_PLAIN,
                                2, (255, 0, 255), 2)
                    distance = abs(right_ear_x - left_ear_x)
                    if distance < 110:
                        status_face = False
                        if detected == '1':  # ไม่อยาก terminal มันซ้ำเฉยๆ
                            # print("Not found your eyes")
                            detected = '0'
                    else:
                        status_face = True
                        check_con += 1
                        if detected == '0':  # ไม่อยากให้ terminal มันซ้ำเฉยๆ
                            rest_time.append(online_lasttime)
                            # print("Detected!")
                            detected = '1'

        else:
            status_face = False
            if detected == '1':  # ไม่อยาก terminal มันซ้ำเฉยๆ
                # print("Not found your face")
                detected = '0'
                result = sum(rest_time)  + online_lasttime

        if status_face:
            online_firsttime = time.time()

        if status_face == False and check_con > 0:
            online_lasttime = int(current_time - online_firsttime)
            
            if value_before != online_lasttime:  # ไม่อยาก terminal มันซ้ำเฉยๆ
                value_before = online_lasttime
                print(online_lasttime)
            if online_lasttime == input_rest and check_con >= 1:
                # print("You are rest ! ")
                # log check
                detected = '0'
                result = sum(rest_time) + online_lasttime
                interrupt = True
                break

        cv2.putText(img, f"Your working times: {int(elapsed_time / 60)} mins", (
            5, 40), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 255, 0), 2)

        # cv2.imshow("Face Detection", img)
        if elapsed_time < 900 or elapsed_time > input_alltime - 600:
            cv2.imshow("Rest Detection", img)

        else:
            cv2.destroyAllWindows()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("---------------------\nInterrupt by user!!!\n---------------------")
            result = sum(rest_time) + online_lasttime
            interrupt = False
            break
    cap.release()
    cv2.destroyAllWindows()
    if interrupt:
        reset(result, input_alltime, input_rest)


def reset(result, input_alltime, input_rest):
    '''Show result when finish program'''
    print("------------------------------------\nAll your rest times : " +
          str(int(result)) + " sec\n------------------------------------")
    detect(input_alltime, input_rest)


def showMessage():
    input_alltime = int(txt1.get()) * 60
    input_rest = int(txt2.get()) * 60
    # print("value1 = " + input_alltime + "\nvalue2 = " + input_rest)
    root.destroy()
    print('--------------------------------------------------------\nProgram will start when the camera opens. Plese wait...\
    \n--------------------------------------------------------')
    detect(input_alltime, input_rest)

btn1 = Button(root, text="ยืนยัน", bg="green", fg="white", command=showMessage).pack()


root.mainloop()