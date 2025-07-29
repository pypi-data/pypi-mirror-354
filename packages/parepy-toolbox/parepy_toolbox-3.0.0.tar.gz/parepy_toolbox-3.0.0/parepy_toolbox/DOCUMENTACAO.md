<a id="common_library"></a>

# common\_library

Common library for PAREpy toolbox

<a id="common_library.sampling"></a>

#### sampling

```python
def sampling(n_samples: int, model: dict, variables_setup: list) -> np.ndarray
```

This algorithm generates a set of random numbers according to a type of distribution.

**Arguments**:

- `n_samples` _Integer_ - Number of samples
- `model` _Dictionary_ - Model parameters
- `variables_setup` _List_ - Random variable parameters (list of dictionaries)
  

**Returns**:

- `random_sampling` _np.array_ - Random samples

<a id="common_library.newton_raphson"></a>

#### newton\_raphson

```python
def newton_raphson(f: Callable, df: Callable, x0: float, tol: float) -> float
```

This function calculates the root of a function using the Newton-Raphson method.

**Arguments**:

- `f` _Python function [def]_ - Function
- `df` _Python function [def]_ - Derivative of the function
- `x0` _Float_ - Initial value
- `tol` _Float_ - Tolerance
  

**Returns**:

- `x0` _Float_ - Root of the function

<a id="common_library.pf_equation"></a>

#### pf\_equation

```python
def pf_equation(beta: float) -> float
```

This function calculates the probability of failure (pf) for a given reliability index (ϐ) using a standard normal cumulative distribution function. The calculation is performed by integrating the probability density function (PDF) of a standard normal distribution.

**Arguments**:

- `beta` _Float_ - Reliability index
  

**Returns**:

- `pf_value` _Float_ - Probability of failure

<a id="common_library.beta_equation"></a>

#### beta\_equation

```python
def beta_equation(pf: float) -> Union[float, str]
```

This function calculates the reliability index value for a given probability of failure (pf).

**Arguments**:

- `pf` _Float_ - Probability of failure
  

**Returns**:

- `beta_value` _Float or String_ - Beta value

<a id="common_library.calc_pf_beta"></a>

#### calc\_pf\_beta

```python
def calc_pf_beta(df_or_path: Union[pd.DataFrame, str], numerical_model: str,
                 n_constraints: int) -> tuple[pd.DataFrame, pd.DataFrame]
```

Calculates the values of probability of failure or reliability index from the columns of a DataFrame that start with 'I_' (Indicator function). If a .txt file path is passed, this function evaluates pf and β values too.

**Arguments**:

- `df_or_path` _DataFrame or String_ - The DataFrame containing the columns with boolean values about indicator function, or a path to a .txt file
- `numerical_model` _Dictionary_ - Containing the numerical model
- `n_constraints` _Integer_ - Number of state limit functions or constraints
  

**Returns**:

- `df_pf` _DataFrame_ - DataFrame containing the values for probability of failure for each 'G_' column
- `df_beta` _DataFrame_ - DataFrame containing the values for beta for each 'G_' column

<a id="common_library.convergence_probability_failure"></a>

#### convergence\_probability\_failure

```python
def convergence_probability_failure(
        df: pd.DataFrame, column: str) -> tuple[list, list, list, list, list]
```

This function calculates the convergence rate of a given column in a data frame. This function is used to check the convergence of the failure probability.

**Arguments**:

- `df` _DataFrame_ - DataFrame containing the data with indicator function column
- `column` _String_ - Name of the column to be analyzed
  

**Returns**:

- `div` _List_ - list containing sample sizes
- `m` _List_ - list containing the mean values of the column. pf value rate
- `ci_l` _List_ - list containing the lower confidence interval values of the column
- `ci_u` _List_ - list containing the upper confidence interval values of the column
- `var` _List_ - list containing the variance values of the column

<a id="common_library.fbf"></a>

#### fbf

```python
def fbf(algorithm: str, n_constraints: int, time_analysis: int,
        results_about_data: pd.DataFrame) -> tuple[pd.DataFrame, list]
```

