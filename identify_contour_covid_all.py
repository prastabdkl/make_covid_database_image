import numpy as np
import cv2
import imutils
import os
from keras.preprocessing import image
import matplotlib.pyplot as plt


# jpg_folder_path = r"C:\Users\prast\Downloads\CS 7000\Final report\COVID-CT-MD\output"
# jpg_folder_path = r"C:\Users\prast\Downloads\CS 7000\Final report\COVID-CT-MD\output\Covid_74.jpg"
directory_path = r'C:\Users\prast\Downloads\CS 7000\Final report\COVID-CT-MD\COVID_dcm' 
result_folder = r"C:\Users\prast\Downloads\CS 7000\Final report\COVID-CT-MD\output\covid"

images_path = os.listdir(directory_path)    
path,dirs,files = next(os.walk(directory_path))
folder_count = len(dirs)

# folder_count = 3
image_count = 1
for i in range(1, folder_count+1):
    max_area = 0
    jpg_folder_path = r'C:\Users\prast\Downloads\CS 7000\Final report\COVID-CT-MD\COVID_dcm\P'+f'{str(i).zfill(3)}' 

    images_path = os.listdir(jpg_folder_path)    
    path,dirs,files = next(os.walk(jpg_folder_path))
    file_count = len(files)
    file_count = int(file_count/2)
    
    for j in range(1, file_count+1):
        img_path = r'C:\Users\prast\Downloads\CS 7000\Final report\COVID-CT-MD\COVID_dcm\P'+f'{str(i).zfill(3)}'+'\Covid_'+f'{str(j)}.jpg' 

        # img_path = r'C:\Users\prast\Downloads\CS 7000\Final report\COVID-CT-MD\output\Covid_'+f'{str(i)}.jpg' 
        img = image.load_img(img_path, grayscale=True, target_size=(512,512))
        img = image.img_to_array(img, dtype='uint8')
        org_img = cv2.imread(img_path)

        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(img, 240, 255, cv2.THRESH_BINARY)
        # thresh = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
        #cv2.bitwise_not(thresh, thresh)

        cnts = cv2.findContours(thresh, cv2.RETR_CCOMP,cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0]
        max_contour = max(cnts, key=cv2.contourArea)

        x,y,w,h = cv2.boundingRect(max_contour)

        # centx = np.sqrt( ((right[0] + left[0])**2)/4)
        # centy = np.sqrt( ((right[1] + left[1])**2)/4 )
        # print(centx, centy)

        # font = cv2.FONT_HERSHEY_SIMPLEX
        # cv2.circle(img, left, 5, (0, 0, 255), -1)
        # cv2.circle(img, right, 5, (0, 0, 255), -1)
        # cv2.circle(img, (int(centx), int(centy)), 5, (0, 0, 255), -1)
        # cv2.line(img, left, right, (255,0,0), 2)
        
        # draw bounding reactangle
        # cv2.rectangle(org_img,(x,y),(x+w,y+h),(0,255,0),2)
        # cv2.putText(img,'Distance: '+str(distance),(10,30), font, 1, (0,0,0),2, cv2.LINE_AA)

        total_area = 0
        for cnt in cnts:
            #cv2.drawContours(org_img, [cnt], -1, (0,255,255), 2)
            total_area += cv2.contourArea(cnt)
        
        if (total_area > max_area):
            max_area = total_area
            max_image_area = org_img
            
        #cv2.drawContours(org_img, [max_contour], -1, (0,0,255), 2)
        # print(total_area - cv2.contourArea(max_contour))
        # cv2.imshow('img', org_img)

    # cv2.imwrite(result_folder+'/Covid_'+f'{str(max_area)}.jpg', max_image_area)
    cv2.imwrite(result_folder+'/Covid_'+f'{str(image_count)}.jpg', max_image_area)
    image_count += 1
    print('images of folder',i, ' captured')

