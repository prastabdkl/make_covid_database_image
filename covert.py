import pydicom as dicom
import os
import cv2
import gdcm
# import PIL # optional
# make it True if you want in PNG format
PNG = False
# Specify the .dcm folder path
# folder_path = r"C:\Users\prast\Downloads\CS 7000\Final report\COVID-CT-MD\COVID_dcm\P001"
# Specify the output jpg/png folder path
jpg_folder_path = r"C:\Users\prast\Downloads\CS 7000\Final report\COVID-CT-MD\COVID"

image_count = 1
for i in range(1,169):
    folder_path = r'C:\Users\prast\Downloads\CS 7000\Final report\COVID-CT-MD\COVID_dcm\P'+f'{str(i).zfill(3)}' 
    
    images_path = os.listdir(folder_path)    
    path,dirs,files = next(os.walk(folder_path))
    file_count = len(files)

    for j in range(-5,5):
        middle_image_index = file_count // 2
        image = f"IM{str(middle_image_index + j).zfill(4)}.dcm"
        # image =f"IM{str(file_count//2).zfill(4)}.dcm"
        # print(image)
        ds = dicom.dcmread(os.path.join(folder_path, image))
        image = image.replace('.dcm', '.jpg')
    
        # image = f"Covid_{i}.jpg" + image
        image = f"Covid_{image_count}.jpg" 
    
        pixel_array_numpy = ds.pixel_array
        # print(pixel_array_numpy)
        cv2.imwrite(os.path.join(jpg_folder_path, image), pixel_array_numpy)
        image_count+=1
    # print(folder_path)  
    
print(image_count-1,' images converted')