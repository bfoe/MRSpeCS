# MRSpeCS
MR Spectro Compartment Segmentation

The Software takes the geometry information from a Single Voxel 
Spectroscopy dataset and a Volumetric 3D image with T1 contrast
and calculates CSF/GM/WM fractions intended to be used as 
proton density correction factors in quantitative MR spectroscopy.
Find a very useful introduction to the subject at: 
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4849426/


This software is basically a script calling external tools:
  - Chris Rorden's `dcm2nii` for DICOM to NIFTI conversion
    (http://people.cas.sc.edu/rorden/mricron/index.html)
  - FSL (http://fsl.fmrib.ox.ac.uk) for the actual calculations 

`dmc2nii` and Windows FSL binaries are included

##
### Runs under:
  - Windows (see details under Windows_supportfiles/README_Windows)
  - Linux   (see details under Linux_supportfiles/README_Linux)
  - MacOS   (see details under MacOS_supportfiles/README_MacOS)

CAUTION: you may get slightly different results on different platforms 
depending on FSL version.

##
### Usage:
    MRSpeCS.py --img=<inputimage> --spec=<inputspectro>
    MRSpeCS.py --help

##
### MR data:    
    Spectro: Philips SPAR format
             Philips DICOM format(spectra are in files called XX*)
    Images:  Philips enhanced DICOM (aka multiframe DICOM, one file per scan)
             NIFTI images manually converted from DICOM using the `dcm2nii` tool
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;![#f03c15](https://placehold.it/15/f03c15/000000?text=+) <b> Currently supports Philips formats only </b> ![#f03c15](https://placehold.it/15/f03c15/000000?text=+)

    
##
### License:
GPL, see details inside `MRSpeCS.py`

##
### Author:
Bernd Foerster, bfoerster at gmail.com
