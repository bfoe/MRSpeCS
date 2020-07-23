#!/usr/bin/python
#
# MRSpeCS - MR Spectro Compartment Segmentation
# .. for proton density corrections in quantitative spectroscopy
#
# you can find a very useful introduction to the subject at:
# Quadrelli S, Mountford C, Ramadan S, "Hitchhiker's Guide to Voxel 
# Segmentation for Partial Volume Correction of In Vivo Magnetic 
# Resonance Spectroscopy" Magn Reson Insights. 2016; 9: 1-8.
# DOI:10.4137/MRI.S32903
# direct link: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4849426/
#
# The Software takes the geometry information from a 
# Single Voxel Spectroscopy dataset (Philips SPAR format),
# and a Volumetric 3D image with T1 contrast(Philips enhanced DICOM)
# then calculates:
#   1) T1 Image switched to axial: T1.nii
#   2) overlay map of the spectroscopy Voxel: SpectroBOX.nii
#      for visualization open 1) in e.g. MRIcro and use 2) as overlay
#   3) the image masks resulting from the segmentation CSF/GM/WM: 
#      T1_CSF.nii, T1_GM.nii, T1_WM.nii
#      these can also be used for overlay visualization 
#   4) the log file MRSpeCS.log (Error messages etc. go here) 
#   5) Finally the results output: MRSpeCS_Results.txt
#      containing the values for CSF/GM/WM fractions
#      these are intended to be used as proton density correction factors 
#      for quantitative spectroscopy
# image files are in radiological orientation
#     
# author: Bernd Foerster, bfoerster at gmail.com
# 
# ----- VERSION HISTORY -----
#
# Version 0.7 - 02, April 2017
#   - public release on GitHub
#    
#
# ----- LICENSE -----                 
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License (GPL) as published 
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version. For more detail see the 
# GNU General Public License at <http://www.gnu.org/licenses/>.
# also the following additional license terms apply:
#
# 1) Personal NO MILITARY clause:
# THE USE OF THIS SOFTWARE OR ANY PARTS OF IT IS EXPLICITLY PROHIBITED FOR
# MILITARY INSTITUTIONS, BOTH GOVERNMENTAL AND PRIVATE "SECURITY" SERVICES, 
# AND ANY INSTITUTIONS DIRECTLY OR INDIRECTLY LINKED TO INTELLIGENCE SERVICES,
# BOTH FOR MILITARY AND CIVIL ESPIONAGE. THIS INCLUDES, BUT IS NOT LIMITED TO,
# CIVIL SERVICES RUN BY THE MILITARY, SUCH AS MILITARY HOSPITALS.
#
# 2) Chris Rorden's MRIcron, all rights reserved. Redistribution and use in 
# binary forms, with or without modification, are permitted provided inclusion 
# of the copyright notice, this list of conditions and the following disclaimer
# is provided with the distribution: Neither the name of the copyright owner
# nor the name of this project (MRIcron) may be used to endorse or promote
# products derived from this software without specific prior written permission
# This software is provided by the copyright holder "as is" and any express or 
# implied warranties, including, but not limited to, the implied warranties of 
# merchantability and fitness for a particular purpose are disclaimed. In no
# event shall the copyright owner be liable for any direct, indirect, 
# incidental, special, exemplary, or consequential damages (including, but not
# limited to, procurement of substitute goods or services; loss of use, data, 
# or profits; or business interruption) however caused and on any theory of
# liability, whether in contract, strict liability, or tort (including 
# negligence or otherwise) arising in any way out of the use of this 
# software, even if advised of the possibility of such damage.
# 
# 3)FMRIB Software Library, Release 3.3 (c) 2006, The University of Oxford
# (the "Software") The Software remains the property of the University of 
# Oxford ("the University"). The Software is distributed "AS IS" under this 
# Licence solely for non-commercial use in the hope that it will be useful,
# but in order that the University as a charitable foundation protects its
# assets for the benefit of its educational and research purposes, the 
# University makes clear that no condition is made or to be implied, nor is 
# any warranty given or to be implied, as to the accuracy of the Software, 
# or that it will be suitable for any particular purpose or for use under any
# specific conditions. Furthermore the University disclaims all responsibility
# for the use which is made of the Software. It further disclaims any 
# liability for the outcomes arising from using the Software. The Licensee
# agrees to indemnify the University and hold the University harmless from and
# against any and all claims, damages and liabilities asserted by third 
# parties (including claims for negligence) which arise directly or indirectly 
# from the use of the Software or the sale of any products based on the 
# Software. No part of the Software may be reproduced, modified , transmitted 
# or transferred in any form or by any means, electronic or mechanical, without
# the express permission of the University. The permission of the University 
# is not required if the said reproduction, modification, transmission or
# transference is done without financial return, the conditions of this Licence
# are imposed upon the receiver of the product, and all original and amended  
# source code is included in any transmitted product. You may be held legally 
# responsible for any copyright infringement that is caused or encouraged by
# your failure to abide by these terms and conditions. You are not permitted 
# under this Licence to use this Software commercially. Use for which any 
# financial return is received shall be defined as commercial use, and includes
# (1) integration of all or part of the source code or the Software into a 
# product for sale or license by or on behalf of Licensee to third parties or
# (2) use of the Software or any derivative of it for research with the final  
# aim of developing software products for sale or license to a third party or 
# (3) use of the Software or any derivative of it for research with the final
# aim of developing non-software products for sale or license to a third party,
# or(4) use of the Software to provide any service to an external organisation 
# for which payment is received. If you are interested in using the Software
# commercially, please contact Isis Innovation Limited ("Isis"), the technology
# transfer company of the University, to negotiate a licence. 
# Contact details are: innovation@isis.ox.ac.uk quoting reference DE/1112.
#
#
# ----- REQUIREMENTS ----- 
#
#   This program was developed under Python Version 2.7.6 for Windows 32bit
#   A windows standalone executable can be "compiled" with PyInstaller
#
#   tested in the FSL v5 Virtual machine under CentOS 6.3 (with Python 2.6.6)
#   requires dcm2nii to be copied to FSL binary dir (usually /usr/local/fsl/bin)
#
#   For basic operation no additional Python libraries are required.
#   To interactively choose input file python tkinter is required 
#   (if not already installed try "yum install tkinter")
#   To read spectro files in DICOM format pydicom is required 
#   (to install try "yum install python-pip" then "pip install pydicom")
#      or see http://pydicom.readthedocs.io/en/stable/getting_started.html 
#     
#   The program requires the following external files from FSL:
#      avscale.exe, fslhd.exe, fslmaths.exe, fslmeants.exe, fslorient.exe,
#      fslswapdim.exe, bet2.exe, convert_xfm.exe, fast.exe, flirt.exe
#      cygwin1.dll (windows only)
#   For Windows the above files are included from the old FSL v3.3.7 distribution
#   running on Cygwin 1.5.18, source code is still available at 
#   https://fsl.fmrib.ox.ac.uk/fsldownloads/oldversions/ the windows binary 
#   distribution unfortunately is not available any more, you still can find
#   some instructions on how to compile FSL v3.3.7 on windows here:
#   https://www.cbica.upenn.edu/sbia/software/glistr/install/flirtwindows.html
#
#   also needed is the following supplied external file from 
#   Cris Rorden's MRIcron software (version 1JUNE2015 32bit BSD License)
#     dcm2nii.exe
#   you can also get this either from 
#   http://people.cas.sc.edu/rorden/mricron/install.html
#   or from https://www.nitrc.org/projects/mricron
#
#
# ----- TO DO LIST ----- 
#
#   - accept files from other vendors (currently Philips only)
#


