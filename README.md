# SBAid

SBAid is a tool allowing for easy testing of dynamic freeway control systems (german: **S**trecken**b**eeinflussungs**a**nlagen) in a simulation.
It can use existing simulators for the actual simulation and makes it easy to configure routes and 
algorithms for testing with the simulators.

Currently supported simulators are:
- [PTV Vissim](https://www.ptvgroup.com/en/products/ptv-vissim)
- A Dummy Simulator using a JSON file with real world measurements

## Running from source

SBAid ist written in python using GTK with libadwaita as its UI toolkit. We highly recommend
taking a look at the [PyGObject](https://pygobject.gnome.org/) documentation before getting started.

### Windows

To run SBAid you will need some dependencies. Most of them should be installed 
(or are only available) via [msys2](https://www.msys2.org/). For setting
up msys see the documentation on the linked page. Then install 
the following dependencies in the ucrt version:

- gtk4
- python3
- gobject
- libadwaita
- libshumate
- python-seaborn
- python-aiofiles
- python-aiosqlite

## File input

SBAid needs file inputs for many of the app's main functionalities. Follow the given guidelines for problem-free file input in SBAid:

### Algorithm writing guidelines

The starting point for implementing an SBA algorithm is the algorithm class. See that file in the source code for implementation guidelines.
For the implementation you will then need several auxiliary classes. See their files for documentation.

Currently the algorithm is based on a GObject. You shouldn't have to install anything, since everything needed to run the algorithm will be shipped with SBAid. However, if you'd like autocompletion or in general want to look into it, you will need pyGObject: https://pygobject.gnome.org/

Instead of python lists, Gio listmodels are mostly used. If you need to create your own, use Gio.ListStore. Refer to https://api.pygobject.gnome.org/ for documentation about Gio.ListStore.

For the different value types for parameters, GLib.Variant and GLib.VariantType are used. Refer to https://api.pygobject.gnome.org/GLib-2.0/structure-VariantType.html and https://api.pygobject.gnome.org/GLib-2.0/structure-Variant.html for documentation about them.

### Bulk operations import guidelines

SBAid allows certain bulk import operations. In order to successfully use these features, it is recommended that the user follows the set guidelines:

- [Guidelines for cross section import](readmes/cross_section_import.md)

- [Guidelines for parameter configuration import](readmes/parameter_configuration_import.md)
