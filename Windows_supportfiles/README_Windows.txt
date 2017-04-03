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

tested on Windows XP Python v2.7 32 bit


Windows Standalone:
=====================
   download the MRSpeCS_Windows ZIPfile from Release, unpack
   simply run "MRSpeCS.exe"
   you may have to run this as administrator (right click "Run as ..")
   this is because this distributable will unpack itself in a
   temporary folder and try to run from there, windows default 
   security settings don't like to execute code from temp folders.


Running in Python (not standalone):
===================================
   install Python 2.7 (download from: https://www.python.org/downloads)
   install pywin32 (download from: https://sourceforge.net/projects/pywin32/files/pywin32)
   install pydicom (included, use command C:\Python2.7\python setup.py install)
   unpack the files in FSLv3.3.7_extract.zip to folder with the main script
   run C:\Python2.7\python MRSpeCS.py


Rebuild the standalone executable:
==================================
   unpack FSLv3.3.7_extract.zip
   run "PyInstaller_build.bat"
   this presumes python is installed in the default location C:\Python27
   if otherwise edit the batch file


Requirements:
=============
   to rebuild the standalone you will need:
   - python (obviously)
   - pyinstaller (http://www.pyinstaller.org/)
   - pydicom (http://pydicom.readthedocs.io)
   - pywin32 (https://sourceforge.net/projects/pywin32/files/pywin32/)
   and tkinter which should already be included in the python distribution

   any problems with the above links you also can download and install 
   the referred packages from the "Unofficial Windows Binaries for Python 
   Extension Packages" at http://www.lfd.uci.edu/~gohlke/pythonlibs/
   for this you may need pip(https://pip.pypa.io/en/stable/installing)
   if you use python>=2.7.9 pip is already included, otherwise you also can use
   pip-win from https://sites.google.com/site/pydatalog/python/pip-for-windows

   The program also requires the following supplied external files:
      avscale.exe, fslhd.exe, fslmaths.exe, fslmeants.exe, fslorient.exe,
      fslswapdim.exe, bet2.exe, convert_xfm.exe, fast.exe, flirt.exe
      and cygwin1.dll
   these are from the old FSL v3.3.7 distribution running on Cygwin 1.5.18
   source code is available at fsl.fmrib.ox.ac.uk/fsldownloads/oldversions/
   the windows binary distribution unfortunately is not available any more
   you can find some instructions on how to compile FSL v3.3 on windows here:
   https://www.cbica.upenn.edu/sbia/software/glistr/install/flirtwindows.html

   also needed is the following supplied external file from 
   Cris Rorden's MRIcron software (version 1JUNE2015 32bit BSD License)
     dcm2nii.exe
   you can also get this either from 
   http://people.cas.sc.edu/rorden/mricron/install.html
   or from https://www.nitrc.org/projects/mricro


Limitations when missing some components
========================================
   - the FSL external files are required (these do the main job;)
   - when missing dcm2nii.exe the script will fail to import 3DT1 image
     files in DICOM format, you can still import NIFTI format
   - when missing pydicom the script will fail to import spectro files in 
     DICOM format, you can still import spectro files in SDAT format
   - when missing tkinter, the script does not permit to choose input
     files interactively, you can still run in command line mode
   - when missing pywin32 the script can't disable the console window close
     this a simple security measure to avoid ungraceful exits, which
     potentially leave large amounts of data in hidden temp files behind
     (recommended user abort is Ctrl-C, which cleans up tempfiles before exit)

           