Program_version = "v0.8" # program version


import sys
import math
import os
import signal
import random
import shutil
import subprocess
import time
import datetime
from getopt import getopt
from getopt import GetoptError
from distutils.version import LooseVersion
try: from MRSpeCS_Report import MRSpeCS_Report
except: pass


TK_installed=True
try: from tkFileDialog import askopenfilename # Python 2
except: 
  try: from tkinter.filedialog import askopenfilename; # Python3
  except: TK_installed=False
try: import Tkinter as tk; # Python2
except: 
  try: import tkinter as tk; # Python3
  except: TK_installed=False

FNULL = open(os.devnull, 'w')
old_target, sys.stderr = sys.stderr, FNULL # replace sys.stdout 
pydicom_installed=False
try: import dicom; pydicom_installed=True  # <v1.0
except: pass
try: import pydicom as dicom; pydicom_installed=True#  >v1.0
except: pass
sys.stderr = old_target # re-enable

pywin32_installed=True
try: import win32console, win32gui, win32con
except: pywin32_installed=True


def exit (code):
    # cleanup 
    try: shutil.rmtree(tempdir)
    except: pass # silent
    if pywin32_installed:
        try: # reenable console windows close button (useful if called command line or batch file)
            hwnd = win32console.GetConsoleWindow()
            hMenu = win32gui.GetSystemMenu(hwnd, False)
            win32gui.EnableMenuItem(hMenu, win32con.SC_CLOSE, win32con.MF_ENABLED)
        except: pass #silent
    sys.exit(code)
def signal_handler(signal, frame):
    lprint ('User abort')
    exit(1)
