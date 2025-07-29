"""Probabilistic Approach to Reliability Engineering (PAREPY)"""
import time
import os
import itertools
from datetime import datetime
from multiprocessing import Pool
from typing import Callable, Optional, List

import numpy as np
import pandas as pd

import parepy_toolbox.common_library as parepyco
import parepy_toolbox.distributions as parepydi


def deterministic_algorithm_structural_analysis(obj: Callable, tol: float, max_iter: int, random_var_settings: list, x0: list, verbose: bool = False, args: Optional[tuple] = None) -> tuple[pd.DataFrame, float, float]:
    """
    Computes the reliability index and probability of failure using FORM (First Order Reliability Method).

    :param obj: The objective function: obj(x, args) -> float or obj(x) -> float, where x is a list with shape n and args is a tuple fixed parameters needed to completely specify the function.
    :param tol: Tolerance for convergence.
    :param max_iter: Maximum number of iterations allowed.
    :param random_var_settings: Containing the distribution type and parameters. Example: {'type': 'normal', 'parameters': {'mean': 0, 'std': 1}}. Supported distributions: (a) 'uniform': keys 'min' and 'max', (b) 'normal': keys 'mean' and 'std', (c) 'lognormal': keys 'mean' and 'std', (d) 'gumbel max': keys 'mean' and 'std', (e) 'gumbel min': keys 'mean' and 'std', (f) 'triangular': keys 'min', 'mode' and 'max', or (g) 'gamma': keys 'mean' and 'std'.
    :param x0: Initial guess.
    :param verbose: If True, prints detailed information about the process.
    :param args: Extra arguments to pass to the objective function (optional).

    :return: Results of reliability analysis. output[0] = Numerical data obtained for the MPP search, output[1] = Failure probability (pf), output[2] = Reliability index (beta).
    """

    results = []
    x_k = x0.copy()
    error = 1 / tol
    iteration = 0
    n = len(random_var_settings)
    start_time = time.perf_counter()

    # Iteration process
    while error > tol and iteration < max_iter:
        row = {}
        mu_eq = []
        sigma_eq = []

        # Conversion Non-normal to Normal
        for i, var in enumerate(random_var_settings):
            paras_scipy = parepydi.convert_params_to_scipy(var['type'], var['parameters'])
            m, s = parepydi.normal_tail_approximation(var['type'], paras_scipy, x_k[i])
            mu_eq.append(m)
            sigma_eq.append(s)

        # yk
        dneq, dneq1 = parepyco.std_matrix(sigma_eq)
        mu_vars = parepyco.mu_matrix(mu_eq)
        y_k = parepyco.x_to_y(np.array(x_k).reshape(-1, 1), dneq1, mu_vars)
        beta_k = np.linalg.norm(y_k)
        for i in range(n):
            row[f"x_{i},k"] = x_k[i]
            row[f"y_{i},k"] = y_k[i, 0]
        row["β_k"] = beta_k

        # Numerical differentiation g(x) and g(y)
        g_diff_x = parepyco.jacobian_matrix(obj, x_k, 'center', h=1E-8, args=args) if args is not None else parepyco.jacobian_matrix(obj, x_k, 'center', h=1E-8)
        g_diff_y = np.matrix_transpose(dneq) @ g_diff_x
        
        # alpha vector
        norm_gdiff = np.linalg.norm(g_diff_y)
        alpha = g_diff_y / norm_gdiff
        for i in range(n):
            row[f"α_{i},k"] = alpha[i, 0]

        # Beta update
        g_y = obj(x_k, args) if args is not None else obj(x_k)
        beta_k1 = beta_k + g_y / (np.matrix_transpose(g_diff_y) @ alpha)
        row["β_k+1"] = beta_k1[0, 0]

        # yk and xk update 
        y_k1 = - alpha @ beta_k1
        for i in range(n):
            row[f"y_{i},k+1"] = y_k1[i, 0]

        x_k1 = parepyco.y_to_x(y_k1, dneq, mu_vars).flatten().tolist()
        for i in range(n):
            row[f"x_{i},k+1"] = x_k1[i]

        # Storage and error
        x_k = x_k1.copy()
        y_k = y_k1.copy()
        iteration += 1
        if beta_k == 0.0:
            beta_k = tol * 1E1
        error = np.abs(beta_k1[0, 0] - beta_k) / beta_k
        row["error"] = error

        # Verbose 
        if verbose:
            elapsed_time = time.perf_counter() - start_time
            print(f"⏱️ Time: {elapsed_time:.4e}s, Iteration {iteration} (error = {error:.4e})")
        results.append(row)

    df = pd.DataFrame(results)

    # Ordering columns
    col_order = (
        [f"x_{i},k" for i in range(n)] +
        [f"y_{i},k" for i in range(n)] +
        ["β_k"] +
        [f"α_{i},k" for i in range(n)] +
        ["β_k+1"] +
        [f"y_{i},k+1" for i in range(n)] +
        [f"x_{i},k+1" for i in range(n)] +
        ["error"]
    )
    results = df[col_order]

    # Last row contain the final beta value and probability of failure
    if verbose:
        print("🧮 Computes β and pf")
    final_beta = df["β_k+1"].iloc[-1]
    final_pf = parepyco.pf_equation(final_beta)

    # hessian = parepyco.hessian_matrix(obj, x: list, method: str, h: float = 1E-5, args: Optional[tuple] = None)
    # if method.lower() == "sorm":
    #     beta_u = beta_k1[0, 0]
    #     mu_eq = []
    #     sigma_eq = []
    #     # Conversion Non-normal to Normal
    #     for i, var in enumerate(variables):
    #         paras_scipy = parepydi.convert_params_to_scipy(var['type'], var['parameters'])
    #         m, s = parepydi.normal_tail_approximation(var['type'], paras_scipy, x_k[i])
    #         mu_eq.append(m)
    #         sigma_eq.append(s)
    #     dneq, dneq1 = parepyco.std_matrix(sigma_eq)
    #     mu_vars = parepyco.mu_matrix(mu_eq)
    #     # Numerical differentiation g(y)
    #     g_diff_x = parepyco.jacobian_matrix(obj, x_k, 'center', h=1E-8, args=args) if args is not None else parepyco.jacobian_matrix(obj, x_k, 'center', h=1E-8)
    #     g_diff_y = np.matrix_transpose(dneq) @ np.array(g_diff_x).reshape(-1, 1)
    #     norm_gdiff = np.linalg.norm(g_diff_y)
    #     m = len(x_k)
    #     q = np.eye(m)
    #     q[:, 0] = y_k.flatten().tolist()
    #     q, _ = np.linalg.qr(q)
    #     q = np.fliplr(q)
    #     a = q.T @ hessian @ q
    #     j = np.eye(m - 1) + beta_u * a[:m-1, :m-1] / norm_gdiff
    #     det_j = np.linalg.det(j)
    #     correction = 1 / np.sqrt(det_j)
    #     pf_sorm = sc.stats.norm.cdf(-beta_u) * correction
    #     beta_sorm = -sc.stats.norm.ppf(pf_sorm)
    if verbose:
        print("✔️ Algorithm finished!")

    return results, final_pf, final_beta


