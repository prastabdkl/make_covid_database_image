import cv2
import random

result_folder = r"/Users/ahnupsingh/avail/make_covid_database_image/output/result"
map = {}

def get_thresh(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
    # thresh = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    #cv2.bitwise_not(thresh, thresh)
    cv2.imwrite(result_folder+'/Covid_.jpg', gray)

    return ret, thresh

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
                print("parent", parent_contour)
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