This function application first barrier failure algorithm.

**Arguments**:

- `algorithm` _str_ - Name of the algorithm
- `n_constraints` _int_ - Number of constraints analyzed
- `time_analysis` _int_ - Time period for analysis
- `results_about_data` _pd.DataFrame_ - DataFrame containing the results to be processed
  

**Returns**:

- `results_about_data` - Updated DataFrame after processing

<a id="common_library.log_message"></a>

#### log\_message

```python
def log_message(message: str) -> None
```

Logs a message with the current time.

**Arguments**:

- `message` _str_ - The message to log.
  

**Returns**:

  None

<a id="common_library.norm_array"></a>

#### norm\_array

```python
def norm_array(ar: list) -> float
```

Evaluates the norm of the array ar.

**Arguments**:

- `ar` _float_ - A list of numerical values (floats) representing the array.
  

**Returns**:

- `float` - The norm of the array.

<a id="common_library.hasofer_lind_rackwitz_fiessler_algorithm"></a>

#### hasofer\_lind\_rackwitz\_fiessler\_algorithm

```python
def hasofer_lind_rackwitz_fiessler_algorithm(
        y_k: np.ndarray, g_y: float, grad_y_k: np.ndarray) -> np.ndarray
```

This function calculates the y new value using the Hasofer-Lind-Rackwitz-Fiessler algorithm.

**Arguments**:

- `y_k` _Float_ - Current y value
- `g_y` _Float_ - Objective function in point y_k
- `grad_y_k` _Float_ - Gradient of the objective function in point y_k
  

**Returns**:

- `y_new` _Float_ - New y value

<a id="distributions"></a>

# distributions

Function of probability distributions

<a id="distributions.crude_sampling_zero_one"></a>

#### crude\_sampling\_zero\_one

```python
def crude_sampling_zero_one(n_samples: int, seed: int = None) -> list
```

This function generates a uniform sampling between 0 and 1.

**Arguments**:

- `n_samples` _Integer_ - Number of samples
- `seed` _Integer_ - Seed for random number generation
  

**Returns**:

- `u` _List_ - Random samples

<a id="distributions.lhs_sampling_zero_one"></a>

#### lhs\_sampling\_zero\_one

```python
def lhs_sampling_zero_one(n_samples: int,
                          dimension: int,
                          seed: int = None) -> np.ndarray
```

This function generates a uniform sampling between 0 and 1 using the Latin Hypercube Sampling Algorithm.

**Arguments**:

- `n_samples` _Integer_ - Number of samples
- `dimension` _Integer_ - Number of dimensions
- `seed` _Integer_ - Seed for random number generation
  

**Returns**:

- `u` _np.array_ - Random samples

<a id="distributions.uniform_sampling"></a>

#### uniform\_sampling

```python
def uniform_sampling(parameters: dict,
                     method: str,
                     n_samples: int,
                     seed: int = None) -> list
```

This function generates a Uniform sampling between a (minimum) and b (maximum).

**Arguments**:

- `parameters` _Dictionary_ - Dictionary of parameters. Keys:  'min' (Minimum value of the uniform distribution [float]), 'max' (Maximum value of the uniform distribution [float])
- `method` _String_ - Sampling method. Supports the following values: 'lhs' (Latin Hypercube Sampling) or 'mcs' (Crude Monte Carlo Sampling)
- `n_samples` _Integer_ - Number of samples
- `seed` _Integer_ - Seed for random number generation. Use None for a random seed
  

**Returns**:

- `u` _List_ - Random samples

<a id="distributions.normal_sampling"></a>

#### normal\_sampling

```python
def normal_sampling(parameters: dict,
                    method: str,
                    n_samples: int,
                    seed: int = None) -> list
```

This function generates a Normal or Gaussian sampling with mean (mu) and standard deviation (sigma).

**Arguments**:

