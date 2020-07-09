# Distributed Running on Drawing Parameters and Outputs

After drawing one instance of input parameters, simulation by using these random parameters is computationally
intensive when you need 10,000 to 100,000 samples. Hence we parallelised this draw-and-simulation
part by exploiting SLURM. 

If your interest is just obtaining large-sample results, then all you need to do is
to just edit the variables `n_tasks`, `n_simulations_per_task`, and `workdir` in [run_all.sh](run_all.sh)
and executing it. An example below provides 10,000-sample results by using 10 nodes, where 1000 samples per node are sequentially generated. 

```
# Settings: an example below gives a sensitivity analysis based on 
# 100*100=1000 random pairs of input parameters (e.g., disease parameters) and output metrics (e.g., total n_deaths)
n_tasks=10
n_simulations_per_task=1000
workdir=${HOME}/covid-19/sensitivity10000
```

What `run_all.sh` is doing is relatively simple and you can further edit [slurm_draw_parameters](slurm_draw_parameters).
if you need to adjust into your environment. As seen below, the first argument of [slurm_draw_parameters](slurm_draw_parameters) is the directory into which you want to store the results. The second argument
is the number of samples sequentially generated in each node. Note that every node adopts a different random seed
and each sequential sample also has a different seed. Hence you do not need to worry about the randomness
of the results.

```
sbatch --wait --array=1-${n_tasks} slurm_draw_parameters ${workdir} ${n_simulations_per_task}
```

Inside [slurm_draw_parameters](slurm_draw_parameters), as seen in the line below,  
each node creates a unique sub-directory under the main `${workdir}` in order to ensure that there is no 
dead lock and/or over-writing of output files. 
In the following calling of `src/draw_parameters.py`, 
the random draws of input parameters and simulated output metrics are stored into this sub-directory
for each parallel job.

```
work_dir="${top_work_dir}/job_${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}"
```

In order to proceed the entire analysis, next we must concatenate all of these results across all nodes.
Let us note that each job creates a text file `workdirlist.txt` that provides the list of all directories
that store `input_parameter_samples.csv` and `output_loss_samples.csv`, which contain
the actual values of input parameters and output metrics, respectively. One row in these two CSV files
corresponds to one sample of input parameters and output metrics, and each column corresponds to one parameter 
variable and one output metric.

Then in the following lines in [run_all.sh](run_all.sh), the list of directories are saved in a text file
`workdirlist.txt` for each of the job. 
Finally, `src/unify_draws.py` reads all of the CSV files located by this unified list of data directories,
and writes one unified `input_parameter_samples.csv` and `output_loss_samples.csv`
at the root of `${workdir}` in order to enable the application of `src/analyse_parameters.py`.

```
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
```



