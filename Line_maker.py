import cv2
from matplotlib import pyplot as plt
import numpy as np
import time
import detect


class PNID:
    
    def __init__(self):
        super().__init__()
    
    def Check_Mainlayout(self, colum_img, row_img):
        x = []
        flag = 0
        for i in range(0,(colum_img.shape[0])):
            for j in range(2,(colum_img.shape[1]-2)):
                if (int(colum_img[i][j-2])+int(colum_img[i][j-1])+int(colum_img[i][j])+int(colum_img[i][j+1])+int(colum_img[i][j+2])) <1:
                    x.append(round(j,-1))
                    flag +=1
            if flag >1:
                break
        flag = 0
        for i in reversed(range(0,(colum_img.shape[0]))):
            for j in range(2,(colum_img.shape[1]-2)):
                if (int(colum_img[i][j-2])+int(colum_img[i][j-1])+int(colum_img[i][j])+int(colum_img[i][j+1])+int(colum_img[i][j+2])) <1:
                    x.append(round(j,-1))
                    flag +=1
            if flag >1:
                break

        y = []
        flag = 0

        for i in range(0,(row_img.shape[1])):
            for j in range(2,(row_img.shape[0]-2)):

                if (int(row_img[j-1][i])+int(row_img[j][i])+int(row_img[j+1][i])) <1:
                    y.append(round(j,-1))
                    flag +=1
            if flag >1:
                break

        flag = 0
        for i in reversed(range(0,(row_img.shape[1]))):
            for j in range(1,(row_img.shape[0]-1)):

                if (int(row_img[j-1][i])+int(row_img[j][i])+int(row_img[j+1][i])) <1:
                    y.append(round(j,-1))
                    flag +=1
            if flag >1:
                break

    
        x_pos = list(set(x))
        y_pos = list(set(y))

        return x_pos, y_pos


    def Make_colum_img(self,img):
        gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
        kener = cv2.getStructuringElement(shape=cv2.MORPH_RECT , ksize=(1,5))
        colum_img = cv2.morphologyEx(gray,cv2.MORPH_CLOSE,kener,iterations=3)

        return colum_img

    def Make_row_img(self,img):
        gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
        kener = cv2.getStructuringElement(shape=cv2.MORPH_RECT , ksize=(5,1))
        row_img = cv2.morphologyEx(gray,cv2.MORPH_CLOSE,kener,iterations=3)

        return row_img

class Make_image:
        
    def __init__(self):
        super().__init__()

    def Make_MainLayOut(self,x_pos, y_pos,original_img):
        
        for y in y_pos:
            if y == min(y_pos):
                pass
            else:
                cv2.rectangle(original_img,(min(x_pos),min(y_pos)),(max(x_pos),y),(255,255,0),3)
        
        return original_img


    def Make_pipeLine(self,colum_img, row_img):

        New_img = np.ones(shape=colum_img.shape) *255

        for i in range(0,colum_img.shape[0]):
             for j in range(0, colum_img.shape[1]):

                if colum_img[i][j] != row_img[i][j]:

                    if min(colum_img[i][j],row_img[i][j]) < 5:
                        New_img[i][j] = 0
                    else:
                        pass
                elif colum_img[i][j] == row_img[i][j]:

                    if min(colum_img[i][j],row_img[i][j]) < 5:
                        New_img[i][j] = 0

        return New_img




pnid = PNID()
make_img = Make_image()

img = cv2.imread("photo\page3.PNG")

colum_img = pnid.Make_colum_img(img)
row_img = pnid.Make_row_img(img)


x_pos,y_pos = pnid.Check_Mainlayout(colum_img,row_img)

x_pos = sorted(x_pos)
y_pos = sorted(y_pos)


crop_img = img[y_pos[0]:y_pos[len(y_pos)-1],x_pos[0]:x_pos[-1]]

dsize =(0,0) 
disp_resize = cv2.resize(colum_img,dsize,fx=0.6,fy=0.6)
disp_resize1 = cv2.resize(row_img,dsize,fx=0.6,fy=0.6)

print(x_pos,y_pos)
cv2.imshow('123',disp_resize)
cv2.imshow('1234',disp_resize1)
cv2.waitKey()