- `parameters` _Dictionary_ - Dictionary of parameters. Keys 'mu' (Mean [float]), 'sigma' (Standard deviation [float])
- `method` _String_ - Sampling method. Supports the following values: 'lhs' (Latin Hypercube Sampling) or 'mcs' (Crude Monte Carlo Sampling)
- `n_samples` _Integer_ - Number of samples
- `seed` _Integer_ - Seed for random number generation. Use None for a random seed
  

**Returns**:

- `u` _List_ - Random samples

<a id="distributions.corr_normal_sampling"></a>

#### corr\_normal\_sampling

```python
def corr_normal_sampling(parameters_b: dict,
                         parameters_g: dict,
                         pho_gb: float,
                         method: str,
                         n_samples: int,
                         seed: int = None) -> list
```

This function generates a Normal or Gaussian sampling with mean (mu) and standard deviation (sigma). Variable g have a correlation rho_gb with b.

**Arguments**:

- `parameters` _Dictionary_ - Dictionary of parameters. Keys 'mu' (Mean [float]), 'sigma' (Standard deviation [float])
- `method` _String_ - Sampling method. Supports the following values: 'lhs' (Latin Hypercube Sampling) or 'mcs' (Crude Monte Carlo Sampling)
- `n_samples` _Integer_ - Number of samples
- `seed` _Integer_ - Seed for random number generation. Use None for a random seed
  

**Returns**:

- `u` _List_ - Random samples

<a id="distributions.lognormal_sampling"></a>

#### lognormal\_sampling

```python
def lognormal_sampling(parameters: dict,
                       method: str,
                       n_samples: int,
                       seed: int = None) -> list
```

This function generates a log-normal sampling with mean and standard deviation.

**Arguments**:

- `parameters` _Dictionary_ - Dictionary of parameters. Keys 'mu' (mean [float]), 'sigma' (standard deviation [float])
- `method` _String_ - Sampling method. Can use 'lhs' (Latin Hypercube Sampling) or 'mcs' (Crude Monte Carlo Sampling)
- `n_samples` _Integer_ - Number of samples
- `seed` _Integer_ - Seed for random number generation
  

**Returns**:

- `u` _List_ - Random samples

<a id="distributions.gumbel_max_sampling"></a>

#### gumbel\_max\_sampling

```python
def gumbel_max_sampling(parameters: dict,
                        method: str,
                        n_samples: int,
                        seed: int = None) -> list
```

This function generates a Gumbel maximum distribution with a specified mean and standard deviation.

**Arguments**:

- `parameters` _Dictionary_ - Dictionary of parameters. Keys 'mu' (mean [float]), 'sigma' (standard deviation [float])
- `method` _String_ - Sampling method. Can use 'lhs' (Latin Hypercube Sampling) or 'mcs' (Crude Monte Carlo Sampling)
- `n_samples` _Integer_ - Number of samples
- `seed` _Integer_ - Seed for random number generation
  

**Returns**:

- `u` _List_ - Random samples

<a id="distributions.gumbel_min_sampling"></a>

#### gumbel\_min\_sampling

```python
def gumbel_min_sampling(parameters: dict,
                        method: str,
                        n_samples: int,
                        seed: int = None) -> list
```

This function generates a Gumbel Minimum sampling with mean and standard deviation.

**Arguments**:

- `parameters` _Dictionary_ - Dictionary of parameters. Keys 'mu' (mean [float]), 'sigma' (standard deviation [float])
- `method` _String_ - Sampling method. Can use 'lhs' (Latin Hypercube Sampling) or 'mcs' (Crude Monte Carlo Sampling)
- `n_samples` _Integer_ - Number of samples
- `seed` _Integer_ - Seed for random number generation
  

**Returns**:

- `u` _List_ - Random samples

<a id="distributions.triangular_sampling"></a>

#### triangular\_sampling

```python
def triangular_sampling(parameters: dict,
                        method: str,
                        n_samples: int,
                        seed: int = None) -> list
```

This function generates a triangular sampling with minimun a, mode c, and maximum b.

