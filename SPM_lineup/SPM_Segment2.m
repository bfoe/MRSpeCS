function SPM_Segment2

% This script uses T1.nii and SpectroBox.nii files calculated by MRSpeCS 
% and applies the two available segmentation methods from SPM.
% Use to compare results from different Segmentation methods (FSL, SPM Standard, SPM New) 


%find SPM
[SPMPath , ~, ~] = fileparts(which('spm')); SPMPath = [SPMPath '/'];
if SPMPath == '/'; error('Error: no SPM installation found'); end;
% read files
[t1File,t1Path]=uigetfile('*.nii','Select T1 image');
if t1File==0; error ('ERROR:  No T1 image file specified'); end;
cd(t1Path)
[boxFile,boxPath]=uigetfile('*.nii','Select Spectro Box');
if boxFile==0; error ('ERROR:  No T1 SpectroBox file specified'); end;



% --------------------------------------------------------------
% Here starts the code for the SPM Standard Segmentation method.
% The parameters below are the default parameters from the GUI 
% plus Cerebro-Spinal-Fluid enabled (in Native Space)
% In the GUI you can find this under:
% spm fmri, second line from top, rightmost, button "Segment"
% --------------------------------------------------------------

% parameters for SPM Segment
disp (sprintf('\nRunning ''Segment'' (SPM standard)\n'))
writeOpts.GM  = [0 0 1]; % GM native
writeOpts.WM  = [0 0 1]; % WM native
writeOpts.CSF = [0 0 1]; % CSF native
writeOpts.biascor = 0;
writeOpts.cleanup = 0;
segmOpts.tpm = char({[SPMPath 'tpm/grey.nii'] [SPMPath 'tpm/white.nii'] [SPMPath 'tpm/csf.nii'] });
segmOpts.ngaus = [2 2 2 4];
segmOpts.regtype = 'mni';
segmOpts.warpreg = 1;
segmOpts.warpco = 25;
segmOpts.biasreg = 0.0001;
segmOpts.biasfwhm = 60;
segmOpts.samp = 3;
segmOpts.msk = char({''});
% run SPM Segment
Vimg      = spm_vol([t1Path, t1File]);
results   = spm_preproc(Vimg,segmOpts);
[po,~] = spm_prep2sn(results);
spm_preproc_write(po,writeOpts);

% analyse segmentation results
V_CSF  = spm_vol([t1Path 'c3' t1File]);
V_GM   = spm_vol([t1Path 'c1' t1File]);  
V_WM   = spm_vol([t1Path 'c2' t1File]);
V_mask = spm_vol([boxPath boxFile]);
csf_mat = (V_CSF.private.dat(:,:,:) .* V_mask.private.dat(:,:,:));
gm_mat  = (V_GM.private.dat(:,:,:)  .* V_mask.private.dat(:,:,:));
wm_mat  = (V_WM.private.dat(:,:,:)  .* V_mask.private.dat(:,:,:));
n_zero_mask = sum(sum(sum(V_mask.private.dat(:,:,:)~=0))); % number of voxels in mask that are not 0
n_one_mask  = sum(sum(sum(V_mask.private.dat(:,:,:)==1))); % number of voxels in mask that are 1
if n_zero_mask ~= n_one_mask; error('Error in mask, there are voxels that are neiter 0 nor 1'); end
csf = sum(sum(sum(csf_mat)))/n_zero_mask;
gm  = sum(sum(sum(gm_mat)))/n_zero_mask;
wm  = sum(sum(sum(wm_mat)))/n_zero_mask;
csf_per = csf / (gm+wm+csf); disp (['csf_per = ' num2str(csf_per)]);
gm_per  = gm  / (gm+wm+csf); disp (['gm_per  = ' num2str(gm_per)]);
wm_per  = wm  / (gm+wm+csf); disp (['wm_per  = ' num2str(wm_per)]);
WCONC   =  floor((gm_per*43300. + wm_per*35880. + csf_per*55556.)/(1.-csf_per));
disp (['WCONC   = ' num2str(WCONC)]);

