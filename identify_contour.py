import numpy as np
import cv2
import imutils
import os
# from keras.preprocessing import image
import matplotlib.pyplot as plt
import glob


from cv_utils import draw_contours, get_thresh, get_contours, mask_image, get_boundary, invert, write, load_img

# jpg_folder_path = r"/Users/ahnupsingh/avail/make_covid_database_image/output/covid/"
# result_folder = r"/Users/ahnupsingh/avail/make_covid_database_image/output/final"

jpg_folder_path = r"C:\Users\prast\Downloads\CS 7000\Final report\COVID-CT-MD\output\covid"
result_folder = r'C:\Users\prast\Downloads\CS 7000\Final report\COVID-CT-MD\output_counter\covid' 


covid_images_directory = r'C:\Users\prast\Downloads\CS 7000\Final report\COVID-CT-MD\images\COVID_dcm' 
covid_selected_images_directory = r"C:\Users\prast\Downloads\CS 7000\Final report\COVID-CT-MD\output\covid"

covid_max_images = r"C:\Users\prast\Downloads\CS 7000\Final report\COVID-CT-MD\output\selected_images\covid"
covid_masked_images = r"C:\Users\prast\Downloads\CS 7000\Final report\COVID-CT-MD\output\masked_images\covid"

normal_images_directory = r'C:\Users\prast\Downloads\CS 7000\Final report\COVID-CT-MD\images\Normal_dcm' 
normal_selected_images_directory = r"C:\Users\prast\Downloads\CS 7000\Final report\COVID-CT-MD\output\normal"

normal_max_images = r"C:\Users\prast\Downloads\CS 7000\Final report\COVID-CT-MD\output\selected_images\normal"
normal_masked_images = r"C:\Users\prast\Downloads\CS 7000\Final report\COVID-CT-MD\output\masked_images\normal"

# images_path = os.listdir(result_folder)    
# path,dirs,files = next(os.walk(result_folder))
# # file_count = len(files)

# # files = glob.glob(result_folder)
# os.remove(path)
# # os.mkdir(result_folder)
# # for f in files:
# #     os.remove(f)
# exit()
def create_masked_image(max_image,final_boundary,destination,filename):
    masked = mask_image(max_image, final_boundary)
    inverted = invert(masked)
    write(destination + filename, inverted)
    
def identify_max_image(source,destination,folder_name,max_images_dest,masked_images_dest):

    images_path = os.listdir(source)    
    path,dirs,files = next(os.walk(source))
    file_count = int(len(files)/2)
    
    max_area = 0
    max_image = 0
    image_position = 0
    final_boundary = None

    # file_count = 50
    destination_folder = destination+'\\'+folder
    if not os.path.isdir(destination_folder):
        os.mkdir(destination_folder)
        
    for i in range(1, file_count+1):
        img_path = f'{source}\Covid_{str(i)}.jpg' 
        org_img = load_img(img_path)

        ret, thresh = get_thresh(org_img)
        cnts, hierarchy = get_contours(thresh)
        boundary = get_boundary(thresh)

        output_img, total_area = draw_contours(org_img, cnts, hierarchy[0])
        
        # masked = mask_image(output_img, boundary)
        # inverted = invert(masked)
        
        if (total_area > max_area):
            max_area = total_area
            max_image = output_img
            image_position = i
            final_boundary = boundary
            
        write(destination_folder + f'/Covid_{folder_name}_{str(i)}_{total_area}.jpg', output_img)
        # write(destination + f'/Covid_{str(i)}_{total_area}_masked.jpg', masked)
        # write(destination + f'/Covid_{str(i)}_{total_area}_inverted.jpg', inverted)
        # print(f"...{i}")


    # masked = mask_image(max_image, final_boundary)
    # inverted = invert(masked)
    write(max_images_dest + f'/max_covid_{folder_name}_{str(image_position)}_{max_area}.jpg', max_image)
    print('done writing max',folder_name)
    
    # max_images_dest = destination+'\\'+'masked_image'
    # if not os.path.isdir(max_images_dest):
    #     os.mkdir(max_images_dest)
    create_masked_image(max_image,final_boundary,masked_images_dest,f'/Covid_{folder_name}_{str(image_position)}.jpg')
    print('done creating mask',folder_name)

# print(covid_images_directory)
path,dirs,files = next(os.walk(covid_images_directory))
# print(covid_images_directory+'\\'+'P001')
# dirs = ['P001']
for folder in dirs:
    identify_max_image(covid_images_directory+'\\'+folder,covid_selected_images_directory,folder,covid_max_images,covid_masked_images)
        
# identify_max_image(covid_images_directory,covid_selected_images_directory)
# identify_max_and_mask(normal_images_directory,normal_selected_images_directory)

