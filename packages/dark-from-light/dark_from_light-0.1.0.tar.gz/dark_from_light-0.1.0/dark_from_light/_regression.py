from typing import Literal

import joblib
import numpy as np
from jaxtyping import Float
from sklearn.ensemble import RandomForestRegressor

from ._sampling import _assymetric_gaussian_draw, _inverse_sampler


class SingleRegressionModel:
    """Class to load and manage a single regression model of flavour EAGLE or TNG."""

    central: RandomForestRegressor
    group: RandomForestRegressor

    def __init__(self, flavour: Literal["EAGLE", "TNG"]):
        self.flavour = flavour
        self.central = joblib.load(
            f"MODELS/RF_reg_model-cen-zall-{self.flavour}-adv.joblib"
        )
        self.group = joblib.load(
            f"MODELS/RF_reg_model-all-zall-{self.flavour}-adv.joblib"
        )

    def predict_central(self, x: Float[np.ndarray, " dim"]):
        return self.central.predict(x)

    def predict_group(self, x: Float[np.ndarray, "dim 4"]):
        return self.group.predict(x)

    def tree_predictions_central(self, x: Float[np.ndarray, " dim"]):
        return np.concatenate([tree.predict(x) for tree in self.central.estimators_])

    def tree_predictions_group(self, x: Float[np.ndarray, "dim 4"]):
        return np.concatenate([tree.predict(x) for tree in self.group.estimators_])


class HybridRegressionModel:
    """Class to load and manage hybrid regression models (EAGLE+TNG)."""

    central_TNG: RandomForestRegressor
    central_EAGLE: RandomForestRegressor
    group_TNG: RandomForestRegressor
    group_EAGLE: RandomForestRegressor

    def __init__(self):
        self.central_TNG = joblib.load("MODELS/RF_reg_model-cen-zall-TNG-adv.joblib")
        self.central_EAGLE = joblib.load(
            "MODELS/RF_reg_model-cen-zall-EAGLE-adv.joblib"
        )
        self.group_TNG = joblib.load("MODELS/RF_reg_model-all-zall-TNG-adv.joblib")
        self.group_EAGLE = joblib.load("MODELS/RF_reg_model-all-zall-EAGLE-adv.joblib")

    def predict_central(
        self,
        x: Float[np.ndarray, " dim"],
    ):
        return 0.5 * (self.central_EAGLE.predict(x) + self.central_TNG.predict(x))

    def predict_group(self, x: Float[np.ndarray, "dim 4"]):
        return 0.5 * (self.group_EAGLE.predict(x) + self.group_TNG.predict(x))

    def tree_predictions_central(
        self,
        x: Float[np.ndarray, " dim"],
    ):
        trees_EAGLE = np.concatenate(
            [tree.predict(x) for tree in self.central_EAGLE.estimators_]
        )
        trees_TNG = np.concatenate(
            [tree.predict(x) for tree in self.central_TNG.estimators_]
        )
        return np.concatenate([trees_EAGLE, trees_TNG])

    def tree_predictions_group(
        self,
        x: Float[np.ndarray, "dim 4"],
    ):
        trees_EAGLE = np.concatenate(
            [tree.predict(x) for tree in self.group_EAGLE.estimators_]
        )
        trees_TNG = np.concatenate(
            [tree.predict(x) for tree in self.group_TNG.estimators_]
        )
        return np.concatenate([trees_EAGLE, trees_TNG])


def _group_regression_input_noerror(
    mmg_data: dict[str, np.ndarray],
    group_count_estimate: int,
    group_total_mass_estimate: float,
    num_montecarlo: int,
) -> Float[np.ndarray, "num_montecarlo 4"]:
    """Generates the input for the group regression model without error on mass

    Parameters
    ----------
    mmg_data : dict[str, np.ndarray]
        Data fields for the most massive galaxy (MMG)
    group_count_estimate : int
        Estimated number of galaxies in the group
    group_total_mass_estimate : float
        Estimated total stellar mass of the group
    num_montecarlo : int
        Number of Monte Carlo samples to generate
    """
    out = np.zeros((num_montecarlo, 4))
    out[:, 0] = mmg_data["STELLAR_MASS"]
    out[:, 1] = group_total_mass_estimate
    out[:, 2] = group_count_estimate
    out[:, 3] = mmg_data["Z_SPEC"]

    return out


