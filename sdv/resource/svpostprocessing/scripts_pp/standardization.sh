#!/bin/bash -e

# Description
#   This script apply standardization.f90,
#
# Notes
#
# Usage
#   ./standardization.sh <PROJECT> <PATH> <VAR>
#
# Input
#   The project ID
#   <PROJECT>
#   An atomic dataset full path as the directory that contains corrected NetCDF files
#   <PATH>  : /prodigfs/project/<PROJECT>/bias-adjusted/<downstream_DRS>/
#   <VAR> : Variable
#   
#

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

        # /prodigfs/esgf/process/<PROJECT>/bias-adjusted/<downstream_DRS>
        "--variable_path")  shift; corrected_path="${1}"        ;;

        # Variable
        "--variable") shift; variable="${1}"   ;;
       
        # Path this script is from
        "--script_dir") shift;  scripts_path="${1}"   ;;


    esac
    shift
done


chemin=${scripts_path}
chemin_prog="$chemin/standardization/"
chemin_config="$chemin/standardization/"
chemin_tables="$chemin/standardization/Tables/day/"
chemin_config_cor="$chemin/correction_cdft/config_cdft/"

echo $project
echo $corrected_path
echo $variable
varcor=$variable'Adjust'

echo $varcor

file_config=$chemin_config_cor/obs_ref_$project.json

obsfile=$(cat $file_config | $chemin_prog/jq-1.5  '.variable[] | select(.name=="'$variable'") | .file' | awk -F"\"" '{print $2}')
nyrefstart=$(cat $file_config | $chemin_prog/jq-1.5  '.variable[] | select(.name=="'$variable'") | .debut' | awk -F"\"" '{print $2}')
nyrefend=$(cat $file_config | $chemin_prog/jq-1.5  '.variable[] | select(.name=="'$variable'") | .fin' | awk -F"\"" '{print $2}')

bc_observation_id=$(cat $file_config | $chemin_prog/jq-1.5  '.variable[] | select(.name=="'$variable'") | .bc_observation_id' | awk -F"\"" '{print $2}')
bc_observation=$(cat $file_config | $chemin_prog/jq-1.5  '.variable[] | select(.name=="'$variable'") | .bc_observation' | awk -F"\"" '{print $2}')


bc_method_id=$(cat $file_config | $chemin_prog/jq-1.5 '.methode.bc_method_id' | awk -F"\"" '{print $2}')
bc_method=$(cat $file_config | $chemin_prog/jq-1.5 '.methode.bc_method' | awk -F"\"" '{print $2}')
institute_id=$(cat $file_config | $chemin_prog/jq-1.5 '.methode.institute_id' | awk -F"\"" '{print $2}')
institute=$(cat $file_config | $chemin_prog/jq-1.5 '.methode.institute' | awk -F"\"" '{print $2}')

contact=$(cat $file_config | $chemin_prog/jq-1.5 '.methode.contact' | awk -F"\"" '{print $2}')
refs=$(cat $file_config | $chemin_prog/jq-1.5 '.methode.refs' | awk -F"\"" '{print $2}')
comment=$(cat $file_config | $chemin_prog/jq-1.5 '.methode.comment' | awk -F"\"" '{print $2}')

bc_period="$nyrefstart-$nyrefend"


echo $nyrefstart,$nyrefend

# --------- main --------- #

msg "INFO" "standardization.sh started"


umask g+w


### load module ##########
module purge
module load uuid/1.6.2
module load netcdf4/4.3.3.1-gfortran
module load cmor/2.9.1-gfortran


cd $chemin_prog


echo $corrected_path

cd $corrected_path

list=$( ls *_raw.nc)

