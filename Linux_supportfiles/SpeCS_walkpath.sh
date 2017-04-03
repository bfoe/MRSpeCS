#!/bin/sh
#
# automatization script:
#   - walks all subdirs of current working dir 1 level up
#   - looks for a log ($trigger) file from previous runs
#     if not found do the processing ($processing_command)
#   - joins all individual logs ($trigger) into $global_log in current dir 
#


# individual log files to look for, if processing was already done
trigger=MRSpeCS_Results.txt
# global log file in current working dir were all individual logfiles are joined
global_log="All_"$trigger
# processing command to execute
processing_command="echo $i > $trigger" # substitute e.g. with "../MRSpeCS.py --img=3DT1.dcm --spec=spectro.SDAT >/dev/nul"


# ------------------- do not change anything beyond this line -------------------------------

# start
rm $global_log >/dev/null 2>&1
echo Start
for i in *
do
   #out=${i%_DTI.nii.gz}_DTI_ECC.nii.gz
   if [ -d "$i" ]; then # if this is a sudir 
   cd $i
      if ! [ -f "$trigger" ]; then # if this is not processed yet 
         echo Processing  : $i
         eval $processing_command # actually do the processing
         if ! [ -f "$trigger" ]; then # check again
            echo ERROR processing : $i
         fi
      else
         echo Already done: $i
      fi
      cat $trigger >> ../$global_log 2>/dev/null
   cd ..
   fi
done
echo done

