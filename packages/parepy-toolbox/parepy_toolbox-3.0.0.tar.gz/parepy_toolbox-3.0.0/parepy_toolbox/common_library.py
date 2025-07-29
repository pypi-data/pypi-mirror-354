"""Common library for PAREpy toolbox"""
from typing import Optional, Callable, Tuple

import scipy as sc
import numpy as np
import pandas as pd

import parepy_toolbox.distributions as parepydi


def std_matrix(std: list) -> tuple[np.ndarray, np.ndarray]:
    """
    Extract D matrix and D^-1 matrix from a list of variables. Used in Y to X or X to Y transformation.

    :param std: Standard deviation parameters.

    return: output[0] = D matrix, output[1] = D^-1 matrix.
    """

    dneq = np.zeros((len(std), len(std)))
    dneq1 = np.zeros((len(std), len(std)))
    for i, sigma in enumerate(std):
        dneq[i, i] = sigma
        dneq1[i, i] = 1 / sigma

    return dneq, dneq1


def mu_matrix(mean: list) -> np.ndarray:
    """
    Extract mean matrix from a list of variables. Used in Y to X or X to Y transformation.

    :param mu: Mean parameters.

    return: Mean matrix.
    """

    mu_neq = np.zeros((len(mean), 1))
    for i, mu in enumerate(mean):
        mu_neq[i, 0] = mu

    return mu_neq


def x_to_y(x: np.ndarray, dneq1: np.ndarray, mu_neq: np.ndarray) -> np.ndarray:
    """
    Transforms a vector of random variables from the X space to the Y space.

    :param x: Random variables in the X space.
    :param dneq1: D^-1 matrix.
    :param mu_neq: Mean matrix.

    :return: Transformed random variables in the Y space.
    """

    return dneq1 @ (x - mu_neq)


def y_to_x(y: np.ndarray, dneq: np.ndarray, mu_neq: np.ndarray) -> np.ndarray:
    """
    Transforms a vector of random variables from the Y space to the X space.

    :param y: Random variables in the Y space.
    :param dneq: D matrix.
    :param mu_neq: Mean matrix.

    :return: Transformed random variables in the X space.
    """

    return dneq @ y + mu_neq


def pf_equation(beta: float) -> float:
    """
    Calculates the probability of failure (pf) for a given reliability index (β), using the cumulative distribution function (CDF) of the standard normal distribution.

    :param beta: Reliability index (β).
    
    :return: Probability of failure (pf).
    """

    return sc.stats.norm.cdf(-beta)


def beta_equation(pf: float) -> float:
    """
    Calculates the reliability index value for a given probability of failure (pf), using the inverse cumulative distribution function (ICDF) of the standard normal distribution.

    :param pf: Probability of failure (pf).

    :return: Reliability index (β).
    """

    return -sc.stats.norm.ppf(pf)