def sampling_algorithm_structural_analysis(obj: Callable, random_var_settings: list, method: str, n_samples: int, number_of_limit_functions: int, parallel: bool = True, verbose: bool = False, random_var_settings_importance_sampling: Optional[list] = None, args: Optional[tuple] = None) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """                                    
    Computes the reliability index and probability of failure using sampling methods.

    :param obj: The objective function: obj(x, args) -> float or obj(x) -> float, where x is a list with shape n and args is a tuple fixed parameters needed to completely specify the function.
    :param random_var_settings: Containing the distribution type and parameters. Example: {'type': 'normal', 'parameters': {'mean': 0, 'std': 1}}. Supported distributions: (a) 'uniform': keys 'min' and 'max', (b) 'normal': keys 'mean' and 'std', (c) 'lognormal': keys 'mean' and 'std', (d) 'gumbel max': keys 'mean' and 'std', (e) 'gumbel min': keys 'mean' and 'std', (f) 'triangular': keys 'min', 'mode' and 'max', or (g) 'gamma': keys 'mean' and 'std'.
    :param method: Sampling method. Supported values: 'lhs' (Latin Hypercube Sampling), 'mcs' (Crude Monte Carlo Sampling) or 'sobol' (Sobol Sampling).
    :param n_samples: Number of samples. For Sobol sequences, this variable represents the exponent "m" (n = 2^m).
    :param number_of_limit_functions: Number of limit state functions or constraints.
    :param parallel: Start parallel process.
    :param verbose: If True, prints detailed information about the process.
    :param args: Extra arguments to pass to the objective function (optional).

    :return: Results of reliability analysis. output[0] = Numerical data obtained for the MPP search, output [1] = Probability of failure values for each indicator function, output[2] = beta_df: Reliability index values for each indicator function.
    """

    block_size = 100
    if method != 'sobol':
        samples_per_block = n_samples // block_size
        samples_per_block_remainder = n_samples % block_size
        setups = [(obj, random_var_settings, method, samples_per_block, number_of_limit_functions, args) for _ in range(block_size)] if args is not None else [(obj, random_var_settings, method, samples_per_block, number_of_limit_functions) for _ in range(block_size)]
        if samples_per_block_remainder > 0:
            setups.append((obj, random_var_settings, method, samples_per_block_remainder, number_of_limit_functions, args) if args is not None else (obj, random_var_settings, method, samples_per_block_remainder, number_of_limit_functions))
    else:
        parallel = False
        setups = [(obj, random_var_settings, method, n_samples, number_of_limit_functions, args) if args is not None else (obj, random_var_settings, method, n_samples, number_of_limit_functions)]

    # Random sampling and computes G function
    start_time = time.perf_counter()
    if parallel:
        with Pool() as pool:
            results = pool.starmap(parepyco.sampling_kernel_without_time, setups)
    else:
        results = [parepyco.sampling_kernel_without_time(*args_aux) for args_aux in setups]
    end_time = time.perf_counter()
    final_df = pd.concat(results, ignore_index=True)
    if verbose:
        print(f"Sampling and computes the G functions {end_time - start_time:.2f} seconds.")

    if verbose:
        filename = f"sampling_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        final_df.to_csv(filename, sep="\t", index=False)
        print(f"file '{filename}' has been successfully saved.")
        print("✔️ Algorithm finished!")

    # Computes pf and beta
    pf_df, beta_df = parepyco.summarize_pf_beta(final_df)

    return final_df, pf_df, beta_df


