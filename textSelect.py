
from os import read
import cv2
from matplotlib import pyplot as plt
import numpy as np
from pandas.core.indexes.base import Index
import pytesseract
from difflib import SequenceMatcher
import pandas as pd
import os
import dbupdate_update

pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


def textSelect(text_result,data_eq_ori,data_PNID_ori) :
    text_result1_split = text_result.split('\n')
    text_result1_split.sort(key=len)
    
    data_list_eq=[]
    data_list_PNID=[]
    ranking_eq =[0]
    ranking_PNID =[0]

    for i, data in enumerate(text_result1_split):

        data = data.replace(" ","")
        print(data + 'data')

        if data ==' ' or data =='\x0c':
            pass
    
        for j, data2 in enumerate(data_eq_ori):
            "print(str(SequenceMatcher(None,data,data2).ratio()) + ' : ' + data2)"

            if SequenceMatcher(None,data,data2).ratio() > ranking_eq[0]:
                data_list_eq = data2
                "print(data_list_eq + ' :  sub_eq')"
                ranking_eq[0] = SequenceMatcher(None,data,data2).ratio() 
   

        for j, data2 in enumerate(data_PNID_ori):

            "print(str(SequenceMatcher(None,data,data2).ratio()) + ' : ' + data2)"
            if SequenceMatcher(None,data,data2).ratio() == 0:
                break;
            
            elif SequenceMatcher(None,data,data2).ratio() > ranking_PNID[0]:
                
                data_list_PNID = data2
                
                ranking_PNID[0] = SequenceMatcher(None,data,data2).ratio()
    
    return data_list_eq,data_list_PNID


    
def GetText(image):
    dsize =(0,0) 
    disp_resize = cv2.resize(img,dsize,fx=3,fy=3)
    image_gauss = cv2.GaussianBlur(disp_resize,(5,5),0)

    sharpening_1 = np.array([[-1, -1, -1, -1, -1],
                            [-1, 2, 2, 2, -1],
                            [-1, 2, 9, 2, -1],
                            [-1, 2, 2, 2, -1],
                            [-1, -1, -1, -1, -1]])/9

    image_sharp = cv2.filter2D(image_gauss, -1, sharpening_1)

    image_gauss = cv2.GaussianBlur(image_sharp,(5,5),0)

    sharpening_2 = np.array([[-1, -1, -1, -1, -1],
                            [-1, 2, 2, 2, -1],
                            [-1, 2, 9, 2, -1],
                            [-1, 2, 2, 2, -1],
                            [-1, -1, -1, -1, -1]])/16

    image_sharp = cv2.filter2D(image_gauss, -1, sharpening_2)

    text_result = pytesseract.image_to_string(image_sharp)

    return text_result, image_sharp


def GetDb_Data(table, item):
    db = dbupdate_update.DBCONN()
    db.SetDataBase("127.0.0.1",3306,"ieps_test2","root","86rhddl0921")
    db.DB_CONN()
    db_data = db.query(table,item)
    db_data1 = pd.DataFrame(db_data)
    db_data1 = db_data1.dropna()
    db_data1 = db_data1.drop_duplicates()
    db_data1 = db_data1.reset_index(drop=True)
    data_list= db_data1[0].values.tolist()

    return data_list


def Data_to_csv(data_ori, path = os.getcwd()):

    for name in data_ori:
        data_ori[name].to_csv(path + "/" + name + ".csv", mode="w",index=False)


'''
data_eq_ori = GetDb_Data("boxid","ItemNo")
data_PNID_ori = GetDb_Data("6_1","pnid")

'''

data_eq_ori= ["PP-4206","PP-4207","PP-4208","PP-4206-2","PP-4207-3","PP-4208-4","PP-4208-5"]
data_PNID_ori= ["s4-00-m-ypd8","s4-00-m-ypd9","s4-00-m-ypd10","s4-00-m-ypd11","s4-00-m-ypd8-1","s4-00-m-ypd9-2","s4-00-m-ypd10-3"]



data_list_eq=[]
data_list_PNID=[]
data_list_file =[]

image_dir = os.getcwd() + "/crop_img"
file_list = os.listdir(image_dir)

file_dir_list =[]
file_name_list=[]
image_dir_list =[]


for i, data in enumerate(file_list):
    if os.path.isdir(os.path.join(image_dir,data)):
        file_dir_list.append(os.path.join(image_dir,data))
        file_name_list.append(data)

for i, path in enumerate(file_dir_list):

    image_path_ori = os.listdir(path)
    image_path = [file for file in image_path_ori if file.endswith(".png") or file.endswith(".PNG")]

    total_data={}
    data_list_eq=[]
    data_list_PNID=[]
    pos_x =[]
    pos_y =[]
    w=[]
    h=[]
    flag =[]

    for j, data1 in enumerate(image_path):

        image_dir = os.path.join(path,data1)
        img = cv2.imread(image_dir,0)
        text_result1, mage_sharp = GetText(img)


        eq, pnid = textSelect(text_result1,data_eq_ori,data_PNID_ori)

        cv2.imshow('123',mage_sharp)
        cv2.waitKey(0)
        Data_label = data1.split('.')[0]
        pos_x_ori,pos_y_ori,w_ori,h_ori,flag_ori = Data_label.split('_')

        pos_x.append(pos_x_ori)
        pos_y.append(pos_y_ori)
        w.append(w_ori)
        h.append(h_ori)
        flag.append(flag_ori)

        data_list_eq.append(eq)
        data_list_PNID.append(pnid)

    data_PNID=pd.DataFrame([data_list_eq,data_list_PNID,flag,pos_x,pos_y,w,h])
    data_PNID = data_PNID.T
    data_PNID.columns = ['eq','pnid','flag','pos_x','pos_y','w','h']
    total_data.update({file_name_list[i] : data_PNID})
    
    Data_to_csv(total_data,path)


'''
print(data_list_PNID)
print(data_list_eq)
print(data_list_file)


image_box= cv2.boxFilter(disp_resize1,ddepth=-1, ksize=(5,5))
bfilter = cv2.bilateralFilter(disp_resize1,9,0,0)
image_blur = cv2.blur(disp_resize1,ksize=(5,5))
image_median = cv2.medianBlur(disp_resize1,ksize=9)

sharpening_2 = np.array([[0, -1, 0],
                         [-1, 4, -1],
                         [0, -1, 0]])

'''


