import logging
from typing import Literal

import astropy
import astropy.constants as const
import astropy.cosmology as cosmology
import astropy.units as u
import numpy as np
from astropy.units.quantity import Quantity
from jaxtyping import Float, Int
from tqdm import tqdm

from ._cosmo import get_cosmology
from ._data_handling import apply_redshift_cut, load_data, save_output_file
from ._halo_params import calculate_virial_quantities
from ._regression import (
    HybridRegressionModel,
    SingleRegressionModel,
    estimate_group_halo_mass,
    get_group_regression_input,
)
from ._sampling import add_mass_cdf, generate_mhalo_pdf


_logger = logging.getLogger(__name__.split(".")[0])


def _calculate_angular_separation(
    ra_central: Quantity,
    dec_central: Quantity,
    ra: Float[Quantity, " dim"],
    dec: Float[Quantity, " dim"],
    angular_diameter_distance: Quantity,
) -> Float[Quantity, " dim"]:
    """Calculates physical separation between a central galaxy and all other galaxies
    using the Vincenty formula and angular diameter distance for the central galaxy.

    Parameters
    ----------
    ra_central : Quantity
        Right Ascension of the central galaxy
    dec_central : Quantity
        Declination of the central galaxy
    ra : Float[Quantity, " dim"]
        Right Ascension of the sample to calculate distances for
    dec : Float[Quantity, " dim"]
        Declination of the sample to calculate distances for
    angular_diameter_distance : Quantity
        Angular diameter distance at the redshift of the central galaxy

    Returns
    -------
    Float[Quantity, " dim"]
        Physical separation in kpc
    """
    angular_separation = astropy.coordinates.angular_separation(
        ra_central, dec_central, ra, dec
    )

    return (angular_separation * angular_diameter_distance).to("kpc")


def _calculate_velocity_difference(
    redshift_central: float, redshift: Float[np.ndarray, " dim"]
) -> Float[np.ndarray, " dim"]:
    """Calculates the absolute radial velocity difference between a central galaxy and all other galaxies.

    Parameters
    ----------
    redshift_central : float
        Redshift of the central galaxy
    redshift : Float[np.ndarray, " dim"]
        Redshift of the other galaxies

    Returns
    -------
    Float[np.ndarray, " dim"]
        Absolute radial velocity difference in km/s
    """
    return np.abs(
        (redshift_central - redshift) / (1 + (redshift_central + redshift) / 2)
    ) * const.c.to("km/s")


def get_galaxy_group(
    mhalo_log: float,
    mmg_data: dict[str, np.ndarray],
    data: dict[str, np.ndarray],
    distance_on_sky: Float[Quantity, " dim"],
) -> tuple[
    Int[np.ndarray, " k"],
    dict[str, Float[np.ndarray, " k"]],
    int,
    float,
    float,
    float,
    float,
]:
    mhalo_linear = 10**mhalo_log * u.Msun
    group_radius, group_velocity, group_temperature = calculate_virial_quantities(
        mhalo_linear, mmg_data["Z_SPEC"], cosmology
    )

    # Absolute radial velocity difference between galaxies and MMG
    velocity_difference = _calculate_velocity_difference(
        mmg_data["Z_SPEC"], data["Z_SPEC"]
    )

    # Define group members as those within 1R_200 and 1V_200
    [group_idx] = np.where(
        (distance_on_sky <= group_radius) & (velocity_difference <= group_velocity)
    )
    group_data = {key: value[group_idx] for key, value in data.items()}

    ## JMP: what about galaxies at the edge?
    ## JMP: shouldn't they be bound to the nearer of the two haloes?
    ## JMP: maybe this condition doesn't apply if velocity cut exists (?)

    # Define Group Inputs for RF Regressor:
    group_countestimate = group_idx.size
    group_total_massestimate = np.log10(np.power(10, group_data["STELLAR_MASS"].sum()))

    return (
        group_data,
        group_countestimate,
        group_total_massestimate,
        group_idx,
        group_radius,
        group_velocity,
        group_temperature,
    )