def reprocess_sampling_results(folder_path: str, verbose: bool = True) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Reprocesses sampling results from multiple .txt files in a specified folder.

    :param folder_path: Path to the folder containing sampling result files (.txt format).
    :param verbose: If True, prints detailed information about the process.

    :return: Results of reprocessing: [0] = Combined dataframe with all sampling data, [1] = Failure probabilities for each limit state function, [2] = Reliability index (beta) for each limit state function.
    """

    start_time = time.perf_counter()

    all_files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]

    dataframes = []
    for file in all_files:
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path, sep="\t")
        dataframes.append(df)

    final_df = pd.concat(dataframes, ignore_index=True)

    if verbose:
        print(f"🧮 {len(dataframes)} files loaded. Total number of samples: {len(final_df)}.")

    col_I = [col for col in final_df.columns if col.startswith("I_")]

    f_df, beta_df = parepyco.summarize_failure_probabilities(final_df)

    end_time = time.perf_counter()

    if verbose:
        print("Reprocessing completed successfully.")
        print(f"🧮 Sampling and computes the G functions {end_time - start_time:.2f} seconds.")
        print("✔️ Algorithm finished!")

    return final_df, f_df, beta_df


def sobol_algorithm(obj: Callable,  random_var_settings: list, n_sobol: int, number_of_limit_functions: int, parallel: bool = False, verbose: bool = False, args: Optional[tuple] = None) -> pd.DataFrame:
    """
    Calculates the Sobol sensitivity indices in structural reliability problems.

    :param obj: The objective function: obj(x, args) -> float or obj(x) -> float, where x is a list with shape n and args is a tuple fixed parameters needed to completely specify the function.
    :param random_var_settings: Containing the distribution type and parameters. Example: {'type': 'normal', 'parameters': {'mean': 0, 'std': 1}}. Supported distributions: (a) 'uniform': keys 'min' and 'max', (b) 'normal': keys 'mean' and 'std', (c) 'lognormal': keys 'mean' and 'std', (d) 'gumbel max': keys 'mean' and 'std', (e) 'gumbel min': keys 'mean' and 'std', (f) 'triangular': keys 'min', 'mode' and 'max', or (g) 'gamma': keys 'mean' and 'std'.
    :param n_sobol: This variable represents the exponent "m" (n = 2^m) to generate Sobol sequence sampling. Must be a positive integer.
    :param number_of_limit_functions: Number of limit state functions or constraints.
    :param parallel: Start parallel process.
    :param verbose: If True, prints detailed information about the process.
    :param args: Extra arguments to pass to the objective function (optional)

    :return: First-order and total-order Sobol sensitivity indices for each input variable. 
    """

    if verbose:
        print("🧮 Starting Sobol analysis...")

    # Sampling for distributions A and B
    start_time = time.perf_counter()
    dist_a, _, _ = sampling_algorithm_structural_analysis(obj, random_var_settings, 'sobol', n_sobol, number_of_limit_functions, parallel=parallel, verbose=verbose, args=args) if args is not None else sampling_algorithm_structural_analysis(obj, random_var_settings, 'sobol', n_sobol, number_of_limit_functions, parallel=parallel, verbose=verbose)
    dist_b, _, _ = sampling_algorithm_structural_analysis(obj, random_var_settings, 'sobol', n_sobol, number_of_limit_functions, parallel=parallel, verbose=verbose, args=args) if args is not None else sampling_algorithm_structural_analysis(obj, random_var_settings, 'sobol', n_sobol, number_of_limit_functions, parallel=parallel, verbose=verbose)

    # DataFrame
    n_samples = 2 ** n_sobol
    y_a = dist_a['G_0'].to_list()
    y_b = dist_b['G_0'].to_list()
    f_0_2 = (sum(y_a) / n_samples) ** 2

    A = dist_a.drop(['G_0', 'I_0'], axis=1).to_numpy()
    B = dist_b.drop(['G_0', 'I_0'], axis=1).to_numpy()
    K = A.shape[1]

    s_i = []
    s_t = []
    for i in range(K):
        C = np.copy(B)
        C[:, i] = A[:, i]
        y_c_i = []
        for j in range(n_samples):
            g = obj(list(C[j, :]), args)
            y_c_i.append(g[0])

        y_a_dot_y_c_i = [y_a[m] * y_c_i[m] for m in range(n_samples)]
        y_b_dot_y_c_i = [y_b[m] * y_c_i[m] for m in range(n_samples)]
        y_a_dot_y_a = [y_a[m] * y_a[m] for m in range(n_samples)]

        var_y = (1 / n_samples) * sum(y_a_dot_y_a) - f_0_2

        s_i.append(((1 / n_samples) * sum(y_a_dot_y_c_i) - f_0_2) / var_y)
        s_t.append(1 - ((1 / n_samples) * sum(y_b_dot_y_c_i) - f_0_2) / var_y)

    end_time = time.perf_counter()
    if verbose:
        print(f"🧮 Sobol analysis completed in {end_time - start_time:.2f} seconds.")
        print("✔️ Algorithm finished!")

    dict_sobol = pd.DataFrame({'s_i': s_i, 's_t': s_t})

    return dict_sobol


def generate_factorial_design(variable_names: List[str], levels_per_variable: List[List[float]], verbose: bool = False) -> pd.DataFrame:
    """
    Generates a full factorial design based on variable names and levels.

    :param variable_names: Variable names.
    :param levels_per_variable: List of lists, where each sublist contains the levels for the corresponding variable.
    :param verbose: If True, prints the number of combinations and preview of the DataFrame.

    :return: All possible combinations of the levels provided.
    """

    if verbose:
        print("🧮 Generating factorial design...")
        for name, levels in zip(variable_names, levels_per_variable):
            print(f" - {name}: {levels}")

    combinations = list(itertools.product(*levels_per_variable))
    df = pd.DataFrame(combinations, columns=variable_names)

    if verbose:
        print(f"🧮 Generated {len(df)} combinations.")
        print("🧮 Sample of factorial design:")
        print("✔️ Algorithm finished!")

    return df


# def sampling_algorithm_structural_analysis_kernel(objective_function: callable, number_of_samples: int, numerical_model: dict, variables_settings: list, number_of_limit_functions: int, none_variable = None) -> pd.DataFrame:
#     """
#     Creates samples and evaluates the limit state functions in structural reliability problems.

