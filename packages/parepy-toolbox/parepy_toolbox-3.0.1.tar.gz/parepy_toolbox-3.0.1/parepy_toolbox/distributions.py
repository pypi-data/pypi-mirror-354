"""Probability distributions"""
import numpy as np
import scipy as sc


def convert_params_to_scipy(dist: str, parameters: dict) -> dict:
    """
    Convert user-provided distribution parameters to the format required by "scipy.stats".

    :param parameters: Original distribution parameters. (a) 'uniform': keys 'min' and 'max', (b) 'normal': keys 'mean' and 'std', (c) 'lognormal': keys 'mean' and 'std', (d) 'gumbel max': keys 'mean' and 'std', (e) 'gumbel min': keys 'mean' and 'std', (f) 'triangular': keys 'min', 'mode' and 'max', or (g) 'gamma': keys 'mean' and 'std'.

    :return: Distribution parameters according scipy.stats documentation.
    """   

    if dist.lower() == 'uniform':
        parameters_scipy = {'loc': parameters['min'], 'scale': parameters['max'] - parameters['min']}
    elif dist.lower() == 'normal':
        parameters_scipy = {'loc': parameters['mean'], 'scale': parameters['std']}
    elif dist.lower() == 'lognormal':
        epsilon = np.sqrt(np.log(1 + (parameters['std'] / parameters['mean']) ** 2))
        lambda_ = np.log(parameters['mean']) - 0.5 * epsilon ** 2
        parameters_scipy = {'s': epsilon, 'loc': 0.0, 'scale': np.exp(lambda_)}
    elif dist.lower() == 'gumbel max':
        gamma = 0.5772156649015329
        alpha = parameters['std'] * np.sqrt(6) / np.pi
        beta = parameters['mean'] - alpha * gamma
        parameters_scipy = {'loc': beta, 'scale': alpha}
    elif dist.lower() == 'gumbel min':
        gamma = 0.5772156649015329
        alpha = parameters['std'] * np.sqrt(6) / np.pi
        beta = parameters['mean'] + alpha * gamma
        parameters_scipy = {'loc': beta, 'scale': alpha}
    elif dist.lower() == 'triangular':
        parameters_scipy = {'c': (parameters['mode'] - parameters['min']) / (parameters['max'] - parameters['min']), 'loc': parameters['min'], 'scale': parameters['max'] - parameters['min']}
    elif dist.lower() == 'gamma':
        a = (parameters['mean'] / parameters['std']) ** 2
        scale = parameters['std'] ** 2 / parameters['mean']
        parameters_scipy = {'a': a, 'loc': 0.0, 'scale': scale}

    return parameters_scipy


