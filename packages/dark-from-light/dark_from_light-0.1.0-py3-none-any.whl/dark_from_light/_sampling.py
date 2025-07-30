import warnings

import numpy as np
import scipy as sp
from jaxtyping import Float


def _inverse_sampler(
    bins: Float[np.ndarray, " dim"],
    cumulative_dist_function: Float[np.ndarray, " dim"],
    num_samples: int,
    rng: np.random.Generator,
) -> Float[np.ndarray, " num_samples"]:
    """
    Inverse sampling method to sample from a given cumulative
    distribution function (CDF).

    Parameters:
    ----------
    cumulative_distribution : Float[np.ndarray, "dim 2"]
        The cumulative distribution function.
    num_samples : int
        The number of samples to generate.
    rng : np.random.Generator
        Random number generator object

    Returns:
    -------
    Float[np.ndarray, " num_samples"]
        The generated samples.
    """
    # Generate uniform sampling of CDF between 0 and 1
    uniform_draw = rng.uniform(0, 1, size=num_samples)

    return np.interp(uniform_draw, cumulative_dist_function, bins)


def _cdf_generator(
    bins: Float[np.ndarray, "n m"], probabilities: Float[np.ndarray, "n m"]
) -> Float[np.ndarray, "n m"]:
    """
    Generate the cumulative distribution function (CDF) from a given
    probability distribution function (PDF).

    Parameters:
    ----------
    probability_distribution : Float[np.ndarray, "n m"]
        Tabulated probability distribution for n objects
        in m value bins. NOTE: this is not a **density**
        function, but a probability distribution function.

    Returns:
    -------
    Float[np.ndarray, "dim 2"]
        The cumulative distribution function.
    """
    # check if sum to 1
    assert np.all(np.sum(probabilities)) == 1, (
        "The probability distribution must sum to 1."
    )

    # check if PDF well-defined with 0 leading and trailing bins
    if np.any(probabilities[:, 0] != 0):
        warnings.warn("PDF should include 0 leading value. Extending the PDF table")
        probabilities = np.insert(probabilities, 0, 0, axis=1)
        extra = 0.5 * np.diff(bins, axis=1)[:, 0]
        bins = np.insert(bins, 0, bins[:, 0] - extra, axis=1)

    # Compute the CDF
    cdf = np.cumsum(probabilities, axis=1)

    return bins, cdf


def add_mass_cdf(data: dict[str, np.ndarray]) -> None:
    """
    Adds the cumulative distribution function (CDF)
    of stellar mass to teh data dictionary.

    Parameters:
    ----------
    data : dict[str, np.ndarray]
        The data dictionary containing stellar mass
        Probability Distribution Function (PDF)
    """
    bins, cdf = _cdf_generator(
        data["STELLAR_MASS_PDF_BINS"], data["STELLAR_MASS_PDF_VALS"]
    )
    data["STELLAR_MASS_CDF_BINS"] = bins
    data["STELLAR_MASS_CDF_VALS"] = cdf


def _assymetric_gaussian_cdf_generator(
    sigma_minus: float, sigma_plus: float
) -> tuple[Float[np.ndarray, " 100"], Float[np.ndarray, " 100"]]:
    """Generates the CDF of a distribution comprised of two
    Gaussian distributions with different sigmas

    Parameters:
    ----------
    sigma_minus : float
        The standard deviation of the Gaussian distribution for negative bins.
    sigma_plus : float
        The standard deviation of the Gaussian distribution for positive bins.

    Returns:
    -------
    tuple[Float[np.ndarray, " 100"], Float[np.ndarray, " 100"]]
        The bins and the CDF of the distribution.
    """
    alpha_minus = 1.0 / np.sqrt(2 * np.pi * sigma_minus**2)

    bins = np.linspace(-5 * sigma_minus, 5 * sigma_plus, 500)

    probabilities = np.zeros_like(bins)
    probabilities[bins < 0] = alpha_minus * np.exp(
        -0.5 * bins[bins < 0] ** 2 / (2 * sigma_minus**2)
    )
    probabilities[bins >= 0] = alpha_minus * np.exp(
        -0.5 * bins[bins > 0] ** 2 / (2 * sigma_plus**2)
    )

    dx = bins[1] - bins[0]
    cdf = np.cumsum(probabilities * dx)
    cdf /= cdf[-1]  # Normalize to 1
    cdf[0] = 0  # Ensure the CDF starts at 0

    return bins, cdf


def _assymetric_gaussian_draw(
    loc: float,
    sigma_minus: float,
    sigma_plus: float,
    num_samples: int,
    rng: np.random.Generator,
) -> Float[np.ndarray, " num_samples"]:
    """Generates samples from a distribution comprised of two
    Gaussian distributions with different sigmas around x=loc

    Parameters:
    ----------
    loc : float
        The location of the distribution.
    sigma_minus : float
        The standard deviation of the Gaussian distribution for negative bins.
    sigma_plus : float
        The standard deviation of the Gaussian distribution for positive bins.
    num_samples : int
        The number of samples to generate.
    rng : np.random.Generator
        Random number generator object

    Returns:
    -------
    Float[np.ndarray, " num_samples"]
        The generated samples.
    """
    bins, cdf = _assymetric_gaussian_cdf_generator(sigma_minus, sigma_plus)

    return _inverse_sampler(bins, cdf, num_samples, rng) + loc


def generate_mhalo_pdf(
    tree_predictions: Float[np.ndarray, " dim"], num_bins: int = 80
) -> tuple[Float[np.ndarray, " num_bins"], Float[np.ndarray, " num_bins"]]:
    """
    Generate the probability distribution function (PDF) for halo mass
    from the tree predictions.

    Parameters:
    ----------
    tree_predictions : Float[np.ndarray, " dim"]
        The tree predictions for halo mass.
    num_bins : int
        The number of bins to use for the histogram.
        Default is 80.

    Returns:
    -------
    Float[np.ndarray, " num_bins"]
        Bin centers for the generated PDF.

    Float[np.ndarray, " num_bins"]
        Corresponding PDF bins.
    """
    # Generate the PDF from the tree predictions
    pdf, bin_edges = np.histogram(tree_predictions, bins=num_bins)[0]
    bin_centers = bin_edges[:-1] + 0.5 * np.diff(bin_edges)

    # Normalize the PDF
    pdf /= np.sum(pdf)

    return bin_centers, pdf
