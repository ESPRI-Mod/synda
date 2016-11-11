#!/bin/bash -e

# Description
#   This script apply prog_cor.f90
#
# Notes
#
# Usage
#   ./correction_cdft.sh <PROJECT> <SCR_PATH> <DEST_PATH> <VAR>
#
# Input
#   The project ID
#   <PROJECT>
#   An atomic dataset full path as the directory that contains NetCDF files
#   <SRC_PATH>  : /prodigfs/project/<PROJECT>/interpolated/<downstream_DRS>/
#   <VAR> : Variable
#
# Output
#   An atomic dataset full path for interpolated NetCDF
#   <DEST_PATH> : /prodigfs/project/<PROJECT>/bias-adjusted/<downstream_DRS>/


# ------ functions ------ #

curdate ()
{
    date +'%Y/%m/%d %I:%M:%S %p'
}

msg ()
{
    l__code="${1}"
    l__msg="${2}"

    echo "$(curdate) ${l__code} ${l__msg}" 1>&2
}


# --------- arguments & initialization --------- #

while [ "${1}" != "" ]; do
    case "${1}" in
        # Project ID/Facet
        "--project")            shift; project="${1}"             ;;

        # /prodigfs/esgf/process/<PROJECT>/interpolated/<downstream_DRS>
        "--src_variable_path")  shift; interpolated_path="${1}"        ;;

        # /prodigfs/project/<PROJECT>/bias-adjusted/<downstream_DRS>
        "--dest_variable_path") shift; corrected_path="${1}"   ;;

        # Variable
        "--variable") shift; variable="${1}"   ;;
       
        # Path this script is from
        "--script_dir") shift;  scripts_path="${1}"   ;;


    esac
    shift
done


### definition des chemins 

chemin=${scripts_path}
chemin_prog="$chemin/correction_cdft/"
chemin_config="$chemin/correction_cdft/config_cdft/"



echo $project
echo $interpolated_path
echo $corrected_path
echo $variable

# --------- main --------- #

msg "INFO" "corretion_cdft.sh started (variable_path = ${interpolated_path})"


umask g+w

timedeb=$(date | awk -F' ' '{print $4}')
echo $timedeb


# This is needed, because cdo expects destination path to exist (or at least parent folders in destination path).
mkdir -p ${corrected_path}

obsfile=$(cat $chemin_config/obs_ref_$project.json | $chemin_prog/jq-1.5  '.variable[] | select(.name=="'$variable'") | .file' | awk -F"\"" '{print $2}')
nyrefstart=$(cat $chemin_config/obs_ref_$project.json | $chemin_prog/jq-1.5  '.variable[] | select(.name=="'$variable'") | .debut' | awk -F"\"" '{print $2}')
nyrefend=$(cat $chemin_config/obs_ref_$project.json | $chemin_prog/jq-1.5  '.variable[] | select(.name=="'$variable'") | .fin' | awk -F"\"" '{print $2}')




echo $obsfile

echo $nyrefstart,$nyrefend

####### Récuperation des informations à partir du nom des fichiers
for file in $(ls ${interpolated_path}); do
 if [ $project == "CMIP5" ];then
	RCP=$(echo $file | awk -F"_" '{print $4}' )
	model=$(echo $file | awk -F"_" '{print $3}' )
        member=$(echo $file | awk -F"_" '{print $5}' )

    fi
    if [ $project == "CORDEX" ];then
	RCP=$(echo $file | awk -F"_" '{print $4}' )
	model=$(echo $file | awk -F"_" '{print $6}' )
        member=$(echo $file | awk -F"_" '{print $5}' )
        GCM=$(echo $file | awk -F"_" '{print $3}' )

    fi

done

if [ $RCP == 'historical' ]; then
	echo "historical"
        msg "INFO" "correction_cdft.sh not executed"
	exit
else
        echo "RCP"
	echo $RCP
        echo $model 
fi


#### definition des paramètres 

obsdir="/prodigfs/bc_obs/$project"
tempdir_prog=$chemin_prog/tmp/$model/$variable\_$$
tempdir_data="/data/tnoel/tmp/$model"

config_file="$chemin_config/config_cdft.ini"

ystart=$(grep nystart $config_file | awk -F"-" '{print $2}' )
yend=$(grep nyend $config_file | awk -F"-" '{print $2}' )

nystart=$(echo ${ystart:0:4})
nyend=$(echo ${yend:0:4})

moving=$(grep moving $config_file | awk -F"-" '{print $2}' )
cor=$(grep cor $config_file | awk -F"-" '{print $2}' )
sshift=$(echo "($moving-$cor)/2" | bc)