def _group_regression_input_pointerror(
    mmg_data: dict[str, np.ndarray],
    group_data: dict[str, np.ndarray],
    group_count_estimate: int,
    group_total_mass_estimate: float,
    num_montecarlo: int,
    rng: np.random.Generator,
) -> Float[np.ndarray, "num_montecarlo 4"]:
    """Generates input for the group regression model using Gaussian errors
    on stellar masses of all galaxies in the group

    Parameters
    ----------
    mmg_data : dict[str, np.ndarray]
        Data fields for the most massive galaxy (MMG)
    group_data : dict[str, np.ndarray]
        Data fields for the group galaxies
    group_count_estimate : int
        Estimated number of galaxies in the group
    group_total_mass_estimate : float
        Estimated total stellar mass of the group
    num_montecarlo : int
        Number of Monte Carlo samples to generate
    rng : np.random.Generator
        Random number generator object

    Returns
    -------
    Float[np.ndarray, "num_montecarlo 4"]
        Monte Carlo samples of stellar mass and group total mass generated from
        Gaussian errors, together with group count, and redshift.
        The draw for group total mass is done from a distribution
        comprised of two Gaussians with different sigmas.

    """
    out = np.zeros((num_montecarlo, 4))

    mass_linear = 10 ** group_data["STELLAR_MASS"]
    mass_lolim = 10 ** (group_data["STELLAR_MASS"] - group_data["STELLAR_MASS_ERROR"])
    mass_uplim = 10 ** (group_data["STELLAR_MASS"] + group_data["STELLAR_MASS_ERROR"])
    mass_error_pos = np.linalg.norm(mass_uplim - mass_linear)
    mass_error_neg = np.linalg.norm(mass_linear - mass_lolim)

    group_error_pos = (
        np.log10(10**group_total_mass_estimate + mass_error_pos)
        - group_total_mass_estimate
    )
    group_error_neg = group_total_mass_estimate - np.log10(
        10**group_total_mass_estimate - mass_error_neg
    )

    out[:, 0] = rng.normal(
        mmg_data["STELLAR_MASS"], mmg_data["STELAR_MASS_ERROR"], num_montecarlo
    )
    out[:, 1] = _assymetric_gaussian_draw(
        group_total_mass_estimate, group_error_neg, group_error_pos, num_montecarlo, rng
    )
    out[:, 2] = group_count_estimate
    out[:, 3] = mmg_data["Z_SPEC"]

    return out


def _group_regression_input_pdf(
    mmg_data: dict[str, np.ndarray],
    group_data: dict[str, np.ndarray],
    group_count_estimate: int,
    num_montecarlo: int,
    rng: np.random.Generator,
) -> Float[np.ndarray, "num_montecarlo 4"]:
    """Generates input for the group regression model using individual galaxy mass CDFs

    Parameters
    ----------
    mmg_data : dict[str, np.ndarray]
        Data fields for the most massive galaxy (MMG)
    group_data : dict[str, np.ndarray]
        Data fields for the group galaxies
    group_count_estimate : int
        Estimated number of galaxies in the group
    num_montecarlo : int
        Number of Monte Carlo samples to generate
    rng : np.random.Generator
        Random number generator object

    Returns
    -------
    Float[np.ndarray, "num_montecarlo 4"]
        Monte Carlo samples of stellar mass and group total mass generated from
        full mass CDFs, together with group count, and redshift
    """
    out = np.zeros((num_montecarlo, 4))

    out[:, 0] = _inverse_sampler(
        mmg_data["STELLAR_MASS_CDF_BINS"],
        mmg_data["STELLAR_MASS_CDF_VALS"],
        num_montecarlo,
        rng,
    )

    # loop through each galaxy in the group and sample from their PDFs
    for i in range(group_data["STELLAR_MASS"].size):
        # sample from the PDF of the group galaxy
        out[:, 1] += _inverse_sampler(
            group_data["STELLAR_MASS_CDF_BINS"][i],
            group_data["STELLAR_MASS_CDF_VALS"][i],
            num_montecarlo,
            rng,
        )

    out[:, 2] = group_count_estimate
    out[:, 3] = mmg_data["Z_SPEC"]

    return out


def get_group_regression_input(
    mmg_data: dict[str, np.ndarray],
    group_data: dict[str, np.ndarray],
    group_count_estimate: int,
    group_total_mass_estimate: float,
    include_error: bool,
    num_montecarlo: int,
    rng: np.random.Generator,
) -> Float[np.ndarray, "num_montecarlo 4"]:
    """Generates input for the group regression model
    based on the type and presence of errors on
    stellar mass in individual galaxies."""

    if include_error:
        if "STELLAR_MASS_CDF_BINS" in group_data.columns.names:
            return _group_regression_input_pdf(
                mmg_data, group_data, group_count_estimate, num_montecarlo, rng
            )
        else:
            return _group_regression_input_pointerror(
                mmg_data,
                group_data,
                group_count_estimate,
                group_total_mass_estimate,
                num_montecarlo,
                rng,
            )

    else:
        return _group_regression_input_noerror(
            mmg_data, group_count_estimate, group_total_mass_estimate, num_montecarlo
        )


def estimate_group_halo_mass(
    group_regression_input: Float[np.ndarray, "num_montecarlo 4"],
    model: SingleRegressionModel | HybridRegressionModel,
) -> tuple[float, Float[np.ndarray, " dim"]]:
    """Estimate group halo mass using the group regression model

    Parameters
    ----------
    group_regression_input : Float[np.ndarray, "num_montecarlo 4"]
        Input for the group regression model
    model : SingleRegressionModel | HybridRegressionModel
        Regression model to use for group mass estimation
    num_montecarlo : int
        Number of Monte Carlo samples to generate

    Returns
    -------
    float:
        Estimated halo mass in log10(Msun)

    Float[np.ndarray, " dim"]:
        All predictions from individual decision trees in the RF
        regression model


    """
    tree_predictions = model.tree_predictions_group(group_regression_input)
    mhalo_estimate = np.mean(tree_predictions)
    return mhalo_estimate, tree_predictions
