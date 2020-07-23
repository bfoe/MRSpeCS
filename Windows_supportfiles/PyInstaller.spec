# -*- mode: python -*-
a = Analysis(['..\MRSpeCS.py'],
             excludes=['lib2to3', 'win32com', 'unicodedata', 'PIL._webp', 'PIL._imagingtk',
                       'scipy', '_ssl', '_hashlib', '_elementtree', '_decimal', '_lzma',
                       'pydoc', '_hashlib', '_ssl',
                       'win32pdh','win32pipe', 'win32api', 'win32evtlog', 'win32wnet', '_testcapi'
                       'setuptools'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
             
for d in a.datas:
    if 'pyconfig' in d[0]: 
        a.datas.remove(d)
        break             
a.binaries += [('avscale.exe', 'avscale.exe', 'DATA')]
a.binaries += [('fslhd.exe', 'fslhd.exe', 'DATA')]
a.binaries += [('fslmaths.exe', 'fslmaths.exe', 'DATA')]
a.binaries += [('fslmeants.exe', 'fslmeants.exe', 'DATA')]
a.binaries += [('fslorient.exe', 'fslorient.exe', 'DATA')]
a.binaries += [('fslswapdim.exe', 'fslswapdim.exe', 'DATA')]
a.binaries += [('bet2.exe', 'bet2.exe', 'DATA')]
a.binaries += [('convert_xfm.exe', 'convert_xfm.exe', 'DATA')]
a.binaries += [('cygwin1.dll', 'cygwin1.dll', 'DATA')]
a.binaries += [('dcm2nii.exe', 'dcm2nii.exe', 'DATA')]
a.binaries += [('fast.exe', 'fast.exe', 'DATA')]
a.binaries += [('flirt.exe', 'flirt.exe', 'DATA')]
a.datas = [x for x in a.datas if not ('mpl-data\\fonts' in os.path.dirname(x[1]))]                     
a.datas = [x for x in a.datas if not ('mpl-data\fonts' in os.path.dirname(x[1]))]                     
a.datas = [x for x in a.datas if not ('mpl-data\\sample_data' in os.path.dirname(x[1]))]            
a.datas = [x for x in a.datas if not ('mpl-data\sample_data' in os.path.dirname(x[1]))]            
a.datas = [x for x in a.datas if not ('tk8.6\msgs' in os.path.dirname(x[1]))]            
a.datas = [x for x in a.datas if not ('tk8.6\images' in os.path.dirname(x[1]))]            
a.datas = [x for x in a.datas if not ('tk8.6\demos' in os.path.dirname(x[1]))]            
a.datas = [x for x in a.datas if not ('tcl8.6\opt0.4' in os.path.dirname(x[1]))]            
a.datas = [x for x in a.datas if not ('tcl8.6\http1.0' in os.path.dirname(x[1]))]            
a.datas = [x for x in a.datas if not ('tcl8.6\encoding' in os.path.dirname(x[1]))]            
a.datas = [x for x in a.datas if not ('tcl8.6\msgs' in os.path.dirname(x[1]))]            
a.datas = [x for x in a.datas if not ('tcl8.6\\tzdata' in os.path.dirname(x[1]))]            
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='MRSpeCS.exe',
          debug=False,
          strip=None,
          upx=False,
          console=True, icon='MRSpeCS.ico')          

