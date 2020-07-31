# How the Efficient Frontier is Computed and How to Read the Policy Recommendations

By running `src/policy_frontier.py` we obtain an efficient frontier between two focused metrics,
which by default are the total number of days in isolation and the total number of deaths.
Each dot in `${prefix}.tradeoffs.pdf` corresponds to the vector of all policy parameters,
and the x-axis and y-axis scores for this vector is computed by many samples of random disease parameters.

This document first provides how these metrics are computed, whose understanding is
essential for meaningful recommendation of policies. Then we discuss how to read the resulting CSV files
`${prefix}.average_case_policies.csv` and `${prefix}.worst_case_policies.csv`.

## Definition of the Frontiers

Remember that the final loss metric such as the total number of deaths
is determined by population, disease, and policy parameters. The government can control
the parameters of isolation and tracing policies while cannot control the population and disease parameters.
In this document, the controllable parameters are called 'policy parameters',
and the uncontrollable ones are called 'environment parameters'.

We denote the space of feasible policy parameters by
<img src="https://render.githubusercontent.com/render/math?math=\Pi\subseteq {\mathbb R}^{d_{policy}}">.
Then let 
<img src="https://render.githubusercontent.com/render/math?math=X_{policy}\in \Pi">
and 
<img src="https://render.githubusercontent.com/render/math?math=X_{env}\in {\mathbb R}^{d_{env}}">
be random variables of the policy and environment parameters, respectively.
The sum of two dimensionalities equals to the number of all parameters in Contact Tracing Model,
i.e., <img src="https://render.githubusercontent.com/render/math?math=d_{policy} %2B d_{env}\equiv d">.
Then let <img src="https://render.githubusercontent.com/render/math?math=Y_1\in {\mathbb R}">
and 
<img src="https://render.githubusercontent.com/render/math?math=Y_2\in {\mathbb R}">
be random variables of the focused output metrics, such as the total isolation days and deaths. 
There exist two functions 
<img src="https://render.githubusercontent.com/render/math?math=f, g: {\mathbb R}^d\to{\mathbb R}">
such that
<img src="https://render.githubusercontent.com/render/math?math=Y_1= f(X_{policy},X_{env}) %2B \varepsilon_1"> and
<img src="https://render.githubusercontent.com/render/math?math=Y_2= g(X_{policy},X_{env}) %2B \varepsilon_2">
where
<img src="https://render.githubusercontent.com/render/math?math=\varepsilon_1"> and 
<img src="https://render.githubusercontent.com/render/math?math=\varepsilon_2"> are
zero-mean random noise variables.

Let <img src="https://render.githubusercontent.com/render/math?math=p(X_{env})">
be the distribution of environment parameters, in order to represent the uncertainty of environment.
If we have some real data to estimate the environment parameters, 
<img src="https://render.githubusercontent.com/render/math?math=p(X_{env})"> is the posterior
conditional on that data. Otherwise we use some prior as 
<img src="https://render.githubusercontent.com/render/math?math=p(X_{env})">.

Then our interest is to find out some policy parameters that work robustly well in many different
environments that can exist, i.e., we are interested in the optimisation of policies under uncertainty.
We do not have to think about the policies for non-existent environments. If some environmental parameters
are uncertain, however, the chosen policy must work well in those possible situations. 

Let us first focus on the average case. We are interested
in functions <img src="https://render.githubusercontent.com/render/math?math=u_{avg}, v_{avg}: \Pi\to{\mathbb R}"> 
such that <img src="https://render.githubusercontent.com/render/math?math=u_{avg}(X_{policy})\triangleq {\mathbb E}_{p(X_{env})}[f(X_{policy},X_{env})]=\int f(X_{policy},X_{env})p(X_{env})dX_{env}">
and <img src="https://render.githubusercontent.com/render/math?math=v_{avg}(X_{policy})\triangleq {\mathbb E}_{p(X_{env})}[g(X_{policy},X_{env})]=\int g(X_{policy},X_{env})p(X_{env})dX_{env}">.
For many metrics of our interest, we expect that there is some trade-off between the minimisation of 
<img src="https://render.githubusercontent.com/render/math?math=u_{avg}"> and that of 
<img src="https://render.githubusercontent.com/render/math?math=v_{avg}">. Hence we want

<a href="https://www.codecogs.com/eqnedit.php?latex=\widehat{X}_{policy}^{(avg)}(C)=\min_{x\in\Pi}&space;u_{avg}(x)\mbox{&space;subject&space;to&space;}v_{avg}(x)\leq&space;C" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\widehat{X}_{policy}^{(avg)}(C)=\min_{x\in\Pi}&space;u_{avg}(x)\mbox{&space;subject&space;to&space;}v_{avg}(x)\leq&space;C" title="\widehat{X}_{policy}^{(avg)}(C)=\min_{x\in\Pi} u_{avg}(x)\mbox{ subject to }v_{avg}(x)\leq C" /></a>  for a specified constant <img src="https://render.githubusercontent.com/render/math?math=C">. 

