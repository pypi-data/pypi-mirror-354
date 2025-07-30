# Copyright 2025 Ravetta Stefano
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

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import TypedDict

from dataclass_wizard import JSONWizard

from ri_excel.model.cell_config import CellConfig, CellConfigType


class ReferenceType(Enum):
    START_FIXED_TO_END_OF_DATA = 'START_FIXED_TO_END_OF_DATA'


@dataclass
class ReferenceConfig(JSONWizard):
    type: ReferenceType
    regex: str | None
    duplicated: bool
    cell: CellConfig

    @staticmethod
    def new_start_fixed_to_end_of_data(cell: CellConfigType,
                                       regex: str | None = None,
                                       duplicated: bool = False) -> ReferenceConfigType:
        return {
            'type': ReferenceType.START_FIXED_TO_END_OF_DATA,
            'regex': regex,
            'duplicated': duplicated,
            'cell': cell
        }


class ReferenceConfigType(TypedDict):
    type: ReferenceType
    regex: str | None
    duplicated: bool
    cell: CellConfigType