def normal_tail_approximation(dist: str, parameters_scipy: dict, x: float) -> tuple[float, float]:
    """
    Converts non-normal distributions to normal approximations while preserving their statistical properties in x point.

    :param dist: Type of distribution. Supported values: 'uniform', 'normal', 'lognormal', 'gumbel max', 'gumbel min', 'triangular', or 'gamma'.
    :param parameters_scipy: Distribution parameters according scipy.stats documentation.
    :param x: Project point.

    return: output[0] = Mean of the normal approximation at point x, output[1] = Standard deviation of the normal approximation at point x.
    """

    if dist.lower() == 'uniform':
        z_aux = sc.stats.uniform.cdf(x, loc=parameters_scipy['loc'], scale=parameters_scipy['scale'])
        z = sc.stats.norm.ppf(z_aux, loc=0, scale=1)
        num = sc.stats.norm.pdf(z, loc=0, scale=1)
        den = sc.stats.uniform.pdf(x, loc=parameters_scipy['loc'], scale=parameters_scipy['scale'])
        std_eq = num / den
        mean_eq = x - std_eq * z
    elif dist.lower() == 'normal':
        mean_eq = parameters_scipy['loc']
        std_eq = parameters_scipy['scale']
    elif dist.lower() == 'lognormal':
        z_aux = sc.stats.lognorm.cdf(x, s=parameters_scipy['s'], loc=parameters_scipy['loc'], scale=parameters_scipy['scale'])
        z = sc.stats.norm.ppf(z_aux, loc=0, scale=1)
        num = sc.stats.norm.pdf(z, loc=0, scale=1)
        den = sc.stats.lognorm.pdf(x, s=parameters_scipy['s'], loc=parameters_scipy['loc'], scale=parameters_scipy['scale'])
        std_eq = num / den
        mean_eq = x - std_eq * z
    elif dist.lower() == 'gumbel max':
        z_aux = sc.stats.gumbel_r.cdf(x, loc=parameters_scipy['loc'], scale=parameters_scipy['scale'])
        z = sc.stats.norm.ppf(z_aux, loc=0, scale=1)
        num = sc.stats.norm.pdf(z, loc=0, scale=1)
        den = sc.stats.gumbel_r.pdf(x, loc=parameters_scipy['loc'], scale=parameters_scipy['scale'])
        std_eq = num / den
        mean_eq = x - std_eq * z
    elif dist.lower() == 'gumbel min':
        z_aux = sc.stats.gumbel_l.cdf(x, loc=parameters_scipy['loc'], scale=parameters_scipy['scale'])
        z = sc.stats.norm.ppf(z_aux, loc=0, scale=1)
        num = sc.stats.norm.pdf(z, loc=0, scale=1)
        den = sc.stats.gumbel_l.pdf(x, loc=parameters_scipy['loc'], scale=parameters_scipy['scale'])
        std_eq = num / den
        mean_eq = x - std_eq * z
    elif dist.lower() == 'triangular':
        z_aux = sc.stats.triang.cdf(x, c=parameters_scipy['c'], loc=parameters_scipy['loc'], scale=parameters_scipy['scale'])
        z = sc.stats.norm.ppf(z_aux, loc=0, scale=1)
        num = sc.stats.norm.pdf(z, loc=0, scale=1)
        den = sc.stats.triang.pdf(x, c=parameters_scipy['c'], loc=parameters_scipy['loc'], scale=parameters_scipy['scale'])
        std_eq = num / den
        mean_eq = x - std_eq * z
    elif dist.lower() == 'gamma':
        z_aux = sc.stats.gamma.cdf(x, a=parameters_scipy['a'], loc=parameters_scipy['loc'], scale=parameters_scipy['scale'])
        z = sc.stats.norm.ppf(z_aux, loc=0, scale=1)
        num = sc.stats.norm.pdf(z, loc=0, scale=1)
        den = sc.stats.gamma.pdf(x, a=parameters_scipy['a'], loc=parameters_scipy['loc'], scale=parameters_scipy['scale'])
        std_eq = num / den
        mean_eq = x - std_eq * z

    return mean_eq, std_eq