nbproc=$(grep proc $config_file | awk -F"-" '{print $2}' )
ram=$(grep ram $config_file | awk -F"-" '{print $2}' )

echo $nbproc,$ram
vram=$(echo "($ram+12)" | bc)
ramk=$(echo "$ram*1000000" | bc)

  if [ $project == "CMIP5" ];then
interpolated_path_hist=$(echo $interpolated_path | sed "s/$RCP/historical/g" ) 
echo $interpolated_path_hist

   fi
    if [ $project == "CORDEX" ];then
chemin_temp=$(echo ${interpolated_path} | awk -F"v20" '{print $1}' )
interpolated_path_hist_part_1=$(echo $chemin_temp | sed "s/$RCP/historical/g" ) 
interpolated_path_hist_part_2=$(ls $interpolated_path_hist_part_1/)
interpolated_path_hist=$interpolated_path_hist_part_1$interpolated_path_hist_part_2
echo $interpolated_path_hist
  fi

##### Verification de la date de début de la simulation
cd $interpolated_path_hist/
list=$( ls *.nc)
min=2005
for file in ${list} ; do
    fileroot=$(echo ${file} | awk -F".nc" '{print $1}' )
     if [ $project == "CMIP5" ];then
    dates=$(echo ${fileroot} | awk -F"_" '{print $6}' )
    fi
    if [ $project == "CORDEX" ];then
    dates=$(echo ${fileroot} | awk -F"_" '{print $9}' )
    fi

    debfile=$(echo ${dates} | awk -F"-" '{print $1}' )
    endfile=$(echo ${dates} | awk -F"-" '{print $2}' )
  
    ydebfile=$(echo ${debfile:0:4})
    yendfile=$(echo ${endfile:0:4})
    

if [[ $ydebfile -le $min ]];then
  min=$ydebfile
fi
done
echo $min
if [[ $min -ge $nystart ]];then
  nystart=$min
  echo $nystart
fi

##### Verification de la date de fin de la simulation
cd $interpolated_path/
list=$( ls *.nc)
max=2005
for file in ${list} ; do
    fileroot=$(echo ${file} | awk -F".nc" '{print $1}' )
     if [ $project == "CMIP5" ];then
    dates=$(echo ${fileroot} | awk -F"_" '{print $6}' )
    fi
    if [ $project == "CORDEX" ];then
    dates=$(echo ${fileroot} | awk -F"_" '{print $9}' )
    fi

    debfile=$(echo ${dates} | awk -F"-" '{print $1}' )
    endfile=$(echo ${dates} | awk -F"-" '{print $2}' )
  
    ydebfile=$(echo ${debfile:0:4})
    yendfile=$(echo ${endfile:0:4})
    
    echo $ydebfile
    echo $yendfile

if [[ $yendfile -ge $max ]];then
  max=$yendfile
fi
done
echo $max
if [[ $max -ge $nyend ]];then
  nyend=$max
  echo $nyend
fi



mkdir -p $tempdir_prog
mkdir -p $tempdir_data


##### traitement du fichier d'observation de référence
echo "Data OBS REF"
if [ ! -e $tempdir_data/$variable\_obs_reference.nc ]; then
echo "cdo selyear,$nyrefstart/$nyrefend $obsdir/$obsfile $tempdir_data/$variable\_obs_reference.nc"
cdo selyear,$nyrefstart/$nyrefend $obsdir/$obsfile $tempdir_data/$variable\_obs_reference.nc
elif [ -f $tempdir_data/$variable\_obs_reference.nc ]; then
 echo "$tempdir_data/$variable\_obs_reference.nc deja traiter"
fi



##### traitement du fichier Model de référence
echo "Data Model REF"

   echo 'year start ref :' $nyrefstart
   echo 'year end ref :' $nyrefend

if [ ! -e $tempdir_data/$variable\_data_model_ref.nc ]; then
if [[ $nyrefstart -lt 2006 && $nyrefend -lt 2006 ]]; then

echo "historical"

echo $interpolated_path_hist

cd $interpolated_path_hist

list=$( ls *.nc)
i=0
for file in ${list} ; do
    fileroot=$(echo ${file} | awk -F".nc" '{print $1}' )
    if [ $project == "CMIP5" ];then
    dates=$(echo ${fileroot} | awk -F"_" '{print $6}' )
    fi
    if [ $project == "CORDEX" ];then
    dates=$(echo ${fileroot} | awk -F"_" '{print $9}' )
    fi


    debfile=$(echo ${dates} | awk -F"-" '{print $1}' )
    endfile=$(echo ${dates} | awk -F"-" '{print $2}' )
    ydebfile=$(echo ${debfile:0:4})
    yendfile=$(echo ${endfile:0:4})
    
        
