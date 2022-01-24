import cv2
from matplotlib import pyplot as plt
from os import read
import pandas as pd
import numpy as np
import os

def crop_YOLO_img(data_file_pandas,img_file,save_path,fx_set=1,fy_set=1 ):

    flag =[]
    pos_x=[]
    pos_y=[]
    w=[]
    h=[]

    for i in range(len(data_file_pandas)):
        in_out = np.float32(data_file_pandas.loc[i][0])
        in_out = int(in_out)
        x= np.float32(data_file_pandas.loc[i][1]) * (img.shape[1])
        x=int(x)
        y= np.float32(data_file_pandas.loc[i][2]) * (img.shape[0])
        y=int(y)
        width =np.float32(data_file_pandas.loc[i][3]) * (img.shape[1])
        width = int(width)
        hight= np.float32(data_file_pandas.loc[i][4]) * (img.shape[0])
        hight = int(hight)

        pos_x.append(x)
        pos_y.append(y)
        w.append(width)
        h.append(hight)
        flag.append(in_out)

        x_ret_1 = int(x - width *0.5)
        x_ret_2 = int(x + width *0.5)
        y_ret_1 = int(y - hight *0.5)
        y_ret_2 = int(y + hight *0.5)


        dsize =(0,0) 
        crop_image = img_file[y_ret_1 : y_ret_2, x_ret_1:x_ret_2]
        disp_resize1 = cv2.resize(crop_image,dsize,fx=fx_set,fy=fy_set)
        cv2.imwrite(save_path + "/" + str(x) +"_"+ str(y) +"_"+str(width) +"_"+str(hight)+"_" + str(in_out) + ".png",disp_resize1)

    return pos_x,pos_y,w,h,flag



def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)



'''
# 경로에 대한 샘플
position_path_file = "det/labels/acid_1.pdf0.txt"
image_path = "det/acid_1.pdf0.png"
image_save_path = "crop_img/"
'''

image_dir = os.getcwd() + "/crop_img"
file_list = os.listdir(image_dir)

image_list=[]
text_list=[]
dir_list=[]

for i, data in enumerate(file_list):
    file_type = data.split('.')
    if file_type[-1] =='txt':
        text_list.append(data)
    elif file_type[-1] =='png':
        image_list.append(data)


for i, data in enumerate(image_list):
    file_name = data.split('.')[:-1]
    dir = image_dir.split(".")[0] + "/" + file_name[0]+file_name[1]
    dir_list.append(dir)
    createFolder(dir)


for image,text,dir in zip(image_list,text_list,dir_list):
    position_path_file = image_dir + "/" + text;
    image_path = image_dir + "/" + image;
    image_save_path = dir;


    img = cv2.imread(image_path,0) 
    postion = open(position_path_file,"r")
    postion = postion.read().split('\n')


    postion_pd = pd.DataFrame(columns=["clss","x_center","y_center","width",'hight'])

    for i in range(len(postion)-1):
        if postion[i].split(' ')[0] == "0":
            postion_pd.loc[i] = postion[i].split(' ')

    postion_pd = postion_pd.reset_index(drop = True)
    crop_YOLO_img(postion_pd,img,image_save_path)

