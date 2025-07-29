"""Holds metadata and methods on Pandora NIRDA"""

# Standard library
from dataclasses import dataclass

# Third-party
import astropy.units as u
import numpy as np
import pandas as pd

from . import PACKAGEDIR
from .hardware import Hardware
from .mixins import DetectorMixins
from .utils import photon_energy
from .wcs import get_wcs


@dataclass
class NIRDetector(DetectorMixins):
    """
    Holds information on the Pandora IR detector
    """

    def __post_init__(self):
        """Some detector specific functions to run on initialization"""
        self._add_trace_params("nirda")
        self.zeropoint = self.estimate_zeropoint()

    def __repr__(self):
        return "NIRDetector"

    @property
    def name(self):
        return "NIRDA"

    @property
    def shape(self):
        """Shape of the detector in pixels"""
        return (2048, 2048)

    @property
    def pixel_scale(self):
        """Pixel scale of the detector"""
        return 1.19 * u.arcsec / u.pixel

    @property
    def pixel_size(self):
        """Size of a pixel"""
        return 18.0 * u.um / u.pixel

    @property
    def bits_per_pixel(self):
        """Number of bits per pixel"""
        return 16 * u.bit / u.pixel

    @property
    def naxis1(self):
        """WCS's are COLUMN major, so naxis1 is the number of columns"""
        return self.shape[1] * u.pixel

    @property
    def naxis2(self):
        """WCS's are COLUMN major, so naxis2 is the number of rows"""
        return self.shape[0] * u.pixel

    @property
    def pixel_read_time(self):
        """Pixel read time"""
        return 1e-5 * u.second / u.pixel

    @property
    def subarray_size(self):
        """Size of standard subarray"""
        return (400, 80)

    def frame_time(self, array_size=None):
        """Time to read out one frame of the subarray"""
        if array_size is None:
            array_size = self.subarray_size
        return np.prod(array_size) * u.pixel * self.pixel_read_time

    @property
    def zodiacal_background_rate(self):
        "Zodiacal light background rate"
        return 4 * u.electron / u.second / u.pixel

    @property
    def stray_light_rate(self):
        "Stray light rate"
        return 2 * u.electron / u.second / u.pixel

    @property
    def thermal_background_rate(self):
        "NIRDA thermal background rate"
        return 10 * u.electron / u.second / u.pixel

    @property
    def dark_rate(self):
        """Dark signal rate, detector only, no thermal"""
        return 1 * u.electron / u.second / u.pixel

    @property
    def read_noise(self):
        """Read noise"""
        return self.correlated_double_sampling_read_noise / np.sqrt(2)

    @property
    def correlated_double_sampling_read_noise(self):
        """This is the read noise obtained when differencing two images."""
        return 18 * u.electron / u.pixel

    @property
    def bias(self):
        """NIRDA detector bias"""
        return 6000 * u.electron

    @property
    def bias_uncertainty(self):
        "Uncertainty in NIRDA detector bias. Every integration has a different bias."
        return (185 * 2) * u.electron

    @property
    def saturation_limit(self):
        "NIRDA saturation limit. Bias contributes to saturation."
        return 80000 * u.electron

    @property
    def non_linearity(self):
        "NIRDA non linearity"
        raise ValueError("Not Set")

    def throughput(self, wavelength: u.Quantity):
        """Optical throughput at the specified wavelength(s)"""
        df = pd.read_csv(f"{PACKAGEDIR}/data/nir_optical_throughput.csv")
        throughput = np.interp(
            wavelength.to(u.nm).value, *np.asarray(df.values).T
        )
        throughput[wavelength.to(u.nm).value < 380] *= 0
        return throughput

    @property
    def gain(self):
        "detector gain"
        return 2.1 * u.electron / u.DN

    def apply_gain(self, values: u.Quantity):
        """Applies a single gain value"""
        if not isinstance(values, u.Quantity):
            raise ValueError("Must pass a quantity.")
        if values.unit == u.electron:
            return values / self.gain
        if values.unit == u.DN:
            return values * self.gain

    def qe(self, wavelength):
        """
        Calculate the quantum efficiency of the detector.

        Parameters
        ----------
        wavelength : npt.NDArray
            Wavelength in microns as `astropy.unit`

        Returns
        -------
        qe : npt.NDArray
            Array of the quantum efficiency of the detector
        """
        if not hasattr(wavelength, "unit"):
            raise ValueError("Pass a wavelength with units")
        wavelength = np.atleast_1d(wavelength)
        sw_coeffs = np.array([0.65830, -0.05668, 0.25580, -0.08350])
        sw_exponential = 100.0
        sw_wavecut_red = 1.69  # changed from 2.38 for Pandora
        sw_wavecut_blue = 0.85  # new for Pandora
        with np.errstate(invalid="ignore", over="ignore"):
            sw_qe = (
                sw_coeffs[0]
                + sw_coeffs[1] * wavelength.to(u.micron).value
                + sw_coeffs[2] * wavelength.to(u.micron).value ** 2
                + sw_coeffs[3] * wavelength.to(u.micron).value ** 3
            )

            sw_qe = np.where(
                wavelength.to(u.micron).value > sw_wavecut_red,
                sw_qe
                * np.exp(
                    (sw_wavecut_red - wavelength.to(u.micron).value)
                    * sw_exponential
                ),
                sw_qe,
            )

            sw_qe = np.where(
                wavelength.to(u.micron).value < sw_wavecut_blue,
                sw_qe
                * np.exp(
                    -(sw_wavecut_blue - wavelength.to(u.micron).value)
                    * (sw_exponential / 1.5)
                ),
                sw_qe,
            )
        sw_qe[sw_qe < 1e-5] = 0
        return sw_qe * u.electron / u.photon

    def sensitivity(self, wavelength):
        """
        Calulate the sensitivity of the detector.

        Parameters
        ----------
        wavelength : npt.NDArray
            Wavelength in microns as `astropy.unit`

        Returns
        -------
        sensitivity : npt.NDArray
            Array of the sensitivity of the detector
        """
        sed = 1 * u.erg / u.s / u.cm**2 / u.angstrom
        E = photon_energy(wavelength)
        telescope_area = np.pi * (Hardware().mirror_diameter / 2) ** 2
        photon_flux_density = (
            telescope_area * sed * self.throughput(wavelength) / E
        ).to(u.photon / u.second / u.angstrom) * self.qe(wavelength)
        sensitivity = photon_flux_density / sed
        return sensitivity

    @property
    def midpoint(self):
        """Mid point of the sensitivity function"""
        w = np.arange(0.1, 3, 0.005) * u.micron
        return np.average(w, weights=self.sensitivity(w))

    def get_wcs(self, ra, dec, theta=u.Quantity(0, unit="degree")):
        """Returns an astropy.wcs.WCS object"""
        return get_wcs(
            self,
            target_ra=ra,
            target_dec=dec,
            theta=theta,
            crpix1=self.subarray_size[1] // 2,
            crpix2=300,  # This is fixed to ensure that the spectrum is roughly in the middle of the sensor...
            distortion_file=f"{PACKAGEDIR}/data/fov_distortion.csv",
        )

    @property
    def info(self):
        zp = self.zeropoint
        return pd.DataFrame(
            {
                "Detector Size": "(2048, 2048)",
                "Subarray Size": "(400, 80)",
                "Pixel Scale": f"{self.pixel_scale.value} {self.pixel_scale.unit.to_string('latex')}",
                "Pixel Size": f"{self.pixel_size.value} {self.pixel_size.unit.to_string('latex')}",
                "Dark Noise": f"{self.dark_rate.value} {self.dark_rate.unit.to_string('latex')}",
                "Wavelength Midpoint": f"{self.midpoint.value:.2f} {self.midpoint.unit.to_string('latex')}",
                "Pixel Read Time": f"{self.pixel_read_time.value:.1e} {self.pixel_read_time.unit.to_string('latex')}",
                "Zeropoint": f"{zp.value:.3e}"
                + "$\\mathrm{\\frac{erg}{A\\,s\\,cm^{2}}}$",
                "R @ 1.3$\\mu m$": 65,
            },
            index=[0],
        ).T.rename({0: "NIRDA"}, axis="columns")
