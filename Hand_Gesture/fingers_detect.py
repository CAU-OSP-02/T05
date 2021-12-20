import cv2
import numpy as np
import math
from PIL import Image

#전역변수선언 
result = 0
score = 0
myanswer =None

#함수선언
def my_score():
    global score
    global result
    if result == myanswer:
        result = 0
        score += 100
        
def img1():
    global result
    result = 1

def img2():
    global result
    result = 2

def img3():
    global result
    result = 3

def img4():
    global result
    result = 4

def img5():
    global result
    result = 5

def img6():
    global result
    result = 6    

def img7():
    global result
    result = 7

def img8():
    global result
    result = 8

def img9():
    global result
    result = 9

def img10():
    global result
    result = 10


#capturing the video
cap = cv2.VideoCapture(0)
img1()
while(cap.isOpened()):
    try:             
        ret, hand = cap.read()
        hand=cv2.flip(hand,1)
        if ret == True:
            pass

        #making the img of dimension
        hand =hand[100:700,100:700]
    
        #using hsv we detect the color of skin
        hsv = cv2.cvtColor(hand, cv2.COLOR_BGR2HSV)
        lower_skin = np.array([0, 58, 30], dtype = "uint8")
        upper_skin = np.array([33, 255, 255], dtype = "uint8")
    
        #applying mask to extract skin color object from the img
        mask = cv2.inRange(hsv, lower_skin, upper_skin)

        #now we dilate our skin color object to remove black spots or noise from it
        kernel = np.ones((5,5),np.uint8)
        mask = cv2.dilate(mask,kernel,iterations = 3)
        blur = cv2.bilateralFilter(mask,9,200,200)
        res = cv2.bitwise_and(hand,hand, mask= blur)

        #convert to BGR -> GRAY 
        hand_gray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)

        #thresholding the image
        ret, thresh = cv2.threshold(hand_gray, 98, 255,cv2.THRESH_TRUNC)
    
        #finding contours in the threshold image
        contours,_ = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        #selecting the contour of max area 
        cnt = max(contours, key = lambda x: cv2.contourArea(x))
    
        hull = cv2.convexHull(cnt)
        hullarea = cv2.contourArea(hull)
        cntarea = cv2.contourArea(cnt)
        x,y,w,h = cv2.boundingRect(hull)
        hand = cv2.rectangle(hand,(x,y),(x+w,y+h),(0,255,0),2)

        ratio=(hullarea+cntarea)/(hullarea-cntarea)
        print("ratio:",ratio)
        img = cv2.drawContours(hand, hull, -2, (0,0,255), 10)

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(hand, 'score :' , (50,50), font, 2, (255,255,255), 4, cv2.LINE_AA)
        cv2.putText(hand, str(score), (300,50), font, 2, (255,255,255), 4, cv2.LINE_AA)
    
        if len(contours) > 0:
            hull = cv2.convexHull(cnt, returnPoints=False)
            defects = cv2.convexityDefects(cnt, hull)
            count_defects = 0
                        
            for i in range(defects.shape[0]):
                s,e,f,d = defects[i,0]
                start = tuple(cnt[s][0])
                end = tuple(cnt[e][0])
                far = tuple(cnt[f][0])
                cv2.circle(img,far,5,[0,0,255],-1)
                cv2.line(img,start,end,[255,0,0],2)
                a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
                b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
                c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
                #find the angles between the sides of triangle
                angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57.295
                if angle <= 90:
                    count_defects += 1
                    print("angle:",count_defects)

            # hand gestures and display the result            
            if count_defects == 0 :
                if 9<ratio<11: #Gesture 1
                    myanswer = 1
                    my_score()
                    img2()
                    
                elif 5<ratio<12: #Gesture 6
                    myanswer = 6
                    my_score()
                    img7()

                elif 12<ratio<15: #Gesture 0
                    myanswer = 10
                    my_score()

                elif 15 <ratio <30: #Gesture 9
                    myanswer = 9
                    my_score()
                    img10()

            elif count_defects == 1 :
                if 7<ratio<10: #Gesture 2
                    myanswer = 2
                    my_score()
                    img3()
                        
                elif 4<ratio <8 : #Gesture 7
                    myanswer = 7
                    my_score()
                    img8()

            elif count_defects == 2:
                if ratio<10: #Gesture 8
                    myanswer = 8
                    my_score()
                    img9()

                elif 6<ratio<11: #Gesture 3
                    myanswer = 3
                    my_score()
                    img4()

            elif count_defects == 3: #Gesture 4
                    myanswer = 4
                    my_score()
                    img5()

            elif count_defects == 4: #Gesture 5
                    myanswer = 5
                    my_score()
                    img6()
        
            cv2.imshow('hand',hand)

    except:
        pass

    k = cv2.waitKey(250) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()    
