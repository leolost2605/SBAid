"""This module defines the SimulationManager class"""
from typing import cast

from gi.repository import GObject

from sbaid.model.results.result import Result
from sbaid.common.location import Location
from sbaid.model.results.result_builder import ResultBuilder
from sbaid.model.simulation.cross_section_state import CrossSectionState
from sbaid.model.simulation.network_state import NetworkState
from sbaid.model.simulation.parameter_configuration_state import ParameterConfigurationState
from sbaid.model.simulation_observer import SimulationObserver
from sbaid.model.network.network import Network
from sbaid.model.algorithm_configuration.algorithm_configuration import AlgorithmConfiguration
from sbaid.model.simulator.simulator import Simulator
from sbaid.model.results.result_manager import ResultManager


class SimulationManager(GObject.GObject):
    """This class defines the SimulationManager class, that manages a running simulation."""

    def __init__(self, project_name: str, algorithm_configuration: AlgorithmConfiguration,
                 network: Network, simulator: Simulator, result_manager: ResultManager,
                 observer: SimulationObserver) -> None:
        """Initialize the SimulationManager class.  This is valid at the exact moment of
        its construction and should be used immediately, i.e. started."""
        super().__init__(project_name=project_name, algorithm_configuration=algorithm_configuration,
                         network=network, simulator=simulator, result_manager=result_manager,
                         observer=observer)
        self.observer = observer
        self.network = network
        self.algorithm_configuration = algorithm_configuration
        self.project_name = project_name
        self.simulator = simulator
        self.result_manager = result_manager

    def cancel(self) -> None:
        """Cancel the running simulation"""

    def start(self) -> None:
        """Start the simulation"""
        result_builder = ResultBuilder(self.result_manager)
        result_builder.begin_result(self.project_name)

        parameter_configuration = self.algorithm_configuration.parameter_configuration
        parameter_configuration_state = ParameterConfigurationState(parameter_configuration)

        route: list[Location] = self.network.route
        cross_section_states: list[CrossSectionState] = self.network.cross_sections
        network_state = NetworkState(route, cross_section_states)

        simulation_start_time, simulation_duration = self.simulator.init_simulation()
        self.algorithm_configuration.algorithm.init(parameter_configuration_state, network_state)

        elapsed_time = 0
        while elapsed_time < simulation_duration:
            self.simulator.continue_simulation(self.algorithm_configuration.evaluation_interval)
            measurements = self.simulator.measure()
            display_interval = self.algorithm_configuration.display_interval
            display = self.algorithm_configuration.algorithm.calculate_display(measurements)

            if elapsed_time % display_interval == 0:
                self.simulator.set_display(display)

            # add to result
            result_builder.begin_snapshot(simulation_start_time + elapsed_time)
            for cross_section_state in cross_section_states:
                name = self.network.cross_sections.find(cross_section_state.id)
                result_builder.begin_cross_section(name)
                if display is not None:
                    result_builder.add_b_display(display.get_b_display(cross_section_state.id))

                for lane in cross_section_state.lanes:
                    result_builder.begin_lane(lane)
                    result_builder.add_average_speed(
                        measurements.get_average_speed(cross_section_state.id, lane))
                    result_builder.add_traffic_volume(
                        measurements.get_traffic_volume(cross_section_state.id, lane))
                    if display is not None:
                        result_builder.add_a_display(
                            display.get_a_display(cross_section_state.id, lane))
                    for vehicle_info in (measurements
                            .get_all_vehicle_infos(cross_section_state.id, lane)):
                        result_builder.begin_vehicle()
                        result_builder.add_vehicle_type(vehicle_info.type)
                        result_builder.add_vehicle_speed(vehicle_info.speed)
                        result_builder.end_vehicle()
                        result_builder.end_vehicle()
                    result_builder.end_lane()
                result_builder.end_cross_section()
            result_builder.end_snapshot()

            self.observer.update_progress(elapsed_time / simulation_duration)

            elapsed_time += self.algorithm_configuration.evaluation_interval

        self.simulator.stop_simulation()
        result = cast(Result, result_builder.end_result())
        self.result_manager.register_result(result)
        self.observer.finished(result.id)
