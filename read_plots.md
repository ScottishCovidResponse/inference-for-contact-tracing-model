# How to Read the Analysis Results

By running `src/analyse_parameters.py` we obtain multiple scatter plots to understand
the relationship between input parameters and output by `Contact-Tracing-Model`.
These plots are provided by [SHapley Additive exPlanations (SHAP)](https://github.com/slundberg/shap),
and you can read [here](./interprete_analysis.md)

in this document we explain how to read the resulting PDF files.
 
The essential formulas of SHAP first appeared in
the [NeurIPS paper](http://papers.nips.cc/paper/7062-a-unified-approach-to-interpreting-model-predictions),
while here we provide a simplified explanation with omitting proofs etc.

## Reading the Plots

Let us take [a 10,000-sample example for dense homogeneous contacts data](./example_result/homogeneous_contacts_dense/total_death.n10k.pdf). The analysis report PDF file has the following pages.  

**Page 1. Scatter plot to confirm the predictive accuracy of the non-linear regression model.** 

We equally splitted the 10,000 samples into 5,000 training and 5,000 test ones. Then we fitted a regression model <img src="https://render.githubusercontent.com/render/math?math=\widehat{f}: {\mathbb R}^d\to{\mathbb R}"> to the training samples, and plotted <img src="https://render.githubusercontent.com/render/math?math=\widehat{f}(\boldsymbol{x}_t)"> versus
<img src="https://render.githubusercontent.com/render/math?math=y_t"> 
where <img src="https://render.githubusercontent.com/render/math?math=(\boldsymbol{x}_t, y_t)_{t=1}^n">
is the collection of 5,000 test samples. You can confirm high accuracy between the predictions and outputs
while there are statistical errors that are partly by model errors (bias) and partly by estimation errors (variance). 
 
**Page 2. Over-all ranking of important parameters.**

By aggregating the SHAP values across all test samples and
based on their magnitudes, we can understand which variables are the most and second or third most important.
The blue points represent the data points of low SHAP values while the red points are the ones with high SHAP values. 
In this example, we have the following observations.

- `random_infection_rate` is most influential to the output. Too high value of  `random_infection_rate` results in 
high positive SHAP values that lead unrealistically high number of death. Hence we must set this parameter a reasonably small value.
- The next important parameter is `exposure_probability4unit_contact`. In our exposure model,
it is assumed that probability of getting exposed is a monotonically increasing function of contact weight,
where the boundary condition is that no contact corresponds to zero exposure probability. 
`exposure_probability4unit_contact` corresponds to the probability of exposure when contact weight is one,
and this parameter determines the overall level of exposure. It is natural to see that small/large values of this parameter
result in negative/positive SHAP values, respectively. This parameter mainly determines the scale of overall infection.
- The third most important parameter is `exposure_exponent` which gives the sensitivity between contact strength and exposure probability. The high the exponent is, the more the exposure probability drastically increases by increase of contact weight. It is also natural to see the importance of this parameter, because it enables to interprete
the abstractly defined contact weight by a more explicit terminology of exposure probability.
- We can see the influence of other parameters as well. The influence towards the entire death, however,
is much smaller than the first three parameters. This implies that we must first tune the first three parameters
into an appropriate level, and next we should fine tune the remaining parameters to match the entire output time-series.

**Pages 3-31. SHAP dependence plots.**

Watching how SHAP values are concretely varying across the samples provides more intuitive and detailed
understanding than just looking at numerical importance values. To this end, one can have a scatter plot
between the values of a chosen input variable and their corresponding SHAP values. This is similar
to the ordinary scatter plot between input and output samples, but is much more superior one, because
influence of the other input variables are neutralised in SHAP values. In other words, you can
see the effective contribution purely by that focused input variable, after removing the influence of other input
variables and output noise that exists in the raw data.

While such plots between one input variable and its SHAP value, the SHAP dependence plots maximally exploit
the efficiency of human eyes when using 2D plots. Remember that our function 
<img src="https://render.githubusercontent.com/render/math?math=\widehat{f}: {\mathbb R}^d\to{\mathbb R}">
is general non-linear, and hence can involve some interaction terms across different input variables.
For example, if the underlying true function <img src="https://render.githubusercontent.com/render/math?math=f: {\mathbb R}^d\to{\mathbb R}"> is <img src="https://render.githubusercontent.com/render/math?math=f(X)=a %2B b \cos 2\pi X_1 %2B c X_2^2">,
then having input-vs-SHAP plots independently
for each input variable of <img src="https://render.githubusercontent.com/render/math?math=(X_1, X_2)"> is sufficient
for watching the structure.
If it were
<img src="https://render.githubusercontent.com/render/math?math=f(X)=a %2B b X_2 \cos 2\pi X_1">, however,
then the sinusoidal relationship between the input <img src="https://render.githubusercontent.com/render/math?math=X_1">
and the output can be inverted depending on the sign of 
another input <img src="https://render.githubusercontent.com/render/math?math=X_2">.
So just watching the *marginal* non-linear relationship between the input and output is insufficient
for some complex underlying functions.
Then the next question that arises is, which is the most influential other variable
for the chosen input variable, in the sense that the relationship between the chosen input and output
is most drastically changed?

In SHAP dependence plots, that most influential other input variable is automatically chosen
for each chosen input variable. In the example of `population_distribution_1`  at page 4, which
means the ratio of population of age group 1, the chosen other variable is `exposure_exponent`.
When `exposure_exponent` is low, i.e., exposure probability is relatively uniform regardless the strength of contacts,
the SHAP value of  `population_distribution_1` is almost always close to zero. When `exposure_exponent` is high,
however, high value of `population_distribution_1` that means large population of young generations
leads negative SHAP values. So it could represent that
Regions having many young people experience less numbers of death than regions having elderly generations
when strength of contacts much influences the exposure probability.
Note that these implications should be ensured by increasing the sample size in drawing random input parameters
and the corresponding outputs by `Contact-Tracing-Model`. Some implications
are just outcomes of noise by small sample size.

For more interesting interactions between two input variables,
please refer to the pages 29 and 30. You can see that relationship between `exposure_probability4unit_contact`
or `exposure_exponent` and the output can quite depend on the value of `random_infection_rate`. When
`random_infection_rate` is high, the two exposure-related parameters are less influential. This
complexity is understandable, because 
contact-based exposure and random infection without contacts cannot be discriminated
from the observable numbers of deaths or infections. Estimation of these important parameters
have complex interactions and hence full joint estimation of the three parameters is essential
unless you decide to use a small fixed value as `random_infection_rate`.

You can refer to other examples
that have different contacts and/or have smaller or larger sample sizes,
in the sub directories under [example_result](./example_result) directory.