def random_sampling(dist: str, parameters: dict, method: str, n_samples: int) -> list:
    """
    Generates random samples from a specified distribution.

    :param dist: Type of distribution. Supported values: 'uniform', 'normal', 'lognormal', 'gumbel max', 'gumbel min', 'triangular', or 'gamma'.
    :param parameters: Original distribution parameters. (a) 'uniform': keys 'min' and 'max', (b) 'normal': keys 'mean' and 'std', (c) 'lognormal': keys 'mean' and 'std', (d) 'gumbel max': keys 'mean' and 'std', (e) 'gumbel min': keys 'mean' and 'std', (f) 'triangular': keys 'min', 'mode' and 'max', or (g) 'gamma': keys 'mean' and 'std'.    
    :param method: Sampling method. Supported values: 'lhs' (Latin Hypercube Sampling), 'mcs' (Crude Monte Carlo Sampling) or 'sobol' (Sobol Sampling).
    :param n_samples: Number of samples. For Sobol sequences, this variable represents the exponent "m" (n = 2^m).

    :return: Random samples.
    """

    # Convert user parameters to scipy.stats format
    parameters_scipy = convert_params_to_scipy(dist, parameters)

    # Generate random samples based on the specified distribution and method
    if dist.lower() == 'uniform':
        if method.lower() == 'mcs':
            rv = sc.stats.uniform(loc=parameters_scipy['loc'], scale=parameters_scipy['scale'])
            x = list(rv.rvs(size=n_samples))
        elif method.lower() == 'lhs':
            sampler = sc.stats.qmc.LatinHypercube(d=1)
            samples = sampler.random(n=n_samples)
            x = [sc.stats.uniform.ppf(i, loc=parameters_scipy['loc'], scale=parameters_scipy['scale']) for i in samples.flatten()]
        elif method.lower() == 'sobol':
            sampler = sc.stats.qmc.Sobol(d=1)
            samples = sampler.random_base2(m=n_samples)
            x = [sc.stats.uniform.ppf(i, loc=parameters_scipy['loc'], scale=parameters_scipy['scale']) for i in samples.flatten()]
    elif dist.lower() == 'normal':
        if method.lower() == 'mcs':
            rv = sc.stats.norm(loc=parameters_scipy['loc'], scale=parameters_scipy['scale'])
            x = list(rv.rvs(size=n_samples))
        elif method.lower() == 'lhs':
            sampler = sc.stats.qmc.LatinHypercube(d=1)
            samples = sampler.random(n=n_samples)
            x = [sc.stats.norm.ppf(i, loc=parameters_scipy['loc'], scale=parameters_scipy['scale']) for i in samples.flatten()]
        elif method.lower() == 'sobol':
            sampler = sc.stats.qmc.Sobol(d=1)
            samples = sampler.random_base2(m=n_samples)
            x = [sc.stats.norm.ppf(i, loc=parameters_scipy['loc'], scale=parameters_scipy['scale']) for i in samples.flatten()]
    elif dist.lower() == 'lognormal':
        if method.lower() == 'mcs':
            rv = sc.stats.lognorm(s=parameters_scipy['s'], loc=parameters_scipy['loc'], scale=parameters_scipy['scale'])
            x = list(rv.rvs(size=n_samples))
        elif method.lower() == 'lhs':
            sampler = sc.stats.qmc.LatinHypercube(d=1)
            samples = sampler.random(n=n_samples)
            x = [sc.stats.lognorm.ppf(i, s=parameters_scipy['s'], loc=parameters_scipy['loc'], scale=parameters_scipy['scale']) for i in samples.flatten()]
        elif method.lower() == 'sobol':
            sampler = sc.stats.qmc.Sobol(d=1)
            samples = sampler.random_base2(m=n_samples)
            x = [sc.stats.lognorm.ppf(i, s=parameters_scipy['s'], loc=parameters_scipy['loc'], scale=parameters_scipy['scale']) for i in samples.flatten()]
    elif dist.lower() == 'gumbel max':
        if method.lower() == 'mcs':
            rv = sc.stats.gumbel_r(loc=parameters_scipy['loc'], scale=parameters_scipy['scale'])
            x = list(rv.rvs(size=n_samples))
        elif method.lower() == 'lhs':
            sampler = sc.stats.qmc.LatinHypercube(d=1)
            samples = sampler.random(n=n_samples)
            x = [sc.stats.gumbel_r.ppf(i, loc=parameters_scipy['loc'], scale=parameters_scipy['scale']) for i in samples.flatten()]
        elif method.lower() == 'sobol':
            sampler = sc.stats.qmc.Sobol(d=1)
            samples = sampler.random_base2(m=n_samples)
            x = [sc.stats.gumbel_r.ppf(i, loc=parameters_scipy['loc'], scale=parameters_scipy['scale']) for i in samples.flatten()]
    elif dist.lower() == 'gumbel min':
        if method.lower() == 'mcs':
            rv = sc.stats.gumbel_l(loc=parameters_scipy['loc'], scale=parameters_scipy['scale'])
            x = list(rv.rvs(size=n_samples))
        elif method.lower() == 'lhs':
            sampler = sc.stats.qmc.LatinHypercube(d=1)
            samples = sampler.random(n=n_samples)
            x = [sc.stats.gumbel_l.ppf(i, loc=parameters_scipy['loc'], scale=parameters_scipy['scale']) for i in samples.flatten()]
        elif method.lower() == 'sobol':
            sampler = sc.stats.qmc.Sobol(d=1)
            samples = sampler.random_base2(m=n_samples)
            x = [sc.stats.gumbel_l.ppf(i, loc=parameters_scipy['loc'], scale=parameters_scipy['scale']) for i in samples.flatten()]
    elif dist.lower() == 'triangular':
        if method.lower() == 'mcs':
            rv = sc.stats.triang(c=parameters_scipy['c'], loc=parameters_scipy['loc'], scale=parameters_scipy['scale'])
            x = list(rv.rvs(size=n_samples))
        elif method.lower() == 'lhs':
            sampler = sc.stats.qmc.LatinHypercube(d=1)
            samples = sampler.random(n=n_samples)
            x = [sc.stats.triang.ppf(i, c=parameters_scipy['c'], loc=parameters_scipy['loc'], scale=parameters_scipy['scale']) for i in samples.flatten()]
        elif method.lower() == 'sobol':
            sampler = sc.stats.qmc.Sobol(d=1)
            samples = sampler.random_base2(m=n_samples)
            x = [sc.stats.triang.ppf(i, c=parameters_scipy['c'], loc=parameters_scipy['loc'], scale=parameters_scipy['scale']) for i in samples.flatten()]
    elif dist.lower() == 'gamma':
        if method.lower() == 'mcs':
            rv = sc.stats.gamma(a=parameters_scipy['a'], loc=parameters_scipy['loc'], scale=parameters_scipy['scale'])
            x = list(rv.rvs(size=n_samples))
        elif method.lower() == 'lhs':
            sampler = sc.stats.qmc.LatinHypercube(d=1)
            samples = sampler.random(n=n_samples)
            x = [sc.stats.gamma.ppf(i, a=parameters_scipy['a'], loc=parameters_scipy['loc'], scale=parameters_scipy['scale']) for i in samples.flatten()]
        elif method.lower() == 'sobol':
            sampler = sc.stats.qmc.Sobol(d=1)
            samples = sampler.random_base2(m=n_samples)
            x = [sc.stats.gamma.ppf(i, a=parameters_scipy['a'], loc=parameters_scipy['loc'], scale=parameters_scipy['scale']) for i in samples.flatten()]

    return x