def first_second_order_derivative_numerical_differentiation_unidimensional(obj: Callable, x: list, pos: str, method: str, order: str = 'first', h: float = 1E-5, args: Optional[tuple] = None) -> float:
    """
    Computes the numerical derivative of a function at a given point in the given dimension using the central, backward and forward difference method.

    :param obj: The objective function: obj(x, args) -> float or obj(x) -> float, where x is a list with shape n and args is a tuple fixed parameters needed to completely specify the function.
    :param x: Point at which to evaluate the derivative.
    :param pos: Dimension in the list x where the derivative is to be calculated. When use order 'xy', pos is a str contain first and second dimension separated by a comma (e.g., '0,1' for the first and second dimensions). 
    :param method: Method to use for differentiation. Supported values: 'center', 'forward', or 'backward'.
    :param order: Order of the derivative to compute (default is first for first-order derivative). Supported values: 'first', 'second', or 'xy'.
    :param h: Step size for the finite difference approximation (default is 1e-10).
    :param args: Extra arguments to pass to the objective function (optional).

    :return: Numerical derivative of order n of the function at point x in dimension pos.
    """

    if order == 'first':
        a = x.copy()
        b = x.copy()
        if method == "forward":
            for i in range(len(x)):
                if i == int(pos):
                    a[i] += h
            den = h
        elif method == "backward":
            for i in range(len(x)):
                if i == int(pos):
                    b[i] -= h
            den = h
        elif method == "center":
            for i in range(len(x)):
                if i == int(pos):
                    a[i] += h
                    b[i] -= h
            den = 2 * h
        fa = obj(a, args) if args is not None else obj(a)
        fb = obj(b, args) if args is not None else obj(b)
        diff = (fa - fb) / den
    elif order == 'second':
        a = x.copy()
        b = x.copy()
        x_aux = x.copy()
        den = h ** 2
        if method == "forward":
            for i in range(len(x)):
                if i == int(pos):
                    a[i] += 2*h
                    x_aux[i] += h
            fa = obj(a, args) if args is not None else obj(a)
            fx = obj(x_aux, args) if args is not None else obj(x_aux)
            fb = obj(b, args) if args is not None else obj(b)
        elif method == "backward":
            for i in range(len(x)):
                if i == int(pos):
                    b[i] -= 2*h
                    x_aux[i] -= h
            fa = obj(a, args) if args is not None else obj(a)
            fx = obj(x_aux, args) if args is not None else obj(x_aux)
            fb = obj(b, args) if args is not None else obj(b)
        elif method == "center":
            for i in range(len(x)):
                if i == int(pos):
                    a[i] += h
                    b[i] -= h
            fa = obj(a, args) if args is not None else obj(a)
            fx = obj(x_aux, args) if args is not None else obj(x_aux)
            fb = obj(b, args) if args is not None else obj(b)
        diff = (fa - 2 * fx + fb) / den
    elif order == 'xy':
        pos_x = int(pos.split(',')[0])
        pos_y = int(pos.split(',')[1])
        a = x.copy()
        a[pos_x] += h
        a[pos_y] += h
        b = x.copy()
        b[pos_x] += h
        b[pos_y] -= h
        c = x.copy()
        c[pos_x] -= h
        c[pos_y] += h
        d = x.copy()
        d[pos_x] -= h
        d[pos_y] -= h
        fa = obj(a, args) if args is not None else obj(a)
        fb = obj(b, args) if args is not None else obj(b)
        fc = obj(c, args) if args is not None else obj(c)
        fd = obj(d, args) if args is not None else obj(d)
        diff = (fa - fb - fc + fd) / (4 * h ** 2)

    return diff


def jacobian_matrix(obj: Callable, x: list, method: str, h: float = 1E-5, args: Optional[tuple] = None) -> np.ndarray:
    """
    Computes Jacobian matrix of a vector-valued function using finite difference methods.

    :param obj: The objective function: obj(x, args) -> float or obj(x) -> float, where x is a list with shape n and args is a tuple fixed parameters needed to completely specify the function.
    :param x: Point at which to evaluate the derivative.
    :param method: Method to use for differentiation. Supported values: 'center', 'forward', or 'backward'.
    :param h: Step size for the finite difference approximation (default is 1e-10).
    :param args: Extra arguments to pass to the objective function (optional).

    :return: Numerical Jacobian matrix at point x.
    """

    jacob = np.zeros((len(x), 1))
    for i in range(len(x)):
        jacob[i, 0] = first_second_order_derivative_numerical_differentiation_unidimensional(obj, x, str(i), method, 'first', h=h, args=args) if args is not None else first_second_order_derivative_numerical_differentiation_unidimensional(obj, x, str(i), method, 'first', h=h)

    return jacob


