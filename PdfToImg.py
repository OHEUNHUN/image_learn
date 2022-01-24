import os
from pdf2image import convert_from_path 

PDF_dir = os.getcwd() + '/Desktop/PNID/PNID_ori/석포'
file_list = os.listdir(PDF_dir)
save_dir = os.getcwd()+ '/Desktop/PNID/photo1/'




for i, name in enumerate(file_list):
    pages = convert_from_path(PDF_dir+ '/' + name) 

    for j, page in enumerate(pages):
        name1 = name.split('.')[0]
        page.save(save_dir + name1 +'_' +str(j)+'.png', "PNG")