def random_sampling_statistcs(dist: str, parameters: dict, value: float):
    """
    """
    
    # Convert user parameters to scipy.stats format
    parameters_scipy = convert_params_to_scipy(dist, parameters)
    
    if dist.lower() == 'uniform':
        rv = sc.stats.uniform(loc=parameters_scipy['loc'], scale=parameters_scipy['scale'])
        pdf = rv.pdf(value)
        cdf = rv.cdf(value)
        icdf = rv.ppf(value)
    elif dist.lower() == 'normal':
        rv = sc.stats.norm(loc=parameters_scipy['loc'], scale=parameters_scipy['scale'])
        pdf = rv.pdf(value)
        cdf = rv.cdf(value)
        icdf = rv.ppf(value)

    return pdf, cdf, icdf

# def crude_sampling_zero_one(n_samples: int, seed: Optional[int] = None) -> list:
#     """
#     Generates a uniform sampling between 0 and 1.

#     :param n_samples: Number of samples.
#     :param seed: Seed for reproducible random number generation. If None (default), the results are non-repeatable.

#     :return: Random samples.
#     """

#     rng = np.random.default_rng(seed=seed)

#     return rng.random(n_samples).tolist()


# def lhs_sampling_zero_one(n_samples: int, dimension: int, seed: Optional[int] = None) -> np.ndarray:
#     """
#     Generates a uniform sampling between 0 and 1 using the Latin Hypercube Sampling algorithm.

#     :param n_samples: Number of samples.
#     :param dimension: Number of dimensions.
#     :param seed: Seed for reproducible random number generation. If None (default), the results are non-repeatable.

#     :return: Random samples.
    
#     # Theory:
#     Latin hypercube sampling is a stratified sampling technique that produces random numbers in terms of the marginal CDF of a random input variable.
    
#     ### PDF
#     $$
#     f(x) = \begin{cases} 
#                 \frac{1}{b-a} & \text{se } a \leq x \leq b \\
#                 0 & \text{caso contrário}
#             \end{cases}
#     $$
    
#     ### CDF
    
#     $$
#     F(x) = \begin{cases}
#                 0 & \text{se } x < a \\
#                 \frac{x-a}{b-a} & \text{se } a \leq x \leq b \\
#                 1 & \text{se } x > b
#             \end{cases}
#     $$
#     """

#     r = np.zeros((n_samples, dimension))
#     p = np.zeros((n_samples, dimension))
#     original_ids = [i for i in range(1, n_samples+1)]
#     if seed is not None:
#         x = crude_sampling_zero_one(n_samples * dimension, seed)
#     else:
#         x = crude_sampling_zero_one(n_samples * dimension)
#     for i in range(dimension):
#         perms = original_ids.copy()
#         r[:, i] = x[:n_samples]
#         del x[:n_samples]
#         rng = np.random.default_rng(seed=seed)
#         rng.shuffle(perms)
#         p[:, i] = perms.copy()
#     u = (p - r) * (1 / n_samples)

#     return u


# def uniform_sampling(parameters: dict, method: str, n_samples: int, seed: Optional[int] = None) -> list:
#     """
#     Generates a uniform sampling between a minimum (a) and maximum (b) value.

