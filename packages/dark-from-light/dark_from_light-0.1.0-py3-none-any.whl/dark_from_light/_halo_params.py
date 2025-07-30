import astropy.constants as c
import astropy.cosmology as cosmology
import astropy.units as u
import numpy as np
from astropy.units.quantity import Quantity
from jaxtyping import Float


def _calculate_virial_radius(
    lin_mhalo: Float[Quantity, " dim"],
    z: Float[np.ndarray, " dim"],
    cosmo: cosmology.Cosmology,
) -> Float[Quantity, " dim"]:
    """Calculates virial radius from halo mass and redshift.
    Uses the relation R_vir = (G M_h / 100 * H(z)^2)^(1/3).

    Parameters
    ----------
    lin_mhalo : Float[np.ndarray, " dim"]
        Halo mass in units of Msun
    z : Float[np.ndarray, " dim"]
        Redshift
    cosmo : Cosmology
        Cosmology object for calculating H(z)q

    Returns:
    -------
    Float[np.ndarray, " dim"]
        Virial radius in kpc
    """
    hubble_param_at_z = cosmo.H(z)
    out = np.power(
        np.divide(lin_mhalo * c.G, 100 * hubble_param_at_z**2), 1.0 / 3.0
    ).to("kpc")
    assert out.unit == "kpc"

    return out


def _calculate_virial_velocity(
    lin_mhalo: Float[Quantity, " dim"], halo_radius: Float[Quantity, " dim"]
) -> Float[Quantity, " dim"]:
    """Calculates virial velocity from halo mass and radius.
    Uses the relation V_vir = sqrt(G M_h / R_vir).

    Parameters
    ----------
    lin_mhalo : Float[Quantity, " dim"]
        Halo mass in units of Msun
    halo_radius : Float[Quantity, " dim"]
        Halo radius in kpc

    Returns
    -------
    Float[Quantity, " dim"]
        Virial velocity in km/s
    """
    out = np.sqrt(np.divide(lin_mhalo * c.G, halo_radius)).to("km/s")
    assert out.unit == "km/s"

    return out


def _calculate_virial_temperature(
    halo_virial_velocity: Float[Quantity, " dim"], mean_molecular_weight: float = 0.6
) -> Float[Quantity, " dim"]:
    """Calculates virial temperature from halo mass and radius.
    Uses the relation T_vir = (mu * m_p * V_vir^2) / (2 * k_B).

    Parameters
    ----------
    halo_virial_velocity : Float[Quantity, " dim"]
        Halo virial velocity in km/s
    mean_molecular_weight : float, optional
        Mean molecular weight, by default 0.6

    Returns
    -------
    Float[Quantity, " dim"]
        Virial temperature in K
    """
    out = np.divide(
        mean_molecular_weight * c.m_p * halo_virial_velocity**2, 2 * c.k_B
    ).to("K")
    assert out.unit == "K"

    return out


def calculate_virial_quantities(
    mhalo_linear: Float[Quantity, " dim"],
    z: Float[np.ndarray, " dim"],
    cosmo: cosmology.Cosmology,
) -> tuple[Float[Quantity, " dim"], Float[Quantity, " dim"], Float[Quantity, " dim"]]:
    """Calculates virial radius, velocity and temperature from halo mass and redshift.

    Parameters
    ----------
    mhalo_linear : Float[np.ndarray, " dim"]
        Halo mass in units of Msun
    z : Float[np.ndarray, " dim"]
        Redshift
    cosmo : Cosmology
        Cosmology object for calculating H(z)

    Returns
    -------
    tuple[Float[Quantity, " dim"], Float[Quantity, " dim"], Float[Quantity, " dim"]]
        Virial radius in kpc, virial velocity in km/s and virial temperature in K
    """
    halo_radius = _calculate_virial_radius(mhalo_linear, z, cosmo)
    halo_velocity = _calculate_virial_velocity(mhalo_linear, halo_radius)
    halo_temperature = _calculate_virial_temperature(halo_velocity)

    return halo_radius, halo_velocity, halo_temperature
