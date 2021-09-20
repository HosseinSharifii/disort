# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 19:45:20 2021
@author: Hossein Sharifi
"""
import os
import sys
import pydicom
import shutil



def return_sorted_dicom(dir_str=[]):
   
    grand_parent_root = 0
    parent_root = 0
    child_root = 0
    # handle the assigned str
    grand_parent_root,parent_root,child_root = handle_roots(dir_str)

    # now handle reading the files according to the assigned dir root 
    if grand_parent_root == 1:
        print('grand_parent_root is given')
        for gf in os.listdir(dir_str):
            if os.path.isdir(dir_str+'/'+gf):
                parent_str =  dir_str+'/'+gf
                for pf in os.listdir(parent_str):
                    if (os.path.isdir(parent_str+'/'+pf) and len(pf.split('_')[0])==8):
                        child_str = parent_str + '/' +pf
                        handle_child_root(child_str)

    elif parent_root == 1:
        print('parent_root is given')
        for pf in os.listdir(dir_str):
            
            if (os.path.isdir(dir_str+'/'+pf) and len(pf.split('_')[0])==8):
                child_str = dir_str + '/' +pf
                handle_child_root(child_str)

    elif child_root == 1:
        print('child_root is given')
        child_str = dir_str
        handle_child_root(child_str)


def handle_roots(dir_str=""):
    grand_parent_root = 0
    parent_root = 0
    child_root = 0
    
    # handle the assigned str
    if dir_str.split('/')[-1] == 'MRI':
        print('grand is activated')
        grand_parent_root = 1
    elif '-' in dir_str.split('/')[-1] and dir_str.split('/')[-1].split('-')[0].isnumeric():
        print('parent is activated')
        parent_root = 1 
    else:
        print('child is activated')
        child_root = 1
    return grand_parent_root , parent_root, child_root

def handle_child_root(child_str = ""):
    # first create a list of image folders
    print('Looking for dicom images in this directory to sort...')
    print(child_str)
    files = os.listdir(child_str)
    sorted_dcm_str = child_str + '/' + 'sorted_dcm'
    if not 'sorted_dcm' in files:
        os.makedirs(sorted_dcm_str)
    else:
        print('sorted dicom directory is already existed')
        return

    img_dir_list = []
    for f in files:
        p = child_str + '/' + f
        if (f.isnumeric() and  os.path.isdir(p)):
            img_dir_list.append(f)
        
    img_dir_list.sort(key=int)
    #print(img_dir_list)

    # Start opening each folder and 
    # try to search for the dcm file
    for f in img_dir_list:
        temp_str = child_str+'/'+f
        if 'pdata' in os.listdir(temp_str):
            temp_str = temp_str + '/'+'pdata'
            if '1' in os.listdir(temp_str):
                temp_str = temp_str+'/'+'1'
                if 'dicom' in os.listdir(temp_str) and 'EnIm1.dcm' in os.listdir(temp_str + '/' + 'dicom'):
                    dcm_str = temp_str + '/' + 'dicom' + '/' + 'EnIm1.dcm'
                    dcm_dataset = pydicom.dcmread(dcm_str)
                    #print(dcm_dataset.dir())
                    img_name = dcm_dataset['SeriesDescription'].value
                    #print(img_name)
                    if '_' in img_name:
                        if img_name.split('_')[0] == 'LA' or img_name.split('_')[0] == 'SA':
                            new_img_str = sorted_dcm_str + '/' +img_name+'.dcm'
                            shutil.copy(dcm_str, new_img_str)
                            print(dcm_dataset['SeriesDescription'].value)

if __name__ == '__main__':

    no_of_arguments = len(sys.argv)
    print(no_of_arguments)
    
    if no_of_arguments == 1:
        print('No directory has been assigned!')
        print('Exiting...')
    elif no_of_arguments == 2:
        print('Start sorting dicom images in the following path directory ...')
        print(sys.argv[1])
        dir_str = sys.argv[1]
        dir_str = dir_str.replace('\\','/')
        print(dir_str)

        return_sorted_dicom(dir_str)

        