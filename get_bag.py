
import numpy as np  
import cv2  
import time
import wda

c = wda.Client()
s = c.session()

def get_corners(cont):
    x_min = cont[0][0][0]
    x_max = cont[0][0][0]
    y_min = cont[0][0][1]
    y_max = cont[0][0][1]
    for point in cont:
        if(point[0][0] < x_min):
            x_min = point[0][0]
        if(point[0][0] > x_max):
            x_max = point[0][0]
        if(point[0][1] < y_min):
            y_min = point[0][1]
        if(point[0][1] > y_max):
            y_max = point[0][1]
    return [(x_min, y_min), (x_max, y_max)]

def get_bag_loc(path):
    img = cv2.imread(path)  
    img = img[240:1220, :]
    imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) 
    ret,thresh = cv2.threshold(imgray,127,255,0) 
    image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # cv2.RETR_TREE
    new_cont = []
    num = 0
    hand_cards_x_min = img.shape[1]
    hand_cards_x_max = 0
    hand_pickup = -1
    for cont in contours:
        rec = get_corners(cont) # get rectagle
        if(rec[1][0] - rec[0][0] > 65 and rec[1][0] - rec[0][0] < 75 and rec[1][1] - rec[0][1] > 74 and rec[1][1] - rec[0][1] < 88 ):
            ret_x = int((rec[1][0] + rec[0][0])/2)
            ret_y = int((rec[1][1] + rec[0][1])/2) + 240
            return (ret_x, ret_y)
        
    return (0,0)

while True:
    c.screenshot('1.png')
    res = get_bag_loc('1.png')
    if(res[0] == 0):
        print('no bag!')
        continue
    print(res)
    s.tap(res[0], res[1])
    c.screenshot('2.png')
    for i in range(5):
        s.tap(375, 800) # touch to get bag
        time.sleep(0.02) # be crazy
    s.tap(40, 60) # return back
    time.sleep(0.3)