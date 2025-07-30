import logging
import pathlib

import astropy
import astropy.io
import numpy as np
from jaxtyping import Float, Int


_logger = logging.getLogger(__name__.split(".")[0])


def load_data(filepath: pathlib.Path) -> dict[str, np.ndarray]:
    """Loads data from a file. Accepts both FITS and ASCII formats.

    Parameters
    ----------
    filepath : pathlib.Path
        path to the input file

    Returns:
    --------
        dict[str, np.ndarray]: _description_
    """
    # PAK: add field validation
    out = dict()
    if filepath.suffix == ".fits":
        with astropy.io.fits.open(filepath) as hdu:
            for key in hdu[1].data.columns.names:
                out[key] = hdu[1].data[key]
    elif filepath.suffix == ".ascii":
        with astropy.io.ascii.read(filepath) as cat:
            for key in cat.columns.names:
                out[key] = np.asarray(cat[key])
    else:
        raise ValueError(f"Unsupported file format: {filepath.suffix}")

    return out


def apply_redshift_cut(
    data: dict[str, np.ndarray], zrange: tuple[float, float]
) -> None:
    """Applies a redshift cut to the data.

    Parameters
    ----------
    data : dict[str, np.ndarray]
        data to be filtered
    zrange : tuple[float, float]
        redshift range

    Returns
    -------
    dict[str, np.ndarray]
        filtered data
    """
    _logger.info("Applying redshift cut")
    size_before = data["Z_SPEC"].size

    [subset] = np.where((data["Z_SPEC"] >= zrange[0]) & (data["Z_SPEC"] <= zrange[1]))
    out = {key: value[subset] for key, value in data.items()}

    size_after = out["Z_SPEC"].size
    _logger.info(
        "Redshift cut applied. Remaining %d (%.2f %%)\n",
        size_after,
        100 * size_after / size_before,
    )


def save_output_file(
    output_filename: pathlib.Path,
    data: dict[str, np.ndarray],
    group_id: Float[np.ndarray, " dim"],
    group_count: Int[np.ndarray, " dim"],
    mhalo: Float[np.ndarray, " dim"],
    mhalo_centrals_only: Float[np.ndarray, " dim"],
    group_total_mass: Float[np.ndarray, " dim"],
    virial_radius: Float[np.ndarray, " dim"],
    viriral_velocity: Float[np.ndarray, " dim"],
    virial_temperature: Float[np.ndarray, " dim"],
    num_iter: Int[np.ndarray, " dim"],
    galaxy_class: Int[np.ndarray, " dim"],
    mhalo_poserr_2sigma: Float[np.ndarray, " dim"],
    mhalo_poserr_1sigma: Float[np.ndarray, " dim"],
    mhalo_negerr_1sigma: Float[np.ndarray, " dim"],
    mhalo_negerr_2sigma: Float[np.ndarray, " dim"],
    mhalo_pdf_bins: Float[np.ndarray, " num_bins"],
    mhalo_pdf: Float[np.ndarray, " num_bins"],
) -> None:
    columns = [astropy.io.fits.Column(name="GAL_ID", format="K", array=data["GAL_ID"])]
    columns.extend(
        [
            astropy.io.fits.Column(name=key, format="E", array=data[key])
            for key in data.keys()
            if key != "GAL_ID"
        ]
    )

    pdf_size = mhalo_pdf.shape[1]
    columns.extend(
        [
            astropy.io.fits.Column(name="groupID", format="K", array=group_id),
            astropy.io.fits.Column(
                name="group_total_Mstar",
                format="E",
                unit="log(Msun)",
                array=group_total_mass,
            ),
            astropy.io.fits.Column(name="group_count", format="K", array=group_count),
            astropy.io.fits.Column(
                name="Mhalo", format="E", unit="log(Msun)", array=mhalo
            ),
            astropy.io.fits.Column(
                name="Mhalo_2sigma_neg",
                format="E",
                unit="log(Msun)",
                array=mhalo_negerr_2sigma,
            ),
            astropy.io.fits.Column(
                name="Mhalo_1sigma_neg",
                format="E",
                unit="log(Msun)",
                array=mhalo_negerr_1sigma,
            ),
            astropy.io.fits.Column(
                name="Mhalo_1sigma_pos",
                format="E",
                unit="log(Msun)",
                array=mhalo_poserr_1sigma,
            ),
            astropy.io.fits.Column(
                name="Mhalo_2sigma_pos",
                format="E",
                unit="log(Msun)",
                array=mhalo_poserr_2sigma,
            ),
            astropy.io.fits.Column(
                name="Mhalo_pdf", format=f"{pdf_size}E", array=mhalo_pdf
            ),
            astropy.io.fits.Column(
                name="Mhalo_pdf_bins",
                format=f"{pdf_size}E",
                unit="log(Msun)",
                array=mhalo_pdf_bins,
            ),
            astropy.io.fits.Column(
                name="Rvir", format="E", unit="kpc", array=virial_radius.value
            ),
            astropy.io.fits.Column(
                name="Vvir",
                format="E",
                unit="km/s",
                array=viriral_velocity.value,
            ),
            astropy.io.fits.Column(
                name="Tvir",
                format="E",
                unit="log10(K)",
                array=np.log10(virial_temperature.value),
            ),
            astropy.io.fits.Column(name="galaxy_class", format="K", array=galaxy_class),
            astropy.io.fits.Column(name="num_iteration", format="K", array=num_iter),
            astropy.io.fits.Column(
                name="Mhalo_central_only",
                format="E",
                unit="log(Msun)",
                array=mhalo_centrals_only,
            ),
        ]
    )

    hdu = astropy.io.fits.BinTableHDU.from_columns(astropy.io.fits.ColDefs(columns))

    if pathlib.Path(output_filename).exists():
        _logger.warning(f"Output file {output_filename} already exists. Overwriting.")

    hdu.writeto(output_filename, overwrite=True)
    _logger.info(f"Output file {output_filename} saved successfully.")
