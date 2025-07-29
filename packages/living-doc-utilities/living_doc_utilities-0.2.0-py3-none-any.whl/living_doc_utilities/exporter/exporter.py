# Copyright 2025 ABSA Group Limited
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
#

"""
This module contains a parent class for creating exporters.
"""


class Exporter:
    """
    A parent class for creating exporters.
    """

    def export(self, **kwargs) -> bool:
        """
        A method for exporting the output in the selected format.

        @param kwargs: Additional arguments for the export method
        @return: True if the export was successful, False otherwise
        """
        raise NotImplementedError("Subclasses should implement this method")
