"""This module contains the HeatMapGenerator class."""

from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.figure import Figure
from gi.repository import GLib
from sbaid.common.diagram_type import DiagramType
from sbaid.model.results.global_diagram_generator import GlobalDiagramGenerator
from sbaid.common.image_format import ImageFormat
from sbaid.common.image import Image
from sbaid.model.results.result import Result
from sbaid.common.diagram_type import DiagramType
from sbaid.model.results.seaborn_image import SeabornImage
from sbaid.common import list_model_iterator


class HeatmapGenerator(GlobalDiagramGenerator):
    """This class contains the logic for generating a heatmap diagram,
    given the simulation results."""

    __diagram_type: DiagramType = DiagramType("heatmap_diagram", "Heatmap")

    def get_diagram(self, result: Result, cross_section_ids: list, image_format: ImageFormat) -> Image:
        data = self.__filter_result_data(result, cross_section_ids)
        colorscheme = LinearSegmentedColormap.from_list('rg',
                                                        ["g", "y", "#ffa500", "r", "#ba0000"], N=256)
        sns.heatmap(data[0], cmap= colorscheme, cbar=True, cbar_kws={'label': 'average km/h'},
                    square=False, xticklabels=data[1], yticklabels=data[2])
        #TODO: dont show all timestamps
        pass

    def get_diagram_type(self) -> DiagramType:
        return self.__diagram_type

    def get_diagram(self, result: Result, cross_section_ids: list, image_format: ImageFormat) -> Image:
        data: tuple[list, list, list] = self.__filter_result_data(result, cross_section_ids)
        fig: Figure = self.__generate_diagram(result.result_name, result.project_name,
                                                 data, result.creation_date_time)
        buffer = BytesIO()

        fig.savefig(buffer, format=image_format.value_name.lower(), bbox_inches='tight')
        plt.close(fig)

        return SeabornImage(buffer.getvalue())

    def __filter_result_data(self, result: Result, cross_section_ids: list) -> tuple[list, list, list]:
        diagram_data = []
        cross_sections = []
        timestamps = []
        for snapshot in list_model_iterator(result.snapshots):
            timestamp = snapshot.get_timestamp()
            if timestamp.getMinute() == 0 and timestamp.getSecond() == 0:
                timestamps.append(snapshot.capture_timestamp)
            else:
                timestamps.append("")
            average_speeds = []
            for cs_snapshot in snapshot.cross_section_snapshots:
                if cs_snapshot.cross_section.id in cross_section_ids:
                    cross_sections.append(cs_snapshot.cross_section.id)
                    average_speeds.append(cs_snapshot.calculate_cs_average_speed())
            diagram_data.append(average_speeds)
        return diagram_data, cross_sections, timestamps

    def __generate_diagram(self, result_name: str, project_name: str, data: tuple[list, list, list], datetime: GLib.DateTime) -> Figure:
        colorscheme = LinearSegmentedColormap.from_list('rg',
                                                        ["#910000", "#c10000", "r", "#ffa500", "y", "g"], N=256)
        diagram_data = np.array(data[0])
        cross_sections = data[1]
        timestamps = data[2]
        formatted_date = datetime.format("%F")
        fig, ax = plt.subplots()
        sns.heatmap(diagram_data, cmap=colorscheme, cbar=True, cbar_kws={'label': 'V [km/h]'},
                         square=False, xticklabels=cross_sections, yticklabels=timestamps, ax=ax)
        ax.set_title(result_name + " from project " + project_name)
        ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
        ax.tick_params(left=False)
        ax.annotate(formatted_date, (0, 0), (-60, -20), xycoords='axes fraction',
                     textcoords='offset points', va='top')
        # plt.tight_layout()
        # plt.show()
        return fig

    def get_diagram_type(self) -> DiagramType:
        """todo"""
        return DiagramType("Heatmap-Diagram", "Heatmap-Diagram")