For a given <img src="https://render.githubusercontent.com/render/math?math=C"> there is no rationality
to choose policy parameters other than 
<img src="https://render.githubusercontent.com/render/math?math=\widehat{X}_{policy}^{(avg)}(C)"> though
this optimum is not guaranteed to be unique.
By gradually changing the value of <img src="https://render.githubusercontent.com/render/math?math=C">,
we should have a set of *optimal* policy parameters that we call the average-case efficient frontier.

Then let us also think of the worst case. Because the true worst case of a continuous random variable
can become infinite, we instead consider some upper percentile, say 99%-tile that corresponds to
Value at Risk (VaR) in finance. We can also think of Conditional Value at Risk, which is the expectation
when exceeding the VaR but we discuss VaR for simplicity.
Let 
<img src="https://render.githubusercontent.com/render/math?math={\mathbb Q}_{p}^{(0.99)}">
be the 99%-tile operator under distribution <img src="https://render.githubusercontent.com/render/math?math=p">.
Then the statistics of our interest are
<img src="https://render.githubusercontent.com/render/math?math=u_{worst}, v_{worst}: \Pi\to{\mathbb R}"> 
such that 
<img src="https://render.githubusercontent.com/render/math?math=u_{worst}(X_{policy})\triangleq {\mathbb Q}_{p(X_{env})}^{(0.99)}[f(X_{policy},X_{env})]"> and
<img src="https://render.githubusercontent.com/render/math?math=v_{worst}(X_{policy})\triangleq {\mathbb Q}_{p(X_{env})}^{(0.99)}[g(X_{policy},X_{env})]">. Then we can think of the trade-off 
between the minimisation of <img src="https://render.githubusercontent.com/render/math?math=u_{worst}">
and that of <img src="https://render.githubusercontent.com/render/math?math=u_{worst}"> in the same manner
as the average case. We call the resulting trade-off as the worst-case efficient frontier.


## Empirical Approximation

Now we have definitions of the average-case and worse-case policy frontiers that exist
under the true functions <img src="https://render.githubusercontent.com/render/math?math=(f, g)">
and the true distributions of environmental parameters.
In reality, what we can have are only a finite number of samples to approximate the true value.
Here we discuss how to empirically approximate the frontiers.

**Empirical Mean or Percentile of the Metrics** 

We first assume that by certain machine learning algorithms we have a good estimate of 
<img src="https://render.githubusercontent.com/render/math?math=(f, g)">
as <img src="https://render.githubusercontent.com/render/math?math=(\widehat{f}, \widehat{g})">.
By calling `src/draw_parameters` we already have
<img src="https://render.githubusercontent.com/render/math?math=n"> random samples
<img src="https://render.githubusercontent.com/render/math?math=X_{policy}"> and
<img src="https://render.githubusercontent.com/render/math?math=X_{env}"> as
<img src="https://render.githubusercontent.com/render/math?math=(\boldsymbol{x}_{i,policy},\boldsymbol{x}_{i,env})_{i=1}^n">. Then for each policy-parameter sample <img src="https://render.githubusercontent.com/render/math?math=\boldsymbol{x}_{i,policy}">, we compute the empirical mean as

<a href="https://www.codecogs.com/eqnedit.php?latex=\widehat{u}_{avg,i}=\frac{1}{n}\sum_{j=1}^n\widehat{f}(\boldsymbol{x}_{i,policy},\boldsymbol{x}_{j,env})" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\widehat{u}_{avg,i}=\frac{1}{n}\sum_{j=1}^n\widehat{f}(\boldsymbol{x}_{i,policy},\boldsymbol{x}_{j,env})" title="\widehat{u}_{avg,i}=\frac{1}{n}\sum_{j=1}^n\widehat{f}(\boldsymbol{x}_{i,policy},\boldsymbol{x}_{j,env})" /></a> and
<a href="https://www.codecogs.com/eqnedit.php?latex=\widehat{v}_{avg,i}=\frac{1}{n}\sum_{j=1}^n&space;\widehat{g}(\boldsymbol{x}_{i,policy},\boldsymbol{x}_{j,env})" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\widehat{v}_{avg,i}=\frac{1}{n}\sum_{j=1}^n&space;\widehat{g}(\boldsymbol{x}_{i,policy},\boldsymbol{x}_{j,env})" title="\widehat{v}_{avg,i}=\frac{1}{n}\sum_{j=1}^n \widehat{g}(\boldsymbol{x}_{i,policy},\boldsymbol{x}_{j,env})" /></a>. 