#     :param parameters: Distribution parameters. (a) key 'min': Minimum value. (b) key 'max': Maximum value.
#     :param method: Sampling method. Supported values: 'lhs' (Latin Hypercube Sampling) or 'mcs' (Crude Monte Carlo Sampling).
#     :param n_samples: Number of samples.
#     :param seed: Seed for reproducible random number generation. If None (default), the results are non-repeatable.

#     :return: Random samples.
#     """

#     # Random uniform sampling between 0 and 1
#     if method.lower() == 'mcs':
#         if seed is not None:
#             u_aux = crude_sampling_zero_one(n_samples, seed)
#         elif seed is None:
#             u_aux = crude_sampling_zero_one(n_samples)
#     elif method.lower() == 'lhs':
#         if seed is not None:
#             u_aux = lhs_sampling_zero_one(n_samples, 1, seed).flatten()
#         elif seed is None:
#             u_aux = lhs_sampling_zero_one(n_samples, 1).flatten()

#     # PDF parameters and generation of samples    
#     a = parameters['min']
#     b = parameters['max']
#     u = [float(a + (b - a) * i) for i in u_aux]

#     return u


# def normal_sampling(parameters: dict, method: str, n_samples: int, seed: int=None) -> list:
#     """
#     Generates a normal (Gaussian) sampling with specified mean (mu) and standard deviation (sigma).

#     :param parameters: Dictionary of parameters, including:
    
#         - 'mu': Mean of the normal distribution.
#         - 'sigma': Standard deviation of the normal distribution.

#     :param method: Sampling method. Supported values: 'lhs' (Latin Hypercube Sampling) or 'mcs' (Crude Monte Carlo Sampling).
#     :param n_samples: Number of samples.
#     :param seed: Seed for random number generation. Default is None for a random seed.

#     :return: List of random samples.
#     """

#     # Random uniform sampling between 0 and 1
#     if method.lower() == 'mcs':
#         if seed is not None:
#             u_aux1 = crude_sampling_zero_one(n_samples, seed)
#             u_aux2 = crude_sampling_zero_one(n_samples, seed+1)
#         elif seed is None:
#             u_aux1 = crude_sampling_zero_one(n_samples)
#             u_aux2 = crude_sampling_zero_one(n_samples)
#     elif method.lower() == 'lhs':
#         if seed is not None:
#             u_aux1 = lhs_sampling_zero_one(n_samples, 2, seed)
#         elif seed is None:
#             u_aux1 = lhs_sampling_zero_one(n_samples, 2)

#     # PDF parameters and generation of samples  
#     mean = parameters['mean']
#     std = parameters['sigma']
#     u = []
#     for i in range(n_samples):
#         if method.lower() == 'lhs':
#             z = float(np.sqrt(-2 * np.log(u_aux1[i, 0])) * np.cos(2 * np.pi * u_aux1[i, 1]))
#         elif method.lower() == 'mcs':
#             z = float(np.sqrt(-2 * np.log(u_aux1[i])) * np.cos(2 * np.pi * u_aux2[i]))
#         u.append(mean + std * z)

#     return u


# def corr_normal_sampling(parameters_b: dict, parameters_g: dict, pho_gb: float, method: str, n_samples: int, seed: int=None) -> list:
#     """
#     Generates a normal (Gaussian) sampling with specified mean (mu) and standard deviation (sigma).

#     Variable g has a correlation `rho_gb` with b.

#     :param parameters: Dictionary of parameters, including:

#         - 'mu': Mean of the normal distribution.
#         - 'sigma': Standard deviation of the normal distribution.

#     :param method: Sampling method. Supported values: 'lhs' (Latin Hypercube Sampling) or 'mcs' (Crude Monte Carlo Sampling).
#     :param n_samples: Number of samples.
#     :param seed: Seed for random number generation. Use None for a random seed.

#     :return: List of random samples.
#     """

#     # Random uniform sampling between 0 and 1
#     if method.lower() == 'mcs':
#         if seed is not None:
#             u_aux1 = crude_sampling_zero_one(n_samples, seed)
#             u_aux2 = crude_sampling_zero_one(n_samples, seed+1)
#         elif seed is None:
#             u_aux1 = crude_sampling_zero_one(n_samples)
#             u_aux2 = crude_sampling_zero_one(n_samples)
#     elif method.lower() == 'lhs':
#         if seed is not None:
#             u_aux1 = lhs_sampling_zero_one(n_samples, 2, seed)
#         elif seed is None:
#             u_aux1 = lhs_sampling_zero_one(n_samples, 2)

