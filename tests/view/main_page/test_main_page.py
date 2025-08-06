import unittest
from unittest import skipIf
from unittest.mock import Mock

from gi.repository import Adw, Gio

from sbaid.common.location import Location
from sbaid.model.network.route import Route
from sbaid.model.simulator.vissim.vissim_simulator import VissimSimulator
from sbaid.view_model.network.cross_section import CrossSection
from sbaid.view.main_page.project_main_page import ProjectMainPage
from sbaid.view_model.network.network import Network
from sbaid.model.network.network import Network as ModelNetwork

# @skipIf(True, "this is for human testing as it spawns a window that will stay indefinitely")
class MainPageTestCase(unittest.TestCase):
    def test_something(self):
        app = Adw.Application()
        app.connect('activate', self.on_activate)
        app.run(None)

    def on_activate(self, app):
        win = Adw.ApplicationWindow(application=app)
        project_mock = Mock()
        project_mock.id = "my id"
        project_mock.name = "My Project 1"
        network_mock = Mock()
        network_mock.cross_sections = Gio.ListStore.new(CrossSection)
        cs_mock = Mock()
        cs_mock.id = "cs id"
        cs_mock.name = "Messquerschnitt 1"
        cs_mock.location = Location(0, 0.5)
        cs_mock_aq = Mock()
        cs_mock_aq.id = "cs id2"
        cs_mock_aq.name = "Anzeigequerschnitt 5"
        cs_mock_aq.location = Location(0, 0.75)
        network_mock.cross_sections.append(CrossSection(cs_mock))
        network_mock.cross_sections.append(CrossSection(cs_mock_aq))
        network_mock.route_points = Gio.ListStore.new(Location)
        network_mock.route_points.append(Location(0, 0))
        network_mock.route_points.append(Location(0, 1))
        project_mock.network = network_mock
        win.set_content(ProjectMainPage(project_mock))
        win.present()

    def on_activate_vissim(self, app):
        win = Adw.ApplicationWindow(application=app)

        vissim = VissimSimulator()
        model_network = ModelNetwork(vissim, Mock())
        network = Network(model_network)

        project_mock = Mock()
        project_mock.id = "my id"
        project_mock.name = "My Project 1"
        project_mock.network = network
        win.set_content(ProjectMainPage(project_mock))
        win.present()


if __name__ == '__main__':
    unittest.main()
