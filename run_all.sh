#!/bin/sh

# Settings: an example below gives a sensitivity analysis based on 
# 10*100=1000 random pairs of input parameters (e.g., disease parameters) and output metrics (e.g., total n_deaths)
n_tasks=10
n_simulations_per_task=100
workdir=${HOME}/covid-19/sensitivity1000

# Parallel sampling of parameters and results
sbatch --wait --array=1-${n_tasks} slurm_draw_parameters ${workdir} ${n_simulations_per_task}

# Unifying the results into CSV files
dirlistfile=${workdir}/workdirlist.txt
rm -f ${dirlistfile}
txtlist=`find ${workdir} -name workdirlist.txt`
touch ${dirlistfile}
for txt in ${txtlist}
do
	cat ${txt} >> ${dirlistfile}
done
python src/unify_draws.py ${dirlistfile} ${workdir}

# Draw SHAP plots for the final sensitivity analysis
python src/analyse_sensitivity.py ${workdir} ${workdir}
