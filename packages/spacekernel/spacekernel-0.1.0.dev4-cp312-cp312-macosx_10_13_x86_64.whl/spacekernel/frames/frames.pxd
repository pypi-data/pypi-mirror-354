#  -*- coding: utf-8 -*-
"""
Author: Rafael R. L. Benevides
"""

from spacekernel.time cimport Time

cdef class Frame:
    """"""

# ========== ========== ========== ========== ========== ========== GCRF
cdef class _GCRF(Frame):
    """"""

    cdef void c_to_ITRF(self,
                           Time time,
                           double[:, :] r_GCRF,
                           double[:, :] v_GCRF,
                           double[:, :] r_ITRF,
                           double[:, :] v_ITRF)

cdef _GCRF GCRF


# ========== ========== ========== ========== ========== ========== ITRF
cdef class _ITRF(Frame):

    cdef void c_to_GCRF(self,
                        Time time,
                        double[:, :] r_ITRF,
                        double[:, :] v_ITRF,
                        double[:, :] r_GCRF,
                        double[:, :] v_GCRF)

    cdef void c_to_TEME(self,
                         Time time,
                         double[:, :] r_ITRF,
                         double[:, :] v_ITRF,
                         double[:, :] r_TEME,
                         double[:, :] v_TEME)

cdef _ITRF ITRF


# ========== ========== ========== ========== ========== ========== TEME
cdef class _TEME(Frame):

    cdef void c_to_ITRF(self,
                        Time time,
                        double[:, :] r_TEME,
                        double[:, :] v_TEME,
                        double[:, :] r_ITRF,
                        double[:, :] v_ITRF)

cdef _TEME TEME