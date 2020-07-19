#!/usr/local/fsl/fslpython/bin/python3
#
# requests a T1 NIFTI image that previousely was used for HippoDeep processing
# reads the Hippodeep output file *_mask_L.nii.gz, *_mask_R.nii.gz and *_hippoLR_volumes.csv
# and gebnerates a PDF report file
#
# ----- VERSION HISTORY -----
#
# Version 0.1 - 10, July 2020
#       - 1st public github Release
#
# ----- LICENSE -----                 
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#    For more detail see the GNU General Public License.
#    <http://www.gnu.org/licenses/>.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#    THE SOFTWARE.
#
# ----- REQUIREMENTS ----- 
#
#    This program was developed under Python Version 3.7
#    with the following additional libraries: 
#    - numpy
#    - nibabel
#    - pillow
#    - fpdf2 (aka PyFPDF)
#      also works with fpdf (versions<2) using temprary PDF files on disk
#
# OBS: For Output Language customization edit the first line in the .csv file
#

from __future__ import print_function
try: import win32gui, win32console
except: pass #silent
from math import floor
import sys
import os
import csv
from io import BytesIO
import numpy as np
import nibabel as nib
from PIL import Image
from fpdf import FPDF
from fpdf import __version__ as fpdf_version



def MRSpeCS_Report(T1_filename, Spectro_filename, Results_filename, PDF_filename):
    
    #define some color lookup tables    
        
    lut_gray = np.zeros ([256,3], dtype=np.uint8)
    lut_gray  [:,0] = np.linspace(0, 255, num=256, endpoint=True)
    lut_gray  [:,1] = lut_gray  [:,0]
    lut_gray  [:,2] = lut_gray  [:,0]
    lut_gray = lut_gray.astype(np.uint8)

    lut_red  = np.zeros ([256,3], dtype=np.uint8)
    lut_red [:,0] = np.linspace(0, 255, num=256, endpoint=True)
    lut_red = lut_red.astype(np.uint8)

    lut_green = np.zeros ([256,3], dtype=np.uint8)
    lut_green[:,1] = np.linspace(0, 255, num=256, endpoint=True)
    lut_green = lut_green.astype(np.uint8)

    lut_blue = np.zeros ([256,3], dtype=np.uint8)
    lut_blue[:,2] = np.linspace(0, 255, num=256, endpoint=True)
    lut_blue = lut_blue.astype(np.uint8)

    lut_yellow  = np.zeros ([256,3], dtype=np.uint8)
    lut_yellow [:,0] = np.linspace(0, 255, num=256, endpoint=True)
    lut_yellow [:,1] = lut_yellow [:,0]
    lut_yellow = lut_yellow.astype(np.uint8)

    lut_magenta = np.zeros ([256,3], dtype=np.uint8)
    lut_magenta [:,0] = np.linspace(0, 255, num=256, endpoint=True)
    lut_magenta [:,2] = lut_magenta [:,0]
    lut_magenta = lut_magenta.astype(np.uint8)

    lut_cyan = np.zeros ([256,3], dtype=np.uint8)
    lut_cyan [:,1] = np.linspace(0, 255, num=256, endpoint=True)
    lut_cyan [:,2] = lut_cyan [:,1]
    lut_cyan = lut_cyan.astype(np.uint8)

    #http://dicom.nema.org/medical/dicom/current/output/chtml/part06/chapter_B.html#sect_B.1.1
    lut_hotiron = np.asarray([
    [ 0, 0,0],[ 2, 0,0],[ 4, 0,0],[ 6, 0,0],[ 8, 0,0],[ 10,0,0],[ 12,0,0],[ 14,0,0],
    [ 16,0,0],[ 18,0,0],[ 20,0,0],[ 22,0,0],[ 24,0,0],[ 26,0,0],[ 28,0,0],[ 30,0,0],
    [ 32,0,0],[ 34,0,0],[ 36,0,0],[ 38,0,0],[ 40,0,0],[ 42,0,0],[ 44,0,0],[ 46,0,0],
    [ 48,0,0],[ 50,0,0],[ 52,0,0],[ 54,0,0],[ 56,0,0],[ 58,0,0],[ 60,0,0],[ 62,0,0],
    [ 64,0,0],[ 66,0,0],[ 68,0,0],[ 70,0,0],[ 72,0,0],[ 74,0,0],[ 76,0,0],[ 78,0,0],
    [ 80,0,0],[ 82,0,0],[ 84,0,0],[ 86,0,0],[ 88,0,0],[ 90,0,0],[ 92,0,0],[ 94,0,0],
    [ 96,0,0],[ 98,0,0],[100,0,0],[102,0,0],[104,0,0],[106,0,0],[108,0,0],[110,0,0],
    [112,0,0],[114,0,0],[116,0,0],[118,0,0],[120,0,0],[122,0,0],[124,0,0],[126,0,0],
    [128,0,0],[130,0,0],[132,0,0],[134,0,0],[136,0,0],[138,0,0],[140,0,0],[142,0,0],
    [144,0,0],[146,0,0],[148,0,0],[150,0,0],[152,0,0],[154,0,0],[156,0,0],[158,0,0],
    [160,0,0],[162,0,0],[164,0,0],[166,0,0],[168,0,0],[170,0,0],[172,0,0],[174,0,0],
    [176,0,0],[178,0,0],[180,0,0],[182,0,0],[184,0,0],[186,0,0],[188,0,0],[190,0,0],
    [192,0,0],[194,0,0],[196,0,0],[198,0,0],[200,0,0],[202,0,0],[204,0,0],[206,0,0],
    [208,0,0],[210,0,0],[212,0,0],[214,0,0],[216,0,0],[218,0,0],[220,0,0],[222,0,0],
    [224,0,0],[226,0,0],[228,0,0],[230,0,0],[232,0,0],[234,0,0],[236,0,0],[238,0,0],
    [240,0,0],[242,0,0],[244,0,0],[246,0,0],[248,0,0],[250,0,0],[252,0,0],[254,0,0],
    [255, 0, 0],[255, 2, 0],[255, 4, 0],[255, 6, 0],[255, 8, 0],[255, 10,0],[255, 12,0],[255, 14,0],
    [255, 16,0],[255, 18,0],[255, 20,0],[255, 22,0],[255, 24,0],[255, 26,0],[255, 28,0],[255, 30,0],
    [255, 32,0],[255, 34,0],[255, 36,0],[255, 38,0],[255, 40,0],[255, 42,0],[255, 44,0],[255, 46,0],
    [255, 48,0],[255, 50,0],[255, 52,0],[255, 54,0],[255, 56,0],[255, 58,0],[255, 60,0],[255, 62,0],
    [255, 64,0],[255, 66,0],[255, 68,0],[255, 70,0],[255, 72,0],[255, 74,0],[255, 76,0],[255, 78,0],
    [255, 80,0],[255, 82,0],[255, 84,0],[255, 86,0],[255, 88,0],[255, 90,0],[255, 92,0],[255, 94,0],
    [255, 96,0],[255, 98,0],[255,100,0],[255,102,0],[255,104,0],[255,106,0],[255,108,0],[255,110,0],
    [255,112,0],[255,114,0],[255,116,0],[255,118,0],[255,120,0],[255,122,0],[255,124,0],[255,126,0],
    [255,128,  4],[255,130,  8],[255,132, 12],[255,134, 16],[255,136, 20],[255,138, 24],[255,140, 28],[255,142, 32],
    [255,144, 36],[255,146, 40],[255,148, 44],[255,150, 48],[255,152, 52],[255,154, 56],[255,156, 60],[255,158, 64],
    [255,160, 68],[255,162, 72],[255,164, 76],[255,166, 80],[255,168, 84],[255,170, 88],[255,172, 92],[255,174, 96],
    [255,176,100],[255,178,104],[255,180,108],[255,182,112],[255,184,116],[255,186,120],[255,188,124],[255,190,128],
    [255,192,132],[255,194,136],[255,196,140],[255,198,144],[255,200,148],[255,202,152],[255,204,156],[255,206,160],
    [255,208,164],[255,210,168],[255,212,172],[255,214,176],[255,216,180],[255,218,184],[255,220,188],[255,222,192],
    [255,224,196],[255,226,200],[255,228,204],[255,230,208],[255,232,212],[255,234,216],[255,236,220],[255,238,224],
    [255,240,228],[255,242,232],[255,244,236],[255,246,240],[255,248,244],[255,250,248],[255,252,252],[255,255,255]])
    lut_hotiron = lut_hotiron.astype(np.uint8)

    lut_rediron = lut_hotiron # alias

    lut_greeniron  = np.zeros ([256,3], dtype=np.uint8)
    lut_greeniron [:,0] = lut_hotiron [:,2]    
    lut_greeniron [:,1] = lut_hotiron [:,0]  
    lut_greeniron [:,2] = lut_hotiron [:,1] 

    lut_blueiron  = np.zeros ([256,3], dtype=np.uint8)
    lut_blueiron [:,0] = lut_hotiron [:,2]    
    lut_blueiron [:,1] = lut_hotiron [:,1]  
    lut_blueiron [:,2] = lut_hotiron [:,0]  

    transparancy = 0.4 # 0.5 is half-transparent, 1.0 is not-transparent 

    #read T1 Image 
    try: img0 = nib.load(T1_filename)
    except: print ("Error reading", T1_filemname); sys.exit(2)
    data0 = np.asanyarray(img0.dataobj).astype(np.float32)
    SpatResol = np.asarray(img0.header.get_zooms())
    
    #read SpectroBOX
    try: img1 = nib.load(Spectro_filename)
    except: print ("Error reading", Spectro_filemname); sys.exit(2)
    data1 = np.asanyarray(img1.dataobj).astype(np.float32)
    data1 /= np.max(data1) # normalize to 1.0

    #read results 
    text0 = 'MRSpeCS Report'
    text1 = 'CSF fraction = '
    text2 = 'GM  fraction = ' 
    text3 = 'WM  fraction = '
    text4 = 'WCONC        = '
    try:   
      with open(Results_filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        line_count = 0
        for row in csv_reader:
          line_count += 1
          if line_count == 3:
            CSF   = float(row[0])
            GM    = float(row[1])
            WM    = float(row[2])
            WCONC = float(row[3])
      text1 += '{:.3f}'.format(CSF)    
      text2 += '{:.3f}'.format(GM)    
      text3 += '{:.3f}'.format(WM)    
      text4 += '{:.0f}'.format(WCONC)              
    except: pass    
    
 
  
    #write PDF header
    pdf = FPDF('P','mm','A4')
    pdf.add_page()
    pdf.set_font("Arial", size=20)
    pdf.cell(200, 45, txt='MRSpeCS Report', ln=1, align="C")
    pdf.set_font("Courier", 'B', size=12)
    pdf.set_text_color(90, 90, 90)
    pdf.cell(200, 5, txt=text1, ln=1, align="L")
    pdf.set_text_color(75, 75, 75)    
    pdf.cell(200, 5, txt=text2, ln=1, align="L")
    pdf.set_text_color(55, 55, 55)      
    pdf.cell(200, 5, txt=text3, ln=1, align="L")
    pdf.set_text_color(55, 55, 200)        
    pdf.cell(200, 5, txt=text4, ln=1, align="L")
    
    # image positioning
    xoffset=10
    yoffset=80
    width=64 
    width1 = data0.shape[0]*SpatResol[0] / data0.shape[1]*SpatResol[1] 
    width2 = data0.shape[0]*SpatResol[0] / data0.shape[2]*SpatResol[2]
    width3 = data0.shape[1]*SpatResol[1] / data0.shape[2]*SpatResol[2]
    tot_w = width1+width2+width3
    width1 = width1/tot_w*190
    width2 = width2/tot_w*190
    width3 = width3/tot_w*190
    #print (width1,width2,width3)
    #print (width1+width2+width3)
    #height1 = width1 / (data0.shape[0]*SpatResol[0] / data0.shape[1]*SpatResol[1])
    #height2 = width2 / (data0.shape[0]*SpatResol[0] / data0.shape[2]*SpatResol[2])
    #height3 = width3 / (data0.shape[1]*SpatResol[1] / data0.shape[2]*SpatResol[2])
    #print (height1,height2,height3)

    
    # --------------------------------------- AXIAL ----------------------------------------------

    # transformations
    data0 = np.rot90(data0, axes=(0,1))
    data1 = np.rot90(data1, axes=(0,1))
    SpatResol[1], SpatResol[0] = SpatResol[0], SpatResol[1]
    
    # find slices that contain ROI 
    slices=[]
    for slice in range (0,data0.shape[2]):
      if len(np.nonzero(data1[:,:,slice])[0])>0: slices.append(slice)
    if len(slices)==0: print("ERROR: no ROI intersection found"); sys.exit(1) 
    else: slice = slices[int(len(slices)/2)] # center slice
    
    height1=width1 * data0.shape[0]/data0.shape[1] * SpatResol[0]/SpatResol[1]

    imgdata0 = data0[:,:,slice]/np.max(data0)*255
    imgdata0 = imgdata0.astype(np.uint8)
    imgdata0  = lut_gray[imgdata0]
    imgdata0 = np.append (imgdata0, np.zeros([imgdata0.shape[0],imgdata0.shape[1],1], dtype=np.uint8),axis=2)
    imgdata0[:,:,3]=255 # but don't use it
    img0 = Image.fromarray(imgdata0)
    
    imgdata1 = data1[:,:,slice]/np.max(data1)*255
    imgdata1 = imgdata1.astype(np.uint8)
    imgdata1  = lut_yellow[imgdata1]
    imgdata1 = np.append (imgdata1, np.zeros([imgdata1.shape[0],imgdata1.shape[1],1], dtype=np.uint8),axis=2)
    alpha = data1[:,:,slice]/np.max(data1)*255*transparancy
    alpha = alpha.astype(np.uint8)
    imgdata1[:,:,3] = alpha 
    img1 = Image.fromarray(imgdata1)    
    
    img0.paste(img1, (0,0), img1)
    img0 = img0.convert ("RGB") # remove alpha channel
    if fpdf_version<"2": #old version, write on disk
      tempfile = '.overlay_axi'+str(slice)+'.png'
      img0.save(tempfile)
    else: #new version, write in memory
      tempfile = BytesIO()
      img0.save(tempfile, 'png')
      tempfile.name = 'test.png'
      tempfile.seek(0)
    xpos=xoffset
    ypos=yoffset
    pdf.image(tempfile, x = xpos, y=ypos, w = width1, h=height1, type="png")
    if fpdf_version<"2": os.remove(tempfile) #old version, delete tempfile    
    

    # --------------------------------------- CORONAL ----------------------------------------------


    # transformations
    data0 = np.rot90(data0, axes=(1,2))
    data1 = np.rot90(data1, axes=(1,2))
    SpatResol[2], SpatResol[1] = SpatResol[1], SpatResol[2]

    # find slices that contain ROI 
    slices=[]
    for slice in range (0,data0.shape[0]):
      if len(np.nonzero(data1[slice,:,:])[0])>0: slices.append(slice)
    if len(slices)==0: print("ERROR: no ROI intersection found"); sys.exit(1) 
    else: slice = slices[int(len(slices)/2)] # center slice  
     
    height2=width2 * data0.shape[1]/data0.shape[2] * SpatResol[1]/SpatResol[2]

    imgdata0 = data0[slice,:,:]/np.max(data0)*255
    imgdata0 = imgdata0.astype(np.uint8)
    imgdata0  = lut_gray[imgdata0]
    imgdata0 = np.append (imgdata0, np.zeros([imgdata0.shape[0],imgdata0.shape[1],1], dtype=np.uint8),axis=2)
    imgdata0[:,:,3]=255 # but don't use it
    img0 = Image.fromarray(imgdata0)
    
    imgdata1 = data1[slice,:,:]/np.max(data1)*255
    imgdata1 = imgdata1.astype(np.uint8)
    imgdata1  = lut_yellow[imgdata1]
    imgdata1 = np.append (imgdata1, np.zeros([imgdata1.shape[0],imgdata1.shape[1],1], dtype=np.uint8),axis=2)
    alpha = data1[slice,:,:]/np.max(data1)*255*transparancy
    alpha = alpha.astype(np.uint8)
    imgdata1[:,:,3] = alpha 
    img1 = Image.fromarray(imgdata1)     
    
    img0.paste(img1, (0,0), img1)
    img0 = img0.convert ("RGB") # remove alpha channel
    if fpdf_version<"2": #old version, write on disk
      tempfile = '.overlay_cor'+str(slice)+'.png'
      img0.save(tempfile)
    else: #new version, write in memory
      tempfile = BytesIO()
      img0.save(tempfile, 'png')
      tempfile.name = 'test.png'
      tempfile.seek(0)    
    xpos=width1 + xoffset
    ypos=yoffset
    pdf.image(tempfile, x = xpos, y=ypos, w = width2, h=height2, type="png")
    if fpdf_version<"2": os.remove(tempfile) #old version, delete tempfile  


    # --------------------------------------- SAGITAL RIGHT ----------------------------------------

    # transformations
    data0 = np.rot90(data0, axes=(0,1),k=3)
    data1 = np.rot90(data1, axes=(0,1),k=3)
    SpatResol[1], SpatResol[0] = SpatResol[0], SpatResol[1]

    # find slices that contain ROI 
    slices=[]
    for slice in range (0,data0.shape[2]):
      if len(np.nonzero(data1[:,:,slice])[0])>0: slices.append(slice)
    if len(slices)==0: print("ERROR: no ROI intersection found"); sys.exit(1) 
    else: slice = slices[int(len(slices)/2)] # center slice         
    
    height3=width3 * data0.shape[0]/data0.shape[1] * SpatResol[0]/SpatResol[1]
    
    imgdata0 = data0[:,:,slice]/np.max(data0)*255
    imgdata0 = imgdata0.astype(np.uint8)
    imgdata0  = lut_gray[imgdata0]
    imgdata0 = np.append (imgdata0, np.zeros([imgdata0.shape[0],imgdata0.shape[1],1], dtype=np.uint8),axis=2)
    imgdata0[:,:,3]=255 # but don't use it
    img0 = Image.fromarray(imgdata0)
    
    imgdata1 = data1[:,:,slice]/np.max(data1)*255
    imgdata1 = imgdata1.astype(np.uint8)
    imgdata1  = lut_yellow[imgdata1]
    imgdata1 = np.append (imgdata1, np.zeros([imgdata1.shape[0],imgdata1.shape[1],1], dtype=np.uint8),axis=2)
    alpha = data1[:,:,slice]/np.max(data1)*255*transparancy
    alpha = alpha.astype(np.uint8)
    imgdata1[:,:,3] = alpha 
    img1 = Image.fromarray(imgdata1)    
    
    img0.paste(img1, (0,0), img1)
    img0 = img0.convert ("RGB") # remove alpha channel
    if fpdf_version<"2": #old version, write on disk
      tempfile = '.overlay_sag'+str(slice)+'.png'
      img0.save(tempfile)
    else: #new version, write in memory
      tempfile = BytesIO()
      img0.save(tempfile, 'png')
      tempfile.name = 'test.png'
      tempfile.seek(0)    
    xpos=width1 + width2 + xoffset
    ypos=yoffset
    pdf.image(tempfile, x = xpos, y=ypos, w = width3, h=height3, type="png")
    if fpdf_version<"2": os.remove(tempfile) #old version, delete tempfile  

         
        
    pdf.output(PDF_filename)




def main():
    MRSpeCS_Report("T1.nii", "SpectroBOX.nii", "mrspecs_Results.txt", "MRSpeCS_Report.pdf")
    if sys.platform=="win32": os.system("pause") # windows
        
if __name__ == '__main__':
    main()        
        
