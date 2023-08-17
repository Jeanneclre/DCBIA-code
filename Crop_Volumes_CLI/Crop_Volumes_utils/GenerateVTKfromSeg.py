import vtk
import argparse
import SimpleITK as sitk
import numpy as np
import os

LABEL_COLORS = {
    1: [216, 101, 79],
    2: [128, 174, 128],
    3: [0, 0, 0],
    4: [230, 220, 70],
    5: [111, 184, 210],
    6: [172, 122, 101],
}

def convertNiftiToVTK(input_path, output_path ) -> None:
        """
        function to generate VTK files from nifti segmentation (labelmap).
        input : path of your segmentation file, path of your futur vtk file
        """
        input_filename = input_path
        output_filename = output_path

        # Read nifti file and convert it to numpy array
        img = sitk.ReadImage(input_filename) 
        img_arr = sitk.GetArrayFromImage(img)

        # Read all the labels present in the image
        present_labels = []
        for label in range(np.max(img_arr)):
                if label+1 in img_arr:
                        present_labels.append(label+1)

        label = np.max(img_arr)
       
        # Read the original Nifti image
        surf = vtk.vtkNIFTIImageReader()
        surf.SetFileName(input_filename)
        surf.Update()
        
        # Apply filter to create an isosurface from the input image
        # convert it to a 3D surfac representation
        dmc = vtk.vtkDiscreteMarchingCubes()
        dmc.SetInputConnection(surf.GetOutputPort())
        dmc.GenerateValues(100, 1, 100)

        # LAPLACIAN smooth to improve VTK rendering
        # by reducing the impact of jagged edges
        SmoothPolyDataFilter = vtk.vtkSmoothPolyDataFilter()
        SmoothPolyDataFilter.SetInputConnection(dmc.GetOutputPort())
        SmoothPolyDataFilter.SetNumberOfIterations(5)
        SmoothPolyDataFilter.SetFeatureAngle(120.0)
        SmoothPolyDataFilter.SetRelaxationFactor(0.6)
        SmoothPolyDataFilter.Update()

        model = SmoothPolyDataFilter.GetOutput()

        # Coloring the VTK according to labels
        color = vtk.vtkUnsignedCharArray() 
        color.SetName("Colors") 
        color.SetNumberOfComponents(3) 
        color.SetNumberOfTuples( model.GetNumberOfCells() )
            
        for i in range(model.GetNumberOfCells()):
            color_tup=LABEL_COLORS[label]
            color.SetTuple(i, color_tup)

        model.GetCellData().SetScalars(color)

        # Save the final VTK model
        Write(model, output_filename)

def Write(vtkdata, output_name):
	outfilename = output_name
	print("Writting:", outfilename)
	polydatawriter = vtk.vtkPolyDataWriter()
	polydatawriter.SetFileName(outfilename)
	polydatawriter.SetInputData(vtkdata)
	polydatawriter.Write()
