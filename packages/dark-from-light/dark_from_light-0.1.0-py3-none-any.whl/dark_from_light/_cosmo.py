import astropy.cosmology as cosmology


def get_cosmology(
    h0: float,
    om0: float,
) -> cosmology.Cosmology:
    """
    Returns a cosmology.FlatLambdaCDM cosmology object
    for a given H0 and Omega_m0.
    """
    return cosmology.cosmology.FlatLambdaCDM(H0=h0, Om0=om0)
