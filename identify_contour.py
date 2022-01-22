import numpy as np
import cv2
import imutils
import os
# from keras.preprocessing import image
import matplotlib.pyplot as plt
import glob


from cv_utils import draw_contours, get_thresh, get_contours, mask_image, get_boundary, invert, write, load_img

SEPARATOR_ = "\\"

base_path = r"C:\Users\prast\Downloads\CS 7000\Final report\COVID-CT-MD"
# base_path = "/Users/ahnupsingh/avail/make_covid_database_image"

covid_images_directory = r"C:\Users\prast\Downloads\CS 7000\Final report\COVID-CT-MD\images\COVID_dcm"
# covid_images_directory = base_path + SEPARATOR_ +  "images" + SEPARATOR_ +  "COVID_dcm"
# covid_selected_images_directory = r"C:\Users\prast\Downloads\CS 7000\Final report\COVID-CT-MD\output\covid"
# covid_max_images = r"C:\Users\prast\Downloads\CS 7000\Final report\COVID-CT-MD\output\selected_images\covid"
# covid_masked_images = r"C:\Users\prast\Downloads\CS 7000\Final report\COVID-CT-MD\output\masked_images\covid"

normal_images_directory = r"C:\Users\prast\Downloads\CS 7000\Final report\COVID-CT-MD\images\Normal_dcm"
# normal_images_directory = base_path + SEPARATOR_ +  "images" + SEPARATOR_ +  "Normal_dcm"
# normal_selected_images_directory = r"C:\Users\prast\Downloads\CS 7000\Final report\COVID-CT-MD\output\normal"
# normal_max_images = r"C:\Users\prast\Downloads\CS 7000\Final report\COVID-CT-MD\output\selected_images\normal"
# normal_masked_images = r"C:\Users\prast\Downloads\CS 7000\Final report\COVID-CT-MD\output\masked_images\normal"

destination = base_path + SEPARATOR_ +  "output"

def remove_files(path):
    files = glob.glob(path)
    for f in files:
        os.remove(f)

def create_masked_image(max_image,final_boundary,destination,filename):
    masked = mask_image(max_image, final_boundary)
    inverted = invert(masked)
    write(destination + filename, inverted)


def create_folders(destination, key, separator=SEPARATOR_):
    key_destination = destination + separator + key
    if not os.path.isdir(key_destination):
        os.mkdir(key_destination)

    selected_images = destination + separator + "selected_images"
    if not os.path.isdir(selected_images):
        os.mkdir(selected_images)

    masked_images = destination + separator + "masked_images"
    print("masked destination" + masked_images)
    if not os.path.isdir(masked_images):
        os.mkdir(masked_images)
        print("masked destination" + masked_images)

    max_image_destination = destination + separator + "selected_images" + separator + key
    if not os.path.isdir(max_image_destination):
        os.mkdir(max_image_destination)

    masked_image_destination = destination + separator + "masked_images" + separator + key
    if not os.path.isdir(masked_image_destination):
        os.mkdir(masked_image_destination)

    return key_destination, max_image_destination, masked_image_destination

    
def identify_max_image(source, destination, folder_name, key=""):
    path,dirs,files = next(os.walk(source))
    file_count = int(len(files)/2)
    
    max_area = 0
    max_image = 0
    image_position = 0
    final_boundary = None

    key_destination, max_image_destination, masked_image_destination = create_folders(destination, key)
    destination_folder = key_destination + SEPARATOR_ + folder_name
    if not os.path.isdir(destination_folder):
        os.mkdir(destination_folder)
        
    for i in range(1, file_count+1):
        img_path = f'{source}' + SEPARATOR_ + f'{key}_{str(i)}.jpg' 
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
            
        write(destination_folder + f'/{key}_{folder_name}_{str(i)}_{total_area}.jpg', output_img)
        # write(destination + f'/{key}_{str(i)}_{total_area}_masked.jpg', masked)
        # write(destination + f'/{key}_{str(i)}_{total_area}_inverted.jpg', inverted)
        # print(f"...{i}")

    print('Destination folder ', destination_folder)

    write(max_image_destination + f'/max_{key}_{folder_name}_{str(image_position)}_{max_area}.jpg', max_image)
    print('done writing max at ', max_image_destination + f'/max_{key}_{folder_name}_{str(image_position)}_{max_area}.jpg')
    
    create_masked_image(max_image, final_boundary, masked_image_destination, f'/{key}_{folder_name}_{str(image_position)}.jpg')
    print('done creating mask at ', masked_image_destination + f'/{key}_{folder_name}_{str(image_position)}.jpg')


path,dirs,files = next(os.walk(covid_images_directory))
# dirs = ['P001']
for folder in dirs:
    source = covid_images_directory + SEPARATOR_ + folder
    identify_max_image(source, destination, folder, key="Covid")
        

path,dirs,files = next(os.walk(covid_images_directory))
# dirs = ['P001']
for folder in dirs:
    source = normal_images_directory + SEPARATOR_ + folder
    identify_max_image(source, destination, folder, key="Normal")