for file in ${list} ; do
    fileroot=$(echo ${file} | awk -F".nc" '{print $1}' )

 if [ $project == "CMIP5" ];then
	RCP=$(echo $file | awk -F"_" '{print $4}' )
	model=$(echo $file | awk -F"_" '{print $3}' )
        member=$(echo $file | awk -F"_" '{print $5}' )
        dates=$(echo $file | awk -F"_" '{print $6}')
    fi
    if [ $project == "CORDEX" ];then
	RCP=$(echo $file | awk -F"_" '{print $4}' )
	model=$(echo $file | awk -F"_" '{print $6}' )
        member=$(echo $file | awk -F"_" '{print $5}' )
        GCM=$(echo $file | awk -F"_" '{print $3}' )
        dates=$(echo $file | awk -F"_" '{print $9}')
        dom=$(echo $file | awk -F"_" '{print $2}')
        version=$(echo $file | awk -F"_" '{print $7}')
    fi

tempdir_prog=$chemin_prog/tmp/$model/$file/
mkdir -p $tempdir_prog


cp $chemin_config/table_$project.def $tempdir_prog/table.def
dump_file=$tempdir_prog/dump.txt

ncdump -h $corrected_path/$file > $dump_file


time_unit=$(grep time:units $dump_file | awk -F"\"" '{print $2}')
input_institute_id=$(grep institute_id $dump_file | awk -F"\"" '{print $2}')
input_institute=$(grep institution $dump_file | awk -F"\"" '{print $2}')
calendar=$(grep calendar $dump_file | awk -F"\"" '{print $2}')
sourc=$(grep "source" $dump_file | awk -F"\"" '{print $2}')
experiment_id=$(grep ":experiment_id" $dump_file | awk -F"\"" '{print $2}')
input_tracking_id=$(grep "tracking_id" $dump_file | awk -F"\"" '{print $2}')


if [ $project == "CMIP5" ];then
echo $project
realization=$(grep  "realization" $dump_file |  awk -F"=" '{print $2}' | awk -F";" '{print $1}' )
physics_version=$(grep  "physics_version" $dump_file | awk -F"=" '{print $2}' | awk -F";" '{print $1}' )
initialization_method=$(grep  "initialization_method" $dump_file | awk -F"=" '{print $2}' | awk -F";" '{print $1}' )
parent_experiment_id=$(grep  "parent_experiment_id" $dump_file | awk -F"\"" '{print $2}')
forcing=$(grep "forcing" $dump_file | awk -F"\"" '{print $2}')
branch_time=$(grep "branch_time" $dump_file | awk -F"=" '{print $2}' | awk -F";" '{print $1}')
parent_rip=$(grep "parent_experiment_rip" $dump_file | awk -F"\"" '{print $2}')
         
fi
 if [ $project == "CORDEX" ];then
echo $project
realization=$(grep  "realization" $dump_file |  awk -F"=" '{print $2}' | awk -F";" '{print $1}' )
physics_version=$(grep  "physics_version" $dump_file | awk -F"=" '{print $2}' | awk -F";" '{print $1}' )
initialization_method=$(grep  "initialization_method" $dump_file | awk -F"=" '{print $2}' | awk -F";" '{print $1}' )
CORDEX_domain=$(grep  "CORDEX_domain" $dump_file | awk -F"\"" '{print $2}')
rcm_version_id=$(grep  "rcm_version_id" $dump_file | awk -F"\"" '{print $2}')
driving_model_ensemble_member=$(grep  "driving_model_ensemble_member" $dump_file | awk -F"\"" '{print $2}')
driving_experiment_name=$(grep  "driving_experiment_name" $dump_file | awk -F"\"" '{print $2}')
forcing=$(grep "forcing" $dump_file | awk -F"\"" '{print $2}')
fi
#=$(grep  "" $dump_file | awk -F"\"" '{print $2}')
#=$(grep  $dump_file | awk -F"\"" '{print $2}')



