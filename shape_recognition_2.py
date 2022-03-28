from tkinter import Image
from unicodedata import name
import cv2
from cv2 import drawChessboardCorners
from cv2 import circle
from cv2 import rectangle
import numpy as np
import math
def find_contours(img, color):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img_mask = cv2.inRange(img_hsv, color[0], color[1])
    contours, _ = cv2.findContours(img_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

img = cv2.imread('green_shapes.jpg')
drawing = img.copy()
color = (
             (56, 190, 90),
             (74, 255, 255)         
        )

contours = find_contours(img, color)

for cnt in contours:
    contours_area = cv2.contourArea(cnt)
    if contours_area > 100:
        print("Площадь контура:", contours_area)
        cv2.drawContours(drawing, [cnt], 0, (255, 255, 255), 2)
        
        (circle_x, circle_y), circle_radius = cv2.minEnclosingCircle(cnt)
        circle_area = math.pi * circle_radius**2
        print("Площадь круга:", circle_area)
        print()

        (bounding_x, bounding_y, bounding_w, bounding_h ) = cv2.boundingRect(cnt)
        bounding_pos1 = (bounding_x, bounding_y)
        bounding_pos2 = (bounding_x + bounding_w, bounding_y + bounding_h )
        print("Площадь прямоугольника:", bounding_h * bounding_w)
        
        rectangle = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rectangle)
        box = np.int0(box)
        rectangle_area = cv2.contourArea(box)
        print("Площадь прямоугольника 2-ого:", rectangle_area)
        #ширина и высота
        rect_w, rect_h = rectangle[1][0],rectangle[1][1]
        #делим длинную сторону на короткую стороно(соотношение)
        aspect_ratio = max(rect_w,rect_h / min(rect_w,rect_h))
        print()

        try: #попробуй
            triangle = cv2.minEnclosingTriangle(cnt)[1]
            triangle = np.int0(triangle)
            triangle_area = cv2.contourArea(triangle)
        except: #иначе выводи
            triangle_area = 0

        print("Площадь треугольника:", triangle_area)
        print()

        shapes_area = {
            # ключи 
            'circle': circle_area,
            'triangle': triangle_area,
            'rectangle' if aspect_ratio > 1.25 else 'square': rectangle_area

        }

        #словарь
        diffs = {
            #правило словаря 
            name: abs(contours_area - shapes_area[name]) for name in shapes_area 
        }
        #ключи и условия
        shape_name = min(diffs, key=diffs.get)
        if shape_name == 'circle':
            cv2.circle(drawing, (int(circle_x), int(circle_y)), int(circle_radius), (255, 255, 0), 2, cv2.LINE_AA)
        elif shape_name == 'triangle':
            cv2.drawContours(drawing, [triangle], 0, (100,255,255), 2, cv2.LINE_AA)
        else:
            cv2.drawContours(drawing, [box], 0, (0,150,255), 2, cv2.LINE_AA)
        print()


        moments = cv2.moments(cnt)
        try:
            x = int(moments['m10']/moments['m00'])
            y = int(moments['m01']/moments['m00'])
            cv2.circle(drawing,(x,y), 4,(0, 100, 255),-1,cv2.LINE_AA)
            
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(drawing, shape_name,(x-40, y + 30), font,1,(0,0,0), 4, cv2.LINE_AA)
            cv2.putText(drawing, shape_name,(x-41, y + 31), font,1,(255,255,255), 2, cv2.LINE_AA)
            
        except:
            #ничего не будем делать
            pass 




cv2.imshow("window", drawing)
cv2.waitKey(0)