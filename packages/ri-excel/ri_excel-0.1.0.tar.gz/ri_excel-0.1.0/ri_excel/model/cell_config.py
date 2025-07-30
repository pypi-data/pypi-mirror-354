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
from typing import Any, TypedDict

from dataclass_wizard import JSONWizard
from openpyxl.utils import column_index_from_string


class CellType(Enum):
    VALUE = 'VALUE'
    REFERENCE = 'REFERENCE'


@dataclass
class CellConfig(JSONWizard):
    type: CellType
    col: int | None
    row: int | None

    @staticmethod
    def new_value(col: str, row: int) -> CellConfigType:
        return {
            'type': CellType.VALUE,
            'col': column_index_from_string(col),
            'row': row,
        }

    @staticmethod
    def new_reference(col: str) -> CellConfigType:
        return {
            'type': CellType.REFERENCE,
            'col': column_index_from_string(col),
            'row': None,
        }


class CellConfigType(TypedDict):
    type: CellType
    col: int | None
    row: int | None


@dataclass
class Cell:
    col: int
    row: int
    row_values: Any