if [[  $ydebfile -le $nyrefstart && $yendfile -ge $nyrefstart ]];then
     echo $ydebfile 
     echo $yendfile

     echo "File to use 1"
     i=$(echo "($i+1)" | bc)
     cp $interpolated_path_hist/$file $tempdir_data/$variable\_tmp$i.nc
  fi
if [[ $ydebfile -gt $nyrefstart && $yendfile -le $nyrefend ]];then
     echo $ydebfile 
     echo $yendfile

     echo "File to use 2"
     i=$(echo "($i+1)" | bc)
     cp $interpolated_path_hist/$file $tempdir_data/$variable\_tmp$i.nc
  fi
if [[  $ydebfile -gt $nyrefstart && $ydebfile -lt $nyrefend && $yendfile -gt $nyrefend ]];then
     echo $ydebfile 
     echo $yendfile

     echo "File to use 3"
     i=$(echo "($i+1)" | bc)
     cp $interpolated_path_hist/$file $tempdir_data/$variable\_tmp$i.nc
  fi
done 
     ncrcat $tempdir_data/$variable\_tmp*.nc $tempdir_data/$variable\_temp_data_model.nc
     echo " cdo selyear,$nyrefstart/$nyrefend $tempdir_data/$variable\_temp_data_model.nc $tempdir_data/$variable\_data_model_ref.nc"
     cdo selyear,$nyrefstart/$nyrefend $tempdir_data/$variable\_temp_data_model.nc $tempdir_data/$variable\_data_model_ref.nc

rm -f $tempdir_data/$variable\_tmp*.nc
rm -f $tempdir_data/$variable\_temp*.nc
fi

if [[ $nyrefstart -lt 2006 && $nyrefend -gt 2005 ]]; then
echo "historical and RCP"


echo $interpolated_path_hist
cd $interpolated_path_hist

list=$( ls *.nc)
i=0
for file in ${list} ; do
    fileroot=$(echo ${file} | awk -F".nc" '{print $1}' )
     if [ $project == "CMIP5" ];then
    dates=$(echo ${fileroot} | awk -F"_" '{print $6}' )
    fi
    if [ $project == "CORDEX" ];then
    dates=$(echo ${fileroot} | awk -F"_" '{print $9}' )
    fi

    debfile=$(echo ${dates} | awk -F"-" '{print $1}' )
    endfile=$(echo ${dates} | awk -F"-" '{print $2}' )
    ydebfile=$(echo ${debfile:0:4})
    yendfile=$(echo ${endfile:0:4})
    
if [[  $ydebfile -le $nyrefstart && $yendfile -ge $nyrefstart ]];then
     echo $ydebfile 
     echo $yendfile

     echo "File to use 1"
     i=$(echo "($i+1)" | bc)
     cp $interpolated_path_hist/$file $tempdir_data/$variable\_tmp$i.nc
fi
if [[ $ydebfile -gt $nyrefstart && $yendfile -le $nyrefend ]];then
     echo $ydebfile 
     echo $yendfile

     echo "File to use 2"
     i=$(echo "($i+1)" | bc)
     cp $interpolated_path_hist/$file $tempdir_data/$variable\_tmp$i.nc
fi
if [[  $ydebfile -gt $nyrefstart && $ydebfile -lt $nyrefend && $yendfile -gt $nyrefend ]];then
     echo $ydebfile 
     echo $yendfile

     echo "File to use 3"
     i=$(echo "($i+1)" | bc)
     cp $interpolated_path_hist/$file $tempdir_data/$variable\_tmp$i.nc
fi
done 

cd $interpolated_path
list=$( ls *.nc)

for file in ${list} ; do
    fileroot=$(echo ${file} | awk -F".nc" '{print $1}' )
    if [ $project == "CMIP5" ];then
    dates=$(echo ${fileroot} | awk -F"_" '{print $6}' )
    fi
    if [ $project == "CORDEX" ];then
    dates=$(echo ${fileroot} | awk -F"_" '{print $9}' )
    fi

    debfile=$(echo ${dates} | awk -F"-" '{print $1}' )
    endfile=$(echo ${dates} | awk -F"-" '{print $2}' )
    ydebfile=$(echo ${debfile:0:4})
    yendfile=$(echo ${endfile:0:4})
   
if [[  $ydebfile -le $nyrefstart && $yendfile -ge $nyrefstart ]];then
     echo $ydebfile 
     echo $yendfile

     echo "File to use 1"
     i=$(echo "($i+1)" | bc)
     cp $interpolated_path/$file $tempdir_data/$variable\_tmp$i.nc
