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
from typing import List, TypedDict

from dataclass_wizard import JSONWizard

from ri_excel.model.result_config import ResultConfig, ResultConfigType
from ri_excel.model.sheet_config import SheetConfig, SheetConfigType


@dataclass
class ExcelConfig(JSONWizard):
    sheets: List[SheetConfig]
    results: List[ResultConfig]

    @staticmethod
    def new(sheets: List[SheetConfigType], results: List[ResultConfigType]) -> ExcelConfigType:
        return {
            'sheets': sheets,
            'results': results,
        }


class ExcelConfigType(TypedDict):
    sheets: List[SheetConfigType]
    results: List[ResultConfigType]
