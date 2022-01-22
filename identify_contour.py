import numpy as np
import cv2
import imutils
import os
# from keras.preprocessing import image
import matplotlib.pyplot as plt

from cv_utils import draw_contours, get_thresh, get_contours, mask_image, get_boundary, invert, write, load_img

jpg_folder_path = r"/Users/ahnupsingh/avail/make_covid_database_image/output/covid/"
result_folder = r"/Users/ahnupsingh/avail/make_covid_database_image/output/final"

# jpg_folder_path = r"C:\Users\prast\Downloads\CS 7000\Final report\COVID-CT-MD\output\Covid_74.jpg"
# folder_path = r'C:\Users\prast\Downloads\CS 7000\Final report\COVID-CT-MD\COVID_dcm\P'+f'{str(i).zfill(3)}' 

images_path = os.listdir(jpg_folder_path)    
path,dirs,files = next(os.walk(jpg_folder_path))
file_count = len(files)

infected_area = 0
infected_image = 0
image_position = 0
boundary = None

# file_count = 2
for i in range(1, file_count):
    img_path = f'{jpg_folder_path}Covid_{str(i)}.jpg' 
    org_img = load_img(img_path)

    ret, thresh = get_thresh(org_img)
    cnts, hierarchy = get_contours(thresh)
    boundary = get_boundary(thresh)

    output_img, total_area = draw_contours(org_img, cnts, hierarchy[0])
    masked = mask_image(output_img, boundary)
    inverted = invert(masked)
    
    cnts = cnts[0]
    
    if (total_area > infected_area):
        infected_area = total_area
        infected_image = output_img
        image_position = i
        boundary = boundary
        
    # write(result_folder + f'/Covid_{str(i)}_{total_area}.jpg', output_img)
    # write(result_folder + f'/Covid_{str(i)}_{total_area}_masked.jpg', masked)
    # write(result_folder + f'/Covid_{str(i)}_{total_area}_inverted.jpg', inverted)
    print(f"...{i}")


write(result_folder + f'/final_{str(image_position)}_{infected_area}.jpg', infected_image)