fi
if [[ $ydebfile -gt $nyrefstart && $yendfile -le $nyrefend ]];then
     echo $ydebfile 
     echo $yendfile

     echo "File to use 2"
     i=$(echo "($i+1)" | bc)
     cp $interpolated_path/$file $tempdir_data/$variable\_tmp$i.nc
fi
if [[  $ydebfile -gt $nyrefstart && $ydebfile -lt $nyrefend && $yendfile -gt $nyrefend ]];then
     echo $ydebfile 
     echo $yendfile

     echo "File to use 3"
     i=$(echo "($i+1)" | bc)
     cp $interpolated_path/$file $tempdir_data/$variable\_tmp$i.nc
fi
done 

     ncrcat $tempdir_data/$variable\_tmp*.nc $tempdir_data/$variable\_temp_data_model.nc
     echo " cdo selyear,$nyrefstart/$nyrefend $tempdir_data/$variable\_temp_data_model.nc $tempdir_data/$variable\_data_model_ref.nc"
     cdo selyear,$nyrefstart/$nyrefend $tempdir_data/$variable\_temp_data_model.nc $tempdir_data/$variable\_data_model_ref.nc

rm -f $tempdir_data/$variable\_tmp*.nc
rm -f $tempdir_data/$variable\_temp*.nc

fi

if [[ $nyrefstart -gt 2005 && $nyrefend -gt  2005 ]]; then
echo "RCP"
cd $interpolated_path/
list=$( ls *.nc)
i=0
for file in ${list} ; do

    fileroot=$(echo ${file} | awk -F".nc" '{print $1}' )
    if [ $project == "CMIP5" ];then
    dates=$(echo ${fileroot} | awk -F"_" '{print $6}' )
    fi
    if [ $project == "CORDEX" ];then
    dates=$(echo ${fileroot} | awk -F"_" '{print $9}' )
    fi


    debfile=$(echo ${dates} | awk -F"-" '{print $1}' )
    endfile=$(echo ${dates} | awk -F"-" '{print $2}' )
    ydebfile=$(echo ${debfile:0:4})
    yendfile=$(echo ${endfile:0:4})

if [[  $ydebfile -le $nyrefstart && $yendfile -ge $nyrefstart ]];then
     echo $ydebfile 
     echo $yendfile

     echo "File to use 1"
     i=$(echo "($i+1)" | bc)
     cp $interpolated_path/$file $tempdir_data/$variable\_tmp$i.nc
fi
if [[ $ydebfile -gt $nyrefstart && $yendfile -le $nyrefend ]];then
     echo $ydebfile 
     echo $yendfile

     echo "File to use 2"
     i=$(echo "($i+1)" | bc)
     cp $interpolated_path/$file $tempdir_data/$variable\_tmp$i.nc
fi
if [[  $ydebfile -gt $nyrefstart && $ydebfile -lt $nyrefend && $yendfile -gt $nyrefend ]];then
    echo $ydebfile 
    echo $yendfile

     echo "File to use 3"
     i=$(echo "($i+1)" | bc)
     cp $interpolated_path/$file $tempdir_data/$variable\_tmp$i.nc
fi
done 
     ncrcat $tempdir_data/\$variable_tmp*.nc $tempdir_data/$variable\_temp_data_model_ref.nc
     echo " cdo selyear,$nyrefstart/$nyrefend $tempdir_data/$variable\_temp_data_model_ref.nc $tempdir_data/$variable\_data_model_ref.nc"
     cdo selyear,$nyrefstart/$nyrefend $tempdir_data/$variable\_temp_data_model_ref.nc $tempdir_data/$variable\_data_model_ref.nc

rm -f $tempdir_data/$variable\_tmp*.nc
rm -f $tempdir_data/$variable\_temp*.nc

fi
elif [ -f $tempdir_data/$variable\_data_model_ref.nc ]; then
 echo "$tempdir_data/$variable\_data_model_ref.nc deja traiter"
fi

Ndimx=$(ncdump -h $tempdir_data/$variable\_data_model_ref.nc | grep "$variable(time"  | awk -F")" '{print $1}' | awk -F"," '{print $3}')
Ndimy=$(ncdump -h $tempdir_data/$variable\_data_model_ref.nc | grep "$variable(time"  | awk -F")" '{print $1}' | awk -F"," '{print $2}')

echo $Ndimx,$Ndimy



