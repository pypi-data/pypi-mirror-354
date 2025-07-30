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

from typing import List, Any, Callable

from ri_excel.model.cell_config import CellConfig
from ri_excel.model.field_config import FieldConfig, FieldType
from ri_excel.model.result_config import ResultConfig
from ri_excel.util import util


class ResultsService:

    def __init__(self, config: List[ResultConfig], get_value_from_row_values: Callable[[tuple, str, CellConfig], Any]):
        self._config: List[ResultConfig] = config
        self._get_value_from_row_values: Callable[[tuple, str, CellConfig], Any] = get_value_from_row_values

        self._results = {}

    def setup(self):
        self._results = {}

    def get_results(self):
        return self._results

    def add_values_to_results(self, row_values: tuple):
        for result in self._config:
            if result.name not in self._results:
                self._results[result.name] = []

            result_obj = self._get_fields_values(result.fields, row_values)
            if result_obj is not None:
                self._results[result.name].append(result_obj)

    def _get_fields_values(self, fields: List[FieldConfig], row_values: tuple) -> dict | None:
        result_obj = {}

        for field in fields:
            value = None

            if field.type == FieldType.DYNAMIC:
                value = self._get_value_from_row_values(row_values, field.sheet, field.cell)

                if util.regex_not_match(field.regex, value):
                    return None

            elif field.type == FieldType.CONST:
                value = field.value

            elif field.type == FieldType.OBJECT:
                value = self._get_fields_values(field.fields, row_values)

            result_obj[field.name] = value

        return result_obj
