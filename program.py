import pandas as pd
import cv2
import requests
import os

mouse_click = False
x_pos, y_pos, r, g, b = 0, 0, 0, 0, 0


# Select where the image will be loaded from. (I plan to add a webcam)
# And don't create file with name - 'img.jpg'
def open_img(name_img_file: str):
    if 'https' not in name_img_file:
        img = cv2.imread(name_img_file)
    elif 'https' in name_img_file:
        img = requests.get(name_img_file)
        out = open("img.jpg", "wb")
        out.write(img.content)
        out.close()
        img = cv2.imread("img.jpg")
    else:
        '''У России два пути, то что я делаю и то что хочу добавить'''
        img = cv2.VideoCapture(0)
    return img


# read csv file in language:
def select_language():
    language = input('input your language eng/rus: ')
    index = ["color", "color_name", "hex", "R", "G", "B"]
    if language.lower() == 'rus':
        df = pd.read_csv('color_data_base.csv', names=index, header=None, encoding='utf-8')
    elif language.lower() == 'eng':
        df = pd.read_csv('colors.csv', names=index, header=None, encoding='utf-8')
    else:
        print('Hey, do as I wrote, otherwise you won\'t go further!!!')
        return select_language()
    return df


# Definition of color and hex
def get_color(R, G, B):
    min_dist = 256*3
    for i in range(len(df)):
        dist = abs(R - int(df.loc[i, "R"])) + abs(G - int(df.loc[i, "G"])) + abs(B - int(df.loc[i, "B"]))
        if dist <= min_dist:
            min_dist = dist
            color = df.loc[i, "color_name"] + ' '+ df.loc[i, "hex"] + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
    return color


# Definition of RGB
def detection_RGB(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, x_pos, y_pos, mouse_click
        mouse_click = True
        x_pos = x
        y_pos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)


# input data
df = select_language()
tp_file = (input('input img/url/web'))
if ('https' or 'jpg' or 'png') in tp_file:
    img = open_img(tp_file)
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', detection_RGB)


    # output info
    while True:
        cv2.imshow("image", img)
        if mouse_click:
            text = get_color(r, g, b)
            print(text)
            mouse_click = False
        # if you need close program => "esc"
        if cv2.waitKey(1) == 27:
            break

    os.remove("img.jpg")

elif tp_file == 'web':
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', detection_RGB)

    while True:
        _, img = cap.read()
        cv2.imshow("image", img)
        if mouse_click:
            text = get_color(r, g, b)
            print(text)
            mouse_click = False
        key = cv2.waitKey(1)
        if cv2.waitKey(1) == 27:
            break
    cap.release()


cv2.destroyAllWindows()
# maybe I'll make an API on Kivy