#     # PDF parameters and generation of samples  
#     mean_b = parameters_b['mean']
#     std_b = parameters_b['sigma']
#     mean_g = parameters_g['mean']
#     std_g = parameters_g['sigma']
#     b = []
#     g = []
#     for i in range(n_samples):
#         if method.lower() == 'lhs':
#             z_1 = float(np.sqrt(-2 * np.log(u_aux1[i, 0])) * np.cos(2 * np.pi * u_aux1[i, 1]))
#             z_2 = float(np.sqrt(-2 * np.log(u_aux1[i, 0])) * np.sin(2 * np.pi * u_aux1[i, 1]))
#         elif method.lower() == 'mcs':
#             z_1 = float(np.sqrt(-2 * np.log(u_aux1[i])) * np.cos(2 * np.pi * u_aux2[i]))
#             z_2 = float(np.sqrt(-2 * np.log(u_aux1[i])) * np.sin(2 * np.pi * u_aux2[i]))
#         b.append(mean_b + std_b * z_1)
#         g.append(mean_g + std_g * (pho_gb * z_1 + z_2 * np.sqrt(1 - pho_gb ** 2)))

#     return b, g


# def lognormal_sampling(parameters: dict, method: str, n_samples: int, seed: int=None) -> list:
#     """
#     Generates a log-normal sampling with specified mean and standard deviation.

#     :param parameters: Dictionary of parameters, including:

#         - 'mu': Mean of the underlying normal distribution.
#         - 'sigma': Standard deviation of the underlying normal distribution.

#     :param method: Sampling method. Supported values: 'lhs' (Latin Hypercube Sampling) or 'mcs' (Crude Monte Carlo Sampling).
#     :param n_samples: Number of samples.
#     :param seed: Seed for random number generation.

#     :return: List of random samples.
#     """



#     # Random uniform sampling between 0 and 1
#     if method.lower() == 'mcs':
#         if seed is not None:
#             u_aux1 = crude_sampling_zero_one(n_samples, seed)
#             u_aux2 = crude_sampling_zero_one(n_samples, seed+1)
#         elif seed is None:
#             u_aux1 = crude_sampling_zero_one(n_samples)
#             u_aux2 = crude_sampling_zero_one(n_samples)
#     elif method.lower() == 'lhs':
#         if seed is not None:
#             u_aux1 = lhs_sampling_zero_one(n_samples, 2, seed)
#         elif seed is None:
#             u_aux1 = lhs_sampling_zero_one(n_samples, 2)

#     # PDF parameters and generation of samples  
#     mean = parameters['mean']
#     std = parameters['sigma']
#     epsilon = np.sqrt(np.log(1 + (std/mean)**2))
#     lambdaa = np.log(mean) - 0.5 * epsilon**2
#     u = []
#     for i in range(n_samples):
#         if method.lower() == 'lhs':
#             z = float(np.sqrt(-2 * np.log(u_aux1[i, 0])) * np.cos(2 * np.pi * u_aux1[i, 1]))
#         elif method.lower() == 'mcs':
#             z = float(np.sqrt(-2 * np.log(u_aux1[i])) * np.cos(2 * np.pi * u_aux2[i]))
#         u.append(np.exp(lambdaa + epsilon * z))

#     return u


# def gumbel_max_sampling(parameters: dict, method: str, n_samples: int, seed: int=None) -> list:
#     """
#     Generates a Gumbel maximum distribution with specified mean and standard deviation.

#     :param parameters: Dictionary of parameters, including:

#         - 'mu': Mean of the Gumbel distribution.
#         - 'sigma': Standard deviation of the Gumbel distribution.

#     :param method: Sampling method. Supported values: 'lhs' (Latin Hypercube Sampling) or 'mcs' (Crude Monte Carlo Sampling).
#     :param n_samples: Number of samples.
#     :param seed: Seed for random number generation.

#     :return: List of random samples.
#     """
#     # Random uniform sampling between 0 and 1
#     if method.lower() == 'mcs':
#         if seed is not None:
#             u_aux = crude_sampling_zero_one(n_samples, seed)
#         elif seed is None:
#             u_aux = crude_sampling_zero_one(n_samples)
#     elif method.lower() == 'lhs':
#         if seed is not None:
#             u_aux = lhs_sampling_zero_one(n_samples, 1, seed).flatten()
#         elif seed is None:
#             u_aux = lhs_sampling_zero_one(n_samples, 1).flatten()