def _convergence_looper(
    mhalo_currentestimate: float,
    mmg_data: dict[str, np.ndarray],
    data: dict[str, np.ndarray],
    model: SingleRegressionModel | HybridRegressionModel,
    distance_on_sky: Float[Quantity, " dim"],
    iteration_limit: int,
    convergence_tol: float,
    include_error: bool,
    num_montecarlo: int,
    rng: np.random.Generator,
) -> tuple[float, int]:
    """Verbose looper for group regression

    Returns
    -------
    mhalo_currentestimate: float
        Converged halo mass estimate in log10(Msun)
    total_iterations: int
        Total number of iterations performed
    """

    delta_mhalo = 1
    iteration_num = 0
    verbose = _logger.isEnabledFor(_logger.INFO)

    if verbose:
        _pbar = tqdm(desc="Iteration number", total=iteration_limit)

    while (delta_mhalo > convergence_tol) & (iteration_num < iteration_limit):
        # Get estimated properties of a group for a given halo mass
        group_data, group_countestimate, group_total_massestimate, _ = get_galaxy_group(
            mhalo_currentestimate,
            mmg_data,
            data,
            distance_on_sky,
        )

        # Get input for group halo mass regression model
        group_regression_input = get_group_regression_input(
            mmg_data,
            group_data,
            group_countestimate,
            group_total_massestimate,
            include_error,
            num_montecarlo,
            rng,
        )

        # Predict New Halo Mass from Group Parameters:
        mhaloestimate_new, _ = estimate_group_halo_mass(group_regression_input, model)

        delta_mhalo = np.abs(mhaloestimate_new - mhalo_currentestimate)
        mhalo_currentestimate = mhaloestimate_new.copy()
        iteration_num += 1

        if verbose:
            _pbar.update(1)

    total_iterations = iteration_num + 1

    # get halo mass distribution from trees using the final group_regression input state
    mhalo_currentestimate, tree_predictions = estimate_group_halo_mass(
        group_regression_input, model
    )

    if verbose:
        _pbar.close()

    return mhalo_currentestimate, total_iterations, tree_predictions


def _perform_group_regression(
    data: dict[str, np.ndarray],
    mmg_data: dict[str, np.ndarray],
    mhaloestimate_central: float,
    model: SingleRegressionModel | HybridRegressionModel,
    include_error: bool,
    num_montecarlo: int,
    convergence_tol: float,
    iteration_limit: int,
    rng: np.random.Generator,
):
    """Performs iterative group regression to estimate halo mass

    Parameters
    ----------
    data: dict[str, np.ndarray]
        data object containing the subset of galaxies left to fit
    mmg_data: dict[str, np.ndarray]
        data object containing the most massive galaxy
    mhaloestimate_central: float
        initial estimate of halo mass from central galaxy stellar mass
        In units of log10(Msun)
    model: SingleRegressionModel | HybridRegressionModel
        regression model to use for group mass estimation
    include_error: bool
        whether to include error on stellar mass in the group regression
    num_montecarlo: int
        number of Monte Carlo samples to generate for group regression
    convergence_tol: float
        convergence tolerance for log10(Halo Mass / Msun)
    iteration_limit: int
        maximum number of iterations to perform


    """
    # Initialize parameters for the while loop:
    mhalo_currentestimate = mhaloestimate_central.copy()

    # Calculate physical separation from angular coordinates
    distance_on_sky = _calculate_angular_separation(
        mmg_data["RA"] * u.deg,
        mmg_data["DEC"] * u.deg,
        data["RA"] * u.deg,
        data["DEC"] * u.deg,
        mmg_data["angular_diameter_distance"],
    )

    # Perform group regression
    converged_mhalo, total_iterations, tree_predictions = _convergence_looper(
        mhalo_currentestimate=mhalo_currentestimate,
        mmg_data=mmg_data,
        data=data,
        model=model,
        distance_on_sky=distance_on_sky,
        iteration_limit=iteration_limit,
        convergence_tol=convergence_tol,
        include_error=include_error,
        num_montecarlo=num_montecarlo,
        rng=rng,
    )

    # Get final halo virial quantities and galaxy membership
    (
        _,
        group_count,
        group_stellar_mass,
        group_idx,
        halo_radius,
        halo_velocity,
        halo_temperature,
    ) = get_galaxy_group(
        mhalo_currentestimate=converged_mhalo,
        mmg_data=mmg_data,
        data=data,
        distance_on_sky=distance_on_sky,
    )

    return (
        group_idx,
        group_count,
        group_stellar_mass,
        converged_mhalo,
        tree_predictions,
        halo_radius,
        halo_velocity,
        halo_temperature,
        total_iterations,
    )


