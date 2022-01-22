import numpy as np
import cv2
import imutils
import os
from keras.preprocessing import image
import matplotlib.pyplot as plt

max_area = 0

jpg_folder_path = r"C:\Users\prast\Downloads\CS 7000\Final report\COVID-CT-MD\output\covid"
# jpg_folder_path = r"C:\Users\prast\Downloads\CS 7000\Final report\COVID-CT-MD\output\Covid_74.jpg"
# folder_path = r'C:\Users\prast\Downloads\CS 7000\Final report\COVID-CT-MD\COVID_dcm\P'+f'{str(i).zfill(3)}' 

result_folder = r"C:\Users\prast\Downloads\CS 7000\Final report\COVID-CT-MD\output_counter"

images_path = os.listdir(jpg_folder_path)    
path,dirs,files = next(os.walk(jpg_folder_path))
file_count = len(files)

max_image_area = 0
file_count = 2
for i in range(1, file_count):
# for i in range(1, 10):
    img_path = r'C:\Users\prast\Downloads\CS 7000\Final report\COVID-CT-MD\output\covid\Covid_'+f'{str(i)}.jpg' 
    img = image.load_img(img_path, grayscale=True, target_size=(512,512))
    img = image.img_to_array(img, dtype='uint8')
    org_img = cv2.imread(img_path)

    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(img, 240, 255, cv2.THRESH_BINARY)
    # thresh = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    #cv2.bitwise_not(thresh, thresh)

    cnts = cv2.findContours(thresh, cv2.RETR_TREE,
                    cv2.CHAIN_APPROX_SIMPLE)
    
    contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    hierarchy = hierarchy[0] # get the actual inner list of hierarchy descriptions
    
    # cv2.drawContours(org_img, hierarchy, -1, (0,255,255), 2)
    print(type(contours))
    print(type(hierarchy))    
    break;
    # for cnt in cnts:
    #     for i in cnt:
    #         for j in i:                
    #             print(j)
    
    # cnts = cnts[0]
    # for cnt in cnts:
    #     print("Countours", cnt[3])
    
    max_contour = max(cnts, key=cv2.contourArea)
    # print("Countours", cnts)

    # left = tuple(c[c[:, :, 0].argmin()][0])
    # right = tuple(c[c[:, :, 0].argmax()][0])

    # distance = np.sqrt( (right[0] - left[0])**2 + (right[1] - left[1])**2 )

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
    # cnt_with_max_area = cnts[0]
    
    for cnt in cnts:
        # cv2.drawContours(org_img, [cnt], -1, (0,255,255), 2)
        total_area += cv2.contourArea(cnt)
        
        # if cv2.contourArea(cnt) > cv2.contourArea(cnt_with_max_area):
        #     cnt_with_max_area = cnt
    
    # print(cnt_with_max_area)
    # index = cnts.index(cnt_with_max_area)
    # print(index)
    # mask = np.zeros_like(img) # Create mask where white is what we want, black otherwise
    # cv2.drawContours(mask, cnts, idx, 255, -1) # Draw filled contour in mask
    # out = np.zeros_like(img) # Extract out the object and place into output image
    # out[mask == 255] = img[mask == 255]

    # # Now crop
    # (y, x) = np.where(mask == 255)
    # (topy, topx) = (np.min(y), np.min(x))
    # (bottomy, bottomx) = (np.max(y), np.max(x))
    # out = out[topy:bottomy+1, topx:bottomx+1]

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

cv2.imwrite(result_folder+'/Covid_'+f'{str(max_area)}.jpg', max_image_area)