#     # PDF parameters and generation of samples  
#     mean = parameters['mean']
#     std = parameters['sigma']
#     gamma = 0.577215665
#     beta = np.pi / (np.sqrt(6) * std)
#     alpha = mean - gamma / beta
#     u = []
#     for i in range(n_samples):
#         u.append(alpha - (1 / beta) * np.log(-np.log(u_aux[i])))

#     return u


# def gumbel_min_sampling(parameters: dict, method: str, n_samples: int, seed: int=None) -> list:
#     """
#     Generates a Gumbel minimum distribution with specified mean and standard deviation.

#     :param parameters: Dictionary of parameters, including:

#         - 'mu': Mean of the Gumbel distribution.
#         - 'sigma': Standard deviation of the Gumbel distribution.

#     :param method: Sampling method. Supported values: 'lhs' (Latin Hypercube Sampling) or 'mcs' (Crude Monte Carlo Sampling).
#     :param n_samples: Number of samples.
#     :param seed: Seed for random number generation.

#     :return: List of random samples.
#     """


#     # Random uniform sampling between 0 and 1
#     if method.lower() == 'mcs':
#         if seed is not None:
#             u_aux = crude_sampling_zero_one(n_samples, seed)
#         elif seed is None:
#             u_aux = crude_sampling_zero_one(n_samples)
#     elif method.lower() == 'lhs':
#         if seed is not None:
#             u_aux = lhs_sampling_zero_one(n_samples, 1, seed).flatten()
#         elif seed is None:
#             u_aux = lhs_sampling_zero_one(n_samples, 1).flatten()

#     # PDF parameters and generation of samples  
#     mean = parameters['mean']
#     std = parameters['sigma']
#     gamma = 0.577215665
#     beta = np.pi / (np.sqrt(6) * std) 
#     alpha = mean + gamma / beta
#     u = []
#     for i in range(n_samples):
#         u.append(alpha + (1 / beta) * np.log(-np.log(1 - u_aux[i])))

#     return u


# def triangular_sampling(parameters: dict, method: str, n_samples: int, seed: int=None) -> list:
#     """
#     Generates a triangular sampling with minimum a, mode c, and maximum b.

#     :param parameters: Dictionary of parameters, including:

#         - 'a': Minimum value of the distribution.
#         - 'c': Mode (most likely value) of the distribution.
#         - 'b': Maximum value of the distribution.

#     :param method: Sampling method. Supported values: 'lhs' (Latin Hypercube Sampling) or 'mcs' (Crude Monte Carlo Sampling).
#     :param n_samples: Number of samples.
#     :param seed: Seed for random number generation.

#     :return: List of random samples.
#     """


#     # Random uniform sampling between 0 and 1
#     if method.lower() == 'mcs':
#         if seed is not None:
#             u_aux = crude_sampling_zero_one(n_samples, seed)
#         elif seed is None:
#             u_aux = crude_sampling_zero_one(n_samples)
#     elif method.lower() == 'lhs':
#         if seed is not None:
#             u_aux = lhs_sampling_zero_one(n_samples, 1, seed).flatten()
#         elif seed is None:
#             u_aux = lhs_sampling_zero_one(n_samples, 1).flatten()

#     # PDF parameters and generation of samples  
#     a = parameters['min']
#     c = parameters['mode']
#     b = parameters['max']
#     u = []
#     for i in range(n_samples):
#         criteria = (c - a) / (b - a)
#         if u_aux[i] < criteria:
#             u.append(a + np.sqrt(u_aux[i] * (b - a) * (c - a)))
#         else:
#             u.append(b - np.sqrt((1 - u_aux[i]) * (b - a) * (b - c)))

#     return u


# def cdf_gumbel_max(x: float, u: float, beta: float) -> float:
#     """
#     Calculates the cumulative distribution function (CDF) of the Maximum Gumbel distribution.

#     :param x: Input value for which the CDF will be calculated.
#     :param u: Location parameter (mode) of the Maximum Gumbel distribution.
#     :param beta: Scale parameter of the Maximum Gumbel distribution.

#     :return: Value of the CDF at point x.
#     """
#     fx = np.exp(-np.exp((- beta * (x - u))))
#     return fx


# def pdf_gumbel_max(x: float, u: float, beta: float) -> float:
#     """
#     Calculates the probability density function (PDF) of the Maximum Gumbel distribution.

#     :param x: Input value for which the PDF will be calculated.
#     :param u: Location parameter (mode) of the Maximum Gumbel distribution.
#     :param beta: Scale parameter of the Maximum Gumbel distribution.