class _PrintHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        self.setFormatter(formatter)

    def emit(self, record: logging.LogRecord) -> None:
        print(self.format(record))


def allocate_galaxy_groups(
    input_data_path: str,
    output_data_path: str,
    model_type: Literal["HYBRID", "EAGLE", "TNG"],
    seed: int,
    include_error: bool,
    hubble_param0: float = 70.0,
    omega_matter0: float = 0.3,
    verbose: bool = False,
    convergence_tol: float = 0.05,
    iteration_limit: int = 10,
    num_montecarlo: int = 100,
    zrange: None | tuple[float, float] = None,
) -> None:
    # set up package-lever logger for a verbosity switch
    if verbose:
        _logger.setLevel(logging.INFO)
        # Only add handler if not already present to avoid duplicates
        if not _logger.handlers:
            handler = _PrintHandler()
            _logger.addHandler(handler)
        _logger.propagate = False

    # Get random number generator with a fixed seed
    # This is required for reproducibility

    _logger.info("Using seed %d for random number generator", seed)
    rng = np.random.default_rng(seed)

    _logger.info("Loading data from %s", input_data_path)
    data = load_data(input_data_path)

    if zrange is not None:
        _logger.info("Applying redshift cut: %s < z < %s", zrange[0], zrange[1])
        apply_redshift_cut(data, zrange)

    _logger.info("Calculating angular diameter distance for all galaxies")
    cosmology = get_cosmology(hubble_param0, omega_matter0)
    data["angular_diameter_distance"] = (
        cosmology.angular_diameter_distance(data["Z_SPEC"]).to("kpc") / u.rad
    )

    if include_error and "STELLAR_MASS_PDF_BINS" in data.keys():
        _logger.info("Using Stellar Mass PDFs for error propagation. Adding CDFs")
        add_mass_cdf(data)

    # Load the regression model
    _logger.info("Loading regression model of type %s", model_type)
    if model_type in ["EAGLE", "TNG"]:
        model = SingleRegressionModel(model_type)
    elif model_type == "HYBRID":
        model = HybridRegressionModel()
    else:
        raise ValueError(f"Unknown model model_type: {model_type}")

    sentinel = -999
    size = data["GAL_ID"].size

    # Initialize output arrays
    group_id = np.full(size, sentinel)
    group_count = np.full(size, sentinel)
    mhalo = np.full(size, sentinel)
    mhalo_centrals_only = np.full(size, sentinel)
    group_total_mass = np.full(size, sentinel)
    galaxy_class = np.full(size, sentinel)
    virial_radius = np.full(size, sentinel)
    virial_velocity = np.full(size, sentinel)
    virial_temperature = np.full(size, sentinel)
    num_iter = np.full(size, sentinel)
    mhalo_poserr_2sigma = np.full(size, sentinel)
    mhalo_poserr_1sigma = np.full(size, sentinel)
    mhalo_negerr_1sigma = np.full(size, sentinel)
    mhalo_negerr_2sigma = np.full(size, sentinel)

    mhalo_pdf = np.full((size, 80), sentinel)
    mhalo_pdf_bins = np.full((size, 80), sentinel)

    # Initialize group finding
    group_id_counter = 0
    num_galaxies_to_fit = size

    while num_galaxies_to_fit > 0:
        _logger.info(
            "Running Group: %d | Galaxies remaining to assign %d",
            group_id_counter,
            num_galaxies_to_fit,
        )

        # Select previously unassigned galaxies
        [unassigned_galaxies] = np.where(group_id == sentinel)

        for key in data.keys():
            data[key] = data[key][unassigned_galaxies]

        # Identify Most Mass Galaxy (MMG) remaining in sample:
        mmg_idx = data["STELLAR_MASS"].argmax()
        mmg_data = {key: value[mmg_idx] for key, value in data.items()}

        # Stage 1: Estimate halo mass from central stellar mass
        central_regression_input = np.array(
            [mmg_data["STELLAR_MASS"], mmg_data["Z_SPEC"]]
        ).reshape(1, 2)
        mhaloestimate_central = model.predict_central(central_regression_input)

        # Stage 2: group regression
        (
            group_idx,
            group_count,
            group_stellar_mass,
            group_halo_mass,
            tree_predictions,
            group_virial_radius,
            group_virial_velocity,
            group_virial_temperature,
            total_iterations,
        ) = _perform_group_regression(
            data=data,
            mmg_data=mmg_data,
            mhaloestimate_central=mhaloestimate_central,
            model=model,
            include_error=include_error,
            num_montecarlo=num_montecarlo,
            convergence_tol=convergence_tol,
            iteration_limit=iteration_limit,
            rng=rng,
        )

        # Translate group_idx and mmg_idx to global indices
        global_group_index = unassigned_galaxies[group_idx]
        global_central_index = unassigned_galaxies[mmg_idx]

        # Update results in the master assignment arrays
        group_id[global_group_index] = group_id_counter
        group_count[global_group_index] = group_count
        mhalo[global_group_index] = group_halo_mass
        mhalo_centrals_only[global_group_index] = mhaloestimate_central
        group_total_mass[global_group_index] = group_stellar_mass
        virial_radius[global_group_index] = group_virial_radius
        virial_velocity[global_group_index] = group_virial_velocity
        virial_temperature[global_group_index] = group_virial_temperature
        num_iter[global_group_index] = total_iterations

        # galaxy class tag 0 for centrals, 1 for satellites
        galaxy_class[global_group_index] = 1
        galaxy_class[global_central_index] = 0

        # halo mass percentile values and full PDF
        median, p2_5, p16, p84, p97_5 = np.percentile(
            tree_predictions, [50, 2.5, 16, 84, 97.5]
        )
        mhalo_poserr_2sigma[global_group_index] = p97_5 - median
        mhalo_poserr_1sigma[global_group_index] = p84 - median
        mhalo_negerr_1sigma[global_group_index] = median - p16
        mhalo_negerr_2sigma[global_group_index] = median - p2_5

        mhalo_pdf_bins[global_group_index, :], mhalo_pdf[global_group_index, :] = (
            generate_mhalo_pdf(tree_predictions)
        )

        group_id_counter += 1
        num_galaxies_to_fit -= group_count

    _logger.info(
        "All galaxies assigned to groups. Writing output to %s", output_data_path
    )
    save_output_file(
        output_filename=output_data_path,
        data=data,
        group_id=group_id,
        group_count=group_count,
        mhalo=mhalo,
        mhalo_centrals_only=mhalo_centrals_only,
        group_total_mass=group_total_mass,
        virial_radius=virial_radius,
        viriral_velocity=virial_velocity,
        virial_temperature=virial_temperature,
        num_iter=num_iter,
        galaxy_class=galaxy_class,
        mhalo_poserr_2sigma=mhalo_poserr_2sigma,
        mhalo_poserr_1sigma=mhalo_poserr_1sigma,
        mhalo_negerr_1sigma=mhalo_negerr_1sigma,
        mhalo_negerr_2sigma=mhalo_negerr_2sigma,
        mhalo_pdf_bins=mhalo_pdf_bins,
        mhalo_pdf=mhalo_pdf,
    )
