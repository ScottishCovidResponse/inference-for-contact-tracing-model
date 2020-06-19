# inference-for-contact-tracing-model

Sensitivty analysis for Contact Tracing Model in RAMP COVID-19 Project.

Randomly generate samples of model parameters, and perform
regression analysis between the input parameters and output time-series of SEIR.
Implications from that regression analysis are visualised with SHAP (SHapley Additive exPlanations).

# Requirement

numpy, scipy, pandas, scikit-learn, docopt, shap, matplotlib

# Usage

`uk.co.ramp.exec.draw_parameters` is a command-line program to
generate samples of model parameters and corresponding model output time-series.
These samples should be fed into `uk.co.ramp.exec.analyse_sensitivity`
to understand which parameter strongly affects which aspect of the output time-series.

Simply executing each script provides a list of command-line options.

```
python draw_parameters.py 
python analyse_sensitivity.py 
```

# Example

Below you get summary results as `relative_importance.csv`,
`total_death.pdf`, and `total_severity.pdf` under the `${HOME}/covid-19/result/` directory.
The CSV file `relative_importance.csv` shows a global information about which variables are most 
influential in general, details about the impact by each variable is further visualised 
in the 2 PDF files. The underlying regression models are saved as `total_death.model` and `total_severity.model`.


```
python draw_parameters.py ~/covid-19/result --n-simulations=1000 \
  --java-project-dir=~/git/Contact-Tracing-Model \
  --tmp-dir=~/covid-19/tmp
  
python analyse_sensitivity.py ~/covid-19/result ~/covid-19/result
```
