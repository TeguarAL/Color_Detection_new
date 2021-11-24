import cv2
import pandas as pd

mouse_click = False
x_pos, y_pos, r, g, b = 0, 0, 0, 0, 0



index = ["color", "color_name", "hex", "R", "G", "B"]
df = pd.read_csv('color_data_base.csv', names=index, header=None, encoding='utf-8')

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




cap = cv2.VideoCapture(0)
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
    if key == 27:
        break


cap.release()
cv2.destroyAllWindows()

