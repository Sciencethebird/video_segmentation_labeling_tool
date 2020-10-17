import numpy as np
import cv2
import os
import threading
import time

cwd = os.getcwd()
#cwd = cwd+'/Desktop/OpenCV_Video_Processing'#+'/test.mp4'
print(cwd)

frame_idx = 0

mouse_x = 0
mouse_y = 0

points_pos = [] #temp points of building segments
segs = [] #stored points of completed segments
mouse_click = False
down = False

folder = 'labals'

print(cv2.WINDOW_AUTOSIZE)
print(cwd+'\\53_12.mp4')
cap = cv2.VideoCapture(cwd+'\\53_12.mp4')

frame_moved = False

def nothing(x):
    global frame_idx, down, cap, frame_moved
    #cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
    if(abs(x - frame_idx) >2):
        frame_moved = True
    frame_idx = x
def save_frame(frame):
    global points_pos, segs
    if len(segs) != 0:
           temp = np.array(frame)
           for segment in segs:
               for idx, coord in enumerate(segment):
                   cv2.line(temp,segment[idx-1],coord,(255,0,0),2)
               for idx, coord in enumerate(segment):
                   cv2.circle(temp,coord,3,(0,0,255),-1)   
           filename = 	"{:0>5d}".format(frame_idx)
           cv2.imwrite('labels\\'+filename+'.jpg',temp)
           print("image Saved", cwd)
    points_pos.clear()
    segs.clear()

def mouse(event,x,y,flags,param):
    global mouse_click, mouse_x, mouse_y, points_pos, segs, red_dot
    mouse_x = x
    mouse_y = y
    if event == cv2.EVENT_LBUTTONDOWN: #storing points
        mouse_click = True
        print('left')
        points_pos.append((x, y))
        if len(points_pos) > 1:
            for idx,xy in enumerate(points_pos[:-1]):
                #print("xxxxyyy",abs(x-xy[0]),abs(y-xy[1]))
                if abs(x-xy[0])<5 and abs(y-xy[1])<5 :
                    points_pos.remove(xy)
                    del points_pos[-1]
        
    elif event == cv2.EVENT_LBUTTONUP:
        mouse_click = False
    elif event == cv2.EVENT_RBUTTONDOWN:
        segs.append(points_pos.copy())
        points_pos.clear()
        #red_dot = not red_dot #showing red dot or not
        
    else:
        pass

frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
cv2.namedWindow('frame',0)
#cv2.namedWindow('lol',0)
cv2.resizeWindow('frame',1920, 1080)
cv2.createTrackbar('B','frame',0,frame_count, nothing)
def trackbar():
    global frame_idx
    #print(frame_idx)
    while True:
        print(frame_idx)
        cv2.setTrackbarPos('B', 'frame',frame_idx)
t = threading.Thread(target = trackbar)
t.start()
speed = 1
while(cap.isOpened()):
    frame_idx+=1
    if frame_idx %speed == 0:
        if frame_moved:
            print('adsasddsa')
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            frame_moved = False
        ret, frame = cap.read()

        cv2.putText(frame, "Speed x {}".format(speed), (50, 50),
		cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 4)	

        cv2.setMouseCallback('frame',mouse)
        key = cv2.waitKey(20)
        if key & 0xFF == ord('q'):
            speed-=1
            if speed <1:
                speed = 1
        if key & 0xFF == ord('e'):
            speed+=1
        if key & 0xFF == ord('x'):
            frame_idx+=100
        if key & 0xFF == ord(' '):
            points_pos = []
            curr_idx = frame_idx
            while True:
                if curr_idx != frame_idx:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
                    ret, frame = cap.read()
                    temp = np.array(frame)
                    points_pos.clear()
                    segs.clear()
                    curr_idx = frame_idx
                temp = np.array(frame) #if you assign directly it will refernce to the original frame    
                cv2.circle(temp,(mouse_x,mouse_y),4,(0,0,255),-1)
                if len(points_pos) != 0:
                    cv2.line(temp,points_pos[-1],(mouse_x,mouse_y),(255,0,0),2)
                for idx, coord in enumerate(points_pos):
                   if idx >0:
                        cv2.line(temp,points_pos[idx-1],coord,(255,0,0),2)
                for idx, coord in enumerate(points_pos):
                   cv2.circle(temp,coord,3,(0,0,255),-1) 
                for segment in segs:
                    for idx, coord in enumerate(segment):
                        cv2.line(temp,segment[idx-1],coord,(255,0,0),2)
                    for idx, coord in enumerate(segment):
                        cv2.circle(temp,coord,3,(0,0,255),-1)    
                        
                #print(mouse_y, mouse_y)
                cv2.imshow('frame', temp)
                #print(points_pos)
                key2 = cv2.waitKey(1) or 0xff
                if key2 == ord('a'):
                    save_frame(frame)
                    frame_idx -=1
                    cv2.setTrackbarPos('B', 'frame',frame_idx)  
                    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
                    ret, frame = cap.read()
                    cv2.imshow('frame', frame)
                if key2 == ord('d'):
                    save_frame(frame)
                    frame_idx +=1
                    cv2.setTrackbarPos('B', 'frame',frame_idx)           
                if key2 == ord(' '):
                    save_frame(frame)
                    break
    
        if key & 0xFF == ord('z'):
            break  
        
        cv2.imshow('frame',frame)

cap.release()
cv2.destroyAllWindows()