def logwrite(message): 
    sys.stderr.write(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    sys.stderr.write(' ('+ID+') - '+message+'\n')
    sys.stderr.flush()   
def lprint (message):
    print (message)
    logwrite(message)
def checkfile(file): # generic check if file exists
    if not os.path.isfile(file): 
        lprint ('ERROR:  File "'+file+'" not found '); exit(1)
def checkcommand(file): # specific for the external executables
    if sys.platform=="win32": file = file+'.exe'
    if not os.path.isfile(file): lprint ('ERROR:  File "'+file+'" not found '); exit(1)
def delete (file):
    try: os.remove(file)
    except: pass #silent
def rename (fromfile, tofile): 
    delete (tofile)   
    try: os.rename (fromfile, tofile)
    except: lprint ('ERROR:  Unable to move file '+fromfile); exit(1)
def copy (fromfile, tofile):
    delete (tofile)   
    try: shutil.copy2(fromfile, tofile)
    except: lprint ('ERROR:  Unable to copy file '+fromfile); exit(1)     
def run (command, parameters):
    string = '"'+command+'" '+parameters
    if debug: logwrite (string)
    process = subprocess.Popen(string, env=my_env,
                  shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdout, stderr) = process.communicate()  
    if debug: logwrite (stdout)
    if debug: logwrite (stderr)    
    if process.returncode != 0: 
        lprint ('ERROR:  returned from "'+os.path.basename(command)+
                '", for details inspect logfile in debug mode')
        exit(1)
    return stdout 
def reset_NIFTI_header (filename):
    command=resourcedir+'fslorient'; checkcommand(command)
    parameters=' -deleteorient '+filename
    run(command,parameters)
    parameters=' -setqformcode 1 '+filename
    run(command,parameters)
    parameters=' -forceradiological '+filename
    run(command,parameters)
    # set image center
    parameters=' -getqform '+filename
    output = run(command, parameters).decode('ascii').rstrip('\n').split(' ')
    output[3] =str( Image_center_X*Image_Resolution_X)
    output[7] =str(-Image_center_Y*Image_Resolution_Y)
    output[11]=str(-Image_center_Z*Image_Resolution_Z)
    output = ' '.join(output)
    parameters=' -setqform '+output+' '+filename
    run(command, parameters)
    parameters=' -setsform '+output+' '+filename
    run(command, parameters)
def _get_from_SPAR (input, varstring):
    value = [text.split(':')[1] for text in input if text.split(':')[0].rstrip(' ')==varstring]
    if len(value)==1: value = value[0]
    else: lprint ('ERROR: unable to read parameter "'+varstring+'" in SPAR'); exit(1)
    return value
def _get_HDRvalue (input, varstring):
    value = [''.join(text.replace("\t"," ").split(' ')[1:]) for text in input if text.replace("\t"," ").split(' ')[0]==varstring]
    if len(value)==1: value = value[0]
    else: lprint ('ERROR: unable to read parameter "'+varstring+'" from NIFTI header'); exit(1)
    return value        
def isDICOM (file): # borrowed from linux' file command's magic pattern file
    try: f = open(file, "rb")
    except: lprint ('ERROR: opening file'), file; exit(1)
    try:
        test = f.read(128) # through the first 128 bytes away
        test = f.read(4) # this should be "DICM"
        f.close()
    except: return False # on error probably not a DICOM file
    if test.decode('ascii') == 'DICM': return True 
    else: return False
def _vax_to_ieee_single_float(data): # borrowed from the python VeSPA project
    #Converts a float in Vax format to IEEE format.
    #data should be a single string of chars that have been read in from 
    #a binary file. These will be processed 4 at a time into float values.
    #Thus the total number of byte/chars in the string should be divisible
    #by 4.
    #Based on VAX data organization in a byte file, we need to do a bunch of 
    #bitwise operations to separate out the numbers that correspond to the
    #sign, the exponent and the fraction portions of this floating point
    #number
    #role :      S        EEEEEEEE      FFFFFFF      FFFFFFFF      FFFFFFFF
    #bits :      1        2      9      10                               32
    #bytes :     byte2           byte1               byte4         byte3    
    f = []; nfloat = int(len(data) / 4)
    for i in range(nfloat):
        byte2 = data[0 + i*4]; byte1 = data[1 + i*4]
        byte4 = data[2 + i*4]; byte3 = data[3 + i*4]
        # hex 0x80 = binary mask 10000000
        # hex 0x7f = binary mask 01111111
        sign  =  (ord(byte1) & 0x80) >> 7
        expon = ((ord(byte1) & 0x7f) << 1 )  + ((ord(byte2) & 0x80 ) >> 7 )
        fract = ((ord(byte2) & 0x7f) << 16 ) +  (ord(byte3) << 8 ) + ord(byte4)
        if sign == 0: sign_mult = 1.0
        else: sign_mult = -1.0;
        if 0 < expon:
            # note 16777216.0 == 2^24  
            val = sign_mult * (0.5 + (fract/16777216.0)) * pow(2.0, expon - 128.0)   
            f.append(val)
        elif expon == 0 and sign == 0: f.append(0)
        else: f.append(0) # may want to raise an exception here ...
    return f        
def usage():
    lprint ('')
    lprint ('Usage: '+Program_name+' [options] --img=<inputimage> --spec=<inputspectro>')
    lprint ('')
    lprint ('   Available options are:')
    lprint ('       --outdir=<path> : output directory, if not specified')
    lprint ('                         output goes to current working directory')
    lprint ('       --noseg         : skip segmentation, only create the Spectro Box')
    lprint ('       -h --help       : usage and help')
    lprint ('       -d --debug      : debug mode, see help for details')
    lprint ('       --version       : version information')
    lprint ('')
def help():
    lprint ('')
    lprint ('Debug mode writes additional information and error messages to the logfile')
    lprint ('and outputs results without angulations/translations labeled "*Isocenter*"')
    lprint ('---- CAUTION: FINAL RESULTS ARE SLIGHTLY DIFFERENT FROM NORMAL MODE -----')
    lprint ('this is because in debug mode the spectro box transformation is done in two')
    lprint ('Separate steps: straigh->isocenter & isocenter->image space, which results in')
    lprint ('slight rounding errors, whereas in normal mode this is done in one single step')
    lprint ('')
    lprint ('')
    lprint ('The program can be called without --img and --spec options,')
    lprint ('in this case the files can be choosen interactively')
    lprint ('')
    lprint ('inputimage:   should be one multiframe (enhanced) DICOM file with a 3DT1 image,')
    lprint ('              the geometry tags in the DICOM header must preserved such that')
    lprint ('              during conversation to NIFTI format Cris Rorden\'s program dcm2nii') 
    lprint ('              can copy this information into the NIFTY header')
    lprint ('              alternatively this can be an already transformed NIFTI file')
    lprint ('              in this case it must be an axial in neurological orientation like')
    lprint ('              dcm2nii\'s reoriented output file (the one initialed with an "o")')    
    lprint ('              NIFTI input files must have .nii.gz or .nii extension')
    lprint ('')
    lprint ('inputspectro: a file containing the geometry information of the spectrum')
    lprint ('              in Philips SPAR format (basically a text file)')
    lprint ('              the following sections have to be present:')
    lprint ('                 ap_size : value with AP voxel size [mm]')
    lprint ('                 lr_size : value with LR voxel size [mm]')
    lprint ('                 cc_size : value with FH voxel size [mm]')
    lprint ('                 ap_off_center : value AP offcenter [mm]')
    lprint ('                 lr_off_center : value LR offcenter [mm]')
    lprint ('                 cc_off_center : value FH offcenter [mm]')
    lprint ('                 ap_angulation : value FH angulation [degrees, -45.0 to 45.0]')
    lprint ('                 lr_angulation : value LR angulation [degrees, -45.0 to 45.0]')
    lprint ('                 cc_angulation : value LR angulation [degrees, -45.0 to 45.0]')
    lprint ('')
         

# general initialization stuff   
debug=False; NIFTI_Input=False; SPAR_Input=True
Image_File=''; Spectro_File=''
space=' '; slash='/'; 
if sys.platform=="win32": slash='\\' # not really needed, but looks nicer ;)
Program_name = os.path.basename(sys.argv[0]); 
if Program_name.find('.')>0: Program_name = Program_name[:Program_name.find('.')]
basedir = os.getcwd()+slash # current working directory is the default output directory 
for arg in sys.argv[1:]: # look in command line arguments if the output directory specified
    if "--outdir" in arg: basedir = os.path.abspath(arg[arg.find('=')+1:])+slash #
ID = str(random.randrange(1000, 2000));ID=ID[:3] # create 3 digit random ID for logfile 
try: sys.stderr = open(basedir+Program_name+'.log', 'a'); # open logfile to append
except: print('Problem opening logfile: '+basedir+Program_name+'.log'); exit(2)
my_env = os.environ.copy(); my_env["FSLOUTPUTTYPE"] = "NIFTI" # set FSLOUTPUTTYPE=NIFTI
FNULL = open(os.devnull, 'w')
# catch signals to be able to cleanup temp files before exit
signal.signal(signal.SIGINT, signal_handler)  # keyboard interrupt
signal.signal(signal.SIGTERM, signal_handler) # kill/shutdown
if  'SIGHUP' in dir(signal): signal.signal(signal.SIGHUP, signal_handler)  # shell exit (linux)
# make tempdir
timestamp=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
tempname='.'+Program_name+'_temp'+timestamp
tempdir=basedir+tempname+slash
if os.path.isdir(tempdir): # this should never happen
    lprint ('ERROR:  Problem creating temp dir (already exists)'); exit(1) 
try: os.mkdir (tempdir)
except: lprint ('ERROR:  Problem creating temp dir: '+tempdir); exit(1) 

  
# configuration specific initializations
# compare python versions with e.g. if LooseVersion(python_version)>LooseVersion("2.7.6"):
python_version = str(sys.version_info[0])+'.'+str(sys.version_info[1])+'.'+str(sys.version_info[2])
# sys.platform = [linux2, win32, cygwin, darwin, os2, os2emx, riscos, atheos, freebsd7, freebsd8]
if sys.platform=="win32":
    os.system("title "+Program_name)
    try: resourcedir = sys._MEIPASS+slash # when on PyInstaller 
    except: # in plain python this is where the script was run from
        resourcedir = os.path.abspath(os.path.dirname(sys.argv[0]))+slash; 
    command='attrib'; parameters=' +H "'+tempdir[:len(tempdir)-1]+'"'; 
    run(command, parameters) # hide tempdir
    if pywin32_installed:
        try: # disable console windows close button (substitutes catch shell exit under linux)
            hwnd = win32console.GetConsoleWindow()
            hMenu = win32gui.GetSystemMenu(hwnd, False)
            win32gui.EnableMenuItem(hMenu, win32con.SC_CLOSE, win32con.MF_GRAYED) 
        except: pass #silent
else:
    try: fsldir = os.environ['FSLDIR']; 
    except: fsldir='/usr/local/fsl'; my_env["FSLDIR"] = fsldir # best guess
    resourcedir = os.path.abspath(fsldir+'/bin')+slash
    if not os.path.isdir(resourcedir): 
        print ('ERROR: FSL not found, ')
        print ('set the FSLDIR environment variable to point to the FSL installation directory\n')
        exit(2)
if TK_installed:        
    TKwindows = tk.Tk(); TKwindows.withdraw() #hiding tkinter window
    TKwindows.update()
    # the following tries to disable showing hidden files/folders under linux
    try: TKwindows.tk.call('tk_getOpenFile', '-foobarz')
    except: pass
    try: TKwindows.tk.call('namespace', 'import', '::tk::dialog::file::')
    except: pass
    try: TKwindows.tk.call('set', '::tk::dialog::file::showHiddenBtn', '1')
    except: pass
    try: TKwindows.tk.call('set', '::tk::dialog::file::showHiddenVar', '0')
    except: pass
    TKwindows.update()


# parse commandline parameters (if present)
try: opts, args =  getopt( sys.argv[1:],'hd',['help','version','debug','img=','spec=','outdir=','noseg'])
except:
    error=str(sys.argv[1:]).replace("[","").replace("]","")
    if "-" in str(error) and not "--" in str(error): 
          lprint ('ERROR: Commandline '+str(error)+',   maybe you mean "--"')
    else: lprint ('ERROR: Commandline '+str(error))
    usage(); exit(2)
if len(args)>0: 
    lprint ('ERROR: Commandline option "'+args[0]+'" not recognized')
    lprint ('       (see logfile for details)')
    logwrite ('       Calling parameters: '+str(sys.argv[1:]).replace("[","").replace("]",""))
    usage(); exit(2)  
argDict = dict(opts)
if "--outdir" in argDict and not [True for arg in sys.argv[1:] if "--outdir" in arg]:
    # "--outdir" must be spelled out, getopt also excepts substrings (e.g. "--outd"), but
    # my simple pre-initialization code to get basedir early doesn't
    lprint ('ERROR: Commandline option "--outdir" must be spelled out')
    usage(); exit(2)
if '-h' in argDict: usage(); help(); exit(0)   
if '--help' in argDict: usage(); help(); exit(0)  
if '-d' in argDict: debug = True  
if '--debug' in argDict: debug = True   
if '--version' in argDict: lprint (Program_name+' '+Program_version); exit(0)
if '--img' in argDict: Image_File=argDict['--img']; checkfile(Image_File)
if '--spec' in argDict: Spectro_File=argDict['--spec']; checkfile(Spectro_File)
if '--noseg' in argDict: nosegmentation=True
else: nosegmentation=False


# ----- start to really do something -----
lprint ('Starting   Spectro Compartment Segmentation - '+Program_name+' '+Program_version)
logwrite ('Calling sequence    '+' '.join(sys.argv))
logwrite ('OS & Python version '+sys.platform+' '+python_version)
logwrite ('tkinter & pydicom   '+str(TK_installed)+' '+str(pydicom_installed))

Interactive = False
# Interactive Input
if TK_installed:
    # Choose Image file
    if Image_File == "" and not NIFTI_Input: # use interactive input if not in commandline
        Image_File = askopenfilename(title="Choose Image file")
        if Image_File == "": lprint ('ERROR:  No Image input file specified'); exit(2)
        Interactive = True
    TKwindows.update()
    # Choose Spectro file
    if Spectro_File == "": # use interactive input if not specified in commandline
        Spectro_File = askopenfilename(title="Choose Spectro file")
        if Spectro_File == "": lprint ('ERROR:  No Spectro input file specified'); exit(2)
        Interactive = True
    TKwindows.update()    
else:
    if Image_File == "": 
        lprint ('ERROR:  No Image input file specified');
        lprint ('        to interactively choose input files you need tkinter')
        lprint ('        on Linux try "yum install tkinter"')
        lprint ('        on MacOS install ActiveTcl from:')
        lprint ('        http://www.activestate.com/activetcl/downloads')
        usage()
        exit(2)
    if Spectro_File == "": 
        lprint ('ERROR:  No Spectro input file specified')
        lprint ('        to interactively choose input files you need tkinter')
        lprint ('        on Linux try "yum install tkinter"')
        lprint ('        on MacOS install ActiveTcl from:')
        lprint ('        http://www.activestate.com/activetcl/downloads')  
        usage()
        exit(2)
Image_File = os.path.abspath(Image_File) 
Spectro_File = os.path.abspath(Spectro_File)       
# auto detect NIFTI by filename extension
extension = os.path.basename(Image_File); 
extension = extension[extension.find('.'):].lower()
if extension=='.nii.gz' or extension=='.nii': NIFTI_Input=True
if debug:
    if NIFTI_Input: logwrite ('Using NIFTI File at '+Image_File)
    else: logwrite ('Using Image File at '+Image_File)


# try correct accidental SDAT choice
if os.path.splitext(Spectro_File)[1] == '.SDAT': 
    Spectro_File=os.path.splitext(Spectro_File)[0]+'.SPAR'
# detect SPAR by filename extension
extension = os.path.splitext(Spectro_File)[1]
if not extension.lower()=='.spar': SPAR_Input=False
if debug:
    if SPAR_Input: logwrite ('Using SPAR spectro  '+Spectro_File)
    else: logwrite ('Using Spectro File  '+Spectro_File)
    logwrite ('All output goes to  '+basedir)
if SPAR_Input: # read spectro orientation from SPAR
    try: input = open(Spectro_File, "r").readlines()
    except: lprint ('ERROR: reading SPAR file'); exit(1)
    Spectro_AP_size = float(_get_from_SPAR(input,'ap_size')) 
    Spectro_LR_size = float(_get_from_SPAR(input,'lr_size'))
    Spectro_FH_size = float(_get_from_SPAR(input,'cc_size'))
    Spectro_AP_offset = float(_get_from_SPAR(input,'ap_off_center'))
    Spectro_LR_offset = float(_get_from_SPAR(input,'lr_off_center'))
    Spectro_FH_offset = float(_get_from_SPAR(input,'cc_off_center'))
    Spectro_AP_rot = float(_get_from_SPAR(input,'ap_angulation'))
    Spectro_LR_rot = float(_get_from_SPAR(input,'lr_angulation'))
    Spectro_FH_rot = float(_get_from_SPAR(input,'cc_angulation'))
else: #try to read spectro orientation from DICOM
    if not isDICOM(Spectro_File): lprint ('ERROR:  specified spectro file is not DICOM'); exit(2)
    if not pydicom_installed: 
        lprint ('ERROR:  Spectro file seems to be in DICOM format but pydicom is not installed ')
        lprint ('        see http://pydicom.readthedocs.io/en/stable/getting_started.html')
        lprint ('        or simply try "yum install python-pip" then "pip install pydicom"')
        exit(2)
    try: Dset = dicom.read_file(Spectro_File)
    except: lprint ('ERROR:  Problem reading DICOM spectro file'); exit(2)
    # some checks
    try: Modality=str(Dset.Modality) # must be MR           
    except: lprint ('ERROR:  Unable to determine DICOM Modality'); exit(1)
    if Modality!='MR': lprint ('DICOM Modality not MR'); exit(1)
    try: Manufacturer=str(Dset.Manufacturer) # currently Philips only
    except: lprint ('ERROR:  Unable to determine Manufacturer'); exit(1)
    if not Manufacturer.find("Philips")>=0: 
        lprint ('ERROR:  Currently only Philips DICOM implemented'); exit(1)
    try: ImageType=str(Dset.ImageType) # sanity check: spectroscopy   
    except: 
        lprint ('ERROR:  Unable to determine if DICOM contains spectroscopy data');exit(1)
    if not ImageType.find("SPECTROSCOPY")>=0: 
        lprint ('ERROR:  DICOM file does not contain spectroscopy data'); exit(1)
    # try to get data out
    i=0
    try: Spectro_AP_rot=float(Dset[0x2005,0x1085][0][0x2005,0x1054].value); i=i+1
    except: lprint ('ERROR:  Unable to extract geometry data from DICOM'); exit(1)
    try: Spectro_FH_rot=float(Dset[0x2005,0x1085][0][0x2005,0x1055].value); i=i+1
    except: lprint ('ERROR:  Unable to extract geometry data from DICOM'); exit(1)
    try: Spectro_LR_rot=float(Dset[0x2005,0x1085][0][0x2005,0x1056].value); i=i+1
    except: lprint ('ERROR:  Unable to extract geometry data from DICOM'); exit(1)
    try: Spectro_AP_size=float(Dset[0x2005,0x1085][0][0x2005,0x1057].value); i=i+1
    except: lprint ('ERROR:  Unable to extract geometry data from DICOM'); exit(1)
    try: Spectro_FH_size=float(Dset[0x2005,0x1085][0][0x2005,0x1058].value); i=i+1
    except: lprint ('ERROR:  Unable to extract geometry data from DICOM'); exit(1)
    try: Spectro_LR_size=float(Dset[0x2005,0x1085][0][0x2005,0x1059].value); i=i+1
    except: lprint ('ERROR:  Unable to extract geometry data from DICOM'); exit(1)
    try: Spectro_AP_offset=float(Dset[0x2005,0x1085][0][0x2005,0x105A].value); i=i+1
    except: lprint ('ERROR:  Unable to extract geometry data from DICOM'); exit(1)
    try: Spectro_FH_offset=float(Dset[0x2005,0x1085][0][0x2005,0x105B].value); i=i+1
    except: lprint ('ERROR:  Unable to extract geometry data from DICOM'); exit(1)
    try: Spectro_LR_offset=float(Dset[0x2005,0x1085][0][0x2005,0x105C].value); i=i+1
    except: lprint ('ERROR:  Unable to extract geometry data from DICOM'); exit(1)  
    if i!=9: lprint ('ERROR:  Unable to extract all geometry data from DICOM'); exit(1) 
# write found geometry to logfile
if debug:    
    logwrite ('Found Spectro Voxel size       (AP/LR/FH) = '
           +str(Spectro_AP_size)+' / '+ str(Spectro_LR_size)+' / '+str(Spectro_FH_size))
    logwrite ('Found Spectro Voxel offset     (AP/LR/FH) = '
           +str(Spectro_AP_offset)+' / '+ str(Spectro_LR_offset)+' / '+str(Spectro_FH_offset))
    logwrite ('Found Spectro Voxel angulation (AP/LR/FH) = '
           +str(Spectro_AP_rot)+' / '+ str(Spectro_LR_rot)+' / '+str(Spectro_FH_rot))
#twiddling with the spectro geometry to get results correct
Spectro_AP_offset = -Spectro_AP_offset # AP swap (duno why) 
Spectro_LR_rot = -Spectro_LR_rot       # AP swap (duno why)
Spectro_FH_rot = -Spectro_FH_rot       # AP swap (duno why)
Spectro_LR_offset = -Spectro_LR_offset # LR swap, spectro = radiological, dcm2nii -> neurological
Spectro_AP_rot = -Spectro_AP_rot       # LR swap, spectro = radiological, dcm2nii -> neurological
Spectro_FH_rot = -Spectro_FH_rot       # LR swap, spectro = radiological, dcm2nii -> neurological
Spectro_LR_rot = -Spectro_LR_rot       # whoo, yet another problem (duno why) 
Spectro_FH_rot = -Spectro_FH_rot       # whoo, yet another problem (duno why) 

# ----- transform DICOM 2 NIFTI (uses dcm2nii) -----
if not NIFTI_Input:
    lprint ('Converting DICOM Image to NIFTI')
    # copy DICOM file to tempdir
    try: shutil.copy2(Image_File, tempdir)
    except: lprint ('ERROR:  Problem copying DICOM File '); exit(1)
    # convert DICOM file to NIFTI
    command=resourcedir+'dcm2nii'; checkcommand(command)    
    parameters  = ' -4 Y -3 N -a Y -c Y -d N -e N -f Y -g N -i N -k 0 -l N'
    parameters += ' -m N -n Y -p N -r Y -t N -v Y -x N "'+tempdir+'"'
    run(command, parameters)
    # dcm2nii "o" files are in neurological orientation
    # switch to radiological
    command=resourcedir+'fslswapdim'; checkcommand(command)
    filename='o'+os.path.basename(os.path.splitext(Image_File)[0])+'.nii'
    parameters=' "'+tempdir+filename+'" -x y z "'+tempdir+'T1.nii"'
    run(command,parameters)
    delete(tempdir+os.path.basename(os.path.splitext(Image_File)[0])+'.nii') #delete unused file
    delete(tempdir+'co'+os.path.basename(os.path.splitext(Image_File)[0])+'.nii') #delete unused
else: 
    # switch to radiological
    command=resourcedir+'fslswapdim'; checkcommand(command)
    parameters=' "'+Image_File+'" -x y z "'+tempdir+'T1.nii"'
    run(command,parameters)
# ----- check NIFTI file (neurological axial required) -----
if not os.path.isfile(tempdir+'T1.nii'): lprint ('ERROR:  NIFTI file not found '); exit(1)
command=resourcedir+'fslhd'; checkcommand(command)
parameters=' "'+tempdir+'T1.nii"'
output = run(command,parameters).decode('ascii')
output = output.replace("\t"," ")
output = " ".join(output.split())
if not 'qform_name Scanner Anat' in output: 
    lprint ('ERROR:  could not locate NIFTI information confirming neurological axial'); exit(1)
if not 'qform_xorient Left-to-Right' in output: 
    lprint ('ERROR:  could not locate NIFTI information confirming neurological axial'); exit(1)
if not 'qform_yorient Posterior-to-Anterior' in output: 
    lprint ('ERROR:  could not locate NIFTI information confirming neurological axial'); exit(1)
if not 'qform_zorient Inferior-to-Superior' in output: 
    lprint ('ERROR:  could not locate NIFTI information confirming neurological axial'); exit(1)
if not 'sform_name Scanner Anat' in output: 
    lprint ('ERROR:  could not locate NIFTI information confirming neurological axial'); exit(1)
if not 'sform_xorient Left-to-Right' in output: 
    lprint ('ERROR:  could not locate NIFTI information confirming neurological axial'); exit(1)
if not 'sform_yorient Posterior-to-Anterior' in output: 
    lprint ('ERROR:  could not locate NIFTI information confirming neurological axial'); exit(1)
if not 'sform_zorient Inferior-to-Superior' in output: 
    lprint ('ERROR:  could not locate NIFTI information confirming neurological axial'); exit(1)

# ----- extract Image transformations -----
lprint ('Extracting transformation matrix from Image')
command=resourcedir+'fslorient'; checkcommand(command)
parameters=' -getqform "'+tempdir+'T1.nii"'
output = run(command, parameters).decode('ascii').split(' ')
if len(output)!=17: lprint ('ERROR:  Problem reading qform form NIFTI '); exit(1)
f = open(tempdir+'temp1.txt', 'w') # this matrix still contains scalings
f.write(output[0]+space+output[1]+space+output[2]+space+output[3]+'\n') 
f.write(output[4]+space+output[5]+space+output[6]+space+output[7]+'\n')
f.write(output[8]+space+output[9]+space+output[10]+space+output[11]+'\n')
f.write(output[12]+space+output[13]+space+output[14]+space+output[15]+'\n')
f.close()
# this isolates the rotations/translations only, without the scalings (data is in lines 1-4)
command=resourcedir+'avscale'; checkcommand(command)
parameters=' "'+tempdir+'temp1.txt"'
output = run(command, parameters).decode('ascii').split('\n')
f = open(tempdir+'ImageTransform_raw.mat', 'w')
f.write(output[1]+'\n') 
f.write(output[2]+'\n')
f.write(output[3]+'\n')
f.write(output[4]+'\n')
f.close()
# get image dimensions
command=resourcedir+'fslhd'; checkcommand(command)
parameters=' "'+tempdir+'T1.nii"'
output = run(command,parameters).decode('ascii').split('\n')
Image_size_X = int(_get_HDRvalue(output,'dim1'))
Image_size_Y = int(_get_HDRvalue(output,'dim2'))
Image_size_Z = int(_get_HDRvalue(output,'dim3'))
Image_Resolution_X = float(_get_HDRvalue(output,'pixdim1'))
Image_Resolution_Y = float(_get_HDRvalue(output,'pixdim2'))
Image_Resolution_Z = float(_get_HDRvalue(output,'pixdim3'))
Image_center_X = int(Image_size_X/2)
Image_center_Y = int(Image_size_Y/2)
Image_center_Z = int(Image_size_Z/2)
# write translation matrices image_center <--> FSL_rotation_center (cubes corner)
f = open(tempdir+'TranslImageOrigin.mat', 'w')
f.write('1 0 0 '+str(-Image_center_X*Image_Resolution_X)+'\n') # in mm
f.write('0 1 0 '+str(-Image_center_Y*Image_Resolution_Y)+'\n') # in mm
f.write('0 0 1 '+str(-Image_center_Z*Image_Resolution_Z)+'\n') # in mm
f.write('0 0 0 1\n')
f.close()
f = open(tempdir+'TranslImageOrigin_Inv.mat', 'w')
f.write('1 0 0 '+str(Image_center_X*Image_Resolution_X)+'\n') # in mm
f.write('0 1 0 '+str(Image_center_Y*Image_Resolution_Y)+'\n') # in mm
f.write('0 0 1 '+str(Image_center_Z*Image_Resolution_Z)+'\n') # in mm
f.write('0 0 0 1\n')
f.close()  
# concat the image transformations
command=resourcedir+'convert_xfm'; checkcommand(command)
parameters=' -omat "'+tempdir+'Image2Isocenter.mat"'
parameters+=' -concat "'+tempdir+'TranslImageOrigin_Inv.mat"'
parameters+=' "'+tempdir+'ImageTransform_raw.mat"'
run(command,parameters)  
# invert the final transformation
command=resourcedir+'convert_xfm'; checkcommand(command)
parameters=' -omat "'+tempdir+'Isocenter2Image.mat"'
parameters+=' -inverse "'+tempdir+'Image2Isocenter.mat"'
run(command,parameters)     
# apply transformation (debug mode only)
if debug:
   print ('Applying   transformation matrix to NIFTI')
   command=resourcedir+'flirt'; checkcommand(command)
   parameters=' -in "'+tempdir+'T1.nii" -ref "'+tempdir+'T1.nii"'
   parameters+=' -out "'+tempdir+'T1_Isocenter.nii"'
   parameters+=' -init "'+tempdir+'Image2Isocenter.mat" -applyxfm'
   run(command,parameters)

# ----- extract Spectrum transformations -----
lprint ('Extracting transformation matrix from Spectrum')
d2r = math.pi/180. # degree to rad conversion
f = open(tempdir+'SpectroRotationLR_raw.mat', 'w') #Spectro X rotation (raw)
f.write('1 0 0 0\n')
f.write('0 '+str( math.cos(Spectro_LR_rot*d2r))+' '+str(math.sin(Spectro_LR_rot*d2r))+' 0 \n')
f.write('0 '+str(-math.sin(Spectro_LR_rot*d2r))+' '+str(math.cos(Spectro_LR_rot*d2r))+' 0 \n')
f.write('0 0 0 1\n')
f.close()
f = open(tempdir+'SpectroRotationAP_raw.mat', 'w') #Spectro Y rotation (raw)
f.write(str( math.cos(Spectro_AP_rot*d2r))+' 0 '+str(math.sin(Spectro_AP_rot*d2r))+' 0 \n')
f.write('0 1 0 0\n')
f.write(str(-math.sin(Spectro_AP_rot*d2r))+' 0 '+str(math.cos(Spectro_AP_rot*d2r))+' 0 \n')
f.write('0 0 0 1\n')
f.close()
f = open(tempdir+'SpectroRotationFH_raw.mat', 'w') #Spectro Z rotation (raw)
f.write(str( math.cos(Spectro_FH_rot*d2r))+' '+str(math.sin(Spectro_FH_rot*d2r))+' 0 0 \n')
f.write(str(-math.sin(Spectro_FH_rot*d2r))+' '+str(math.cos(Spectro_FH_rot*d2r))+' 0 0 \n')
f.write('0 0 1 0\n')
f.write('0 0 0 1\n')
f.close()
#X
command=resourcedir+'convert_xfm'; checkcommand(command)
parameters=' -omat "'+tempdir+'temp.mat"'
parameters+=' -concat "'+tempdir+'SpectroRotationLR_raw.mat"'
parameters+=' "'+tempdir+'TranslImageOrigin.mat"'
run(command,parameters)
parameters=' -omat "'+tempdir+'SpectroRotationLR.mat"'
parameters+=' -concat "'+tempdir+'TranslImageOrigin_Inv.mat"'
parameters+=' "'+tempdir+'temp.mat"'
run(command,parameters)
#Y
command=resourcedir+'convert_xfm'; checkcommand(command)
parameters=' -omat "'+tempdir+'temp.mat"'
parameters+=' -concat "'+tempdir+'SpectroRotationAP_raw.mat"'
parameters+=' "'+tempdir+'TranslImageOrigin.mat"'
run(command,parameters)
parameters=' -omat "'+tempdir+'SpectroRotationAP.mat"'
parameters+=' -concat "'+tempdir+'TranslImageOrigin_Inv.mat"'
parameters+=' "'+tempdir+'temp.mat"'
run(command,parameters)
#Z
command=resourcedir+'convert_xfm'; checkcommand(command)
parameters=' -omat "'+tempdir+'temp.mat"'
parameters+=' -concat "'+tempdir+'SpectroRotationFH_raw.mat"'
parameters+=' "'+tempdir+'TranslImageOrigin.mat"'
run(command,parameters)
parameters=' -omat "'+tempdir+'SpectroRotationFH.mat"'
parameters+=' -concat "'+tempdir+'TranslImageOrigin_Inv.mat"'
parameters+=' "'+tempdir+'temp.mat"'
run(command,parameters)
#XYZ
command=resourcedir+'convert_xfm'; checkcommand(command)
parameters=' -omat "'+tempdir+'temp.mat"'
parameters+=' -concat "'+tempdir+'SpectroRotationAP.mat"'
parameters+=' "'+tempdir+'SpectroRotationLR.mat"'
run(command,parameters)
parameters=' -omat "'+tempdir+'SpectroRotation.mat"'
parameters+=' -concat "'+tempdir+'SpectroRotationFH.mat"'
parameters+=' "'+tempdir+'temp.mat"'
run(command,parameters)
#Spectro Translation
f = open(tempdir+'SpectroTranslation.mat', 'w')
f.write('1 0 0 '+str(Spectro_LR_offset)+'\n') #in mm
f.write('0 1 0 '+str(Spectro_AP_offset)+'\n') #in mm
f.write('0 0 1 '+str(Spectro_FH_offset)+'\n') #in mm
f.write('0 0 0 1\n')
f.close()
#Spectro Transformation: all rotations and translations
command=resourcedir+'convert_xfm'; checkcommand(command)
parameters=' -omat "'+tempdir+'SpectroTransformation.mat"'
parameters+=' -concat "'+tempdir+'SpectroTranslation.mat"'
parameters+=' "'+tempdir+'SpectroRotation.mat"'
run(command,parameters) 

# ----- generate Spectrum BOX -----
lprint ('Generating Spectro BOX')
#make a box at image origin
Xsize = int(Spectro_LR_size/Image_Resolution_X); sXsize = str(Xsize)
Ysize = int(Spectro_AP_size/Image_Resolution_Y); sYsize = str(Ysize)
Zsize = int(Spectro_FH_size/Image_Resolution_Z); sZsize = str(Zsize)
Xmin  = int(Image_center_X - Xsize/2); sXmin = str(Xmin)
Ymin  = int(Image_center_Y - Ysize/2); sYmin = str(Ymin)
Zmin  = int(Image_center_Z - Zsize/2); sZmin = str(Zmin)
command=resourcedir+'fslmaths'; checkcommand(command)
parameters=' "'+tempdir+'T1.nii" -mul 0 -add 1 -roi '
parameters+=sXmin+space+sXsize+space+sYmin+space+sYsize+space+sZmin+space+sZsize
parameters+=' 0 1 "'+tempdir+'SpectroBOX_straight.nii" -odt float '
run(command,parameters)
if debug:    
    # apply spectro transformation to isocenter 
    command=resourcedir+'flirt'; checkcommand(command)
    parameters=' -in "'+tempdir+'SpectroBOX_straight.nii"'
    parameters+=' -ref "'+tempdir+'SpectroBOX_straight.nii"'
    parameters+=' -out "'+tempdir+'SpectroBOX_Isocenter_raw.nii"'
    parameters+=' -init "'+tempdir+'SpectroTransformation.mat" -applyxfm '
    run(command,parameters)      
    # bin result
    command=resourcedir+'fslmaths'; checkcommand(command)
    parameters=' "'+tempdir+'SpectroBOX_Isocenter_raw.nii"'
    parameters+=' -bin "'+tempdir+'SpectroBOX_Isocenter.nii" -odt char'
    run(command,parameters)     
    # apply spectro transformation from isocenter to image space (inverse image transformation)
    command=resourcedir+'flirt'; checkcommand(command)
    parameters=' -in "'+tempdir+'SpectroBOX_Isocenter_raw.nii"'
    parameters+=' -ref "'+tempdir+'SpectroBOX_Isocenter_raw.nii"'
    parameters+=' -out "'+tempdir+'SpectroBOX_raw.nii"'
    parameters+=' -init "'+tempdir+'Isocenter2Image.mat" -applyxfm '
    run(command,parameters)
else:    
   # concat SpectroTransformation.mat & Isocenter2Image.mat
    command=resourcedir+'convert_xfm'; checkcommand(command)
    parameters=' -omat "'+tempdir+'Spectro2ImageTransformation.mat"'
    parameters+=' -concat "'+tempdir+'Isocenter2Image.mat"'
    parameters+=' "'+tempdir+'SpectroTransformation.mat"'
    run(command,parameters) 
    command=resourcedir+'flirt'; checkcommand(command)
    parameters=' -in "'+tempdir+'SpectroBOX_straight.nii"'
    parameters+=' -ref "'+tempdir+'SpectroBOX_straight.nii"'
    parameters+=' -out "'+tempdir+'SpectroBOX_raw.nii"'
    parameters+=' -init "'+tempdir+'Spectro2ImageTransformation.mat" -applyxfm '
    run(command,parameters) 
# bin result
command=resourcedir+'fslmaths'; checkcommand(command)
parameters=' "'+tempdir+'SpectroBOX_raw.nii" -bin "'+tempdir+'SpectroBOX.nii" -odt char'
run(command,parameters)    
# clean up NIFTI header
reset_NIFTI_header ('"'+tempdir+'T1.nii"')
reset_NIFTI_header ('"'+tempdir+'SpectroBOX.nii"')
if debug: 
    reset_NIFTI_header ('"'+tempdir+'T1_Isocenter.nii"')
    reset_NIFTI_header ('"'+tempdir+'SpectroBOX_Isocenter.nii"')


# ----- segmentation -----
if not nosegmentation:
    lprint ('Running    Segmentation')
    if sys.platform=="win32": # from here on things go differently for a while
        # the FAST segmentation tool under windows doesn't like NIFTI, so first transform to Analyze
        #os.environ["FSLOUTPUTTYPE"] = "ANALYZE" # set FSLOUTPUTTYPE=ANALYZE
        my_env = os.environ.copy(); my_env["FSLOUTPUTTYPE"] = "ANALYZE" # set FSLOUTPUTTYPE=ANALYZE
        # convert Image to ANALYZE
        command=resourcedir+'dcm2nii'; checkcommand(command)
        parameters=' -n N -s Y -m N "'+tempdir+'T1.nii"'
        run(command,parameters)          
        # Brain Extraction BET2 
        command=resourcedir+'bet2'; checkcommand(command)
        parameters=' "'+tempdir+'fT1.hdr" "'+tempdir+'T1_BET"'
        run(command,parameters)      
        # Segmentation  (windows version only works with analyze images)
        command=resourcedir+'fast'; checkcommand(command)
        # see conversion table at the end of https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FAST
        parameters=' -v0 -n -e -ov -b 0.1 -l 20 -i 4 --p "'+tempdir+'T1_BET.img"'
        run(command,parameters)    
        # transform ANALYZE results back to NIFTI
        lprint ('Measuring  Compartments')
        command=resourcedir+'dcm2nii'; checkcommand(command)
        parameters=' -n Y -m N -g N "'+tempdir+'T1_bet_pve_0.img"'
        run(command,parameters)
        parameters=' -n Y -m N -g N "'+tempdir+'T1_bet_pve_1.img"'
        run(command,parameters)
        parameters=' -n Y -m N -g N "'+tempdir+'T1_bet_pve_2.img"'
        run(command,parameters)
        #rename files
        rename(tempdir+'fT1_bet_pve_0.nii', tempdir+'T1_CSF.nii')
        rename(tempdir+'fT1_bet_pve_1.nii', tempdir+'T1_GM.nii')
        rename(tempdir+'fT1_bet_pve_2.nii', tempdir+'T1_WM.nii')
    else: # FSL v5 on linux
        # Brain Extraction BET2 
        command=resourcedir+'bet2'; checkcommand(command)
        parameters=' "'+tempdir+'T1.nii" "'+tempdir+'T1_BET.nii"'
        run(command,parameters)      
        # Segmentation  (windows version only works with analyze images)
        command=resourcedir+'fast'; checkcommand(command)
        parameters=' "'+tempdir+'T1_BET.nii"' # no option switches default is OK in FSL v5
        run(command,parameters)
        #rename files
        rename(tempdir+'T1_BET_pve_0.nii', tempdir+'T1_CSF.nii')
        rename(tempdir+'T1_BET_pve_1.nii', tempdir+'T1_GM.nii')
        rename(tempdir+'T1_BET_pve_2.nii', tempdir+'T1_WM.nii')
    # now we are back identical for both systems
    # clean up NIFTI header 
    reset_NIFTI_header ('"'+tempdir+'T1_CSF.nii"')
    reset_NIFTI_header ('"'+tempdir+'T1_GM.nii"')
    reset_NIFTI_header ('"'+tempdir+'T1_WM.nii"')

 
    # Extracting values
    command=resourcedir+'fslmeants'; checkcommand(command)
    parameters=' -i "'+tempdir+'T1_CSF.nii" -m "'+tempdir+'SpectroBOX.nii"'
    output = run(command,parameters).decode('ascii').split(' ')
    CSF_frac=float(output[0])
    parameters=' -i "'+tempdir+'T1_GM.nii" -m "'+tempdir+'SpectroBOX.nii"'
    output = run(command,parameters).decode('ascii').split(' ')
    GM_frac=float(output[0])
    parameters=' -i "'+tempdir+'T1_WM.nii" -m "'+tempdir+'SpectroBOX.nii"'
    output = run(command,parameters).decode('ascii').split(' ')
    WM_frac=float(output[0])
    # normalize sum to 1.0 (raw outputs are always around 0.985, duno why)
    total=CSF_frac+GM_frac+WM_frac
    CSF_frac = CSF_frac/total
    GM_frac = GM_frac/total
    WM_frac = WM_frac/total
    # calculate correction factor
    # Water Conc. = F(GM)*43300mM + F(WM)*35880mM + F(CSF)*55556mM / (1-F(CFS))
    # http://s-provencher.com/pub/LCModel/manual/manual.pdf (page 131)
    WCONC =  (GM_frac*43300. + WM_frac*35880. + CSF_frac*55556.)/(1.-CSF_frac)
    WCONC = str(int(WCONC))
    CSF_frac = "%.6f" % CSF_frac
    GM_frac  = "%.6f" % GM_frac
    WM_frac  = "%.6f" % WM_frac

    #write Results
    lprint ('   CSF:   '+str(CSF_frac))
    lprint ('   GM:    '+str(GM_frac))
    lprint ('   WM:    '+str(WM_frac))
    lprint ('WCONC:    '+str(WCONC))
    f = open(tempdir+Program_name+'_Results.txt', 'w')
    f.write(Program_name+space+Program_version+' Results:\n')
    f.write('CSF \tGM \tWM \tWCONC \tImage_File \tSpectro_File \tbasedir\n')  
    f.write(str(CSF_frac)+' \t')
    f.write(str(GM_frac)+' \t')
    f.write(str(WM_frac)+' \t')
    f.write(str(WCONC)+' \t')
    f.write(Image_File+' \t')
    f.write(Spectro_File+' \t')
    f.write(basedir+' \n') 
    f.close()

try: 
    MRSpeCS_Report(tempdir+'T1.nii', tempdir+'SpectroBOX.nii', tempdir+Program_name+'_Results.txt' , tempdir+Program_name+"_Report.pdf")
    lprint ("PDF report generated")
except: lprint ("PDF report generation failed")

# name collision detection
stp=''
if os.path.isfile(basedir+'T1.nii'): stp=timestamp+ID+'_' 
if os.path.isfile(basedir+'SpectroBOX.nii'): stp=timestamp+ID+'_'
if os.path.isfile(basedir+'T1_Isocenter.nii'): stp=timestamp+ID+'_'
if os.path.isfile(basedir+'SpectroBOX_Isocenter.nii'): stp=timestamp+ID+'_'
if os.path.isfile(basedir+'T1_CSF.nii'): stp=timestamp+ID+'_'
if os.path.isfile(basedir+'T1_GM.nii'): stp=timestamp+ID+'_'
if os.path.isfile(basedir+'T1_WM.nii'): stp=timestamp+ID+'_'
if os.path.isfile(basedir+Program_name+'_Results.txt'): stp=timestamp+ID+'_'
if os.path.isfile(basedir+Program_name+'_Report.pdf'): stp=timestamp+ID+'_'
# get output results
copy (tempdir+'T1.nii', basedir+stp+'T1.nii')
copy (tempdir+'SpectroBOX.nii', basedir+stp+'SpectroBOX.nii')
copy (tempdir+Program_name+"_Report.pdf", basedir+stp+Program_name+'_Report.pdf')
if debug: 
    copy(tempdir+'T1_Isocenter.nii', basedir+stp+'T1_Isocenter.nii')
    copy(tempdir+'SpectroBOX_Isocenter.nii', basedir+stp+'SpectroBOX_Isocenter.nii')
if not nosegmentation:
    copy(tempdir+'T1_CSF.nii', basedir+stp+'T1_CSF.nii')
    copy(tempdir+'T1_GM.nii', basedir+stp+'T1_GM.nii')
    copy(tempdir+'T1_WM.nii', basedir+stp+'T1_WM.nii')
    copy(tempdir+Program_name+'_Results.txt', basedir+stp+Program_name+'_Results.txt')
        

#delete tempdir
try: shutil.rmtree(tempdir)
except: pass # silent
lprint ('done\n')
sys.stderr.close() # close logfile

if pywin32_installed:
    try: # reenable console windows close button (useful if called command line or batch file)
        hwnd = win32console.GetConsoleWindow()
        hMenu = win32gui.GetSystemMenu(hwnd, 1)
        win32gui.DeleteMenu(hMenu, win32con.SC_CLOSE, win32con.MF_BYCOMMAND)
    except: pass #silent
if Interactive:
    if sys.platform=="win32": os.system("pause") # windows
    else: 
        #os.system('read -s -n 1 -p "Press any key to continue...\n"')
        import termios
        print("Press any key to continue...")
        fd = sys.stdin.fileno()
        oldterm = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)
        try: result = sys.stdin.read(1)
        except IOError: pass
        finally: termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
