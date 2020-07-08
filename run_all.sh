#!/bin/sh

# Settings
n_tasks=10
n_simulations_per_task=100
workdir=${HOME}/covid-19/trial

# Main jobs
sbatch --wait --array=0-${n_tasks}:1 slurm_draw_parameters ${workdir} ${n_simulations_per_task}

dirlistfile=${workdir}/workdirlist.txt
rm -f ${dirlistfile}
touch ${dirlistfile}
ls ${workdir}/job_*_* > ${dirlistfile}

python src/unify_draws.py ${dirlistfile} ${workdir}

python src/analyse_sensitivity.py ${workdir} ${workdir}