if [ ! -e $tempdir_data/rcp_meta_data.nc ]; then
echo "Extraction meta data RCP"
cd $interpolated_path/
list=$( ls -1 *.nc | head -1 )
for file in ${list} ; do

ncks -d time,1,2 $file $tempdir_data/rcp_meta_data.nc
done
fi

tcal=$( ncdump -h  $tempdir_data/$variable\_data_model_ref.nc | grep calendar| awk -F"\"" '{print $2}' )

    if [ $tcal == "standard" -o $tcal == "gregorian" -o $tcal == "proleptic_gregorian" ];then
	echo "tcal = 1"
	icaltype=1
    fi
    if [ $tcal == "360_day" -o $tcal == "360d" -o $tcal == "360" ];then
	echo "tcal = 2"
	icaltype=2
    fi
    if [ $tcal == "365_day" -o $tcal == "365" -o $tcal == "365d" -o $tcal == "noleap" ];then
	echo "tcal = 3"
	icaltype=3  
    fi



###########################################################
#                       Compilation                       #
###########################################################
echo "data Model"


echo "Compile fortran code"

cd $chemin_prog
ifort calcul_periods.f90 -o calcul_period.e
period_file="$tempdir_prog/period.txt"


ifort -c -O3 -ipo -pg -openmp -zero -module $tempdir_prog m_sort.f90 -o $tempdir_prog/m_sort.o
ifort -c -O3 -ipo -pg -openmp -zero -module $tempdir_prog m_ymdsju.f90 -o $tempdir_prog/m_ymdsju.o
ifort -c -O3 -ipo -pg -openmp -zero -module $tempdir_prog $tempdir_prog/m_ymdsju.o m_mask.f90 -o $tempdir_prog/m_mask.o
ifort -c -O3 -ipo -pg -openmp -zero -module $tempdir_prog $tempdir_prog/m_sort.o m_cdft_tas.f90 -o $tempdir_prog/m_cdft_tas.o
ifort -c -O3 -ipo -pg -openmp -zero -module $tempdir_prog $tempdir_prog/m_sort.o m_cdft_pr.f90 -o $tempdir_prog/m_cdft_pr.o
ifort -O3 -ipo -pg -openmp -zero -module $tempdir_prog $tempdir_prog/m_sort.o $tempdir_prog/m_cdft_tas.o $tempdir_prog/m_cdft_pr.o $tempdir_prog/m_ymdsju.o $tempdir_prog/m_mask.o -I/opt/netcdf43/ifort/include $chemin_prog/prog_cor.f90 -L /opt/netcdf43/ifort/lib/ -lnetcdf -lnetcdff -o $tempdir_prog/prog_cor.e 


### Calcul des périodes
./calcul_period.e $nystart $nyend $moving $cor $period_file


#### Boucle sur les périodes
k=0
while read line  
do   
  k=$(echo "($k+1)" | bc)

  tmp_start_moving=$(echo ${line} | awk -F"-" '{print $1}' )
  tmp_end_moving=$(echo ${line} | awk -F"-" '{print $2}' )
  tmp_start_cor=$(echo ${line} | awk -F"-" '{print $3}' )  
  tmp_end_cor=$(echo ${line} | awk -F"-" '{print $4}' )

   start_moving=$(echo $tmp_start_moving | sed 's/ \{1,\}/ /g')
   end_moving=$(echo $tmp_end_moving | sed 's/ \{1,\}/ /g')
   start_cor=$(echo $tmp_start_cor | sed 's/ \{1,\}/ /g')
   end_cor=$(echo $tmp_end_cor | sed 's/ \{1,\}/ /g')

   if [ $tcal == "standard" -o $tcal == "gregorian" -o $tcal == "proleptic_gregorian" ];then
    start_cor_n=$start_cor'0101'
    end_cor_n=$end_cor'1231'
   fi
    if [ $tcal == "360_day" -o $tcal == "360d" -o $tcal == "360" ];then
    start_cor_n=$start_cor'0101'
    end_cor_n=$end_cor'1230'

    fi
    if [ $tcal == "365_day" -o $tcal == "365" -o $tcal == "365d" -o $tcal == "noleap" ];then
    start_cor_n=$start_cor'0101'
    end_cor_n=$end_cor'1231'

    fi


   echo "start moving : " $start_moving
   echo "end moving : " $end_moving
   echo "start cor : " $start_cor
   echo "end cor : " $end_cor

   if [ $project == "CMIP5" ];then
    corfile=$variable"Adjust_day_"$model"_"$RCP"_"$member"_"$start_cor_n"-"$end_cor_n"_raw.nc"
    fi
    if [ $project == "CORDEX" ];then
    corfile=$variable"Adjust_EUR-11_"$GCM"_"$RCP"_"$member"_"$model"_v1_day_"$start_cor_n"-"$end_cor_n"_raw.nc"
   fi