def hessian_matrix(obj: Callable, x: list, method: str, h: float = 1E-5, args: Optional[tuple] = None) -> np.ndarray:
    """
    Computes Hessian matrix of a vector-valued function using finite difference methods.

    :param obj: The objective function: obj(x, args) -> float or obj(x) -> float, where x is a list with shape n and args is a tuple fixed parameters needed to completely specify the function.
    :param x: Point at which to evaluate the derivative.
    :param method: Method to use for differentiation. Supported values: 'center', 'forward', or 'backward'.
    :param h: Step size for the finite difference approximation (default is 1e-10).
    :param args: Extra arguments to pass to the objective function (optional).

    :return: Numerical Hessian matrix at point x.
    """

    hessian = np.zeros((len(x), len(x)))
    for i in range(len(x)):
        for j in range(len(x)):
            if i == j:
                hessian[i, j] = first_second_order_derivative_numerical_differentiation_unidimensional(obj, x, str(i), method, 'second', h=h, args=args) if args is not None else first_second_order_derivative_numerical_differentiation_unidimensional(obj, x, str(i), method, 'second', h=h)
            else:
                hessian[i, j] = first_second_order_derivative_numerical_differentiation_unidimensional(obj, x, f'{j},{i}', method, 'xy', h=h, args=args) if args is not None else first_second_order_derivative_numerical_differentiation_unidimensional(obj, x, f'{j},{i}', method, 'xy', h=h)

    return hessian


def sampling_kernel_without_time(obj: Callable, random_var_settings: list, method: str, n_samples: int, number_of_limit_functions: int, args: Optional[tuple] = None) -> pd.DataFrame:
    """
    Generates random samples from a specified distribution using kernel density estimation.

    :param obj: The objective function: obj(x, args) -> float or obj(x) -> float, where x is a list with shape n and args is a tuple fixed parameters needed to completely specify the function.
    :param random_var_settings: Containing the distribution type and parameters. Example: {'type': 'normal', 'parameters': {'mean': 0, 'std': 1}}. Supported distributions: (a) 'uniform': keys 'min' and 'max', (b) 'normal': keys 'mean' and 'std', (c) 'lognormal': keys 'mean' and 'std', (d) 'gumbel max': keys 'mean' and 'std', (e) 'gumbel min': keys 'mean' and 'std', (f) 'triangular': keys 'min', 'mode' and 'max', or (g) 'gamma': keys 'mean' and 'std'.
    :param method: Sampling method. Supported values: 'lhs' (Latin Hypercube Sampling), 'mcs' (Crude Monte Carlo Sampling) or 'sobol' (Sobol Sampling).
    :param n_samples: Number of samples. For Sobol sequences, this variable represents the exponent "m" (n = 2^m).
    :param number_of_limit_functions: Number of limit state functions or constraints.
    :param args: Extra arguments to pass to the objective function (optional).

    :return: Random samples, objective function evaluations and indicator functions.
    """

    n_real_samples = 2**n_samples if method == 'sobol' else n_samples
    random_data = np.zeros((n_real_samples, len(random_var_settings)))

    # Generate random samples for each variable
    for i, dist_info in enumerate(random_var_settings):
        random_data[:, i] = parepydi.random_sampling(dist_info['type'], dist_info['parameters'], method, n_samples)

    # Evaluate objective function for each sample
    g_matrix = np.zeros((n_real_samples, number_of_limit_functions))
    indicator_matrix = np.zeros_like(g_matrix)
    for idx, sample in enumerate(random_data):
        g_values = obj(list(sample), args) if args is not None else obj(list(sample))
        g_matrix[idx, :] = g_values
        indicator_matrix[idx, :] = [1 if g <= 0 else 0 for g in g_values]

    # Build DataFrame
    df = pd.DataFrame(random_data, columns=[f'X_{i}' for i in range(len(random_var_settings))])
    for j in range(number_of_limit_functions):
        df[f'G_{j}'] = g_matrix[:, j]
        df[f'I_{j}'] = indicator_matrix[:, j]

    # dataset_x = {}
    # for i, value in enumerate(random_var_settings):
    #     dataset_x[f'X_{i}'] = parepydi.random_sampling(value['type'], value['parameters'], method, n_samples)
    # random_data = pd.DataFrame(dataset_x)
    # results = random_data.apply(lambda row: obj(list(row), args), axis=1) if args is not None else random_data.apply(lambda row: obj(list(row)), axis=1)
    # g_names = []
    # for i in range(number_of_limit_functions):
    #     g_names.append(f'G_{i}')
    # random_data[g_names] = pd.DataFrame(results.tolist(), index=random_data.index)
    # for col in g_names:
    #     random_data[f'I_{col}'] = np.where(random_data[col] <= 0, 1, 0)

    return df