% write values to file
fileID=fopen([t1Path 'SPM_SegmentSTD_Results.txt'],'w');
fprintf(fileID, 'SPM Standard Segmentation results:\n\n');
fprintf(fileID, '   CSF:   %f\n', csf_per);
fprintf(fileID, '    GM:   %f\n', gm_per);
fprintf(fileID, '    WM:   %f\n', wm_per);
fprintf(fileID, ' WCONC:   %d\n', WCONC);
fclose(fileID);

% cleanup
movefile ([t1Path 'c1' t1File], [t1Path 'T1_GM_SPMsegment.nii']);
movefile ([t1Path 'c2' t1File], [t1Path 'T1_WM_SPMsegment.nii']);
movefile ([t1Path 'c3' t1File], [t1Path 'T1_CSF_SPMsegment.nii']);



% --------------------------------------------------------------
% Here starts the code for the SPM New Segmentation method.
% The parameters below are the default parameters from the GUI 
% but saving the Skull and Other tissue images is disabled.
% To find this in the GUI, follow the steps as above and in the 
% Batch Editor window on the Menu at the top click:
% SPM - Tools - New Segment
% 
% -------------------------------------------------------------


% the "New Segment" method still uses jobman
% see spm8/toolbox/seg/spm_preproc_run.m on how to take it outathere
% don't mixitup with spm8/config/spm_run_preproc.m, that's for
% the above standard method (welcome to the confusion;)
spm('defaults','fmri');
spm_jobman('initcfg') 
% run SPM New Segment
matlabbatch{1}.spm.tools.preproc8.channel.vols = {[t1Path t1File ',1']};
matlabbatch{1}.spm.tools.preproc8.channel.biasreg = 0.0001;
matlabbatch{1}.spm.tools.preproc8.channel.biasfwhm = 60;
matlabbatch{1}.spm.tools.preproc8.channel.write = [0 0];
matlabbatch{1}.spm.tools.preproc8.tissue(1).tpm = {[SPMPath 'toolbox/Seg/TPM.nii,1']};
matlabbatch{1}.spm.tools.preproc8.tissue(1).ngaus = 2;
matlabbatch{1}.spm.tools.preproc8.tissue(1).native = [1 0]; % GM native
matlabbatch{1}.spm.tools.preproc8.tissue(1).warped = [0 0];
matlabbatch{1}.spm.tools.preproc8.tissue(2).tpm = {[SPMPath 'toolbox/Seg/TPM.nii,2']};
matlabbatch{1}.spm.tools.preproc8.tissue(2).ngaus = 2;
matlabbatch{1}.spm.tools.preproc8.tissue(2).native = [1 0]; % WM native
matlabbatch{1}.spm.tools.preproc8.tissue(2).warped = [0 0];
matlabbatch{1}.spm.tools.preproc8.tissue(3).tpm = {[SPMPath 'toolbox/Seg/TPM.nii,3']};
matlabbatch{1}.spm.tools.preproc8.tissue(3).ngaus = 2;
matlabbatch{1}.spm.tools.preproc8.tissue(3).native = [1 0]; % CSF native
matlabbatch{1}.spm.tools.preproc8.tissue(3).warped = [0 0];
matlabbatch{1}.spm.tools.preproc8.tissue(4).tpm = {[SPMPath 'toolbox/Seg/TPM.nii,4']};
matlabbatch{1}.spm.tools.preproc8.tissue(4).ngaus = 3;
matlabbatch{1}.spm.tools.preproc8.tissue(4).native = [0 0]; % Skull off (used, but not saved)
matlabbatch{1}.spm.tools.preproc8.tissue(4).warped = [0 0];
matlabbatch{1}.spm.tools.preproc8.tissue(5).tpm = {[SPMPath 'toolbox/Seg/TPM.nii,5']};
matlabbatch{1}.spm.tools.preproc8.tissue(5).ngaus = 4;
matlabbatch{1}.spm.tools.preproc8.tissue(5).native = [0 0]; % Other off (used, but not saved)
matlabbatch{1}.spm.tools.preproc8.tissue(5).warped = [0 0];
matlabbatch{1}.spm.tools.preproc8.tissue(6).tpm = {[SPMPath 'toolbox/Seg/TPM.nii,6']};
matlabbatch{1}.spm.tools.preproc8.tissue(6).ngaus = 2;
matlabbatch{1}.spm.tools.preproc8.tissue(6).native = [0 0]; % Air off (used, but not saved)
matlabbatch{1}.spm.tools.preproc8.tissue(6).warped = [0 0];
matlabbatch{1}.spm.tools.preproc8.warp.reg = 4;
matlabbatch{1}.spm.tools.preproc8.warp.affreg = 'mni';
matlabbatch{1}.spm.tools.preproc8.warp.samp = 3;
matlabbatch{1}.spm.tools.preproc8.warp.write = [0 0];
spm_jobman('run',matlabbatch)

