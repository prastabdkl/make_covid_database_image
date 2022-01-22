import cv2
import random
import numpy as np

result_folder = r"/Users/ahnupsingh/avail/make_covid_database_image/output/result"
map = {}

def get_thresh(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
    # thresh = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    #cv2.bitwise_not(thresh, thresh)
    cv2.imwrite(result_folder+'/Covid_.jpg', gray)

    return ret, thresh

def get_boundary(thresh):
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours[0]

def get_contours(thresh):
    hierarchy = [[]]
    # contours = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # inner_contours = get_inner_contours(contours, hierarchy)

    return contours, hierarchy
    
    #  # get the actual inner list of hierarchy descriptions
    
    # cv2.drawContours(org_img, hierarchy, -1, (0,255,255), 2)
    # print(type(contours))
    # print(type(hierarchy))   


def get_inner_contours(contours, hierarchy):
    print("Hierarchy: ")
    hierarchy = hierarchy[0]

    inner_contours = []

    for h in hierarchy:
        if h[3] == 0:
            print(h)
            print("contour", contours[h[0]])
            inner_contours.append(contours[h[0]])

    return inner_contours


def draw_contours(img, contours, hierarchy):
    j = 1
    total_area = 0
    if hierarchy.any():
        for i in range(0, len(contours)):
            if hierarchy[i][3] != -1 and hierarchy[i][2] != -1:

                parent_contour = hierarchy[hierarchy[i][3]]
                # print("parent", parent_contour)
                # if parent_contour has no parent
                if not has_parent(parent_contour):
                    color, name = get_random_color()
                    cv2.drawContours(img, contours, i, color, 2)
                    total_area += cv2.contourArea(contours[0])
                    map[name] = (contours, i)

                    # img = add_label(img, str(i) + " " + str(hierarchy[i]), (10,30 + j * 30), color)
                    j = j + 1

    # contours, i = map[list(map.keys())[1]]
    return img, total_area


def get_random_color():
    value1 = int(random.random() * 1000 % 255)
    value2 = int(random.random() * 1000 % 255)
    value3 = int(random.random() * 1000 % 255)
    return (value1, value2, value3), str(value1+value2+value3)


def add_label(img, label, position, color=get_random_color()):
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, label, position, font, 1, color,2, cv2.LINE_4)
    return img

def has_parent(hierarchy):
    return hierarchy[3] != -1


def draw_bounding_rect(img, contours):
    c = max(contours, key=cv2.contourArea)

    left = tuple(c[c[:, :, 0].argmin()][0])
    right = tuple(c[c[:, :, 0].argmax()][0])

    distance = np.sqrt( (right[0] - left[0])**2 + (right[1] - left[1])**2 )

    
    centx = np.sqrt( ((right[0] + left[0])**2)/4)
    centy = np.sqrt( ((right[1] + left[1])**2)/4 )
    print(centx, centy)

    x,y,w,h = cv2.boundingRect(c)

    # draw bounding reactangle
    # cv2.rectangle(img,(x,y),(x+w,y+h),255,-1)

    # draw bounding circle
    # cv2.circle(img, (int(centx), int(centy)), int(w/2), 255, -1)

    # draw bounding contour
    cv2.drawContours(img, contours, -1, 255, -1)

    print(x, y, w, h)
    return img


def mask_image(img, contours):
    # mask = np.zeros_like(img) # Create mask where white is what we want, black otherwise
    # cv2.drawContours(mask, contours, idx, 255, -1) # Draw filled contour in mask

    mask = np.zeros(img.shape[:2], dtype="uint8")
    mask = draw_bounding_rect(mask, contours)
    masked = cv2.bitwise_and(img, img, mask=mask)

    return masked


def invert(img):
    height, width, _ = img.shape

    for i in range(height):
        for j in range(width):
            # img[i,j] is the RGB pixel at position (i, j)
            # check if it's [0, 0, 0] and replace with [255, 255, 255] if so
            if img[i,j].sum() == 0:
                img[i, j] = [255, 255, 255]
    
    return img