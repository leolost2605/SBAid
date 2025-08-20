from typing import Iterable

import aiofiles
import csv

from gi.repository import Gio

from sbaid.model.algorithm_configuration.parameter_exporter import (ParameterExporter,
                                                                    ParameterExporterForeachFunc)
from sbaid.common import list_model_iterator
from sbaid.model.algorithm_configuration.parameter import Parameter

class CSVParameterExporter(ParameterExporter):

    def can_handle_format(self, export_format: str) -> bool:
        return export_format == "csv"

    async def for_each_parameter(self, file: Gio.File, parameters: Gio.ListModel,
                                 foreach_func: ParameterExporterForeachFunc):
        params = self.__populate_data(list_model_iterator(parameters))
        params[0] = ["cs_id"]
        for param in list_model_iterator(parameters):
            for entry in await self.__format_parameters(param, [row[0] for row
                                                                in list_model_iterator(parameters)],
                                                        params[0]):
                cs_index, param_index, value = entry
                params[cs_index][param_index] = value

        async with aiofiles.open(file.get_path(), "w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(params)

    def __populate_data(self, parameters: Iterable[Parameter]) -> list[list[str]]:
        param_names = []
        cross_sections = []
        data = []
        for i, param in enumerate(parameters):
            if param.cross_section not in cross_sections:
                cross_sections.append(param.cross_section)
                data.append([])
            if param.name not in param_names:
                param_names.append(param.name)
                data[i].append(i)
        return data

    async def __format_parameters(self, parameter: Parameter, ids: list[str], header: list[str])\
            -> list[tuple[int, int, str]]:
        entries = []
        try:
            cs_id_index = ids.index(parameter.cross_section.id)
        except ValueError:
            cs_id_index = len(ids) - 1
            entries.append(tuple[0, len(ids), parameter.cross_section.id])
        try:
            entries.append(tuple[cs_id_index, header[0].index(parameter.name)])
        except ValueError:
            entries.append(tuple[0, len(header), parameter.name])
            entries.append(tuple[cs_id_index, len(header), parameter.value])
        return entries