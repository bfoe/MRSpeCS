MRSpeCS - MR Spectro Compartment Segmentation
=============================================
The Software takes the geometry information from a Single Voxel 
Spectroscopy dataset and a Volumetric 3D image with T1 contrast
and calculates CSF/GM/WM fractions intended to be used as 
proton density correction factors in quantitative MR spectrospcopy.
Find a very usefull introduction to the subject at: 
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4849426/

Usage:
   MRSpeCS.py --img=<inputimage> --spec=<inputspectro>
   some help available with "MRSpeCS.py --help"
   
License:
   GPL, see details inside MRSpeCS.py
   
Author:
   Bernd Foerster, bfoerster at gmail.com

tested on FSL v5 CentOS 6.3 Virtual Machine with Pyhton v2.6.6


Linux Installation:
===================
   - Requires FSL, see installation procedure at:
         https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FslInstallation/Linux
   - install included "dcm2nii" tool:
         sudo cp dcm2nii /usr/local/fsl/bin/dcm2nii 
         sudo chmod +x /usr/local/fsl/bin/dcm2nii
     observe: "/usr/local/fsl/bin" is the default FSL folder, if FSL was
     installed FSL to another location substitute with the respective folder
   - to be able to interactively choose input files "tkinter" is required
     which normally is already installed with python, if not so, try:
         sudo yum install tkinter
   - to be able to read spectro input files in DICOM format "pydicom" is
     required, to install try:
         yum install python-pip
         pip install pydicom
     or see http://pydicom.readthedocs.io/en/stable/getting_started.html
  - run MRSpeCS.py


Also included:
==============
   - short shell script "SpeCS_walkpath.sh" for batch procesing under Linux/MacOS
     just a proof of concept, you still have to edit this file 
     in order to actually run SpeCS
     have a look, and give it a try ;)
   
   - files from FSL "FSLv5.0.4_extract.zip" potentially replacing the need 
     for full FSL installation, also containes dcm2nii.
     usage:
         su
         tar -zxvf FSLv5.0.4_extract.tar.gz 
         mv fsl /usr/local
     CAUTION: don't overwrite this on an existing FSL installation
     This is just a quick hack for testing
     Full original FSL installation is still the recommended way

   - pydicom tarball, in case this disapears from the above website
     extract with:
         tar -zxvf pydicom-0.9.9.tar.gz
         cd pydicom-0.9.9
         sudo /usr/bin/python setup.py install
