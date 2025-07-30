# Copyright 2024-2025 IQM
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Provider of calibration sets and quality metrics from remote IQM servers."""

from copy import deepcopy
import logging

from iqm.pulla.interface import CalibrationSet, CalibrationSetId
from iqm.station_control.client.station_control import StationControlClient

logger = logging.getLogger(__name__)

CalibrationDataFetchException = RuntimeError


class CalibrationDataProvider:
    """Access calibration info via station control client and cache data in memory."""

    def __init__(self, station_control_client: StationControlClient):
        self._station_control_client = station_control_client
        self._calibration_sets: dict[CalibrationSetId, CalibrationSet] = {}

    def get_calibration_set(self, cal_set_id: CalibrationSetId) -> CalibrationSet:
        """Get the calibration set from the database and cache it."""
        logger.debug("Get the calibration set from the database: cal_set_id=%s", cal_set_id)
        try:
            if cal_set_id not in self._calibration_sets:
                cal_set_values = self._station_control_client.get_calibration_set_values(cal_set_id)
                self._calibration_sets[cal_set_id] = cal_set_values
            return deepcopy(self._calibration_sets[cal_set_id])
        except Exception as e:
            raise CalibrationDataFetchException("Could not fetch calibration set from the database.") from e

    def get_latest_calibration_set(self, chip_label) -> tuple[CalibrationSet, CalibrationSetId]:
        """Get the latest calibration set id for chip label from the database."""
        logger.debug("Get the latest calibration set for chip label: chip_label=%s", chip_label)
        try:
            latest_cal_set_id = self._station_control_client.get_latest_calibration_set_id(chip_label)
        except Exception as e:
            raise CalibrationDataFetchException(
                f"Could not fetch latest calibration set id from the database: {e}"
            ) from e

        return self.get_calibration_set(latest_cal_set_id), latest_cal_set_id
