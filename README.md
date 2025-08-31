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

Please read the following instructions carefully and thoroughly before starting to follow
them.

To run SBAid you will need some dependencies. Most of them should be installed 
(or are only available) via [msys2](https://www.msys2.org/). For setting
up msys see the documentation on the linked page. Then install 
the following dependencies in the [ucrt](https://www.msys2.org/docs/environments/) version:

- gtk4
- python3
- gobject
- libadwaita
- libshumate
- python-pywin32
- python-pandas
- python-seaborn
- python-aiofiles
- python-aiosqlite
- python-jsonschema
- python-sortedcontainers

From now on, everything should be done using msys.
Most importantly, you should use the msys ucrt python
and not another python installation.

Then, you can clone SBAid preferably via the msys
git somewhere into your msys home folder.

Now, navigate into your SBAid directory and set up a python
virtual environment.

```
python -m venv --system-site-packages ./venv
```

Using pip from the virtual environment, install
the last few missing dependencies:

- aiopathlib

You should be ready to run SBAid now. In this mode
it is currently only supported to run SBAid from the 
project root. Navigate there and then run:

```
PYTHONPATH=. GTK_A11Y=none ./venv/bin/python ./sbaid/__init__.py
```

If you are running on a machine without a GPU, or in general
if SBAid immediately crashes without any meaningful error output,
try running on the CPU renderer:

```
GSK_RENDERER=cairo PYTHONPATH=. GTK_A11Y=none ./venv/bin/python ./sbaid/__init__.py
```

#### TL;DR

We definitely recommend reading the full instructions above.
If you read them and understood what they do, here is a
list of commands that you can copy and paste into your
msys2 terminal for getting SBAid quickly up and running.

Update msys installation (might require closing the console
and reopening it)
```
pacman -Syu
```
Install dependencies
```
pacman -S git mingw-w64-ucrt-x86_64-libadwaita mingw-w64-ucrt-x86_64-libshumate mingw-w64-ucrt-x86_64-python-aiofiles mingw-w64-ucrt-x86_64-python-aiosqlite mingw-w64-ucrt-x86_64-python-gobject mingw-w64-ucrt-x86_64-python-jsonschema mingw-w64-ucrt-x86_64-python-pywin32 mingw-w64-ucrt-x86_64-python-seaborn mingw-w64-ucrt-x86_64-python-sortedcontainers
```
Navigate where you want to clone SBAid to
```
cd ~ # Navigate where you want to clone SBAid to
```
Clone SBAid
```
git clone https://github.com/leolost2605/SBAid.git
```
Navigate into SBAid
```
cd SBAid
```
Setup python virtual environment
```
python -m venv --system-site-packages ./venv
```
Install the last pip dependencies inside the venv
```
./venv/bin/pip install aiopathlib
```
Run SBAid with GPU:
```
PYTHONPATH=. GTK_A11Y=none ./venv/bin/python ./sbaid/__init__.py
```
Run SBAid without GPU:
```
GSK_RENDERER=cairo PYTHONPATH=. GTK_A11Y=none ./venv/bin/python ./sbaid/__init__.py
```

### Troubleshooting

If SBAid crashes before even starting, i.e. it doesn't
even show a window you might want to try running it on
the CPU renderer:
```
GSK_RENDERER=cairo PYTHONPATH=. GTK_A11Y=none ./venv/bin/python
```

The important part here is the `GSK_RENDERER=cairo` environment
variable.

---
If SBAid crashes sometimes and, in the msys terminal, a warning gets printed
along the lines of
> failed to get console output format, falling back to utf8

you can try setting the correct Codepage:
```
chcp.com 65001
```

## File input

SBAid needs file inputs for many of the app's main functionalities. Follow the given guidelines for problem-free file input in SBAid:

### Algorithm writing guidelines

The starting point for implementing an SBA algorithm is the algorithm class. See that file in the source code for implementation guidelines.
For the implementation you will then need several auxiliary classes. See their files for documentation.

Currently the algorithm is based on a GObject. You shouldn't have to install anything, since everything needed to run the algorithm will be shipped with SBAid. However, if you'd like autocompletion or in general want to look into it, you will need pyGObject: https://pygobject.gnome.org/

Instead of python lists, Gio listmodels are mostly used. If you need to create your own, use Gio.ListStore. Refer to https://api.pygobject.gnome.org/ for documentation about Gio.ListStore.

For the different value types for parameters, GLib.Variant and GLib.VariantType are used. Refer to https://api.pygobject.gnome.org/GLib-2.0/structure-VariantType.html and https://api.pygobject.gnome.org/GLib-2.0/structure-Variant.html for documentation about them.

### Dummy Simulator

The Dummy simulator is a simulator implementation that
uses collected traffic data in JSON format in order to provide deterministic simulation output data. The algorithm
has no effect on the simulation in this implementation.

[blueprint for dummy simulation file](docs/dummy_template.json)

### Bulk operations import guidelines

SBAid allows certain bulk import operations. In order to successfully use these features, it is recommended that the user follows the set guidelines:

- [Guidelines for cross section import](docs/cross_section_import.md)

- [Guidelines for parameter configuration import](docs/parameter_configuration_import.md)