timedeb=$(date | awk -F' ' '{print $4}')
echo $timedeb


### Ecriture du script de correction 
echo PROCESSING MODEL $model

cat << EOF > $tempdir_prog/batch.$model.$variable.$k

#!/bin/sh
#PBS -l nodes=1:ppn=$nbproc
#PBS -l mem=$ramk 
module load cdo/1.6.8
module load netcdf4/4.3.3.1-ifort
module load gnu/4.4.7
ulimit -s 16000

timedeb=\$(date | awk -F' ' '{print \$4}')
echo \$timedeb

export OMP_NUM_THREADS=$nbproc

start_moving=$start_moving
end_moving=$end_moving
start_cor=$start_cor
end_cor=$end_cor
interpolated_path=$interpolated_path
interpolated_path_hist=$interpolated_path_hist
tempdir_data=$tempdir_data
project=$project
var=$variable
k=$k

echo \$k

echo "Data OBS REF"
if [ ! -e $tempdir_data/\$var\_data_model_$k.nc ]; then

if [[ \$start_moving -lt 2006 && \$end_moving -lt 2006 ]]; then

echo "historical"

echo \$interpolated_path_hist

cd \$interpolated_path_hist

list=\$( ls *.nc)
i=0
for file in \${list} ; do
    fileroot=\$(echo \${file} | awk -F".nc" '{print \$1}' )
     if [ \$project == "CMIP5" ];then
    dates=\$(echo \${fileroot} | awk -F"_" '{print \$6}' )
    fi
    if [ \$project == "CORDEX" ];then
    dates=\$(echo \${fileroot} | awk -F"_" '{print \$9}' )
    fi

    debfile=\$(echo \${dates} | awk -F"-" '{print \$1}' )
    endfile=\$(echo \${dates} | awk -F"-" '{print \$2}' )
  
    ydebfile=\$(echo \${debfile:0:4})
    yendfile=\$(echo \${endfile:0:4})
    
    echo \$ydebfile
    echo \$yendfile

if [[  \$ydebfile -le \$start_moving && \$yendfile -ge \$start_moving ]];then
    echo \$ydebfile 
    echo \$yendfile

     echo "File to use 1"
     i=\$(echo "(\$i+1)" | bc)
     cp \$interpolated_path_hist/\$file \$tempdir_data/\$var\_tmp\$i\_\$k.nc
  fi
if [[ \$ydebfile -gt \$start_moving && \$yendfile -le \$end_moving ]];then
    echo \$ydebfile 
    echo \$yendfile

     echo "File to use 2"
     i=\$(echo "(\$i+1)" | bc)
     cp \$interpolated_path_hist/\$file \$tempdir_data/\$var\_tmp\$i\_\$k.nc
  fi
if [[  \$ydebfile -gt \$start_moving && \$ydebfile -lt \$end_moving && \$yendfile -gt \$end_moving ]];then
    echo \$ydebfile 
    echo \$yendfile

     echo "File to use 3"
     i=\$(echo "(\$i+1)" | bc)
     cp \$interpolated_path_hist/\$file \$tempdir_data/\$var\_tmp\$i\_\$k.nc
  fi

done 
     ncrcat \$tempdir_data/\$var\_tmp*_\$k.nc \$tempdir_data/\$var\_temp_data_model_$k.nc
     echo " cdo selyear,\$start_moving/\$end_moving \$tempdir_data/\$var\_temp_data_model_$k.nc \$tempdir_data/\$var\_data_model_$k.nc"
     cdo selyear,\$start_moving/\$end_moving \$tempdir_data/\$var\_temp_data_model_$k.nc \$tempdir_data/\$var\_data_model_$k.nc

    rm -f \$tempdir_data/\$var\_tmp*_\$k.nc
    rm -f \$tempdir_data/\$var\_temp*_\$k.nc
fi

if [[ \$start_moving -lt 2006 && \$end_moving -gt 2005 ]]; then

echo "historical and RCP"

echo \$interpolated_path_hist

cd \$interpolated_path_hist

list=\$( ls *.nc)
i=0
for file in \${list} ; do
    fileroot=\$(echo \${file} | awk -F".nc" '{print \$1}' )
    if [ \$project == "CMIP5" ];then
    dates=\$(echo \${fileroot} | awk -F"_" '{print \$6}' )
    fi
    if [ \$project == "CORDEX" ];then
    dates=\$(echo \${fileroot} | awk -F"_" '{print \$9}' )
    fi

    debfile=\$(echo \${dates} | awk -F"-" '{print \$1}' )
    endfile=\$(echo \${dates} | awk -F"-" '{print \$2}' )
    ydebfile=\$(echo \${debfile:0:4})
    yendfile=\$(echo \${endfile:0:4})
    
