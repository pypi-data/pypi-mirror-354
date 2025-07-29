# author: Jan Tschada
# SPDX-License-Identifier: Apache-2.0

from enum import Enum


class OutputType(str, Enum):
    """
    Enumeration of output types for geolocal time data.

    Attributes:
        LOCAL: Represents local time output.
        DTC: Represents DTC (Date-Time Code) output.
    """
    LOCAL = "local"
    DTC = "dtc"