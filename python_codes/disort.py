# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 19:45:20 2021
@author: Hossein Sharifi
"""
import os
import json 
import pydicom
import numpy as np
import shutil



def return_sorted_dicom(dir_str=[]):

    # first create a list of image folders
    files = os.listdir(dir_str)
    sorted_dcm_str = dir_str + '/' + 'sorted_dcm'
    if not 'sorted_dcm' in files:
        os.makedirs(sorted_dcm_str)
    img_dir_list = []
    for f in files:
        p = dir_str + '/' + f
        if (f.isnumeric() and  os.path.isdir(p)):
            print(f)
            img_dir_list.append(f)
        
    img_dir_list.sort(key=int)
    #print(img_dir_list)
    #print(os.getcwd())

    # Start opening each folder and 
    # try to search for the dcm file
    for f in img_dir_list:
        temp_str = dir_str+'/'+f
        if 'pdata' in os.listdir(temp_str):
            temp_str = temp_str + '/'+'pdata'
            if '1' in os.listdir(temp_str):
                temp_str = temp_str+'/'+'1'
                if 'dicom' in os.listdir(temp_str):
                    dcm_str = temp_str + '/' + 'dicom' + '/' + 'EnIm1.dcm'
                    dcm_dataset = pydicom.dcmread(dcm_str)
                    #print(dcm_dataset.dir())
                    img_name = dcm_dataset['SeriesDescription'].value
                    if img_name in ['SA_1','SA_2','SA_3','SA_4',
                                    'SA_5','SA_6','LA_2CH','LA_PLUS_60',
                                    'LA_PLUS60','LA_MINUS_60','LA_MINUS60']:
                        new_img_str = sorted_dcm_str + '/' +img_name+'.dcm'
                        shutil.copy(dcm_str, new_img_str)
                        print(dcm_dataset['SeriesDescription'].value)


if __name__ == '__main__':
    dir_str = '/Users/hosseinsharifi/Downloads/test_dicom'
    return_sorted_dicom(dir_str)