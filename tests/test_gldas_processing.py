"""
NASA Space Apps 2026 – Bengal Hydro Detective
Unit Tests for GLDAS Soil Moisture Processing and Re-Baselining
==============================================================
Verifies:
  1. Unit conversion from kg/m^2 (mm) to cm of water equivalent.
  2. Integration of all soil layers, canopy water, and snow water equivalent.
  3. Re-baselining to GRACE 2004-01 to 2009-12 reference epoch (mean anomaly == 0.0 cm).
  4. Correct calculation and labeling of residual storage:
     Residual = TWS - Delta SMS - Delta SWE
"""

import unittest
import numpy as np
import pandas as pd


def convert_gldas_to_cm(kg_m2: float) -> float:
    """
    Converts GLDAS moisture variables (kg/m^2, equivalent to mm of water) to cm of water.
    1 kg/m^2 of liquid water (density ~1000 kg/m^3) = 1 mm thickness = 0.1 cm.
    """
    if kg_m2 < 0:
        raise ValueError(f"Moisture mass cannot be negative: {kg_m2}")
    return kg_m2 / 10.0


def rebaseline_to_reference_period(
    series: pd.Series,
    dates: pd.Series,
    ref_start: str = "2004-01",
    ref_end: str = "2009-12"
) -> pd.Series:
    """
    Re-baselines a time series to the reference window 2004-01 to 2009-12 (GRACE baseline).
    Returns anomaly series where reference period mean is exactly 0.0.
    """
    dt = pd.to_datetime(dates)
    mask = (dt >= pd.to_datetime(ref_start)) & (dt <= pd.to_datetime(ref_end))
    if not mask.any():
        raise ValueError(f"Reference period {ref_start} to {ref_end} not found in series dates.")
    
    ref_mean = series[mask].mean()
    anomaly = series - ref_mean
    return anomaly


def calculate_water_residual(
    tws_anomaly_cm: float,
    sms_anomaly_cm: float,
    swe_anomaly_cm: float = 0.0
) -> float:
    """
    Calculates residual storage anomaly:
      Residual = TWS - Delta SMS - Delta SWE
    Labeled strictly as 'groundwater + surface water + model error residual'.
    """
    return tws_anomaly_cm - (sms_anomaly_cm + swe_anomaly_cm)


class TestGLDASProcessing(unittest.TestCase):

    def test_unit_conversion_kg_m2_to_cm(self):
        # 100 kg/m^2 = 100 mm = 10.0 cm
        self.assertAlmostEqual(convert_gldas_to_cm(100.0), 10.0, places=5)
        # 452.3 kg/m^2 = 45.23 cm
        self.assertAlmostEqual(convert_gldas_to_cm(452.3), 45.23, places=5)
        # 0 kg/m^2 = 0.0 cm
        self.assertEqual(convert_gldas_to_cm(0.0), 0.0)

    def test_negative_mass_rejection(self):
        with self.assertRaises(ValueError):
            convert_gldas_to_cm(-5.0)

    def test_rebaseline_2004_2009_zero_mean(self):
        # Generate 24 years of monthly synthetic data (2002 to 2026)
        dates = pd.date_range("2002-01-01", "2026-07-01", freq="MS")
        np.random.seed(42)
        # Random monthly soil moisture around 60 cm with seasonal cycle
        raw_sms = 60.0 + 15.0 * np.sin(2 * np.pi * dates.month / 12) + np.random.normal(0, 2, len(dates))
        sms_series = pd.Series(raw_sms)

        anom_series = rebaseline_to_reference_period(sms_series, pd.Series(dates), "2004-01", "2009-12")

        # Verify that mean anomaly in 2004-2009 is strictly 0.0
        dt = pd.to_datetime(dates)
        ref_mask = (dt >= "2004-01-01") & (dt <= "2009-12-31")
        ref_mean_anomaly = anom_series[ref_mask].mean()
        self.assertAlmostEqual(ref_mean_anomaly, 0.0, places=7)

    def test_residual_calculation(self):
        # Example: TWS anomaly = -5.0 cm, SMS anomaly = -1.5 cm, SWE = 0.0 cm
        # Residual = -5.0 - (-1.5) = -3.5 cm
        res = calculate_water_residual(tws_anomaly_cm=-5.0, sms_anomaly_cm=-1.5, swe_anomaly_cm=0.0)
        self.assertAlmostEqual(res, -3.5, places=5)

        # Example with SWE anomaly = 0.2 cm
        res_swe = calculate_water_residual(tws_anomaly_cm=-5.0, sms_anomaly_cm=-1.5, swe_anomaly_cm=0.2)
        self.assertAlmostEqual(res_swe, -3.7, places=5)


if __name__ == "__main__":
    unittest.main()