if [[  \$ydebfile -le \$start_moving && \$yendfile -ge \$start_moving ]];then
   echo \$ydebfile 
   echo \$yendfile

     echo "File to use 1"
     i=\$(echo "(\$i+1)" | bc)
     cp \$interpolated_path_hist/\$file \$tempdir_data/\$var\_tmp\$i\_\$k.nc
  fi
if [[ \$ydebfile -gt \$start_moving && \$yendfile -le \$end_moving ]];then
   echo \$ydebfile 
   echo \$yendfile

     echo "File to use 2"
     i=\$(echo "(\$i+1)" | bc)
     cp \$interpolated_path_hist/\$file \$tempdir_data/\$var\_tmp\$i\_\$k.nc
  fi
if [[  \$ydebfile -gt \$start_moving && \$ydebfile -lt \$end_moving && \$yendfile -gt \$end_moving ]];then
   echo \$ydebfile 
   echo \$yendfile

     echo "File to use 3"
     i=\$(echo "(\$i+1)" | bc)
     cp \$interpolated_path_hist/\$file \$tempdir_data/\$var\_tmp\$i\_\$k.nc
  fi

done 
cd \$interpolated_path

list=\$( ls *.nc)
for file in \${list} ; do
    fileroot=\$(echo \${file} | awk -F".nc" '{print \$1}' )
     if [ \$project == "CMIP5" ];then
    dates=\$(echo \${fileroot} | awk -F"_" '{print \$6}' )
    fi
    if [ \$project == "CORDEX" ];then
    dates=\$(echo \${fileroot} | awk -F"_" '{print \$9}' )
    fi

    debfile=\$(echo \${dates} | awk -F"-" '{print \$1}' )
    endfile=\$(echo \${dates} | awk -F"-" '{print \$2}' )
    ydebfile=\$(echo \${debfile:0:4})
    yendfile=\$(echo \${endfile:0:4})
    
if [[  \$ydebfile -le \$start_moving && \$yendfile -ge \$start_moving ]];then
   echo \$ydebfile 
   echo \$yendfile

     echo "File to use 1"
     i=\$(echo "(\$i+1)" | bc)
     cp \$interpolated_path/\$file \$tempdir_data/\$var\_tmp\$i\_\$k.nc
  fi
if [[ \$ydebfile -gt \$start_moving && \$yendfile -le \$end_moving ]];then
   echo \$ydebfile 
   echo \$yendfile

     echo "File to use 2"
     i=\$(echo "(\$i+1)" | bc)
     cp \$interpolated_path/\$file \$tempdir_data/\$var\_tmp\$i\_\$k.nc
  fi
if [[  \$ydebfile -gt \$start_moving && \$ydebfile -lt \$end_moving && \$yendfile -gt \$end_moving ]];then
    echo \$ydebfile 
    echo \$yendfile

     echo "File to use 3"
     i=\$(echo "(\$i+1)" | bc)
     cp \$interpolated_path/\$file \$tempdir_data/\$var\_tmp\$i\_\$k.nc
  fi
done 

     ncrcat \$tempdir_data/\$var\_tmp*_\$k.nc \$tempdir_data/\$var\_temp_data_model_$k.nc
     echo " cdo selyear,\$start_moving/\$end_moving \$tempdir_data/\$var\_temp_data_model_$k.nc \$tempdir_data/\$var\_data_model_$k.nc"
     cdo selyear,\$start_moving/\$end_moving \$tempdir_data/\$var\_temp_data_model_$k.nc \$tempdir_data/\$var\_data_model_$k.nc

    rm -f \$tempdir_data/\$var\_tmp*_\$k.nc
    rm -f \$tempdir_data/\$var\_temp*.nc
fi

if [[ \$start_moving -gt 2005 && \$end_moving -gt  2005 ]]; then

echo "RCP"
cd \$interpolated_path/
list=\$( ls *.nc)
i=0
for file in \${list} ; do
    fileroot=\$(echo \${file} | awk -F".nc" '{print \$1}' )
    
    if [ \$project == "CMIP5" ];then
    dates=\$(echo \${fileroot} | awk -F"_" '{print \$6}' )
    fi
    if [ \$project == "CORDEX" ];then
    dates=\$(echo \${fileroot} | awk -F"_" '{print \$9}' )
    fi
    