def summarize_pf_beta(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Generates a summary DataFrame containing the probability of failure (pf) and reliability index (β) for each indicator function column in the input DataFrame.

    :param df: Random samples, objective function evaluations and indicator functions.

    :return: output [0] = Probability of failure values for each indicator function, output[1] = beta_df: Reliability index values for each indicator function.

    """
    
    pf_values = {}
    beta_values = {}

    for col in df.columns:
        if col.startswith("I_"):
            idx = col.split("_")[1]
            pf = df[col].mean()
            beta = beta_equation(pf)
            pf_values[f"pf_{idx}"] = pf
            beta_values[f"beta_{idx}"] = beta

    pf_df = pd.DataFrame([pf_values])
    beta_df = pd.DataFrame([beta_values])

    return pf_df, beta_df


def convergence_probability_failure(df: pd.DataFrame, column: str) -> tuple[list, list, list, list, list]:
    """
    Calculates the convergence rate of the probability of failure.

    :param df: Random samples, objective function evaluations and indicator functions.
    :param column: Name of the column to be analyzed. Supported values: 'I_0', 'I_1', ..., 'I_n' where n is the number of limit state functions.

    :return: output[0] = div: List of sample sizes considered at each step, output[1] = m: List of mean values (estimated probability of failure), output[2] = ci_l: List containing the lower confidence interval values of the column, output[3] = ci_u: List containing the upper confidence interval values of the column, output[4] = var: List containing the variance values of the column. 
    """

    column_values = df[column].to_list()
    step = 1000
    div = [i for i in range(step, len(column_values), step)]
    m = []
    ci_u = []
    ci_l = []
    var = []
    for i in range(0, len(div)+1):
        if i == len(div):
            aux = column_values.copy()
            div.append(len(column_values))
        else:
            aux = column_values[:div[i]]
        mean = np.mean(aux)
        std = np.std(aux, ddof=1)
        n = len(aux)
        confidence_level = 0.95
        t_critic = sc.stats.t.ppf((1 + confidence_level) / 2, df=n-1)
        margin = t_critic * (std / np.sqrt(n))
        confidence_interval = (mean - margin, mean + margin)
        m.append(mean)
        ci_u.append(confidence_interval[1])
        ci_l.append(confidence_interval[0])
        var.append((mean * (1 - mean))/n)

    return div, m, ci_l, ci_u, var


# def sampling(n_samples: int, model: dict, variables_setup: list) -> np.ndarray:
#     """
#     Generates a set of random numbers according to a specified probability distribution model.

#     :param n_samples: Number of samples to generate.
#     :param model: Dictionary containing the model parameters.
#     :param variables_setup: List of dictionaries, each containing parameters for a random variable.

#     :return: Numpy array with the generated random samples.
#     """

#     # Model settings
#     model_sampling = model['model sampling'].upper()
#     id_type = []
#     id_corr = []
#     for v in variables_setup:
#         if 'parameters' in v and 'corr' in v['parameters']:
#             id_type.append('g-corr-g_var')
#             id_corr.append(v['parameters']['corr']['var'])
#         else:
#             id_type.append('g')
#     for k in id_corr:
#         id_type[k] = 'g-corr-b_var'

#     if model_sampling in ['MCS', 'LHS']:
#         random_sampling = np.zeros((n_samples, len(variables_setup)))

#         for j, variable in enumerate(variables_setup):
#             if id_type[j] == 'g-corr-b_var':
#                 continue
#             type_dist = variable['type'].upper()
#             seed_dist = variable['seed']
#             params = variable['parameters']

#             if (type_dist == 'NORMAL' or type_dist == 'GAUSSIAN') and id_type[j] == 'g':
#                 mean = params['mean']
#                 sigma = params['sigma']
#                 parameters = {'mean': mean, 'sigma': sigma}
#                 random_sampling[:, j] = parepydi.normal_sampling(parameters, method=model_sampling.lower(), n_samples=n_samples, seed=seed_dist)

#             elif (type_dist == 'NORMAL' or type_dist == 'GAUSSIAN') and id_type[j] == 'g-corr-g_var':
#                 mean = params['mean']
#                 sigma = params['sigma']
#                 parameters_g = {'mean': mean, 'sigma': sigma}
#                 pho = params['corr']['pho']
#                 m = params['corr']['var']
#                 parameters_b = variables_setup[m]['parameters']
#                 random_sampling[:, m], random_sampling[:, j] = parepydi.corr_normal_sampling(parameters_b, parameters_g, pho, method=model_sampling.lower(), n_samples=n_samples, seed=seed_dist)

#             elif type_dist == 'UNIFORM' and id_type[j] == 'g':
#                 min_val = params['min']
#                 max_val = params['max']
#                 parameters = {'min': min_val, 'max': max_val}
#                 random_sampling[:, j] = parepydi.uniform_sampling(parameters, method=model_sampling.lower(), n_samples=n_samples, seed=seed_dist)

#             elif type_dist == 'GUMBEL MAX' and id_type[j] == 'g':
#                 mean = params['mean']
#                 sigma = params['sigma']
#                 parameters = {'mean': mean, 'sigma': sigma}
#                 random_sampling[:, j] = parepydi.gumbel_max_sampling(parameters, method=model_sampling.lower(), n_samples=n_samples, seed=seed_dist)

#             elif type_dist == 'GUMBEL MIN' and id_type[j] == 'g':
#                 mean = params['mean']
#                 sigma = params['sigma']
#                 parameters = {'mean': mean, 'sigma': sigma}
#                 random_sampling[:, j] = parepydi.gumbel_min_sampling(parameters, method=model_sampling.lower(), n_samples=n_samples, seed=seed_dist)

#             elif type_dist == 'LOGNORMAL' and id_type[j] == 'g':
#                 mean = params['mean']
#                 sigma = params['sigma']
#                 parameters = {'mean': mean, 'sigma': sigma}
#                 random_sampling[:, j] = parepydi.lognormal_sampling(parameters, method=model_sampling.lower(), n_samples=n_samples, seed=seed_dist)

#             elif type_dist == 'TRIANGULAR' and id_type[j] == 'g':
#                 min_val = params['min']
#                 max_val = params['max']
#                 mode = params['mode']
#                 parameters = {'min': min_val, 'max': max_val, 'mode': mode}
#                 random_sampling[:, j] = parepydi.triangular_sampling(parameters, method=model_sampling.lower(), n_samples=n_samples, seed=seed_dist)
#     elif model_sampling in ['MCS-TIME', 'MCS_TIME', 'MCS TIME', 'LHS-TIME', 'LHS_TIME', 'LHS TIME']:
#         time_analysis = model['time steps']
#         random_sampling = np.empty((0, len(variables_setup)))
#         match = re.search(r'\b(MCS|LHS)\b', model_sampling.upper(), re.IGNORECASE)
#         model_sampling = match.group(1).upper()

#         for _ in range(n_samples):
#             temporal_sampling = np.zeros((time_analysis, len(variables_setup)))

#             for j, variable in enumerate(variables_setup):
#                 if id_type[j] == 'g-corr-b_var':
#                     continue
#                 type_dist = variable['type'].upper()
#                 seed_dist = variable['seed']
#                 sto = variable['stochastic variable']
#                 params = variable['parameters']

#                 if (type_dist == 'NORMAL' or type_dist == 'GAUSSIAN') and id_type[j] == 'g':
#                     mean = params['mean']
#                     sigma = params['sigma']
#                     parameters = {'mean': mean, 'sigma': sigma}
#                     if sto is False:
#                         temporal_sampling[:, j] = parepydi.normal_sampling(parameters, method=model_sampling.lower(), n_samples=1, seed=seed_dist)
#                         temporal_sampling[1:, j]
#                     else:
#                         temporal_sampling[:, j] = parepydi.normal_sampling(parameters, method=model_sampling.lower(), n_samples=time_analysis, seed=seed_dist)

#                 elif (type_dist == 'NORMAL' or type_dist == 'GAUSSIAN') and id_type[j] == 'g-corr-g_var':
#                     mean = params['mean']
#                     sigma = params['sigma']
#                     parameters_g = {'mean': mean, 'sigma': sigma}
#                     pho = params['corr']['pho']
#                     m = params['corr']['var']
#                     parameters_b = variables_setup[m]['parameters']
#                     if sto is False:
#                         temporal_sampling[:, m], temporal_sampling[:, j] = parepydi.corr_normal_sampling(parameters_b, parameters_g, pho, method=model_sampling.lower(), n_samples=1, seed=seed_dist)
#                         temporal_sampling[1:, j]
#                         temporal_sampling[1:, m]
#                     else:
#                         temporal_sampling[:, m], temporal_sampling[:, j] = parepydi.corr_normal_sampling(parameters_b, parameters_g, pho, method=model_sampling.lower(), n_samples=time_analysis, seed=seed_dist)

#                 elif type_dist == 'UNIFORM' and id_type[j] == 'g':
#                     min_val = params['min']
#                     max_val = params['max']
#                     parameters = {'min': min_val, 'max': max_val}
#                     if sto is False:
#                         temporal_sampling[:, j] = parepydi.uniform_sampling(parameters, method=model_sampling.lower(), n_samples=1, seed=seed_dist)
#                         temporal_sampling[1:, j]
#                     else:
#                         temporal_sampling[:, j] = parepydi.uniform_sampling(parameters, method=model_sampling.lower(), n_samples=time_analysis, seed=seed_dist)

#                 elif type_dist == 'GUMBEL MAX' and id_type[j] == 'g':
#                     mean = params['mean']
#                     sigma = params['sigma']
#                     parameters = {'mean': mean, 'sigma': sigma}
#                     if sto is False:
#                         temporal_sampling[:, j] = parepydi.gumbel_max_sampling(parameters, method=model_sampling.lower(), n_samples=1, seed=seed_dist)
#                         temporal_sampling[1:, j]
#                     else:
#                         temporal_sampling[:, j] = parepydi.gumbel_max_sampling(parameters, method=model_sampling.lower(), n_samples=time_analysis, seed=seed_dist)

#                 elif type_dist == 'GUMBEL MIN' and id_type[j] == 'g':
#                     mean = params['mean']
#                     sigma = params['sigma']
#                     parameters = {'mean': mean, 'sigma': sigma}
#                     if sto is False:
#                         temporal_sampling[:, j] = parepydi.gumbel_min_sampling(parameters, method=model_sampling.lower(), n_samples=1, seed=seed_dist)
#                         temporal_sampling[1:, j]
#                     else:
#                         temporal_sampling[:, j] = parepydi.gumbel_min_sampling(parameters, method=model_sampling.lower(), n_samples=time_analysis, seed=seed_dist)

#                 elif type_dist == 'LOGNORMAL' and id_type[j] == 'g':
#                     mean = params['mean']
#                     sigma = params['sigma']
#                     parameters = {'mean': mean, 'sigma': sigma}
#                     if sto is False:
#                         temporal_sampling[:, j] = parepydi.lognormal_sampling(parameters, method=model_sampling.lower(), n_samples=1, seed=seed_dist)
#                         temporal_sampling[1:, j]
#                     else:
#                         temporal_sampling[:, j] = parepydi.lognormal_sampling(parameters, method=model_sampling.lower(), n_samples=time_analysis, seed=seed_dist)

#                 elif type_dist == 'TRIANGULAR' and id_type[j] == 'g':
#                     min_val = params['min']
#                     max_val = params['max']
#                     mode = params['mode']
#                     parameters = {'min': min_val, 'max': max_val, 'mode': mode}
#                     if sto is False:
#                         temporal_sampling[:, j] = parepydi.triangular_sampling(parameters, method=model_sampling.lower(), n_samples=1, seed=seed_dist)
#                         temporal_sampling[1:, j]
#                     else:
#                         temporal_sampling[:, j] = parepydi.triangular_sampling(parameters, method=model_sampling.lower(), n_samples=time_analysis, seed=seed_dist)

#             random_sampling = np.concatenate((random_sampling, temporal_sampling), axis=0)  

#         time_sampling = np.zeros((time_analysis * n_samples, 1))
#         cont = 0
#         for _ in range(n_samples):
#             for m in range(time_analysis):
#                 time_sampling[cont, 0] = int(m)
#                 cont += 1
#         random_sampling = np.concatenate((random_sampling, time_sampling), axis=1)   

#     return random_sampling


# def calc_pf_beta(df_or_path: Union[pd.DataFrame, str], numerical_model: str, n_constraints: int) -> tuple[pd.DataFrame, pd.DataFrame]:
#     """
#     Calculates the probability of failure (pf) and reliability index (β) based on the columns of a DataFrame
#     that start with 'I' (indicator function). If a .txt file path is passed, this function evaluates pf and β values too.

#     :param df_or_path: A DataFrame containing boolean indicator columns prefixed with 'I', or a string path to a .txt file.

#     :param numerical_model: Dictionary containing the numerical model.

#     :param n_constraints: Number of limit state functions or constraints.

#     :return: Tuple of DataFrames:

#         - df_pf: probability of failure values for each column prefixed with 'G'.
#         - df_beta: reliability index values for each column prefixed with 'G'.
#     """

#     # Read dataset
#     if isinstance(df_or_path, str) and df_or_path.endswith('.txt'):
#         df = pd.read_csv(df_or_path, delimiter='\t')
#     else:
#         df = df_or_path

#     # Calculate pf and beta values
#     if numerical_model.upper() in ['MCS', 'LHS']:
#         filtered_df = df.filter(like='I_', axis=1)
#         pf_results = filtered_df.mean(axis=0)
#         df_pf = pd.DataFrame([pf_results.to_list()], columns=pf_results.index)
#         beta_results = [beta_equation(pf) for pf in pf_results.to_list()] 
#         df_beta = pd.DataFrame([beta_results], columns=pf_results.index)
#     elif numerical_model.upper() in ['TIME-MCS', 'TIME-LHS', 'TIME MCS', 'TIME LHS', 'MCS TIME', 'LHS TIME', 'MCS-TIME', 'LHS-TIME']:
#         df_pf = pd.DataFrame()
#         df_beta = pd.DataFrame()
#         for i in range(n_constraints):
#             filtered_df = df.filter(like=f'I_{i}', axis=1)
#             pf_results = filtered_df.mean(axis=0)
#             beta_results = [beta_equation(pf) for pf in pf_results.to_list()]
#             df_pf[f'G_{i}'] = pf_results.to_list()
#             df_beta[f'G_{i}'] = beta_results

#     return df_pf, df_beta


# def fbf(algorithm: str, n_constraints: int, time_analysis: int, results_about_data: pd.DataFrame) -> tuple[pd.DataFrame, list]:
#     """
#     This function application first barrier failure algorithm.

#     :param algorithm: Name of the algorithm.
#     :param n_constraints: Number of constraints analyzed.
#     :param time_analysis: Time period for analysis.
#     :param results_about_data: DataFrame containing the results to be processed.

#     :return: Updated DataFrame after processing.
#     """

#     if algorithm.upper() in ['MCS-TIME', 'MCS_TIME', 'MCS TIME']:
#         i_columns = []
#         for i in range(n_constraints):
#             aux_column_names = []
#             for j in range(time_analysis):
#                 aux_column_names.append('I_' + str(i) + '_t=' + str(j))
#             i_columns.append(aux_column_names)

#         for i in i_columns:
#             matrixx = results_about_data[i].values
#             for id, linha in enumerate(matrixx):
#                 indice_primeiro_1 = np.argmax(linha == 1)
#                 if linha[indice_primeiro_1] == 1:
#                     matrixx[id, indice_primeiro_1:] = 1
#             results_about_data = pd.concat([results_about_data.drop(columns=i),
#                                             pd.DataFrame(matrixx, columns=i)], axis=1)
#     else:
#         i_columns = []
#         for i in range(n_constraints):
#             i_columns.append(['I_' + str(i)])
    
#     return results_about_data, i_columns


# def log_message(message: str) -> None:
#     """
#     Logs a message with the current time.

#     :param message: The message to log.
    
#     :return: None
#     """
#     current_time = datetime.now().strftime('%H:%M:%S')
#     print(f'{current_time} - {message}')


# def norm_array(ar: list) -> float:
#     """
#     Evaluates the norm of the array ar.

#     :param ar: A list of numerical values (floats) representing the array.

#     :return: The norm of the array.
#     """
#     norm_ar = [i ** 2 for i in ar]
#     norm_ar = sum(norm_ar) ** 0.5
#     return norm_ar


# def hasofer_lind_rackwitz_fiessler_algorithm(y_k: np.ndarray, g_y: float, grad_y_k: np.ndarray) -> np.ndarray:
#     """
#     Calculates the new y value using the Hasofer-Lind-Rackwitz-Fiessler algorithm.

#     :param y_k: Current y value.
#     :param g_y: Objective function at point `y_k`.
#     :param grad_y_k: Gradient of the objective function at point `y_k`.

#     :return: New y value.
#     """

#     num = np.dot(np.transpose(grad_y_k), y_k) - np.array([[g_y]])
#     print("num: ", num)
#     num = num[0][0]
#     den = (np.linalg.norm(grad_y_k)) ** 2
#     print("den: ", den)
#     aux = num / den
#     y_new = aux * grad_y_k

#     return y_new

# def goodness_of_fit(data: Union[np.ndarray, list], distributions: Union[str, list] = 'all') -> dict:
#     """
#     Evaluates the fit of distributions to the provided data.

#     This function fits various distributions to the data using the distfit library and returns the top three distributions based on the fit score.

#     Args:
#         data (np.array or list): Data to which distributions will be fitted. It should be a list or array of numeric values.
#         distributions (str or list, optional): Distributions to be tested. If 'all', all available distributions will be tested. Otherwise, it should be a list of strings specifying the names of the distributions to test. The default is 'all'.

#     Returns:
#         dict: A dictionary containing the top three fitted distributions. Each entry is a dictionary with the following keys:
#             - 'rank': Ranking of the top three distributions based on the fit score.
#             - 'type' (str): The name of the fitted distribution.
#             - 'params' (tuple): Parameters of the fitted distribution.
    
#     Raises:
#         ValueError: If the expected 'score' column is not present in the DataFrame returned by `dist.summary()`.
#     """

#     if distributions == 'all':
#         dist = distfit()
#     else:
#         dist = distfit(distr=distributions)
    
#     dist.fit_transform(data)
#     summary_df = dist.summary
#     sorted_models = summary_df.sort_values(by='score').head(3)
    
#     top_3_distributions = {
#         f'rank_{i+1}': {
#             'type': model['name'],
#             'params': model['params']
#         }
#         for i, model in sorted_models.iterrows()
#     }
    
#     return top_3_distributions

# def newton_raphson(f: Callable, df: Callable, x0: float, tol: float) -> float:
#     """
#     Calculates the root of a function using the Newton-Raphson method.

#     :param f: Function for which the root is sought.
#     :param df: Derivative of the function.
#     :param x0: Initial guess for the root.
#     :param tol: Tolerance for convergence.

#     :return: Approximated root of the function.
#     """

#     if abs(f(x0)) < tol:
#         return x0
#     else:
#         return newton_raphson(f, df, x0 - f(x0)/df(x0), tol)