**Arguments**:

- `parameters` _Dictionary_ - Dictionary of parameters. Keys 'a' (minimum [float]), 'c' (mode [float]), and 'b' (maximum [float])
- `method` _String_ - Sampling method. Can use 'lhs' (Latin Hypercube Sampling) or 'mcs' (Crude Monte Carlo Sampling)
- `n_samples` _Integer_ - Number of samples
- `seed` _Integer_ - Seed for random number generation
  

**Returns**:

- `u` _List_ - Random samples

<a id="distributions.cdf_gumbel_max"></a>

#### cdf\_gumbel\_max

```python
def cdf_gumbel_max(x: float, u: float, beta: float) -> float
```

Calculates the cumulative distribution function (CDF) of the Maximum Gumbel distribution.

**Arguments**:

- `x` _Float_ - Input value for which the CDF will be calculated.
- `u` _Float_ - Location parameter (mode) of the Maximum Gumbel distribution.
- `beta` _Float_ - Scale parameter of the Maximum Gumbel distribution.
  

**Returns**:

- `fx` _Float_ - Value of the CDF at point x.

<a id="distributions.pdf_gumbel_max"></a>

#### pdf\_gumbel\_max

```python
def pdf_gumbel_max(x: float, u: float, beta: float) -> float
```

Calculates the probability density function (PDF) of the Maximum Gumbel distribution.

**Arguments**:

- `x` _Float_ - Input value for which the PDF will be calculated.
- `u` _Float_ - Location parameter (mode) of the Maximum Gumbel distribution.
- `beta` _Float_ - Scale parameter of the Maximum Gumbel distribution.
  

**Returns**:

- `fx` _Float_ - Value of the PDF at point x.

<a id="distributions.cdf_gumbel_min"></a>

#### cdf\_gumbel\_min

```python
def cdf_gumbel_min(x: float, u: float, beta: float) -> float
```

Calculates the cumulative distribution function (CDF) of the Minimum Gumbel distribution.

**Arguments**:

- `x` _Float_ - Input value for which the CDF will be calculated.
- `u` _Float_ - Location parameter (mode) of the Minimum Gumbel distribution.
- `beta` _Float_ - Scale parameter of the Minimum Gumbel distribution.
  

**Returns**:

- `fx` _Float_ - Value of the CDF at point x.

<a id="distributions.pdf_gumbel_min"></a>

#### pdf\_gumbel\_min

```python
def pdf_gumbel_min(x: float, u: float, beta: float) -> float
```

Calculates the probability density function (PDF) of the Minimum Gumbel distribution.

**Arguments**:

- `x` _float_ - Input value for which the PDF will be calculated.
- `u` _float_ - Location parameter (mode) of the Minimum Gumbel distribution.
- `beta` _float_ - Scale parameter of the Minimum Gumbel distribution.
  

**Returns**:

- `fx` _float_ - Value of the PDF at point x.

<a id="distributions.cdf_normal"></a>

#### cdf\_normal

```python
def cdf_normal(x: float, u: float, sigma: float) -> float
```

Calculates the cumulative distribution function (CDF) of the Normal distribution.

**Arguments**:

- `x` _float_ - Input value for which the CDF will be calculated.
- `u` _float_ - Mean (location) of the Normal distribution.
- `sigma` _float_ - Standard deviation (scale) of the Normal distribution.
  

**Returns**:

- `fx` _float_ - Value of the CDF at point x.

<a id="distributions.pdf_normal"></a>

#### pdf\_normal

```python
def pdf_normal(x: float, u: float, sigma: float) -> float
```

Calculates the probability density function (PDF) of the Normal distribution.

**Arguments**:

- `x` _Float_ - Input value for which the PDF will be calculated.
- `u` _Float_ - Mean (location) of the Normal distribution.
- `sigma` _Float_ - Standard deviation (scale) of the Normal distribution.
  

**Returns**:

- `fx` _Float_ - Value of the PDF at point x.

<a id="distributions.log_normal"></a>

