from astropy.io import fits


def get_primary_header(fits_file):
    """Given a fits file returns the primary header

    Args:
        fits_file: name of the fits file

    Returns:
        header
    """
    return fits.open(fits_file)[0].header

