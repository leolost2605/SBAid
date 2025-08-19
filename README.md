# SBAid

SBAid is a tool allowing for easy testing of Streckenbeeinflussungsanlagen in a simulation.
It can use existing simulators for the actual simulation and makes it easy to configure routes and 
algorithms for testing with the simulators.

Currently supported simulators are:
- [PTV Vissim](https://www.ptvgroup.com/en/products/ptv-vissim)
- A Dummy Simulator using a JSON file with real world measurements

## Installing from source

SBAid ist written in python using GTK with libadwaita as its UI toolkit. We highly recommend
taking a look at the [PyGObject](https://pygobject.gnome.org/) documentation before getting started.