We can also compute the empirical 99%-tiles 
<img src="https://render.githubusercontent.com/render/math?math=\widehat{u}_{worst,i}"> and
<img src="https://render.githubusercontent.com/render/math?math=\widehat{v}_{worst,i}">.
Here we are computing the average or quantile across many environmental parameters
but with fixed policy parameters. We just reuse the existing samples without the burden of another random generation.

We compute the empirical statistics for all policy parameter samples <img src="https://render.githubusercontent.com/render/math?math=(\boldsymbol{x}_{i,policy})_{i=1}">, and the total computational cost is quadratic to the sample size <img src="https://render.githubusercontent.com/render/math?math=n">. When the sample size is large, e.g., <img src="https://render.githubusercontent.com/render/math?math=n>10^3">, this quadratic cost is too expensive and we squash the samples of environmental parameters. Let
<img src="https://render.githubusercontent.com/render/math?math=\pi_1, \pi_2, \ldots, \pi_k"> be randomly chosen 
indices. Then

<a href="https://www.codecogs.com/eqnedit.php?latex=\widehat{u}_{avg,i}=\frac{1}{k}\sum_{j=1}^k&space;\widehat{f}(\boldsymbol{x}_{i,policy},\boldsymbol{x}_{\pi_j,env})" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\widehat{u}_{avg,i}=\frac{1}{k}\sum_{j=1}^k&space;\widehat{f}(\boldsymbol{x}_{i,policy},\boldsymbol{x}_{\pi_j,env})" title="\widehat{u}_{avg,i}=\frac{1}{k}\sum_{j=1}^k \widehat{f}(\boldsymbol{x}_{i,policy},\boldsymbol{x}_{\pi_j,env})" /></a> and
<a href="https://www.codecogs.com/eqnedit.php?latex=\widehat{v}_{avg,i}=\frac{1}{k}\sum_{j=1}^k&space;\widehat{g}(\boldsymbol{x}_{i,policy},\boldsymbol{x}_{\pi_j,env})" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\widehat{v}_{avg,i}=\frac{1}{k}\sum_{j=1}^k&space;\widehat{g}(\boldsymbol{x}_{i,policy},\boldsymbol{x}_{\pi_j,env})" title="\widehat{v}_{avg,i}=\frac{1}{k}\sum_{j=1}^k \widehat{g}(\boldsymbol{x}_{i,policy},\boldsymbol{x}_{\pi_j,env})" /></a>. 

We think 
<img src="https://render.githubusercontent.com/render/math?math=k=1,000"> provides a sufficient accuracy and hence
the total computational cost becomes linear to the sample size as <img src="https://render.githubusercontent.com/render/math?math={\mathcal O}(kn)">.

**Empirical Metrics and their Frontier** 

Scatter plot of the empirical statistics
<img src="https://render.githubusercontent.com/render/math?math=(\widehat{u}_{avg,i},\widehat{v}_{avg,i})_{i=1}^n">
clarifies how much scores can be achieved when we adopt the policies only on the frontier.
By sorting the score values of x-axis, we compute the path of piecewise-linear empirical frontier as the following figure example.

<img src="./image/isolation_vs_infection.jpg" alt="Efficient Frontier between Isolation Days and Number of Infections" width="50%">

Our ultimate interest is which settings of the policy parameters are on the line of the efficient frontier.
Because each point in the scatter plot corresponds to one vector of policy parameters,
we can see the substance of the policy parameters
as each row in the `${prefix}.average_case_policies.csv` and `${prefix}.worst_case_policies.csv` files.
You can see an [average-case example](../example_result/sample_covid_model/frontier.average_case_policies.csv)
and a [worst-case one](../example_result/sample_covid_model/frontier.average_case_policies.csv).

Finally let us note that some policy parameters, which are not so influential to the output metrics,
tend to be at random because of their unimportance. Hence the choice of policy parameters should be
done with consideration of their importance, which are available by sensitivity analysis plots. In the next example,
we can see that a binary parameter `alert_by_tested_positive` and integer parameters `*_isolation_time_mean` are strongly influential to the total number of days in isolation. We should carefully watch the corresponding columns of
the policy CSV files, while values in the other columns tend to be noises and we should not read too much
from the actual values of the unimportant parameters.

In order to understand the importance of each policy parameter, we should watch the sensitivities to both x-axis and y-axis metrics. The total number of infections is strongly driven by exposure-related disease parameters and hence many policy parameters are less influential. Unless having more reliable priors on the disease parameters, impact of policy parameter choice to the total number of infections is masked by much stronger influence of disease parameters.


<img src="./image/sensitivity2isolation.jpg" alt="Sensitivity to the Total Days in Isolation" width="90%">

<img src="./image/sensitivity2infection.jpg" alt="Sensitivity to the Total Number of Infections" width="90%">




