The starting point for implementing an SBA algorithm is the algorithm class. See that file for how to do an implementation.
For the implementation you will then need several auxiliary classes. See their files for documentation.

Currently the algorithm is based on a GObject. You shouldn't have to install anything since everything needed to run the algorithm will be shipped with SBAid. However if you'd like autocompletion or in general want to look into it you will need pyGObject: https://pygobject.gnome.org/

Instead of lists most of the time listmodels are used. If you need to create your own use Gio.ListStore. Refer to https://api.pygobject.gnome.org/ for documentation about Gio.ListStore.

For the different value types for parameters, GLib.Variant and GLib.VariantType are used. Refer to https://api.pygobject.gnome.org/GLib-2.0/structure-VariantType.html and https://api.pygobject.gnome.org/GLib-2.0/structure-Variant.html for documentation about them.