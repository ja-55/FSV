# Fundamental Stock Valuation Model (FSV)

<i><b>***UNDER CONSTRUCTION***</i></b>

### Objective
Discounted cash flow model for the purpose of valuing an individual equity. The model accepts an input sheet with a specified set of fundamental data. The model generates a 5 year fundamental forecast, which is then used to synthesize the value of a single share.

### Input Sheet Organization

### Model Components



### Sensitivity
The following variables can be set to accept a range of assumptions over the forecast horizon. Sensitivity can be turned off in order to accept a deterministic input. Sensitivity can be defined by a distribution or range.

* Revenue growth
* Gross margin expansion

### Order of Operations
1) Forecast revenue (set manually based on historical growth extrapolation)
2) Forecast COS (set margin manually based on historical extrapolation)

### Questions to Deal With
* Margin inertia - Growth can be set based on a distribution, but margins are more path dependent; how to account for this in individual simulations?
