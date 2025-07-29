#  -*- coding: utf-8 -*-
"""
Author: Rafael R. L. Benevides
"""

from .geocentric import TEME_from_ITRF, ITRF_from_TEME, GCRF_from_ITRF, ITRF_from_GCRF

from .frames import get_GCRF, get_ITRF, get_TEME, Frame


GCRF = get_GCRF()
ITRF = get_ITRF()
TEME = get_TEME()
