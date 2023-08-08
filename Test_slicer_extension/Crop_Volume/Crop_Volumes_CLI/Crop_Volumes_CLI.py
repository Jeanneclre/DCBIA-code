#!/usr/bin/env python-real

import argparse
import SimpleITK as sitk
from Crop_Volumes_utils.FilesType import Search
import numpy as np
import os,json




def main(args):

    path_input = args.scan_files_path
    ROI_Path = args.path_ROI_file
    OutputPath = args.output_path
    suffix_namefile = args.suffix
    
    print("in main of cli")
    ScanList = Search(path_input, ".nii.gz",".nrrd.gz",".gipl.gz")
    for key,data in ScanList.items():
        
        for patient_path in data:
            patient = os.path.basename(patient_path).split('_Scan')[0].split('_scan')[0].split('_Or')[0].split('_OR')[0].split('_MAND')[0].split('_MD')[0].split('_MAX')[0].split('_MX')[0].split('_CB')[0].split('_lm')[0].split('_T2')[0].split('_T1')[0].split('_Cl')[0].split('.')[0]

            ScanOutPath = OutputPath+"/"+patient+suffix_namefile+key
            
            img = sitk.ReadImage(patient_path)
            # size = np.array(img.GetSize())
            # print("size of the image: ",size)

            ## PADDING ##
            # img = img.sitk.ConstantPadImageFilter()
            # testPath = OutputPath+"/"+"paddedImage"+key
            # sitk.WriteImage(img,testPath)

            print("working on patient: ",patient)
            ROI = json.load(open(ROI_Path))['markups'][0]
            ROI_Center = np.array(ROI['center'])
            ROI_Size = np.array(ROI['size'])

            Lower = ROI_Center - ROI_Size / 2
            Upper = ROI_Center + ROI_Size / 2

            Lower = np.array(img.TransformPhysicalPointToContinuousIndex(Lower)).astype(int)
            Upper = np.array(img.TransformPhysicalPointToContinuousIndex(Upper)).astype(int)

            # Crop the image
            crop_image = img[Lower[0]:Upper[0],
                            Lower[1]:Upper[1],
                            Lower[2]:Upper[2]]
            
            try:
                sitk.WriteImage(crop_image,ScanOutPath)
            except:
                print("Error for patient: ",patient)




if __name__ == "__main__":
    
    print("dans le cli")
    parser = argparse.ArgumentParser()


    parser.add_argument('scan_files_path',type=str)
    parser.add_argument('path_ROI_file',type=str)
    parser.add_argument("output_path",type=str)
    parser.add_argument('suffix',type=str)
   # parser.add_argument('logPath',type=str)


    args = parser.parse_args()


    main(args)