#### log\_normal

```python
def log_normal(x: float, lambdaa: float,
               epsilon: float) -> tuple[float, float]
```

Calculates the location (u) and scale (sigma) parameters for a Log-Normal distribution.

**Arguments**:

- `x` _Float_ - Input value.
- `lambdaa` _Float_ - Shape parameter of the Log-Normal distribution.
- `epsilon` _Float_ - Scale parameter of the Log-Normal distribution.
  

**Returns**:

- `u` _Float_ - Location parameter.
- `sigma` _Float_ - Scale parameter.

<a id="distributions.non_normal_approach_normal"></a>

#### non\_normal\_approach\_normal

```python
def non_normal_approach_normal(x, dist, params)
```

This function convert non normal distribution to normal distribution.

**Arguments**:

- `x` _Float_ - Random variable
- `dist` _String_ - Type of distribution: 'gumbel max', 'gumbel min', 'lognormal')
- `params` _Dictionary_ - Parameters of distribution
  

**Returns**:

- `mu_t` _Float_ - mean normal model
- `sigma_t` _Float_ - standard deviation normal model

<a id="pare"></a>

# pare

PAREpy toolbox: Probabilistic Approach to Reliability Engineering

<a id="pare.sampling_algorithm_structural_analysis_kernel"></a>

#### sampling\_algorithm\_structural\_analysis\_kernel

```python
def sampling_algorithm_structural_analysis_kernel(setup: dict) -> pd.DataFrame
```

This function creates the samples and evaluates the limit state functions in structural reliability problems. Based on the data, it calculates probabilities of failure and reliability indexes.

**Arguments**:

- `setup` _Dictionary_ - Setup settings
  'number of samples' (Integer): Number of samples (key in setup dictionary)
  'numerical model' (Dictionary): Numerical model settings (key in setup dictionary)
  'variables settings' (List): Variables settings, listed as dictionaries (key in setup dictionary)
  'number of state limit functions or constraints' (Integer): Number of state limit functions or constraints (key in setup dictionary)
  'none variable' (None, list, float, dictionary, str or any): None variable. User can use this variable in objective function (key in setup dictionary)
  'objective function' (Python function): Objective function. The PAREpy user defined this function (key in setup dictionary)
  'name simulation' (String or None): Output filename (key in setup dictionary)
  

**Returns**:

- `results_about_data` _DataFrame_ - Results about reliability analysis
- `failure_prob_list` _List_ - Failure probability list
- `beta_list` _List_ - Beta list

<a id="pare.sampling_algorithm_structural_analysis"></a>

#### sampling\_algorithm\_structural\_analysis

```python
def sampling_algorithm_structural_analysis(
        setup: dict) -> tuple[pd.DataFrame, list, list]
```

This function creates the samples and evaluates the limit state functions in structural reliability problems.

**Arguments**:

- `setup` _Dictionary_ - Setup settings.
  'number of samples' (Integer): Number of samples (key in setup dictionary)
  'numerical model' (Dictionary): Numerical model settings (key in setup dictionary)
  'variables settings' (List): Variables settings (key in setup dictionary)
  'number of state limit functions or constraints' (Integer): Number of state limit functions or constraints
- `'none_variable'` _None, list, float, dictionary, str or any_ - None variable. User can use this variable in objective function (key in setup dictionary)
  'objective function' (Python function): Objective function. The PAREpy user defined this function (key in setup dictionary)
  'name simulation' (String or None): Output filename (key in setup dictionary)
  

**Returns**:

- `results_about_data` _DataFrame_ - Results about reliability analysis
- `failure_prob_list` _List_ - Failure probability list
- `beta_list` _List_ - Beta list

<a id="pare.concatenates_txt_files_sampling_algorithm_structural_analysis"></a>

#### concatenates\_txt\_files\_sampling\_algorithm\_structural\_analysis

```python
def concatenates_txt_files_sampling_algorithm_structural_analysis(
        setup: dict) -> tuple[pd.DataFrame, list, list]
```