cat << EOF > $tempdir_prog/config.def
#
# parameters utilised by cmor_setup
#
inpath=$chemin_tables
file_action=12
verbosity=1
exit_control=1
force_time=true
force_timebnds=true
#
# output directory
repertoire=$corrected_path
#
# specific parameters
#
model_id=$model
source=$sourc 
input_institute_id=$input_institute_id
input_tracking_id=$input_tracking_id
calendar=$calendar 
time_units=$time_unit
#
# common parameters
#
project=$project-Adjust
product=bias-adjusted-output
frequency=day
experiment_id=$experiment_id
realization=$realization
forcing=$forcing
physics_version=$physics_version
initialization_method=$initialization_method
EOF


if [ $project == "CMIP5" ];then
cat << EOF >> $tempdir_prog/config.def
parent_experiment_id=$parent_experiment_id
project_id="CMIP5-Adjust"
parent_experiment_rip=$parent_rip
branch_time=$branch_time
EOF

fi
 
 if [ $project == "CORDEX" ];then
cat << EOF >> $tempdir_prog/config.def
driving_model_id=$GCM
driving_model_ensemble_member=$driving_model_ensemble_member
driving_experiment_name=$driving_experiment_name
CORDEX_domain=$CORDEX_domain
rcm_version_id=$rcm_version
project_id="CORDEX-Adjust"
EOF
fi

cat << EOF >> $tempdir_prog/config.def
#### parametres de la correction
institute_id=$institute_id
bc_method_id=$bc_method_id
bc_observation_id=$bc_observation_id
bc_period=$bc_period
#
# long specific parameters
#
input_institute=$input_institute
#
# long common parameters
#
institute=$institute
#
bc_method=$bc_method

bc_observation=$bc_observation
contact=$contact

refs=$ref
comment=$comment

EOF

echo "Compile fortran code"


gfortran -ffree-line-length-none -g -DCOLOREDOUTPUT -I /opt/uuid-1.6.2/include -I/opt/netcdf43/gfortran/include -I/opt/cmor-2.9.1/include/cdTime -I /usr/include/udunits2/ -I/opt/cmor-2.9.1/include $chemin_prog/standardization.f90 -L /opt/uuid-1.6.2/lib -luuid -L/opt/cmor-2.9.1/lib -lcmor -L /opt/netcdf43/gfortran/lib/ -lnetcdf -lnetcdff -ludunits2 -o $tempdir_prog/standardization.e

if [ $project == "CMIP5" ];then
    outcmor=$varcor'_day_'$model'_'$RCP'_'$member'_'$dates'.nc'
    outputfile=$varcor'_WRL-50i_'$model'_'$RCP'_'$member'_v1-'$bc_method_id'-'$bc_observation_id'-'$bc_period'_day_'$dates'.nc'
    fi
if [ $project == "CORDEX" ];then
    outcmor=$varcor'_day_'$model'_'$RCP'_'$member'_'$dates'.nc'
    outputfile=$varcor'_'$dom'_'$GCM'_'$RCP'_'$member'_'$model'_'$version'-'$bc_method_id'-'$bc_observation_id'-'$bc_period'_day_'$dates'.nc'
fi



cat << EOF > $tempdir_prog/batch_cmor_$file.sh
#!/bin/sh
### load module ##########
module purge
module load uuid/1.6.2
module load netcdf4/4.3.3.1-gfortran
module load cmor/2.9.1-gfortran

cd $tempdir_prog/
$tempdir_prog/standardization.e $corrected_path/$file $varcor

cd $corrected_path/
mv $outcmor $outputfile


EOF

fileout=$corrected_path$outputfile
cd $tempdir_prog/

chmod +x  $tempdir_prog/batch_cmor_$file.sh

 if [ ! -e $fileout ]; then
       echo "$fileout a traiter"

	qsub -l nodes=1:ppn=4 -l mem=8gb -l vmem=12gb  -q std $tempdir_prog/batch_cmor_$file.sh

 elif [ -f $fileout ]; then
 	echo "$fileout deja traiter"
 fi
 done 


msg "INFO" "ecriture_cmor.sh complete"