% analyse segmentation results
V_CSF  = spm_vol([t1Path 'c3' t1File]);
V_GM   = spm_vol([t1Path 'c1' t1File]);  
V_WM   = spm_vol([t1Path 'c2' t1File]);
V_mask = spm_vol([boxPath boxFile]);
csf_mat = V_CSF.private.dat(:,:,:) .* V_mask.private.dat(:,:,:);
gm_mat  = V_GM.private.dat(:,:,:)  .* V_mask.private.dat(:,:,:);
wm_mat  = V_WM.private.dat(:,:,:)  .* V_mask.private.dat(:,:,:);
n_zero_mask = sum(sum(sum(V_mask.private.dat(:,:,:)~=0))); % number of voxels in mask that are not 0
n_one_mask  = sum(sum(sum(V_mask.private.dat(:,:,:)==1))); % number of voxels in mask that are 1
if n_zero_mask ~= n_one_mask; error('Error in mask, there are voxels that are neiter 0 nor 1'); end
csf = sum(sum(sum(csf_mat)))/n_zero_mask;
gm  = sum(sum(sum(gm_mat)))/n_zero_mask;
wm  = sum(sum(sum(wm_mat)))/n_zero_mask;
csf_per = csf / (gm+wm+csf); disp (['csf_per = ' num2str(csf_per)]);
gm_per  = gm  / (gm+wm+csf); disp (['gm_per  = ' num2str(gm_per)]);
wm_per  = wm  / (gm+wm+csf); disp (['wm_per  = ' num2str(wm_per)]);
WCONC =  floor((gm_per*43300. + wm_per*35880. + csf_per*55556.)/(1.-csf_per));
disp (['WCONC   = ' num2str(WCONC)]);

% write values to file
fileID=fopen([t1Path 'SPM_SegmentNEW_Results.txt'],'w');
fprintf(fileID, 'SPM New Segmentation results:\n\n');
fprintf(fileID, '   CSF:   %f\n', csf_per);
fprintf(fileID, '    GM:   %f\n', gm_per);
fprintf(fileID, '    WM:   %f\n', wm_per);
fprintf(fileID, ' WCONC:   %d\n', WCONC);
fclose(fileID);

% cleanup
movefile ([t1Path 'c1' t1File], [t1Path 'T1_GM_SPMnewSegment.nii']);
movefile ([t1Path 'c2' t1File], [t1Path 'T1_WM_SPMnewSegment.nii']);
movefile ([t1Path 'c3' t1File], [t1Path 'T1_CSF_SPMnewSegment.nii']);
[~, basename, ~]=fileparts([t1Path t1File]);
delete([t1Path basename '_seg8.mat']);

