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
from typing import Any, TypedDict, List, Iterable

from dataclass_wizard import JSONWizard, LoadMixin
from dataclass_wizard.abstractions import AbstractParser

from ri_excel.model.cell_config import CellConfig, CellConfigType


class FieldType(Enum):
    CONST = 'CONST'
    DYNAMIC = 'DYNAMIC'
    OBJECT = 'OBJECT'


@dataclass
class FieldConfig(JSONWizard, LoadMixin):
    name: str
    sheet: str | None
    type: FieldType
    value: Any | None
    cell: CellConfig | None
    regex: str | None = None
    fields: List[Any] | None = None

    def load_to_iterable(self: Iterable, base_type: List[Any], elem_parser: AbstractParser) -> List[FieldConfig]:
        return [FieldConfig.from_dict(field) for field in self]

    @staticmethod
    def new_dynamic(name: str, sheet: str, col: str, regex: str | None = None) -> FieldConfigType:
        return {
            'name': name,
            'sheet': sheet,
            'type': FieldType.DYNAMIC,
            'regex': regex,
            'value': None,
            'cell': CellConfig.new_reference(col),
            'fields': None,
        }

    @staticmethod
    def new_const(name: str, value: Any) -> FieldConfigType:
        return {
            'name': name,
            'sheet': None,
            'type': FieldType.CONST,
            'regex': None,
            'value': value,
            'cell': None,
            'fields': None,
        }

    @staticmethod
    def new_object(name: str, fields: List[FieldConfigType]) -> FieldConfigType:
        return {
            'name': name,
            'sheet': None,
            'type': FieldType.OBJECT,
            'regex': None,
            'value': None,
            'cell': None,
            'fields': fields,
        }


class FieldConfigType(TypedDict):
    name: str
    sheet: str | None
    type: FieldType
    value: Any | None
    cell: CellConfigType | None
    regex: str | None
    fields: List[FieldConfigType] | None