#     :param objective_function: User-defined Python function to evaluate the limit state(s).
#     :param number_of_samples: Number of samples to generate.
#     :param numerical_model: Dictionary with model configuration (e.g., sampling type).
#     :param variables_settings: List of variable definitions with distribution parameters.
#     :param number_of_limit_functions: Number of limit state functions or constraints.
#     :param none_variable: Optional auxiliary input to be passed to the objective function.

#     :return: DataFrame with reliability analysis results.
#     """

#     # Ensure all variables have seeds
#     for var in variables_settings:
#         if 'seed' not in var:
#             var['seed'] = None

#     n_dimensions = len(variables_settings)
#     algorithm = numerical_model['model sampling']
#     is_time_analysis = algorithm.upper() in ['MCS-TIME', 'MCS_TIME', 'MCS TIME', 'LHS-TIME', 'LHS_TIME', 'LHS TIME']
#     time_analysis = numerical_model['time steps'] if is_time_analysis else None

#     # Generate samples
#     dataset_x = parepyco.sampling(
#         n_samples=number_of_samples,
#         model=numerical_model,
#         variables_setup=variables_settings
#     )

#     # Initialize output arrays
#     capacity = np.zeros((len(dataset_x), number_of_limit_functions))
#     demand = np.zeros((len(dataset_x), number_of_limit_functions))
#     state_limit = np.zeros((len(dataset_x), number_of_limit_functions))
#     indicator_function = np.zeros((len(dataset_x), number_of_limit_functions))

