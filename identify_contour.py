import numpy as np
import cv2
import imutils
import os
# from keras.preprocessing import image
import matplotlib.pyplot as plt

from cv_utils import draw_contours, get_thresh, get_contours, mask_image, get_boundary

max_area = 0

jpg_folder_path = r"/Users/ahnupsingh/avail/make_covid_database_image/output/covid/"
# jpg_folder_path = r"C:\Users\prast\Downloads\CS 7000\Final report\COVID-CT-MD\output\Covid_74.jpg"
# folder_path = r'C:\Users\prast\Downloads\CS 7000\Final report\COVID-CT-MD\COVID_dcm\P'+f'{str(i).zfill(3)}' 

result_folder = r"/Users/ahnupsingh/avail/make_covid_database_image/output/result"

images_path = os.listdir(jpg_folder_path)    
path,dirs,files = next(os.walk(jpg_folder_path))
file_count = len(files)

max_image_area = 0
# file_count = 2
for i in range(1, file_count):
    img_path = f'{jpg_folder_path}Covid_{str(i)}.jpg' 

    # img = image.load_img(img_path, grayscale=True, target_size=(512,512))
    # img = image.img_to_array(img, dtype='uint8')
    org_img = cv2.imread(img_path)
    ret, thresh = get_thresh(org_img)
    cnts, hierarchy = get_contours(thresh)
    boundary = get_boundary(thresh)

    org_img, total_area = draw_contours(org_img, cnts, hierarchy[0])
    masked = mask_image(org_img, boundary)
    
    cnts = cnts[0]

    # font = cv2.FONT_HERSHEY_SIMPLEX
    # cv2.circle(img, left, 5, (0, 0, 255), -1)
    # cv2.circle(img, right, 5, (0, 0, 255), -1)
    # cv2.circle(img, (int(centx), int(centy)), 5, (0, 0, 255), -1)
    # cv2.line(img, left, right, (255,0,0), 2)
    

    # cv2.putText(img,'Distance: '+str(distance),(10,30), font, 1, (0,0,0),2, cv2.LINE_AA)

    total_area = 0
    # cnt_with_max_area = cnts[0]
    
    # for cnt in cnts:
    #     # print("Contour ::: ", cnt)
    #     # cv2.drawContours(org_img, [cnt], 0, (0,255,255), 2)
    #     total_area += cv2.contourArea(cnt)
        
    #     # if cv2.contourArea(cnt) > cv2.contourArea(cnt_with_max_area):
    #     #     cnt_with_max_area = cnt
    
    # print(cnt_with_max_area)
    # index = cnts.index(cnt_with_max_area)
    # print(index)

    # # Show the output image
    # cv2.imshow('Output', out)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # break;    
    # cv2.drawContours(org_img, [cnt], -1, (0,255,255), 2)
        
    
    if (total_area > max_area):
        max_area = total_area
        max_image_area = org_img
        
    #cv2.drawContours(org_img, [max_contour], -1, (0,0,255), 2)
    # print(total_area - cv2.contourArea(max_contour))
    # cv2.imshow('img', org_img)

    cv2.imwrite(result_folder+'/Covid_'+f'{str(i)}.jpg', org_img)
    cv2.imwrite(result_folder+'/masked_'+f'{str(i)}.jpg', masked)