#     :return: Value of the PDF at point x.
#     """
#     fx = beta * np.exp((- beta * (x - u))) - np.exp((- beta * (x - u)))
#     return fx


# def cdf_gumbel_min(x: float, u: float, beta: float) -> float:
#     """
#     Calculates the cumulative distribution function (CDF) of the Minimum Gumbel distribution.

#     :param x: Input value for which the CDF will be calculated.
#     :param u: Location parameter (mode) of the Minimum Gumbel distribution.
#     :param beta: Scale parameter of the Minimum Gumbel distribution.

#     :return: Value of the CDF at point x.
#     """
#     fx = 1 - np.exp(- np.exp((beta * (x - u))))
#     return fx


# def pdf_gumbel_min(x: float, u: float, beta: float) -> float:
#     """
#     Calculates the probability density function (PDF) of the Minimum Gumbel distribution.

#     :param x: Input value for which the PDF will be calculated.
#     :param u: Location parameter (mode) of the Minimum Gumbel distribution.
#     :param beta: Scale parameter of the Minimum Gumbel distribution.

#     :return: Value of the PDF at point x.
#     """
#     fx = beta * np.exp((beta * (x - u))) - np.exp(beta * (x - u))
#     return fx


# def cdf_normal(x: float, u: float, sigma: float) -> float:
#     """
#     Calculates the cumulative distribution function (CDF) of the Normal distribution.

#     :param x: Input value for which the CDF will be calculated.
#     :param u: Mean (location) of the Normal distribution.
#     :param sigma: Standard deviation (scale) of the Normal distribution.

#     :return: Value of the CDF at point x.
#     """
#     fx = norm.cdf(x, loc=u, scale=sigma)
#     return fx


# def pdf_normal(x: float, u: float, sigma: float) -> float:
#     """
#     Calculates the probability density function (PDF) of the Normal distribution.

#     :param x: Input value for which the PDF will be calculated.
#     :param u: Mean (location) of the Normal distribution.
#     :param sigma: Standard deviation (scale) of the Normal distribution.

#     :return: Value of the PDF at point x.
#     """
#     fx = norm.pdf(x, loc=u, scale=sigma)
#     return fx


# def log_normal(x: float, lambdaa: float, epsilon: float) -> tuple[float, float]:
#     """
#     Calculates the location (u) and scale (sigma) parameters for a Log-Normal distribution.

#     :param x: Input value.
#     :param lambdaa: Shape parameter of the Log-Normal distribution.
#     :param epsilon: Scale parameter of the Log-Normal distribution.

#     :return: Tuple containing:
#         - u: Location parameter.
#         - sigma: Scale parameter.
#     """
#     loc = x * (1 - np.log(x) + lambdaa)
#     sigma = x * epsilon
#     return loc, sigma


# def non_normal_approach_normal(x, dist, params):
#     """
#     Converts a non-normal distribution to an equivalent normal distribution.

#     :param x: Random variable.
#     :param dist: Type of distribution. Supported values: 'gumbel max', 'gumbel min', 'lognormal'.
#     :param params: Dictionary of distribution parameters, depending on the selected distribution type.

#         - For 'gumbel max' or 'gumbel min': {'mu': location, 'sigma': scale}
#         - For 'lognormal': {'lambda': shape, 'epsilon': scale}

#     :return: Tuple containing:
#         - mu_t: Mean of the equivalent normal distribution.
#         - sigma_t: Standard deviation of the equivalent normal distribution.
#     """
#     if dist == 'gumbel max':
#         u = params.get('u')
#         beta = params.get('beta')
#         cdf_x = cdf_gumbel_max(x, u, beta)
#         pdf_temp = pdf_gumbel_max(x, u, beta)
#     elif dist == 'gumbel min':
#         u = params.get('u')
#         beta = params.get('beta')
#         cdf_x = cdf_gumbel_min(x, u, beta)
#         pdf_temp = pdf_gumbel_min(x, u, beta)
    
#     if dist == 'lognormal':
#         epsilon = params.get('epsilon')
#         lambdaa = params.get('lambda')
#         loc_eq, sigma_eq = log_normal(x, lambdaa, epsilon)
#     else:
#         icdf = norm.ppf(cdf_x, loc=0, scale=1)
#         sigma_eq = norm.pdf(icdf, loc=0, scale=1) / pdf_temp
#         loc_eq = x - sigma_eq * icdf

#     return float(loc_eq), float(sigma_eq)