#     # Evaluate objective function
#     for idx, sample in enumerate(dataset_x):
#         c_i, d_i, g_i = objective_function(list(sample), none_variable)
#         capacity[idx, :] = c_i
#         demand[idx, :] = d_i
#         state_limit[idx, :] = g_i
#         indicator_function[idx, :] = [1 if val <= 0 else 0 for val in g_i]

#     # Stack all results
#     results = np.hstack((dataset_x, capacity, demand, state_limit, indicator_function))

#     # Format results into DataFrame
#     if is_time_analysis:
#         block_size = int(len(results) / number_of_samples)
#         all_rows = []
#         for i in range(number_of_samples):
#             block = results[i * block_size:(i + 1) * block_size, :].T.flatten().tolist()
#             all_rows.append(block)
#         results_about_data = pd.DataFrame(all_rows)
#     else:
#         results_about_data = pd.DataFrame(results)

#     # Create column names
#     column_names = []

#     for i in range(n_dimensions):
#         if is_time_analysis:
#             for t in range(time_analysis):
#                 column_names.append(f'X_{i}_t={t}')
#         else:
#             column_names.append(f'X_{i}')

#     if is_time_analysis:
#         for t in range(time_analysis):
#             column_names.append(f'STEP_t_{t}')

#     for i in range(number_of_limit_functions):
#         if is_time_analysis:
#             for t in range(time_analysis):
#                 column_names.append(f'R_{i}_t={t}')
#         else:
#             column_names.append(f'R_{i}')

#     for i in range(number_of_limit_functions):
#         if is_time_analysis:
#             for t in range(time_analysis):
#                 column_names.append(f'S_{i}_t={t}')
#         else:
#             column_names.append(f'S_{i}')

#     for i in range(number_of_limit_functions):
#         if is_time_analysis:
#             for t in range(time_analysis):
#                 column_names.append(f'G_{i}_t={t}')
#         else:
#             column_names.append(f'G_{i}')

#     for i in range(number_of_limit_functions):
#         if is_time_analysis:
#             for t in range(time_analysis):
#                 column_names.append(f'I_{i}_t={t}')
#         else:
#             column_names.append(f'I_{i}')

#     results_about_data.columns = column_names

#     # First Barrier Failure (FBF) adjustment if time-dependent
#     if is_time_analysis:
#         results_about_data, _ = parepyco.fbf(
#             algorithm,
#             number_of_limit_functions,
#             time_analysis,
#             results_about_data
#         )

#     return results_about_data



