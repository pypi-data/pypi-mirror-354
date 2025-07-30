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

from openpyxl.reader.excel import load_workbook
from openpyxl.workbook import Workbook

from ri_excel.model.excel_config import ExcelConfig, ExcelConfigType
from ri_excel.service.result_service import ResultsService
from ri_excel.service.sheet_service import SheetsService


class ExcelReader:
    def __init__(self, filename: str, config: ExcelConfigType):
        self._config: ExcelConfig = ExcelConfig.from_dict(config)
        self._workbook: Workbook = load_workbook(filename=filename, read_only=True)

        self._sheets_service: SheetsService | None = None
        self._results_service: ResultsService | None = None

    def get_results(self) -> dict[str, list]:
        self._sheets_service = SheetsService(self._config.sheets, self._workbook)
        self._sheets_service.load_data()

        self._results_service = ResultsService(self._config.results, self._sheets_service.get_value)
        self._results_service.setup()

        for row_values in self._sheets_service.iter_main_values():
            self._results_service.add_values_to_results(row_values)

        return self._results_service.get_results()
