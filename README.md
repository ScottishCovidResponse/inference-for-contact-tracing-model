# inference-for-contact-tracing-model

Sensitivty analysis for Contact Tracing Model in RAMP COVID-19 Project.

Randomly generate samples of model parameters, and perform
regression analysis between the input parameters and output time-series of SEIR.
Implications from that regression analysis are visualised with SHAP (SHapley Additive exPlanations).

# Requirement

numpy, scipy, pandas, scikit-learn, docopt, shap, matplotlib

# Usage

`src/draw_parameters.py` is a command-line program to
generate samples of model parameters and corresponding model output time-series.
These samples should be fed into `src/analyse_sensitivity.py`
to understand which parameter strongly affects which aspect of the output time-series. When generating large samples in parallel at DiRAC cluster,
`src/unify_draws.py` integrates multiple sample files into one file.

Simply executing each script provides a list of command-line options.

```
python draw_parameters.py
python unify_draws.py  
python analyse_sensitivity.py 
```

# Example for Single Node Machine

Make sure that you installed all of the required python packages and correctly set `${PYTHONPATH}`. Then
by the commands below you get summary results as `total_death.pdf`, `peak_severity.pdf`, and
`relative_importance.csv` under the `${HOME}/covid-19/sensitivity1000/` directory.
The two PDF files provide various [SHAP](https://github.com/slundberg/shap) plots for understanding the non-linear dependence between each parameter and two metrics: the total number of deaths in the whole period and 
the peak of the number of severe infections defined as the maximum of severity in output time-series.
The CSV file `relative_importance.csv` shows numerical values of parameter importance in general.
The underlying regression models are saved as `total_death.model` and `peak_severity.model`.
These sensitivity analyses are based on 1,000 samples of input parameters and output metrics,
and hence robustness of the implications should be ensured by larger sample-size experiments.

```
python src/draw_parameters.py ~/covid-19/sensitivity1000 \
	--job-name=sensitivity1000 \
	--n-simulations=1000 \
   --java-project-dir=~/git/Contact-Tracing-Model
  
python analyse_sensitivity.py ~/covid-19/sensitivity1000 ~/covid-19/sensitivity1000
```

Internally, `src/draw_parameters.py` 
generate disease and population settings, while copying the rest information from `~/git/Contact-Tracing-Model/input`,
and save them into the specified directory `~/covid-19/sensitivity1000` that also stores all of the intermediate
outcomes during the simulation. Always change the work directory name When trying a different input setting.

# Example in Distributed Computing Environment

In order to ensure the robustness of implications, we encourage to watch the results whose sample sizes
are 1,000, 10,000, and 100,000. Specifically for the DiRAC cluster, we implemented scripts for parallel
simulations using SLURM. You can refer to [this document](run_at_DiRAC.md) for the details.


