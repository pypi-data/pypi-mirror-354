# **<u> Stratified linear regression mixture models </u>** <br>

## Main classes

- `Joint2Regressor`: Stratified multiple regression with continuity constraints for two (or K) groups.
- `JointKRegressor`: Stratified regression across K groups, with joint constraints, lasso and quantile.
- `Joint2GMMRegressor`: EM algorithm for stratified Gaussian mixture regression with constraints.
- `JointUtils`: Utilities for group splitting, closest point to median finding, etc.

## Key Features

- Joint multi-group regression with continuity or custom constraints at the join point.
- Supports quantile regression, penalized regression (lasso, ridge, elasticnet), and stratified GMM.
- Stratified multivariate piecewise regression, not directly available in scikit-learn or statsmodels.

Note : This package is provided “as is” for reproducing results, even if not all features are fully <br> 
implemented or tested. For the moment the lasso and ridge includes the $beta_0$, hence the eventual <br> 
intercept may be removed (centering $y_\ell$). The code development had involved the use of modern <br> 
tools, for code refactoring into classes, writing of the docstring, and help for code cleaning and <br>
debugging, robustfying the data entry types, etc.

## Installation

`pip install stratifreg`

## Usage

`import stratifreg`

`from stratifreg import two_groups`


## References

- Priam, R. (2025). Family of linear regression mixture models stratified along the outcome. <br>
Open Archive: [hal-04179813v3](https://hal.science/hal-04179813v3)