Concatenates .txt files generated by the sampling_algorithm_structural_analysis algorithm, and calculates probabilities of failure and reliability indexes based on the data.

**Arguments**:

- `setup` _Dictionary_ - Setup settings.
- `'folder_path'` _String_ - Path to the folder containing the .txt files (key in setup dictionary)
  'number of state limit functions or constraints' (Integer): Number of state limit functions or constraints
  'simulation name' (String or None): Name of the simulation (key in setup dictionary)
  

**Returns**:

- `results_about_data` _DataFrame_ - A DataFrame containing the concatenated results from the .txt files.
- `failure_prob_list` _List_ - A list containing the calculated failure probabilities for each indicator function.
- `beta_list` _List_ - A list containing the calculated reliability indices (beta) for each indicator function.

<a id="pare.sobol_algorithm"></a>

#### sobol\_algorithm

```python
def sobol_algorithm(setup)
```

This function calculates the Sobol indices in structural reliability problems.

**Arguments**:

- `setup` _Dictionary_ - Setup settings.
  'number of samples' (Integer): Number of samples (key in setup dictionary)
  'variables settings' (List): Variables settings, listed as dictionaries (key in setup dictionary)
  'number of state limit functions or constraints' (Integer): Number of state limit functions or constraints (key in setup dictionary)
  'none variable' (None, list, float, dictionary, str or any): None variable. User can use this variable in objective function (key in setup dictionary)
  'objective function' (Python function): Objective function defined by the user (key in setup dictionary)
  

**Returns**:

- `dict_sobol` _DataFrame_ - A dictionary containing the first-order and total-order Sobol sensitivity indixes for each input variable.

<a id="pare.generate_factorial_design"></a>

#### generate\_factorial\_design

```python
def generate_factorial_design(level_dict)
```

Generates a full factorial design based on the input dictionary of variable levels. The function computes all possible combinations of the provided levels for each variable and returns them in a structured DataFrame.

**Arguments**:

- `level_dict` _Dictionary_ - A dictionary where keys represent variable names, and values are lists, arrays, or sequences representing the levels of each variable.
  

**Returns**:

- `DataFrame` - A dictionary containing all possible combinations of the levels provided in the input dictionary. Each column corresponds to a variable defined in level_dict. And each row represents one combination of the factorial design.

<a id="pare.deterministic_algorithm_structural_analysis"></a>

#### deterministic\_algorithm\_structural\_analysis

```python
def deterministic_algorithm_structural_analysis(
        setup: dict) -> tuple[pd.DataFrame, float, int]
```

This function performs a deterministic structural reliability analysis using an iterative algorithm.
It calculates the reliability index (`beta`), the probability of failure (`pf`), and returns a DataFrame
containing the results of each iteration.

**Arguments**:

- `setup` _Dictionary_ - setup settings.
- `'tolerance'` _float_ - The convergence tolerance for the algorithm (key in setup dictionary).
  'max iterations' (int): The maximum number of iterations allowed (key in setup dictionary).
  'numerical model' (Any): The numerical model used for the analysis (user-defined) (key in setup dictionary).
  'variables settings' (List[dict]): Variables settings, listed as dictionaries (key in setup dictionary).
  'number of state limit functions or constraints' (int): Number of state limit functions or constraints (key in setup dictionary).
  'none variable' (None, list, float, dictionary, str or any): None variable. User can use this variable in objective function (key in setup dictionary).
  'objective function' (Python function): Objective function defined by the user (key in setup dictionary).
  'gradient objective function' (Callable): The gradient of the objective function (key in setup dictionary).
  'name simulation' (str): A name or identifier for the simulation (key in setup dictionary).
  

**Returns**:

- `results_df` _pd.DataFrame_ - A DataFrame with the results of each iteration.
- `pf` _float_ - The probability of failure calculated using the final reliability index.
- `beta` _int_ - The final reliability index.

<a id="script_teste"></a>

# script\_teste

<a id="__init__"></a>

# \_\_init\_\_

