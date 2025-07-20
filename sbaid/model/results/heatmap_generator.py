"""This module contains the HeatMapGenerator class."""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
from sbaid.common.diagram_type import DiagramType
from sbaid.model.results.global_diagram_generator import GlobalDiagramGenerator
from sbaid.common.image_format import ImageFormat
from sbaid.common.image import Image
from sbaid.model.results.result import Result


class HeatmapGenerator(GlobalDiagramGenerator):
    """This class contains the logic for generating a heatmap diagram,
    given the simulation results."""

    def get_diagram(self, result: Result, cross_section_ids: list, image_format: ImageFormat) -> Image:
        data = self.__filter_result_data(result, cross_section_ids)
        colorscheme = LinearSegmentedColormap.from_list('rg',
                                                        ["g", "y", "#ffa500", "r", "#ba0000"], N=256)
        sns.heatmap(data[0], cmap= colorscheme, cbar=True, cbar_kws={'label': 'average km/h'},
                    square=False, xticklabels=data[1], yticklabels=data[2])
        #TODO: dont show all timestamps
        pass

    def __filter_result_data(self, result: Result, cross_section_ids: list) -> tuple[list, list, list]:
        """TODO:
                needed data:
                - Result: (name, project_name, creation_date_time)
                - Snapshot: (capture_timestamp)
                - CrossSectionSnapshot: (cross_section_name + cross_section_snapshot.get_average_speed())
                """
        diagram_data = []  #lists for all measuring times with the average speed for all selected cross sections
        cross_sections = []
        timestamps = []
        for snapshot in result.snapshots:
            timestamps.append(snapshot.capture_timestamp)
            average_speeds = []
            for cs_snapshot in snapshot.cross_section_snapshots:
                if cs_snapshot.cross_section.id in cross_section_ids:
                    cross_sections.append(cs_snapshot.cross_section.id)
                    average_speeds.append(cs_snapshot.get_average_speed())
            diagram_data.append(average_speeds)
        return diagram_data, cross_sections, timestamps

    def generate_diagram(self, result_name: str, project_name: str, diagram_data: list,
                         cross_sections: list, timestamps: list) -> Image:
        #TODO: convert shown image to our Image
        diagram_data = np.array(diagram_data)

        fig, ax = plt.subplots()
        im = ax.imshow(diagram_data)

        cbar = ax.figure.colorbar(im, ax=ax)
        cbar.ax.set_ylabel("average km/h", rotation=-90, va="bottom")

        ax.set_xticks(range(len(cross_sections)), labels="cross sections",
                      rotation=45, ha="right", rotation_mode="anchor")
        ax.set_yticks(range(len(timestamps)), labels="time")
        ax.set_title(result_name + "from project " + project_name)

        plt.show()

    def get_diagram(self, result: Result, cross_section_ids: list[str],  # type: ignore[empty-body]
                    export_format: ImageFormat) -> Image:
        pass

    def get_diagram_type(self) -> DiagramType:
        """todo"""
        return DiagramType("Heatmap-Diagram", "Heatmap-Diagram")
