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

from typing import List, Dict

from openpyxl.workbook import Workbook

from ri_excel.model.cell_config import CellConfig
from ri_excel.model.sheet_config import SheetConfig
from ri_excel.service.reference_service import ReferenceService


class SheetsService:
    def __init__(self, config: List[SheetConfig], workbook: Workbook):
        self._main_config: SheetConfig = SheetsService._get_main_config(config)
        self._secondaries_config: List[SheetConfig] = SheetsService._get_secondaries_config(config)
        self._workbook = workbook

        self._main_reference_service: ReferenceService | None = None
        self._secondary_reference_services: Dict[str, ReferenceService] = {}

    def load_data(self):
        self._main_reference_service = ReferenceService(
            config=self._main_config.reference,
            worksheet=self._workbook[self._main_config.name]
        )

        for sheet_config in self._secondaries_config:
            reference_service = ReferenceService(
                config=sheet_config.reference,
                worksheet=self._workbook[sheet_config.name],
            )

            reference_service.load_reference_values()

            if sheet_config.name in self._secondary_reference_services or sheet_config.name == self._main_config.name:
                raise Exception(f'Sheet configuration {sheet_config.name} is duplicated')

            self._secondary_reference_services[sheet_config.name] = reference_service

    def iter_main_values(self):
        return self._main_reference_service.iter_rows()

    def get_value(self, row_values: tuple, sheet_name: str, cell: CellConfig):
        if sheet_name in self._secondary_reference_services:
            key_value = str(row_values[self._main_config.reference.cell.col - 1].value)
            return self._secondary_reference_services[sheet_name].get_cell_value(cell, key_value)

        else:
            return row_values[cell.col - 1].value

    @staticmethod
    def _get_main_config(config: List[SheetConfig]) -> SheetConfig:
        master_config = None
        master_config_count = 0

        for sheet_config in config:
            if sheet_config.isMain:
                master_config = sheet_config
                master_config_count += 1

        if master_config_count == 0:
            raise Exception('There must be a main sheet inside the Excel file')

        elif master_config_count > 1:
            raise Exception('There must be only one main sheet inside the Excel file')

        return master_config

    @staticmethod
    def _get_secondaries_config(config: List[SheetConfig]) -> List[SheetConfig]:
        secondaries_config: List[SheetConfig] = []

        for sheet_config in config:
            if not sheet_config.isMain:
                secondaries_config.append(sheet_config)

        return secondaries_config