debfile=\$(echo \${dates} | awk -F"-" '{print \$1}' )
    endfile=\$(echo \${dates} | awk -F"-" '{print \$2}' )
    ydebfile=\$(echo \${debfile:0:4})
    yendfile=\$(echo \${endfile:0:4})
    

if [[  \$ydebfile -le \$start_moving && \$yendfile -ge \$start_moving ]];then
   echo \$ydebfile 
   echo \$yendfile

     echo "File to use 1"
     i=\$(echo "(\$i+1)" | bc)
     cp \$interpolated_path/\$file \$tempdir_data/\$var\_tmp\$i\_\$k.nc
  fi
if [[ \$ydebfile -gt \$start_moving && \$yendfile -le \$end_moving ]];then
   echo \$ydebfile 
   echo \$yendfile

     echo "File to use 2"
     i=\$(echo "(\$i+1)" | bc)
     cp \$interpolated_path/\$file \$tempdir_data/\$var\_tmp\$i\_\$k.nc
  fi
if [[  \$ydebfile -gt \$start_moving && \$ydebfile -lt \$end_moving && \$yendfile -gt \$end_moving ]];then
   echo \$ydebfile 
   echo \$yendfile

     echo "File to use 3"
     i=\$(echo "(\$i+1)" | bc)
     cp \$interpolated_path/\$file \$tempdir_data/\$var\_tmp\$i\_\$k.nc
  fi
done 
     ncrcat \$tempdir_data/\$var\_tmp*_\$k.nc \$tempdir_data/\$var\_temp_data_model_$k.nc
     echo " cdo selyear,\$start_moving/\$end_moving \$tempdir_data/\$var\_temp_data_model_$k.nc \$tempdir_data/\$var\_data_model_$k.nc"
     cdo selyear,\$start_moving/\$end_moving \$tempdir_data/\$var\_temp_data_model_$k.nc \$tempdir_data/\$var\_data_model_$k.nc

    rm -f \$tempdir_data/\$var\_tmp*_\$k.nc
    rm -f \$tempdir_data/\$var\_temp*.nc

fi
elif [ -f $tempdir_data/\$var\_data_model_$k.nc ]; then
 echo "$tempdir_data/\$var\_data_model_$k.nc deja traiter"
fi

timefin=\$(date | awk -F' ' '{print \$4}')
echo \$timefin

if [ ! -e \$tempdir_data/\$var\_data_model_$k\_out.nc ]; then
echo 'Préparation fichier output'
cdo selyear,\$start_cor/\$end_cor \$tempdir_data/\$var\_data_model_$k.nc \$tempdir_data/\$var\_data_model_$k\_out.nc
elif [ -f \$tempdir_data/\$var\_data_model_$k\_out.nc ]; then
echo 'Fichier Préparé'
fi

if [ ! -e $corrected_path/$corfile ]; then
echo 'Extraction fichier output'
ncks -x -v $variable \$tempdir_data/\$var\_data_model_$k\_out.nc $corrected_path/$corfile
ncks -A -x $tempdir_data/rcp_meta_data.nc $corrected_path/$corfile
elif [ -f $corrected_path/$corfile ]; then
echo 'Fichier output Pret'
fi





cd \$tempdir_prog

echo '\$tempdir_prog/prog_cor.e $variable $tempdir_data/\$var\_data_model_ref.nc $tempdir_data/\$var\_obs_reference.nc $tempdir_data/\$var\_data_model_$k.nc $corrected_path/corfile_para.nc $nystart $nyend $nyrefstart $nyrefend $icaltype $moving $cor $k $ram $Ndimx $Ndimy'
$tempdir_prog/prog_cor.e $variable $tempdir_data/\$var\_data_model_ref.nc $tempdir_data/\$var\_obs_reference.nc $tempdir_data/\$var\_data_model_$k.nc $corrected_path/$corfile $nystart $nyend $nyrefstart $nyrefend $icaltype $moving $cor $k $ram $Ndimx $Ndimy


EOF

########### 
 chmod +x $tempdir_prog/batch.$model.$variable.$k

fileout=$corrected_path$corfile
echo $fileout

#### lancement du job de correction 

 if [ ! -e $fileout ]; then
       echo "$fileout a traiter"
	qsub -l nodes=1:ppn=$nbproc -l mem=$ram\gb -l vmem=$vram\gb  -q std $tempdir_prog/batch.$model.$variable.$k
 elif [ -f $fileout ]; then
 	echo "$fileout deja traiter"
 fi


done < $period_file

msg "INFO" "correction_cdft.sh complete"
