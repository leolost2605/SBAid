"""todo"""
from matplotlib.colors import LinearSegmentedColormap

from sbaid.common.diagram_type import DiagramType
from sbaid.common.image import Image
from sbaid.common.image_format import ImageFormat
from sbaid.model.results.cross_section_diagram_generator import CrossSectionDiagramGenerator
from sbaid.model.results.result import Result
import seaborn as sns
import matplotlib.pyplot as plt
# import GlobalDatabase


class QVGenerator(CrossSectionDiagramGenerator):
    """todo"""
    diagram_name = "QV-Diagram"
    def get_diagram_type(self) -> DiagramType:  # pylint:disable=useless-parent-delegation
        """todo"""
        return super().get_diagram_type()

    def get_diagram(self, result: Result, cross_section_id: str,
                    export_format: ImageFormat) -> None:
        # cross_section_snapshot = GlobalDatabase.get_cross_section_snapshot(cross_section_id)
        data = self.__filter_result_data(result, cross_section_id)
        self.generate_diagram(data)

        pass

    def __filter_result_data(self, result: Result, cross_section_id) -> tuple[list, list]:
        average_speed = []
        traffic_density = []

        for snapshot in result.snapshots:
            for cs_snapshot in snapshot.cross_section_snapshots:
                if cs_snapshot.id == cross_section_id:
                    average_speed.append(cs_snapshot.average_speed)
                    traffic_density.append(cs_snapshot.traffic_density)

        return average_speed, traffic_density

    def generate_diagram(self, data: tuple[list, list]) -> Image:
        """todo help m"""

        colorscheme = LinearSegmentedColormap.from_list('rg',
                                                        ["#910000", "#c10000", "r", "#ffa500", "y", "g"], N=256)


        average_speeds = data[0]
        traffic_density = data[1]
        ax = plt.subplot(figsize=(6.5, 6.5))
        sns.scatterplot(x=average_speeds, y=traffic_density, ax=ax)
        plt.show()
